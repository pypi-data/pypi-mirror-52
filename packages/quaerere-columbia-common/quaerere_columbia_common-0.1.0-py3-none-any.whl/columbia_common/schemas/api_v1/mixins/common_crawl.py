__all__ = ['CCDataFieldsMixin', 'CCIndexesFieldsMixin', 'CCScansFieldsMixin']

from marshmallow import fields


class CCDataFieldsMixin:
    url_key = fields.String(required=True, load_from='urlkey')
    timestamp = fields.DateTime(format="%Y%m%d%H%M%S", required=True)
    url = fields.Url(required=True)
    status = fields.Integer(required=True)
    filename = fields.String(required=True)
    offset = fields.Integer()
    digest = fields.String()
    length = fields.Integer()
    mime = fields.String()
    mime_detected = fields.String(load_from='mime-detected')
    charset = fields.String()
    languages = fields.String()


class CCIndexesFieldsMixin:
    id = fields.String(required=True)
    name = fields.String(required=True)
    timegate = fields.Url(required=True)
    cdx_api = fields.Url(required=True, load_from='cdx-api')


class CCScansFieldsMixin:
    web_site_key = fields.String(required=True)
    web_site_url = fields.Url(required=True)
    cc_index_key = fields.String(required=True)
    status = fields.String()
    task_id = fields.UUID()
