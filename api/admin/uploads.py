import os
from uuid import uuid4

from flask import Blueprint, request

from auth.decorators import admin_required
from extensions import db
from models.media import MediaFile


admin_uploads_bp = Blueprint(
    "admin_uploads",
    __name__,
    url_prefix="/admin/uploads",
)

UPLOAD_DIR = "/app/uploads"


@admin_uploads_bp.route("/image", methods=["POST"])
@admin_required
def upload_image(current_user):
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "Empty filename"}, 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    file.save(file_path)

    media_file = MediaFile(
        filename=filename,
        original_filename=file.filename,
        file_size=os.path.getsize(file_path),
        mime_type=file.mimetype,
        uploaded_by=current_user.id,
    )

    db.session.add(media_file)
    db.session.commit()

    return {
        "message": "File uploaded",
        "file": {
            "id": media_file.id,
            "filename": media_file.filename,
            "original_filename": media_file.original_filename,
            "mime_type": media_file.mime_type,
            "file_size": media_file.file_size,
            "path": f"/uploads/{media_file.filename}",
        },
    }, 201


@admin_uploads_bp.route("", methods=["GET"])
@admin_required
def list_uploads(current_user):
    files = MediaFile.query.order_by(MediaFile.created_at.desc()).all()

    return {
        "files": [
            {
                "id": file.id,
                "filename": file.filename,
                "original_filename": file.original_filename,
                "file_size": file.file_size,
                "mime_type": file.mime_type,
                "uploaded_by": file.uploaded_by,
                "created_at": file.created_at.isoformat() if file.created_at else None,
                "url": f"/uploads/{file.filename}",
            }
            for file in files
        ]
    }