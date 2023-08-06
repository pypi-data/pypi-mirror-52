"""
Interfacing Trumba Accounts' Service, the account module provides
functions for adding and deleting editors and set their calendar permissions
The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""


from functools import partial
import logging
import re
from lxml import etree, objectify
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import quote, unquote
from restclients_core.exceptions import DataFailureException
from uw_trumba.models import Permission
from uw_trumba import (
    get_bot_resource, get_sea_resource, get_tac_resource)
from uw_trumba.exceptions import (
    AccountNameEmpty, AccountNotExist, AccountUsedByDiffUser,
    CalendarNotExist, CalendarOwnByDiffAccount,
    InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher,
    NoAllowedPermission, ErrorCreatingEditor, NoDataReturned,
    UnexpectedError, UnknownError)


add_account_url_prefix = "/service/accounts.asmx/CreateEditor"
del_account_url_prefix = "/service/accounts.asmx/CloseEditor"
set_permission_url_prefix = "/service/calendars.asmx/SetPermissions"
logger = logging.getLogger(__name__)


def _make_add_account_url(name, userid):
    """
    :return: the URL string for the GET request call to
    Trumba CreateEditor method
    """
    return "{0}?Name={1}&Email={2}@uw.edu&Password=".format(
        add_account_url_prefix, re.sub(r' ', '%20', name), userid)


def add_editor(name, userid):
    """
    :param name: a string representing the user's name
    :param userid: a string representing the user's UW NetID
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_add_account_url(name, userid)
    return _process_resp(url,
                         get_sea_resource(url),
                         _is_editor_added
                         )


def _make_del_account_url(userid):
    """
    :return: the URL string for GET request call to
    Trumba CloseEditor method
    """
    return "{0}?Email={1}@uw.edu".format(
        del_account_url_prefix, userid)


def delete_editor(userid):
    """
    :param userid: a string representing the user's UW NetID
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_del_account_url(userid)
    return _process_resp(url,
                         get_sea_resource(url),
                         _is_editor_deleted
                         )


def _make_set_permissions_url(calendar_id, userid, level):
    """
    :return: the URL string for GET request call
    to Trumba SetPermissions method
    """
    return "{0}?CalendarID={1}&Email={2}@uw.edu&Level={3}".format(
        set_permission_url_prefix, calendar_id, userid, level)


def set_perm_editor(calendar, userid):
    if calendar.is_bot():
        return set_bot_permissions(calendar.calendarid,
                                   userid, Permission.EDIT)
    elif calendar.is_tac():
        return set_tac_permissions(calendar.calendarid,
                                   userid, Permission.EDIT)
    else:
        return set_sea_permissions(calendar.calendarid,
                                   userid, Permission.EDIT)


def set_perm_showon(calendar, userid):
    if calendar.is_bot():
        return set_bot_permissions(calendar.calendarid,
                                   userid, Permission.SHOWON)
    elif calendar.is_tac():
        return set_tac_permissions(calendar.calendarid,
                                   userid, Permission.SHOWON)
    else:
        return set_sea_permissions(calendar.calendarid,
                                   userid, Permission.SHOWON)


def set_perm_none(calendar, userid):
    if calendar.is_bot():
        return set_bot_permissions(calendar.calendarid,
                                   userid, Permission.NONE)
    elif calendar.is_tac():
        return set_tac_permissions(calendar.calendarid,
                                   userid, Permission.NONE)
    else:
        return set_sea_permissions(calendar.calendarid,
                                   userid, Permission.NONE)


def set_bot_permissions(calendar_id, userid, level):
    """
    :param calendar_id: an integer representing calendar ID
    :param userid: a string representing the user's UW NetID
    :param level: a string representing the permission level
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_set_permissions_url(
        calendar_id, userid, level)
    return _process_resp(url,
                         get_bot_resource(url),
                         _is_permission_set
                         )


def set_sea_permissions(calendar_id, userid, level):
    """
    :param calendar_id: an integer representing calendar ID
    :param userid: a string representing the user's UW NetID
    :param level: a string representing the permission level
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_set_permissions_url(
        calendar_id, userid, level)
    return _process_resp(url,
                         get_sea_resource(url),
                         _is_permission_set
                         )


def set_tac_permissions(calendar_id, userid, level):
    """
    :param calendar_id: an integer representing calendar ID
    :param userid: a string representing the user's UW NetID
    :param level: a string representing the permission level
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_set_permissions_url(
        calendar_id, userid, level)
    return _process_resp(url,
                         get_tac_resource(url),
                         _is_permission_set
                         )


def _process_resp(request_id, response, is_success_func):
    """
    :param request_id: campus url identifying the request
    :param response: the GET method response object
    :param is_success_func: the name of the function for
        verifying a success code
    :return: True if successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    if response.status != 200:
        raise DataFailureException(request_id,
                                   response.status,
                                   response.reason
                                   )
    if response.data is None:
        raise NoDataReturned(request_id, 200)

    root = objectify.fromstring(response.data)
    if (root.ResponseMessage is None or
            root.ResponseMessage.attrib['Code'] is None):
        raise UnknownError(request_id, 200)
    resp_code = int(root.ResponseMessage.attrib['Code'])
    func = partial(is_success_func)
    if func(resp_code):
        return True
    _check_err(resp_code, request_id)


def _is_editor_added(code):
    """
    :param code: an integer value
    :return: True if the code means successful, False otherwise.
    """
    return code == 1001 or code == 3012


def _is_editor_deleted(code):
    """
    :param code: an integer value
    :return: True if the code means successful, False otherwise.
    """
    return code == 1002


def _is_permission_set(code):
    """
    :param code: an integer value
    :return: True if the code means successful, False otherwise.
    """
    return code == 1003


def _check_err(code, request_id):
    """
    :param code: an integer value
    :param request_id: campus url identifying the request
    Check possible error code returned in the response body
    raise the corresponding TrumbaException
    """
    if code == 3006:
        raise CalendarNotExist(request_id, code)
    elif code == 3007:
        raise CalendarOwnByDiffAccount(request_id, code)
    elif code == 3008:
        raise AccountNotExist(request_id, code)
    elif code == 3009 or code == 3013:
        raise AccountUsedByDiffUser(request_id, code)
    elif code == 3010:
        raise InvalidPermissionLevel(request_id, code)
    elif code == 3011:
        raise FailedToClosePublisher(request_id, code)
    elif code == 3014:
        raise InvalidEmail(request_id, code)
    elif code == 3015:
        raise NoAllowedPermission(request_id, code)
    elif code == 3016:
        raise AccountNameEmpty(request_id, code)
    elif code == 3017 or code == 3018:
        raise ErrorCreatingEditor(request_id, code)
    else:
        raise UnexpectedError(request_id, code)
