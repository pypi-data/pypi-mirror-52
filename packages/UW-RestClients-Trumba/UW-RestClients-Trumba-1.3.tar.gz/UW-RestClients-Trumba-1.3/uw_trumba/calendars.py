"""
Interfacing with Trumba Calendars' service, this module
provides methods to obtain calendar info and
user calendar permissions in Trumba
The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
import re
from uw_trumba.models import TrumbaCalendar, is_bot, is_sea, is_tac
from uw_trumba import post_bot_resource, post_sea_resource, post_tac_resource
from uw_trumba.permissions import Permissions, load_json


logger = logging.getLogger(__name__)
calendarlist_url = "/service/calendars.asmx/GetCalendarList"
re_cal_id = re.compile(r'[1-9]\d*')


class Calendars:

    def __init__(self):
        """
        Build a dictionary of {calenderid, TrumbaCalendar} for each campus
        """
        self.perm_loader = Permissions()
        self.campus_calendars = {}
        self.sea_calendar_ids = set()
        self._load(TrumbaCalendar.SEA_CAMPUS_CODE)
        self._load(TrumbaCalendar.BOT_CAMPUS_CODE)
        self._load(TrumbaCalendar.TAC_CAMPUS_CODE)

    def _load(self, campus):
        """
        Load a dictionary of {calenderid, TrumbaCalendar} to
        the self.campus_calendars[campus]
        :except: DataFailureException if the underline request failed.
        """
        calendar_dict = {}
        data = _get_campus_calenders(campus)
        if (data['d']['Calendars'] is not None and
                len(data['d']['Calendars']) > 0):
            self._extract_cals(campus, data['d']['Calendars'],
                               calendar_dict, None)
        self.campus_calendars[campus] = calendar_dict

    def _extract_cals(self, campus, resp_fragment, calendar_dict, parent):
        """
        Extract calendars and load permissions. Update calendar_dict.
        """
        for record in resp_fragment:
            if (re.match(r'Internal Event Actions', record['Name']) or
                    re.match(r'Migrated .*', record['Name'])):
                continue

            if not _is_valid_calendarid(record.get('ID')):
                logger.warn(
                    "InvalidCalendarId, {0} skipped!".format(record))
                continue

            calendarid = int(record.get('ID'))

            if self._not_shared_from_sea(campus, calendarid):
                trumba_cal = TrumbaCalendar(calendarid=calendarid,
                                            campus=campus)
                if parent is None:
                    trumba_cal.name = record.get('Name')
                else:
                    trumba_cal.name = "{0} >> {1}".format(
                        parent, record.get('Name'))

                self.perm_loader.get_cal_permissions(trumba_cal)
                calendar_dict[trumba_cal.calendarid] = trumba_cal

                if (record.get('ChildCalendars') is not None and
                        len(record['ChildCalendars']) > 0):
                    self._extract_cals(campus,
                                       record['ChildCalendars'],
                                       calendar_dict,
                                       trumba_cal.name)

    def _not_shared_from_sea(self, campus, calendar_id):
        """
        return True if the calendar_id is not a Seattle calendar
        share with Bothell or Tacoma
        """
        if is_sea(campus):
            self.sea_calendar_ids.add(calendar_id)
            return True
        return calendar_id not in self.sea_calendar_ids

    def exists(self, campus_code):
        """
        :return: true if the campus has some calendars
        """
        cals = self.campus_calendars.get(campus_code)
        return cals is not None and len(cals) > 0

    def get_campus_calendars(self, campus_code):
        if self.exists(campus_code):
            return sorted(self.campus_calendars[campus_code].values())
        return None

    def get_calendar(self, campus_code, calendarid):
        if self.exists(campus_code):
            return self.campus_calendars[campus_code].get(calendarid)
        return None

    def has_calendar(self, campus_code, calendarid):
        return (self.exists(campus_code) and
                self.get_calendar(campus_code, calendarid) is not None)

    def total_calendars(self, campus_code):
        if self.exists(campus_code):
            return len(self.get_campus_calendars(campus_code))
        return 0


def _is_valid_calendarid(calendarid):
    return re_cal_id.match(str(calendarid)) is not None


def _get_campus_calenders(campus):
    """
    :except DataFailureException: when the request failed
    """
    if is_bot(campus):
        resp = post_bot_resource(calendarlist_url, "{}")
    elif is_tac(campus):
        resp = post_tac_resource(calendarlist_url, "{}")
    elif is_sea(campus):
        resp = post_sea_resource(calendarlist_url, "{}")
    else:
        logger.error("Invalid campus code: {0}".format(campus))
        return None
    request_id = "{0} {1}".format(campus, calendarlist_url)
    return load_json(request_id, resp)
