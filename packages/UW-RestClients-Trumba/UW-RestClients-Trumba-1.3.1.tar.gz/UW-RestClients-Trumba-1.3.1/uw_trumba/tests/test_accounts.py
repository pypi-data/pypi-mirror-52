from unittest import TestCase
from commonconf import settings
from restclients_core.exceptions import DataFailureException
from uw_trumba.account import _make_add_account_url,\
    add_editor, _make_del_account_url, delete_editor,\
    _make_set_permissions_url, set_bot_permissions, set_sea_permissions,\
    set_tac_permissions, set_perm_editor, set_perm_showon, set_perm_none,\
    _is_editor_added, _is_editor_deleted, _is_permission_set,\
    _check_err
from uw_trumba.models import TrumbaCalendar
from uw_trumba.exceptions import AccountNameEmpty, AccountNotExist,\
    AccountUsedByDiffUser, CalendarNotExist, CalendarOwnByDiffAccount,\
    InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher,\
    NoAllowedPermission, ErrorCreatingEditor, NoDataReturned, UnknownError,\
    UnexpectedError


ADD_ACC_URL = "/service/accounts.asmx/CreateEditor?"
DEL_ACC_URL = "/service/accounts.asmx/CloseEditor?"
SET_PERM_URL = "/service/calendars.asmx/SetPermissions?"


class TrumbaTestAccounts(TestCase):

    def test_make_add_account_url(self):
        self.assertEqual(
            _make_add_account_url('Margaret Murray',
                                  'murray4'),
            (ADD_ACC_URL + "Name=Margaret%20Murray&" +
             "Email=murray4@uw.edu&Password="))

    def test_add_editor_error_cases(self):
        self.assertRaises(AccountNameEmpty,
                          add_editor, '', '')

        self.assertRaises(InvalidEmail,
                          add_editor, '010', '')

        self.assertRaises(AccountUsedByDiffUser,
                          add_editor, '011', 'test10')

    def test_add_editor_normal_cases(self):
        self.assertTrue(add_editor('008', 'test8'))
        self.assertTrue(add_editor('010', 'test10'))

    def test_make_del_account_url(self):
        self.assertEqual(_make_del_account_url('murray4'),
                         (DEL_ACC_URL + "Email=murray4@uw.edu"))

    def test_delete_editor_normal_cases(self):
        self.assertTrue(delete_editor('test10'))

    def test_delete_editor_error_cases(self):
        self.assertRaises(AccountNotExist,
                          delete_editor, '')

        self.assertRaises(AccountNotExist,
                          delete_editor, 'test')

    def test_make_set_permissions_url(self):
        self.assertEqual(
            _make_set_permissions_url(1, 'test10', 'EDIT'),
            (SET_PERM_URL + "CalendarID=1&Email=test10@uw.edu" +
             "&Level=EDIT"))

    def test_set_sea_permissions_error_cases(self):
        self.assertRaises(AccountNotExist,
                          set_sea_permissions, 1, '', 'EDIT')

        self.assertRaises(NoAllowedPermission,
                          set_sea_permissions, 1, 'test10', 'PUBLISH')

    def test_set_sea_permissions_normal_cases(self):
        self.assertTrue(set_sea_permissions(1, 'test10', 'SHOWON'))
        self.assertTrue(set_sea_permissions(1, 'test10', 'EDIT'))
        cal = TrumbaCalendar(calendarid=1, campus='sea')
        self.assertTrue(set_perm_editor(cal, 'test10'))
        self.assertTrue(set_perm_showon(cal, 'test10'))
        self.assertTrue(set_perm_none(cal, 'test10'))

    def test_is_permission_set(self):
        self.assertTrue(_is_permission_set(1003))
        self.assertFalse(_is_permission_set(-1003))

    def test_is_editor_added(self):
        self.assertTrue(_is_editor_added(1001))
        self.assertTrue(_is_editor_added(3012))
        self.assertFalse(_is_editor_added(-1001))

    def test_is_editor_deleted(self):
        self.assertTrue(_is_editor_deleted(1002))
        self.assertFalse(_is_editor_deleted(-1002))

    def test_check_err(self):
        self.assertRaises(CalendarNotExist,
                          _check_err,
                          3006, 'test if CalendarNotExist is thrown')

        self.assertRaises(CalendarOwnByDiffAccount,
                          _check_err,
                          3007, 'test if CalendarOwnByDiffAccount is thrown')

        self.assertRaises(AccountNotExist,
                          _check_err,
                          3008, 'test if AccountNotExist is thrown')

        self.assertRaises(AccountUsedByDiffUser,
                          _check_err,
                          3009, 'test if AccountUsedByDiffUser is thrown')

        self.assertRaises(AccountUsedByDiffUser,
                          _check_err,
                          3013, 'test if AccountUsedByDiffUser is thrown')

        self.assertRaises(InvalidPermissionLevel,
                          _check_err,
                          3010, 'test if InvalidPermissionLevel is thrown')

        self.assertRaises(FailedToClosePublisher,
                          _check_err,
                          3011, 'test if FailedToClosePublisher is thrown')

        self.assertRaises(InvalidEmail,
                          _check_err,
                          3014, 'test if InvalidEmail is thrown')

        self.assertRaises(NoAllowedPermission,
                          _check_err,
                          3015, 'test if NoAllowedPermission is thrown')

        self.assertRaises(AccountNameEmpty,
                          _check_err,
                          3016, 'test if AccountNameEmpty is thrown')

        self.assertRaises(ErrorCreatingEditor,
                          _check_err,
                          3017, 'test if ErrorCreatingEditor is thrown')

        self.assertRaises(ErrorCreatingEditor,
                          _check_err,
                          3018, 'test if ErrorCreatingEditor is thrown')

        self.assertRaises(UnexpectedError,
                          _check_err,
                          3020, 'test if UnexpectedError is thrown')

    def test_set_bot_permissions_error_cases(self):
        self.assertRaises(AccountNotExist,
                          set_bot_permissions, 2, '', 'EDIT')

        self.assertRaises(NoAllowedPermission,
                          set_bot_permissions, 2, 'test10', 'PUBLISH')

    def test_set_bot_permissions_normal_cases(self):
        self.assertTrue(set_bot_permissions(2, 'test10', 'SHOWON'))
        self.assertTrue(set_bot_permissions(2, 'test10', 'EDIT'))
        cal = TrumbaCalendar(calendarid=2, campus='bot')
        self.assertTrue(set_perm_editor(cal, 'test10'))
        self.assertTrue(set_perm_showon(cal, 'test10'))
        self.assertTrue(set_perm_none(cal, 'test10'))

    def test_set_tac_permissions_error_cases(self):
        self.assertRaises(AccountNotExist,
                          set_tac_permissions, 3, '', 'EDIT')

        self.assertRaises(NoAllowedPermission,
                          set_tac_permissions, 3, 'test10', 'PUBLISH')

    def test_set_tac_permissions_normal_cases(self):
        self.assertTrue(set_tac_permissions(3, 'test10', 'SHOWON'))
        self.assertTrue(set_tac_permissions(3, 'test10', 'EDIT'))
        cal = TrumbaCalendar(calendarid=3, campus='tac')
        self.assertTrue(set_perm_editor(cal, 'test10'))
        self.assertTrue(set_perm_showon(cal, 'test10'))
        self.assertTrue(set_perm_none(cal, 'test10'))
