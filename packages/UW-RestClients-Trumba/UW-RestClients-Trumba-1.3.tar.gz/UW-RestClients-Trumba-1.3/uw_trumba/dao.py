import os
import json
from base64 import urlsafe_b64encode
from os.path import abspath, dirname
from urllib.parse import urlencode
from restclients_core.dao import DAO


class TrumbaCalendar_DAO(DAO):
    def service_name(self):
        return 'calendar'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]


class TrumbaSea_DAO(TrumbaCalendar_DAO):

    def is_mock(self):
        return self.get_implementation().is_mock()

    def service_name(self):
        return 'trumba_sea'

    def _get_basic_auth(self):
        service = self.service_name().upper()
        return "{0}:{1}".format(
            self.get_service_setting("{0}_ID".format(service), ""),
            self.get_service_setting("{0}_PSWD".format(service), ""))

    def _custom_headers(self, method, url, headers, body):
        credentials = self._get_basic_auth().encode()
        headers["Authorization"] = "Basic {0}".format(
            urlsafe_b64encode(credentials).decode("ascii"))
        return headers

    def _get_mock_file_path(self, url, method, body):
        ret = "{0}.{1}".format(url, method.title())
        if body != "{}":
            ret = "{0}_{1}".format(ret, urlencode(json.loads(body)))
        return ret

    def _edit_mock_response(self, method, url, headers, body, response):
        if response.status == 404 and method != "GET":
            alternative_url = self._get_mock_file_path(url, method, body)
            backend = self.get_implementation()
            new_resp = backend.load(method, alternative_url, headers, body)
            response.status = new_resp.status
            response.data = new_resp.data


class TrumbaBot_DAO(TrumbaSea_DAO):
    def service_name(self):
        return 'trumba_bot'


class TrumbaTac_DAO(TrumbaSea_DAO):
    def service_name(self):
        return 'trumba_tac'
