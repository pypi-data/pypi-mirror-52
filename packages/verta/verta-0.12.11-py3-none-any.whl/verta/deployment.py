# -*- coding: utf-8 -*-

import six
from six.moves.urllib.parse import urljoin, urlparse

import json
import gzip
import os
import time
import warnings

import requests

from .client import _GRPC_PREFIX
from . import _utils


class DeployedModel:
    """
    Object for interacting with deployed models.

    .. deprecated:: 0.13.7
        The `socket` parameter will be renamed to `host` in v0.14.0

    This class provides functionality for sending predictions to a deployed model on the Verta
    backend.

    Authentication credentials must be present in the environment through `$VERTA_EMAIL` and
    `$VERTA_DEV_KEY`.

    Parameters
    ----------
    host : str
        Hostname of the Verta Web App.
    model_id : str
        ID of the deployed ExperimentRun/ModelRecord.

    """
    def __init__(self, host=None, model_id=None, socket=None):
        # this is to temporarily maintain compatibility with anyone passing in `socket` as a kwarg
        # TODO v0.14.0: remove `socket` param
        # TODO v0.14.0: remove default `None`s for `host` and `model_id` params
        # TODO v0.14.0: remove the following block of param checks
        if host is None and socket is None and model_id is None:
            raise TypeError("missing 2 required positional arguments: 'host' and 'model_id'")
        elif host is not None and socket is not None:
            raise ValueError("cannot specify both `host` and `socket`; please only provide `host`")
        elif host is None:
            if socket is None:
                raise TypeError("missing 1 required positional argument: 'host'")
            else:
                warnings.warn("`socket` will be renamed to `host` in a later version",
                              category=FutureWarning)
                host = socket
                del socket
        elif model_id is None:
            raise TypeError("missing 1 required positional argument: 'model_id'")

        self._session = requests.Session()
        self._session.headers.update({_GRPC_PREFIX+'source': "PythonClient"})
        try:
            self._session.headers.update({_GRPC_PREFIX+'email': os.environ['VERTA_EMAIL']})
        except KeyError:
            six.raise_from(EnvironmentError("${} not found in environment".format('VERTA_EMAIL')), None)
        try:
            self._session.headers.update({_GRPC_PREFIX+'developer_key': os.environ['VERTA_DEV_KEY']})
        except KeyError:
            six.raise_from(EnvironmentError("${} not found in environment".format('VERTA_DEV_KEY')), None)

        back_end_url = urlparse(host)
        self._scheme = back_end_url.scheme or "https"
        self._socket = back_end_url.netloc + back_end_url.path.rstrip('/')

        self._id = model_id
        self._status_url = "{}://{}/api/v1/deployment/status/{}".format(self._scheme, self._socket, model_id)

        self._prediction_url = None

    def __repr__(self):
        return "<Model {}>".format(self._id)

    @classmethod
    def from_url(cls, url, token):
        """
        Returns a :class:`DeployedModel` based on a custom URL and token.

        Parameters
        ----------
        url : str, optional
            Prediction endpoint URL or path. Can be copy and pasted directly from the Verta Web App.
        token : str, optional
            Prediction token. Can be copy and pasted directly from the Verta Web App.

        Returns
        -------
        :class:`DeployedModel`

        """
        parsed_url = urlparse(url)

        deployed_model = cls(parsed_url.netloc, "")
        deployed_model._id = None
        deployed_model._status_url = None

        deployed_model._prediction_url = urljoin("{}://{}".format(parsed_url.scheme, parsed_url.netloc), parsed_url.path)
        deployed_model._session.headers['Access-Token'] = token

        return deployed_model

    def _set_token_and_url(self):
        response = self._session.get(self._status_url)
        _utils.raise_for_http_error(response)
        status = response.json()
        if status['status'] == 'error':
            raise RuntimeError(status['message'])
        if 'token' in status and 'api' in status:
            self._session.headers['Access-Token'] = status['token']
            self._prediction_url = urljoin("{}://{}".format(self._scheme, self._socket), status['api'])
        else:
            raise RuntimeError("token not found in status endpoint response; deployment may not be ready")

    def _predict(self, x, compress=False):
        """This is like ``DeployedModel.predict()``, but returns the raw ``Response`` for debugging."""
        if 'Access-token' not in self._session.headers or self._prediction_url is None:
            self._set_token_and_url()

        if compress:
            # create gzip
            gzstream = six.BytesIO()
            with gzip.GzipFile(fileobj=gzstream, mode='wb') as gzf:
                gzf.write(six.ensure_binary(json.dumps(x)))
            gzstream.seek(0)

            return self._session.post(
                self._prediction_url,
                headers={'Content-Encoding': 'gzip'},
                data=gzstream.read(),
            )
        else:
            return self._session.post(self._prediction_url, json=x)

    def predict(self, x, compress=False, max_retries=5):
        """
        Make a prediction using input `x`.

        Parameters
        ----------
        x : list
            A batch of inputs for the model.
        compress : bool, default False
            Whether to compress the request body.
        max_retries : int, default 5
            Maximum number of times to retry a request on a connection failure.

        Returns
        -------
        prediction : list
            Output returned by the deployed model for `x`.

        Raises
        ------
        RuntimeError
            If the deployed model encounters an error while running the prediction.
        requests.HTTPError
            If the server encounters an error while handing the HTTP request.

        """
        for i_retry in range(max_retries):
            response = self._predict(x, compress)
            if response.ok:
                return response.json()
            elif response.status_code == 502:  # bad gateway; the error happened in the model back end
                data = response.json()
                raise RuntimeError("deployed model encountered an error: {}"
                                   .format(data.get('message', "(no specific error message found)")))
            elif response.status_code >= 500 or response.status_code == 429:
                sleep = 0.3*(2**i_retry)  # 5 retries is 9.3 seconds total
                print("received status {}; retrying in {:.1f}s".format(response.status_code, sleep))
                time.sleep(sleep)
            else:
                break
        _utils.raise_for_http_error(response)
