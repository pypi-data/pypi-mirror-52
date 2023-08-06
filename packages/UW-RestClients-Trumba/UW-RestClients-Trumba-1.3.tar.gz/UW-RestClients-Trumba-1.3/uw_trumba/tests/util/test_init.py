from unittest import TestCase
import logging
from uw_trumba.dao import (
    TrumbaCalendar_DAO, TrumbaSea_DAO, TrumbaBot_DAO, TrumbaTac_DAO)
from uw_trumba.util import (
    fdao_trumba_override, fdao_trumba_sea_override,
    fdao_trumba_bot_override, fdao_trumba_tac_override)


@fdao_trumba_override
@fdao_trumba_sea_override
@fdao_trumba_bot_override
@fdao_trumba_tac_override
class TestUtilMock(TestCase):

    def test_fdao(self):
        self.assertTrue(TrumbaCalendar_DAO().get_implementation().is_mock())
        self.assertTrue(TrumbaSea_DAO().get_implementation().is_mock())
        self.assertTrue(TrumbaBot_DAO().get_implementation().is_mock())
        self.assertTrue(TrumbaTac_DAO().get_implementation().is_mock())
