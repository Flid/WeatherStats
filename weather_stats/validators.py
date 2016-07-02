# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps

from formencode.declarative import singletonmethod
from formencode.schema import Schema as fSchema
from formencode.validators import *


def _patch_validator_message(f):
    @wraps(f)
    def _patched(self, msgName, state, **kw):
        return (msgName, f(self, msgName, state, **kw))

    return singletonmethod(_patched)


def _patch_invalid_init(f):
    @wraps(f)
    def _patched(self, *args, **kwargs):
        f(self, *args, **kwargs)
        try:
            self.code, self.msg = self.msg
        except ValueError:
            self.code = None

    return _patched

# Patch formencode to save Invalid key, which caused an error message
Validator.message = _patch_validator_message(Validator.__dict__['message'].func)
Invalid.__init__ = _patch_invalid_init(Invalid.__init__)


# Let's add `description` field to validator
old_validator_init = FancyValidator.__init__


def patched_validator_init(self, *args, **kwargs):
    self.description = kwargs.pop('description', None)
    return old_validator_init(self, *args, **kwargs)

FancyValidator.__init__ = patched_validator_init


class Schema(fSchema):
    allow_extra_fields = True
    filter_extra_fields = True


class Pipeline(FancyValidator):
    validators_list = None

    def __init__(self, *args, **kwargs):
        super(Pipeline, self).__init__(**kwargs)
        self.validators_list = args

    def _to_python(self, value, state):

        for validator in self.validators_list:
            value = validator.to_python(value, state)

        return value


class GTEValidator(FancyValidator):
    """
    Allows to check if value of one input arg is less than another arg.
    """
    name_less = None
    name_greater = None

    messages = {
        'invalid': 'value of `%(name_less)s` should not be less than `%(name_greater)s`',
    }

    def _to_python(self, value_dict, state):
        assert self.name_greater
        assert self.name_less

        if value_dict[self.name_less] <= value_dict[self.name_greater]:
            return value_dict

        message = self.message(
            'invalid',
            state,
            name_less=self.name_less,
            name_greater=self.name_greater,
        )

        raise Invalid(
            message,
            '',
            state,
            error_dict={
                self.name_greater: Invalid(message, value_dict, state),
            },
        )
