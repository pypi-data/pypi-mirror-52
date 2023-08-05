#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom group management forms for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import sqlalchemy
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

#
# Flask related modules.
#
from flask_babel import gettext, lazy_gettext

#
# Custom modules.
#
import hawat.db
import hawat.forms
from mentat.datatype.sqldb import GroupModel, UserModel


def check_name_existence(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating user logins during account create action.
    """
    try:
        hawat.db.db_get().session.query(GroupModel).\
            filter(GroupModel.name == field.data).\
            one()
    except sqlalchemy.orm.exc.NoResultFound:
        return
    except:  # pylint: disable=locally-disabled,bare-except
        pass
    raise wtforms.validators.ValidationError(gettext('Group with this name already exists.'))


def check_name_uniqueness(form, field):
    """
    Callback for validating user logins during account update action.
    """
    item = hawat.db.db_get().session.query(GroupModel).\
        filter(GroupModel.name == field.data).\
        filter(GroupModel.id != form.db_item_id).\
        all()
    if not item:
        return
    raise wtforms.validators.ValidationError(gettext('Group with this name already exists.'))


def check_parent_not_self(form, field):
    """
    Callback for validating that parent group is not self.
    """
    if field.data and form.db_item_id == field.data.id:
        raise wtforms.validators.ValidationError(gettext('You must not select a group as its own parent! Naughty, naughty you!'))


def get_available_users():
    """
    Query the database for list of all available user accounts.
    """
    return hawat.db.db_query(UserModel).order_by(UserModel.fullname).all()


def format_select_option_label_user(item):
    """
    Format option for selection of user accounts.
    """
    return "{} ({})".format(item.fullname, item.login)


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return hawat.db.db_query(GroupModel).order_by(GroupModel.name).all()


class BaseGroupForm(hawat.forms.BaseItemForm):
    """
    Class representing base group form.
    """
    description = wtforms.StringField(
        lazy_gettext('Description:'),
        validators = [
            wtforms.validators.DataRequired()
        ]
    )
    source = wtforms.HiddenField(
        default = 'manual',
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 50)
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )


class CreateGroupForm(BaseGroupForm):
    """
    Class representing group create form.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 100),
            check_name_existence
        ]
    )
    enabled = wtforms.RadioField(
        lazy_gettext('State:'),
        validators = [
            wtforms.validators.InputRequired(),
        ],
        choices = [
            (True,  lazy_gettext('Enabled')),
            (False, lazy_gettext('Disabled'))
        ],
        filters = [hawat.forms.str_to_bool],
        coerce = hawat.forms.str_to_bool
    )
    members = QuerySelectMultipleField(
        lazy_gettext('Members:'),
        query_factory = get_available_users,
        get_label = format_select_option_label_user,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>')
    )
    managers = QuerySelectMultipleField(
        lazy_gettext('Managers:'),
        query_factory = get_available_users,
        get_label = format_select_option_label_user,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>')
    )
    parent = QuerySelectField(
        lazy_gettext('Parent group:'),
        validators = [
            wtforms.validators.Optional(),
            check_parent_not_self
        ],
        query_factory = get_available_groups,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # Handle additional custom keywords.
        #

        self.db_item_id = None


class UpdateGroupForm(BaseGroupForm):
    """
    Class representing group update form for regular users.
    """


class AdminUpdateGroupForm(BaseGroupForm):
    """
    Class representing group update form for administrators.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 100),
            check_name_uniqueness
        ]
    )
    enabled = wtforms.RadioField(
        lazy_gettext('State:'),
        validators = [
            wtforms.validators.InputRequired(),
        ],
        choices = [
            (True,  lazy_gettext('Enabled')),
            (False, lazy_gettext('Disabled'))
        ],
        filters = [hawat.forms.str_to_bool],
        coerce = hawat.forms.str_to_bool
    )
    members = QuerySelectMultipleField(
        lazy_gettext('Members:'),
        query_factory = get_available_users,
        get_label = format_select_option_label_user,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>')
    )
    managers = QuerySelectMultipleField(
        lazy_gettext('Managers:'),
        query_factory = get_available_users,
        get_label = format_select_option_label_user,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>')
    )
    parent = QuerySelectField(
        lazy_gettext('Parent group:'),
        validators = [
            wtforms.validators.Optional(),
            check_parent_not_self
        ],
        query_factory = get_available_groups,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # Handle additional custom keywords.
        #

        # Store the ID of original item in database to enable the ID uniqueness
        # check with check_name_uniqueness() validator.
        self.db_item_id = kwargs['db_item_id']
