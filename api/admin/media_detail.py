from flask import Blueprint

from auth.decorators import admin_required
from models.media import MediaFile


admin_media_detail_bp = Blueprint(
    "admin_media_detail",
    __name__,
    url_prefix="/admin/uploads",
)


@admin_media_detail_bp.route("/<int:file_id>", methods=["GET"])
@admin_required
def media_detail(current_user, file_id):
    media_file = MediaFile.query.get(file_id)

    if not media_file:
        return {
            "error": "File not found",
        }, 404

    return {
        "id": media_file.id,
        "filename": media_file.filename,
        "original_filename": media_file.original_filename,
        "mime_type": media_file.mime_type,
        "file_size": media_file.file_size,
        "uploaded_by": media_file.uploaded_by,
        "created_at": media_file.created_at.isoformat()
        if media_file.created_at
        else None,
        "url": f"/uploads/{media_file.filename}",
    }
