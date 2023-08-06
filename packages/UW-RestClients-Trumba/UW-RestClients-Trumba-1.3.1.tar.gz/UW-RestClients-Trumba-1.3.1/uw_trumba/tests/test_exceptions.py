from unittest import TestCase
from commonconf import settings
from uw_trumba.exceptions import AccountNameEmpty, AccountNotExist,\
    AccountUsedByDiffUser, CalendarNotExist, CalendarOwnByDiffAccount,\
    InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher,\
    NoAllowedPermission, ErrorCreatingEditor, NoDataReturned, UnknownError,\
    UnexpectedError, UnknownError


class TrumbaTestExceptions(TestCase):

    def test_exceptions(self):
        ex = CalendarNotExist("test_url", 3006)
        self.assertEqual(str(ex), "test_url ==> 3006: CalendarNotExist")

        ex = CalendarOwnByDiffAccount("test_url", 3007)
        self.assertEqual(str(ex),
                         "test_url ==> 3007: CalendarOwnByDiffAccount")

        ex = AccountNotExist("test_url", 3008)
        self.assertEqual(str(ex),
                         "test_url ==> 3008: AccountNotExist")

        ex = AccountUsedByDiffUser("test_url", 3009)
        self.assertEqual(str(ex),
                         "test_url ==> 3009: AccountUsedByDiffUser")

        ex = InvalidPermissionLevel("test_url", 3010)
        self.assertEqual(str(ex),
                         "test_url ==> 3010: InvalidPermissionLevel")

        ex = FailedToClosePublisher("test_url", 3011)
        self.assertEqual(str(ex),
                         "test_url ==> 3011: FailedToClosePublisher")

        ex = InvalidEmail("test_url", 3014)
        self.assertEqual(str(ex),
                         "test_url ==> 3014: InvalidEmail")

        ex = NoAllowedPermission("test_url", 3015)
        self.assertEqual(str(ex),
                         "test_url ==> 3015: NoAllowedPermission")

        ex = AccountNameEmpty("test_url", 3016)
        self.assertEqual(str(ex),
                         "test_url ==> 3016: AccountNameEmpty")

        ex = ErrorCreatingEditor("test_url", 3017)
        self.assertEqual(str(ex),
                         "test_url ==> 3017: ErrorCreatingEditor")

        ex = UnexpectedError("test_url", 200)
        self.assertEqual(str(ex),
                         "test_url ==> 200: UnexpectedError")

        ex = UnknownError("test_url", 200)
        self.assertEqual(str(ex),
                         "test_url ==> 200: UnknownError")
