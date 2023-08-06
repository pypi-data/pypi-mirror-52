from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_trumba.models import TrumbaCalendar
from uw_trumba.permissions import (
    Permissions, _create_req_body, _check_err,
    _get_permissions, _extract_uwnetid, _is_valid_email)
from uw_trumba.exceptions import (
    TrumbaException, CalendarNotExist, CalendarOwnByDiffAccount,
    NoDataReturned, UnknownError, UnexpectedError)


class TestPermissions(TestCase):

    def test_get_permissions(self):
        cal = TrumbaCalendar(calendarid=10000, campus='sea')
        self.assertRaises(DataFailureException, _get_permissions, cal)
        cal = TrumbaCalendar(calendarid=1, campus='sea')
        self.assertIsNotNone(_get_permissions(cal))

        cal = TrumbaCalendar(calendarid=2, campus='bot')
        self.assertIsNotNone(_get_permissions(cal))

        cal = TrumbaCalendar(calendarid=3, campus='tac')
        self.assertIsNotNone(_get_permissions(cal))

    def test_get_cal_permissions(self):
        p_m = Permissions()
        cal = TrumbaCalendar(calendarid=1,
                             campus='sea',
                             name='Seattle calendar')
        p_m.get_cal_permissions(cal)
        self.assertEqual(p_m.total_accounts(), 3)
        self.assertTrue(p_m.account_exists('dummyp'))
        self.assertTrue(p_m.account_exists('dummye'))
        self.assertTrue(p_m.account_exists('dummys'))
        self.assertEqual(len(cal.permissions), 3)
        self.assertEqual(cal.permissions['dummyp'].uwnetid, 'dummyp')

    def test_check_err(self):
        self.assertRaises(UnexpectedError,
                          _check_err,
                          {"d": {"Messages": [{"Code": 3009,
                                               "Description": "..."}]}}, "")

        self.assertRaises(CalendarOwnByDiffAccount,
                          _check_err,
                          {"d": {"Messages": [{"Code": 3007}]}}, "")

        self.assertRaises(CalendarNotExist,
                          _check_err,
                          {"d": {"Messages": [{"Code": 3006}]}}, "")

        self.assertRaises(NoDataReturned,
                          _check_err, {'d': None}, "")

        self.assertRaises(UnknownError,
                          _check_err,
                          {"d": {"Messages": []}}, "")

        self.assertRaises(UnknownError,
                          _check_err,
                          {"d": {"Messages": [{"Code": None}]}}, "")

        self.assertIsNone(_check_err({"d": {"Messages": None}}, ""))

    def test_create_body(self):
        self.assertEqual(_create_req_body(1), '{"CalendarID": 1}')

    def test_is_valid_email(self):
        self.assertTrue(_is_valid_email('test@UW.EDU'))
        self.assertTrue(_is_valid_email('test-email@uw.edu'))
        self.assertTrue(_is_valid_email('Test_email@uw.edu'))
        self.assertTrue(_is_valid_email('test.email@uw.edu'))
        self.assertFalse(_is_valid_email('test@washington.edu'))
        self.assertFalse(_is_valid_email('0test@uw.edu'))
        self.assertFalse(_is_valid_email(''))

    def test_extract_uwnetid(self):
        self.assertEqual(_extract_uwnetid('test@uw.edu'), 'test')
        self.assertEqual(_extract_uwnetid('test@UW.EDU'), 'test')
        self.assertEqual(_extract_uwnetid('TEST@UW.EDU'), 'test')
        self.assertEqual(_extract_uwnetid('test'), 'test')
        self.assertEqual(_extract_uwnetid('@uw.edu'), '')
        self.assertEqual(_extract_uwnetid('bad@washington.edu'),
                         'bad@washington.edu')
        self.assertEqual(_extract_uwnetid(''), '')
