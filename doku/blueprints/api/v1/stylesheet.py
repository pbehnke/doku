from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, EXCLUDE
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from doku.models import db
from doku.models.document import Variable
from doku.models.schemas import DocumentSchema, TemplateSchema, StylesheetSchema
from doku.models.template import Template, Stylesheet
from doku.utils.db import get_or_404, get_or_create
from doku.utils.decorators import login_required

bp = Blueprint("api.v1.stylesheet", __name__)


@bp.before_request
@login_required
def login_check():
    pass


@bp.route("/upload/<int:stylesheet_id>", methods=["PUT"])
def upload(stylesheet_id: int):
    style: Stylesheet = get_or_404(
        db.session.query(Stylesheet).filter_by(id=stylesheet_id)
    )
    schema = StylesheetSchema(
        unknown=EXCLUDE, session=db.session, instance=style, partial=True
    )

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    if request.files.get("source", None) is not None:
        file: FileStorage = request.files.get("source")
        data["source"] = file.read()
        file.close()

    try:
        stylesheet = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    db.session.commit()

    result = schema.dump(stylesheet)
    return jsonify(result)


@bp.route("/", methods=["PUT"])
def update():
    return StylesheetSchema.update()


@bp.route("/", methods=["POST"])
def create():
    return StylesheetSchema.create()


@bp.route("/", methods=["GET"])
def get_all():
    return StylesheetSchema.get_all()


@bp.route("/<int:template_id>/", methods=["GET"])
def get(template_id: int):
    return StylesheetSchema.get(template_id)


@bp.route("/<int:template_id>/", methods=["DELETE"])
def delete(template_id: int):
    return StylesheetSchema.delete(template_id)
