import logging
import hashlib
import hmac
import requests
from time import sleep, time
from datetime import datetime
from enum import Enum

logger = logging.getLogger('cryptocom_api')

RATE_LIMIT_PER_SECOND = 10


def current_timestamp():
    return int(datetime.timestamp(datetime.now()) * 1000)


class CryptoComApi:
    class ApiVersion(Enum):
        V1 = "v1"
        V2 = "v2"

    _API_VERSION_ROOT_PATH = {
        ApiVersion.V1: "https://api.crypto.com/v1/",
        ApiVersion.V2: "https://api.crypto.com/v2/"
    }

    __key = ""
    __secret = ""
    __public_only = True

    __last_api_call = 0

    version = ApiVersion.V1

    response_code = {
        ApiVersion.V1: 'code',
        ApiVersion.V2: 'code'
    }
    response_message = {
        ApiVersion.V1: 'msg',
        ApiVersion.V2: 'message'
    }
    response_result = {
        ApiVersion.V1: 'data',
        ApiVersion.V2: 'result'
    }

    response = None

    error = None

    def __init__(self, key=None, secret=None, version=ApiVersion.V2):
        self.version = CryptoComApi.ApiVersion(version)
        self.API_ROOT = self._API_VERSION_ROOT_PATH[self.version]

        logger.debug(f"API version {version} initialized, root path is: {self.API_ROOT}")

        if key and secret:
            self.__key = key
            self.__secret = secret
            self.__public_only = False

    def get_code(self):
        return self.response and self.response[self.response_code[self.version]]

    def get_message(self):
        return self.response and self.response[self.response_message[self.version]]

    def get_result(self):
        return self.response and self.response[self.response_result[self.version]]

    def _sign(self, params, method=None, id=None, nonce=None):
        to_sign = ""
        for key in sorted(params.keys()):
            to_sign += key + str(params[key])

        if self.version == CryptoComApi.ApiVersion.V1:
            to_sign += str(self.__secret)
            return hashlib.sha256(to_sign.encode()).hexdigest()
        if self.version == CryptoComApi.ApiVersion.V2:
            to_sign = method + \
                      (str(id) if id else "") + \
                      self.__key + \
                      to_sign + \
                      str(nonce)
            return hmac.new(
                bytes(str(self.__secret), 'utf-8'),
                msg=bytes(to_sign, 'utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()

    def _request(self, path, param=None, method='get'):
        ms_from_last_api_call = current_timestamp() - self.__last_api_call
        if ms_from_last_api_call < 1000/RATE_LIMIT_PER_SECOND:
            delay_for_ms = 1000/RATE_LIMIT_PER_SECOND - min(1000/RATE_LIMIT_PER_SECOND, ms_from_last_api_call)
            logger.debug(f"API call '{path}' rate limiter activated, delaying for {delay_for_ms}ms")
            sleep(delay_for_ms / 1000)

        self.__last_api_call = current_timestamp()

        self.error = None

        if method == 'post':
            if self.version == CryptoComApi.ApiVersion.V1:
                r = requests.post(self.API_ROOT + path, data=param)
            else:
                r = requests.post(self.API_ROOT + path, json=param, headers={"Content-Type": "application/json"})
        elif method == 'delete':
            if self.version == CryptoComApi.ApiVersion.V1:
                r = requests.delete(self.API_ROOT + path, data=param)
            else:
                r = requests.delete(self.API_ROOT + path, json=param, headers={"Content-Type": "application/json"})
        elif method == 'get':
            r = requests.get(self.API_ROOT + path, params=param)
        else:
            return {}

        try:
            if r.elapsed:
                logger.debug(f"{path}, elapsed: {r.elapsed}")
        finally:
            pass

        try:
            if r.status_code != 200:
                logger.warning(f"Response {r.status_code} NOK: {r.text}")
                self.error = {'http_code': r.status_code}
                try:
                    self.error.update(r.json())
                except:
                    pass
                return {}

            self.response = r.json()

            if int(self.get_code()) != 0:
                # error occurred
                logger.warning(f'Error code: {self.get_code()}')
                logger.warning(f'Error msg: {self.get_message()}')
                self.error = self.response
                return {}
            return self.get_result()
        except Exception as e:
            logger.error(f"{e}\r\nResponse text: {r.text}")
            self.error = {'exception': r.text}
            return {}

    def _post(self, path, params=None):
        if self.__public_only:
            return {}
        if params is None:
            params = {}

        if self.version == CryptoComApi.ApiVersion.V1:
            params['api_key'] = self.__key
            params['time'] = current_timestamp()
            params['sign'] = self._sign(params)

        if self.version == CryptoComApi.ApiVersion.V2:
            id = 1
            nonce = current_timestamp()
            sig = self._sign(params, method=path, id=id, nonce=nonce)
            param = {
                'params': params,
                'sig': sig,
                'api_key': self.__key,
                'method': path,
                'nonce': nonce,
                'id': id}
            return self._request(path, param, method='post')

        return self._request(path, params, method='post')