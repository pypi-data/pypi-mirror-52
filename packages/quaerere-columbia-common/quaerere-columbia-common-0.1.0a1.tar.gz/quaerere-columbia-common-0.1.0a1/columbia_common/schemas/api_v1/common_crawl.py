__all__ = ['CCDataSchema', 'CCIndexesSchema', 'CCScansSchema']

from marshmallow import fields
from quaerere_base_common.schema import BaseSchema

from .mixins import (
    CCDataFieldsMixin, CCIndexesFieldsMixin, CCScansFieldsMixin)


class CCDataSchema(CCDataFieldsMixin, BaseSchema):
    _key = fields.String()


class CCIndexesSchema(CCIndexesFieldsMixin, BaseSchema):
    _key = fields.String()


class CCScansSchema(CCScansFieldsMixin, BaseSchema):
    _key = fields.String()
