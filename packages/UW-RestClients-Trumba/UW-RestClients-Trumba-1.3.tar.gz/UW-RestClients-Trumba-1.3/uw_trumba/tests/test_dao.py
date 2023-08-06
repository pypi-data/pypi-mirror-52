from unittest import TestCase
from commonconf import override_settings
from restclients_core.models import MockHTTP
from uw_trumba.dao import (
    TrumbaSea_DAO, TrumbaBot_DAO, TrumbaTac_DAO)
from uw_trumba.tests import (
    fdao_trumba_sea_override, fdao_trumba_bot_override,
    fdao_trumba_tac_override)


@fdao_trumba_sea_override
@fdao_trumba_bot_override
@fdao_trumba_tac_override
class TestTrumbaDao(TestCase):

    def test_is_using_file_dao(self):
        self.assertTrue(TrumbaSea_DAO().is_mock())
        self.assertTrue(TrumbaBot_DAO().is_mock())
        self.assertTrue(TrumbaBot_DAO().is_mock())

    @override_settings(RESTCLIENTS_TRUMBA_SEA_ID="ss",
                       RESTCLIENTS_TRUMBA_SEA_PSWD="ppp",
                       RESTCLIENTS_TRUMBA_BOT_ID="bb",
                       RESTCLIENTS_TRUMBA_BOT_PSWD="ppp",
                       RESTCLIENTS_TRUMBA_TAC_ID="tt",
                       RESTCLIENTS_TRUMBA_TAC_PSWD="ppp")
    def test_get_basic_auth(self):
        self.assertEqual(TrumbaSea_DAO()._get_basic_auth(),
                         "ss:ppp")
        self.assertEqual(TrumbaBot_DAO()._get_basic_auth(),
                         "bb:ppp")
        self.assertEqual(TrumbaTac_DAO()._get_basic_auth(),
                         "tt:ppp")
        self.assertEqual(TrumbaSea_DAO()._custom_headers('GET', '/', {}, None),
                         {'Authorization': 'Basic c3M6cHBw'})

    def test_service_mock_paths(self):
        self.assertEqual(len(TrumbaSea_DAO().service_mock_paths()), 1)

    def test_get_mock_file_path(self):
        self.assertEqual(
            TrumbaSea_DAO()._get_mock_file_path(
                "/service/calendars.asmx/GetPermissions", 'POST', "{}"),
            "/service/calendars.asmx/GetPermissions.Post")

        self.assertEqual(
            TrumbaSea_DAO()._get_mock_file_path(
                "/service/calendars.asmx/GetPermissions",
                'POST', '{"CalendarID": 1}'),
            "/service/calendars.asmx/GetPermissions.Post_CalendarID=1")

    def test_edit_mock_response(self):
        response = MockHTTP()
        response.status = 404
        TrumbaSea_DAO()._edit_mock_response(
            'POST', "/service/calendars.asmx/GetPermissions",
            {"Content-Type": "application/json"},
            '{"CalendarID": 1}', response)
        self.assertEqual(response.status, 200)
