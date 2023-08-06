from unittest import TestCase
from uw_trumba.calendars import (
    Calendars, _is_valid_calendarid, _get_campus_calenders)


class TestCalendars(TestCase):

    def test_get_campus_calenders(self):
        self.assertIsNotNone(_get_campus_calenders('sea'))
        self.assertIsNotNone(_get_campus_calenders('bot'))
        self.assertIsNotNone(_get_campus_calenders('tac'))
        self.assertIsNone(_get_campus_calenders('sss'))

    def test_load(self):
        cals = Calendars()

        self.assertTrue(cals.exists('bot'))

        self.assertEquals(cals.total_calendars('bot'), 3)
        self.assertEquals(cals.total_calendars('sea'), 10)
        self.assertEquals(cals.total_calendars('tac'), 1)

        sorted_cals = cals.get_campus_calendars('sea')
        self.assertEqual(len(sorted_cals), 10)
        self.assertEqual(sorted_cals[0].name, "Seattle calendar")
        self.assertEqual(sorted_cals[1].name,
                         "Seattle calendar >> Seattle child calendar1")

        self.assertTrue(cals.has_calendar('sea', 1))
        trumba_cal = cals.get_calendar('sea', 1)
        self.assertEqual(trumba_cal.calendarid, 1)
        self.assertEqual(trumba_cal.campus, 'sea')
        self.assertEqual(trumba_cal.name, 'Seattle calendar')
        self.assertEqual(
            trumba_cal.to_json(),
            {'calendarid': 1,
             'campus': 'sea',
             'name': 'Seattle calendar',
             'permissions': {
                 'dummyp': {'uwnetid': 'dummyp',
                            'display_name': 'Dummy publisher',
                            'level': 'PUBLISH'},
                 'dummye': {'uwnetid': 'dummye',
                            'display_name': 'Dummy editor',
                            'level': 'EDIT'},
                 'dummys': {'uwnetid': 'dummys',
                            'display_name': 'Dummy showon',
                            'level': 'SHOWON'}}})
        perms = sorted(trumba_cal.permissions.values())
        self.assertEqual(len(perms), 3)
        self.assertTrue(perms[0].is_publish())
        self.assertTrue(perms[1].is_edit())
        self.assertTrue(perms[2].is_showon())

        trumba_cal1 = cals.get_calendar('sea', 11321)
        self.assertEqual(trumba_cal1.name,
                         "{}{}{}{}".format('Seattle calendar >> Seattle',
                                           ' child calendar3 >> Seattle',
                                           ' child-sub-calendar32 >> Seattle',
                                           ' child-sub-sub-calendar321'))

        self.assertIsNone(cals.get_campus_calendars('sss'))
        self.assertIsNone(cals.get_calendar('sea', 21))
        self.assertIsNone(cals.get_calendar('sss', 11321))

        cals.campus_calendars['bot'] = {}
        self.assertFalse(cals.exists('bot'))
        self.assertEquals(cals.total_calendars('bot'), 0)

    def test_is_valid_calendarid(self):
        self.assertTrue(_is_valid_calendarid(1))
        self.assertFalse(_is_valid_calendarid(0))
        self.assertFalse(_is_valid_calendarid(-1))
