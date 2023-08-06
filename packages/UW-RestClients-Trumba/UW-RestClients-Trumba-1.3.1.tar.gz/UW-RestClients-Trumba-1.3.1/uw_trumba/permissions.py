"""
Interfacing with Trumba Calendars' service, this module
provides methods to obtain calendar info and
user calendar permissions in Trumba
The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""

import json
import logging
import re
from restclients_core.exceptions import DataFailureException
from uw_trumba.models import Permission
from uw_trumba import (
    post_bot_resource, post_sea_resource, post_tac_resource)
from uw_trumba.exceptions import (
    CalendarOwnByDiffAccount, CalendarNotExist, NoDataReturned,
    UnknownError, UnexpectedError)


logger = logging.getLogger(__name__)
re_email = re.compile(r'[a-z][a-z0-9\-\_\.]{,127}@uw.edu', re.I)
permissions_url = "/service/calendars.asmx/GetPermissions"


class Permissions:

    def __init__(self):
        self.account_set = set()
        # a set of the uwnetids of all the existing accounts

    def account_exists(self, uwnetid):
        return uwnetid in self.account_set

    def add_account(self, uwnetid):
        if not self.account_exists(uwnetid):
            self.account_set.add(uwnetid)

    def get_cal_permissions(self, calendar):
        """
        :param calendar: a TrumbaCalendar object
        Set the calendar.permissions attribute with a dict of
        {uwnetid, Permission} and add uwnetids into self.account_set.
        """
        try:
            data = _get_permissions(calendar)
            if (data.get('d') is not None and
                    data['d'].get('Users') is not None and
                    len(data['d']['Users']) > 0):
                self._load_permissions(calendar, data['d']['Users'])
        except Exception as ex:
            logger.error("get_cal_permissions on {0} ==> {1}".format(
                    calendar, str(ex)))

    def _load_permissions(self, calendar, resp_fragment):
        for record in resp_fragment:
            # skip the non UW users
            if not _is_valid_email(record.get('Email')):
                continue
            netid = _extract_uwnetid(record['Email'])
            perm = Permission(uwnetid=netid,
                              level=record.get('Level'),
                              display_name=record.get('Name'))
            calendar.permissions[netid] = perm
            self.add_account(netid)

    def total_accounts(self):
        return len(self.account_set)


def _create_req_body(calendar_id):
    return json.dumps({'CalendarID': calendar_id})


def _get_permissions(calendar):
    if calendar.is_bot():
        resp = post_bot_resource(
            permissions_url, _create_req_body(calendar.calendarid))
    elif calendar.is_tac():
        resp = post_tac_resource(
            permissions_url, _create_req_body(calendar.calendarid))
    else:
        resp = post_sea_resource(
            permissions_url, _create_req_body(calendar.calendarid))
    request_id = "{0} {1} CalendarID:{2}".format(calendar.campus,
                                                 permissions_url,
                                                 calendar.calendarid)
    return load_json(request_id, resp)


def _is_valid_email(email):
    return re_email.match(email) is not None


def _extract_uwnetid(email):
    return re.sub("@uw.edu", "", email, flags=re.I).lower()


def _check_err(data, request_id):
    """
    :param data: response json data (must be not None).
    Check possible error code returned in the response body
    raise the coresponding exceptions
    """
    if data.get('d') is None:
        raise NoDataReturned(request_id, 200)

    if data['d'].get('Messages') is None:
        return

    msg = data['d']['Messages']
    if len(msg) == 0 or msg[0].get('Code') is None:
        raise UnknownError(request_id, 200)

    code = int(msg[0]['Code'])
    if code == 3006:
        raise CalendarNotExist(request_id, code)
    elif code == 3007:
        raise CalendarOwnByDiffAccount(request_id, code)
    else:
        logger.warn("Unexpected Error Code: {0} {1}".format(
                code, msg[0].get('Description')))
        raise UnexpectedError(request_id, code)


def load_json(request_id, post_response):
    if post_response.status != 200:
        raise DataFailureException(request_id,
                                   post_response.status,
                                   post_response.reason)
    if post_response.data is None:
        raise NoDataReturned(request_id, 200)
    data = json.loads(post_response.data)
    _check_err(data, request_id)
    return data
