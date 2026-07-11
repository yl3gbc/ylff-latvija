from flask import Flask, redirect, request, send_from_directory, session
from flask_cors import CORS
from sqlalchemy import text

from admin.deactivate import admin_deactivate_bp
from admin.delete_media import admin_delete_media_bp
from admin.media_detail import admin_media_detail_bp
from admin.routes import admin_bp
from admin.uploads import admin_uploads_bp
from admin.users import admin_users_bp
from auth.routes import auth_bp
from config import Config
from extensions import db
from models.activation import Activation
from models.media import MediaFile
from models.object import YLFFObject
from models.page_content import PageContent
from models.qso_record import QSORecord
from models.expedition_plan import ExpeditionPlan
from routes.activations import activations_bp
from routes.admin_activations_page import admin_activations_page_bp
from routes.admin_adif_upload import admin_adif_upload_bp
from routes.admin_activations_manage import admin_activations_manage_bp
from routes.admin_auth import admin_auth_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.admin_pages import admin_pages_bp
from routes.admin_objects import admin_objects_bp
from routes.admin_expeditions import admin_expeditions_bp
from routes.call_search import call_search_bp
from routes.expedition_plan import expedition_plan_bp
from routes.home_page import home_page_bp
from routes.object_detail import object_detail_bp
from routes.object_geojson import object_geojson_bp
from routes.object_list import object_list_bp
from routes.object_page import object_page_bp
from routes.objects import objects_bp
from routes.operator_page import operator_page_bp
from routes.public_pages import public_pages_bp
from routes.top_objects import top_objects_bp
from routes.top_operators import top_operators_bp
from routes.users import users_bp


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)


@app.before_request
def protect_admin_routes():
    protected_prefixes = (
        "/ylff-control",
        "/ylff-control-2026",
    )

    public_admin_paths = (
        "/ylff-control/login",
        "/ylff-control/logout",
    )

    path = request.path

    if path in public_admin_paths:
        return None

    if path.startswith(protected_prefixes):
        if not session.get("ylff_admin_logged_in"):
            return redirect(
                "/ylff-control/login?next=" + path
            )

    return None


app.register_blueprint(auth_bp)
app.register_blueprint(admin_auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_users_bp)
app.register_blueprint(admin_deactivate_bp)
app.register_blueprint(admin_uploads_bp)
app.register_blueprint(admin_delete_media_bp)
app.register_blueprint(admin_media_detail_bp)
app.register_blueprint(home_page_bp)
app.register_blueprint(objects_bp)
app.register_blueprint(object_geojson_bp)
app.register_blueprint(object_detail_bp)
app.register_blueprint(object_list_bp)
app.register_blueprint(object_page_bp)
app.register_blueprint(activations_bp)
app.register_blueprint(admin_activations_page_bp)
app.register_blueprint(admin_adif_upload_bp)
app.register_blueprint(admin_activations_manage_bp)
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(admin_pages_bp)
app.register_blueprint(admin_objects_bp)
app.register_blueprint(admin_expeditions_bp)
app.register_blueprint(call_search_bp)
app.register_blueprint(expedition_plan_bp)
app.register_blueprint(operator_page_bp)
app.register_blueprint(public_pages_bp)
app.register_blueprint(top_operators_bp)
app.register_blueprint(top_objects_bp)
app.register_blueprint(users_bp)


with app.app_context():
    db.create_all()


@app.route("/health")
def health():
    return {
        "status": "healthy",
    }


@app.route("/db-check")
def db_check():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "ok",
        }

    except Exception as error:
        return {
            "database": "error",
            "message": str(error),
        }, 500


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        "/app/uploads",
        filename,
    )


@app.route("/map")
def ylff_map():
    return send_from_directory(
        "/app/static",
        "ylff-map.html",
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8003,
        debug=True,
    )
