import json
from restclients_core import models


EDITOR = 'editor'
SHOWON = 'showon'
EDITOR_GROUP_DESC =\
     "Specifying who can add/edit/delete events on this calendar"
SHOWON_GROUP_DESC =\
    "Specifying the editor groups who can share their calendar events" +\
    " on this calendar"
ADMIN_GROUP_NAME = 'u_eventcal_support'


def is_bot(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.BOT_CAMPUS_CODE


def is_sea(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.SEA_CAMPUS_CODE


def is_tac(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.TAC_CAMPUS_CODE


def is_valid_campus_code(campus_code):
    return is_bot(campus_code) or is_sea(campus_code) or is_tac(campus_code)


def is_editor(group_type):
    # group_type: editor or showon in lower case
    return group_type is not None and group_type == EDITOR


def is_showon(group_type):
    # group_type: editor or showon in lower case
    return group_type is not None and group_type == SHOWON


class TrumbaCalendar(models.Model):
    SEA_CAMPUS_CODE = 'sea'
    BOT_CAMPUS_CODE = 'bot'
    TAC_CAMPUS_CODE = 'tac'
    CAMPUS_CHOICES = (
        (SEA_CAMPUS_CODE, 'Seattle'),
        (BOT_CAMPUS_CODE, 'Bothell'),
        (TAC_CAMPUS_CODE, 'Tacoma')
        )
    calendarid = models.PositiveIntegerField()
    campus = models.CharField(max_length=3,
                              choices=CAMPUS_CHOICES,
                              default=SEA_CAMPUS_CODE)
    name = models.CharField(max_length=196, default=None)

    def get_group_admin(self):
        return ADMIN_GROUP_NAME

    def get_group_desc(self, group_type):
        # group_type: editor or showon in lower case
        if is_editor(group_type):
            return EDITOR_GROUP_DESC
        else:
            return SHOWON_GROUP_DESC

    def get_group_name(self, group_type):
        # group_type: editor or showon in lower case
        return "u_eventcal_{0}_{1}-{2}".format(self.campus,
                                               self.calendarid,
                                               group_type)

    def get_group_title(self, group_type):
        # group_type: editor or showon in lower case
        return "{0} calendar {1} group".format(self.name, group_type)

    def is_bot(self):
        return is_bot(self.campus)

    def is_sea(self):
        return is_sea(self.campus)

    def is_tac(self):
        return is_tac(self.campus)

    def add_permission(self, permission):
        self.permissions[permission.uwnetid] = permission

    def to_json(self):
        return {'calendarid': self.calendarid,
                'campus': self.campus,
                'name': self.name,
                'permissions': {k: v.to_json()
                                for k, v in self.permissions.items()}}

    def __eq__(self, other):
        return self.calendarid == other.calendarid

    def __lt__(self, other):
        return (self.campus == other.campus and
                self.name < other.name)

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        super(TrumbaCalendar, self).__init__(*args, **kwargs)
        self.permissions = {}  # a dict of {uwnetid, Permission}


class Permission(models.Model):
    EDIT = 'EDIT'
    PUBLISH = 'PUBLISH'
    REPUBLISH = 'REPUBLISH'
    SHOWON = 'SHOWON'
    VIEW = 'VIEW'
    NONE = 'NONE'
    LEVEL_CHOICES = ((EDIT, 'Can add, delete and change content'),
                     (PUBLISH, 'Can view, edit and publish'),
                     (REPUBLISH, 'Can view, edit and republish'),
                     (SHOWON, 'Can view and show on'),
                     (VIEW, 'Can view content'),
                     (NONE, 'None'))
    uwnetid = models.CharField(max_length=32)
    display_name = models.CharField(max_length=96, default=None)
    level = models.CharField(max_length=6, choices=LEVEL_CHOICES, default=VIEW)

    def get_trumba_userid(self):
        return "{0}@uw.edu".format(self.uwnetid)

    def is_edit(self):
        return self.level is not None and self.level == Permission.EDIT

    def is_showon(self):
        return self.level is not None and self.level == Permission.SHOWON

    def is_publish(self):
        return self.level is not None and self.level == Permission.PUBLISH

    def is_republish(self):
        return self.level is not None and self.level == Permission.REPUBLISH

    def is_view(self):
        return self.level is not None and self.level == Permission.VIEW

    def in_editor_group(self):
        return self.is_edit() or self.is_publish()

    def in_showon_group(self):
        return self.is_showon() or self.is_republish()

    def is_showon_or_higher(self):
        # Return True if self.level is edit or a higher permission
        return self.in_editor_group() or self.in_showon_group()

    def is_higher_permission(self, level):
        # Return True if self.level is higher than the given level
        return (self.is_publish() and
                level != Permission.PUBLISH or
                self.is_edit() and
                level != Permission.PUBLISH and
                level != Permission.EDIT or
                self.is_showon() and
                level == Permission.VIEW)

    def set_edit(self):
        self.level = Permission.EDIT

    def set_publish(self):
        self.level = Permission.PUBLISH

    def set_showon(self):
        self.level = Permission.SHOWON

    def set_republish(self):
        self.level = Permission.REPUBLISH

    def set_view(self):
        self.level = Permission.VIEW

    def to_json(self):
        return {'uwnetid': self.uwnetid,
                'display_name': self.display_name,
                'level': self.level}

    def __eq__(self, other):
        return (self.uwnetid == other.uwnetid and
                self.display_name == other.display_name and
                self.level == other.level)

    def __lt__(self, other):
        return (self.is_higher_permission(other.level) or
                self.level == other.level and
                self.uwnetid < other.uwnetid)

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        super(Permission, self).__init__(*args, **kwargs)


def new_edit_permission(uwnetid, display_name=None):
    return Permission(uwnetid=uwnetid,
                      display_name=display_name,
                      level=Permission.EDIT)


def new_showon_permission(uwnetid, display_name=None):
    return Permission(uwnetid=uwnetid,
                      display_name=display_name,
                      level=Permission.SHOWON)
