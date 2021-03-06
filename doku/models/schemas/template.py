from typing import Optional

from flask import url_for, jsonify
from marshmallow import fields, ValidationError
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from werkzeug.exceptions import BadRequest

from doku.models import DateSchemaMixin, db
from doku.models.document import Variable
from doku.models.schemas.common import ApiSchemaMixin, DokuSchema
from doku.models.template import Template, Stylesheet
from doku.utils.db import get_or_create


class TemplateSchema(DokuSchema, DateSchemaMixin, ApiSchemaMixin):
    class Meta:
        model = Template
        exclude = ("documents", "styles")
        load_instance = True

    API_NAME = "template"

    id = auto_field()
    name = auto_field()
    source = auto_field()
    documents = Nested("DocumentSchema", many=True, exclude=("template",))
    base_style = Nested("StylesheetSchema", exclude=("base_templates",))
    styles = Nested("StylesheetSchema", many=True, exclude=("templates",))
    available_fields = fields.List(fields.String, dump_only=True)
    add_styles_url = fields.Method("_add_styles_url", dump_only=True, allow_none=True)
    remove_styles_url = fields.Method(
        "_remove_styles_url", dump_only=True, allow_none=True
    )

    def _add_styles_url(self, template) -> Optional[str]:
        if template.id is None:
            return None
        return url_for("api.v1.template.add_stylesheet", template_id=template.id)

    def _remove_styles_url(self, template) -> Optional[str]:
        if template.id is None:
            return None
        return url_for("api.v1.template.remove_stylesheet", template_id=template.id)

    @classmethod
    def update(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(partial=True, session=db.session, many=isinstance(data, list))
        try:
            template = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        for document in template.documents:
            for name in template.available_fields:
                get_or_create(Variable, document=document, name=name)
        if commit:
            db.session.commit()
        result = schema.dump(template)
        return jsonify(result)


class StylesheetSchema(DokuSchema, DateSchemaMixin, ApiSchemaMixin):
    class Meta:
        model = Stylesheet
        exclude = ("base_templates", "templates")
        load_instance = True

    API_NAME = "template"

    id = auto_field()
    name = auto_field()
    source = auto_field()
    base_templates = Nested("TemplateSchema", exclude=("base_style",), many=True)
    templates = Nested("TemplateSchema", exclude=("styles",), many=True)

    upload_url = fields.Method("_upload_url", dump_only=True, allow_none=True)

    def _upload_url(self, stylesheet) -> Optional[str]:
        if stylesheet.id is None:
            return None
        return url_for("api.v1.stylesheet.upload", stylesheet_id=stylesheet.id)
