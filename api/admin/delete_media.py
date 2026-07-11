import os

from flask import Blueprint

from auth.decorators import admin_required
from extensions import db
from models.media import MediaFile


admin_delete_media_bp = Blueprint(
    "admin_delete_media",
    __name__,
    url_prefix="/admin/uploads",
)

UPLOAD_DIR = "/app/uploads"


@admin_delete_media_bp.route("/<int:file_id>", methods=["DELETE"])
@admin_required
def delete_media(current_user, file_id):
    media_file = db.session.get(MediaFile, file_id)

    if not media_file:
        return {
            "error": "File not found",
        }, 404

    file_path = os.path.join(
        UPLOAD_DIR,
        media_file.filename,
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(media_file)

    db.session.commit()

    return {
        "message": "File deleted",
        "file_id": file_id,
    }
