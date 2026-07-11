from werkzeug.utils import secure_filename
from pathlib import Path
import html

from flask import Blueprint, redirect, request

from extensions import db
from models.object import YLFFObject
from models.activation import Activation
from models.qso_record import QSORecord


admin_objects_bp = Blueprint(
    "admin_objects",
    __name__,
)


STATUS_OPTIONS = [
    "active",
    "planned",
    "included",
    "inactive",
    "cancelled",
]


# AI mistake record, 2026-06-20:
# Wrong assistant patch inserted object image upload helper constants between
# @admin_objects_bp.route(...) and def admin_objects_list().
# Wrong line that caused SyntaxError and HTTP 502:
#     OBJECT_IMAGE_UPLOAD_DIR = Path(__file__).resolve().parents[1] / "static" / "object-images"
# Correct rule: helper constants/functions must be placed before route decorators
# in this original source file.

OBJECT_IMAGE_UPLOAD_DIR = Path(__file__).resolve().parents[1] / "static" / "object-images"
OBJECT_IMAGE_ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def save_object_image_upload(uploaded_file, reference):
    if not uploaded_file or not uploaded_file.filename:
        return None

    suffix = Path(uploaded_file.filename).suffix.lower()
    if suffix not in OBJECT_IMAGE_ALLOWED_SUFFIXES:
        raise ValueError("Atļauti tikai JPG, JPEG, PNG vai WEBP attēli.")

    OBJECT_IMAGE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_reference = secure_filename(reference)
    filename = f"{safe_reference}{suffix}"
    target = OBJECT_IMAGE_UPLOAD_DIR / filename

    uploaded_file.save(target)

    return f"/static/object-images/{filename}"


@admin_objects_bp.route("/ylff-control/objects")
def admin_objects_list():
    search = request.args.get("search", "").strip()

    query = YLFFObject.query

    if search:
        like = f"%{search}%"

        query = query.filter(
            (YLFFObject.reference.ilike(like))
            | (YLFFObject.name.ilike(like))
            | (YLFFObject.locator.ilike(like))
            | (YLFFObject.status.ilike(like))
        )

    objects = query.order_by(
        YLFFObject.reference.asc()
    ).all()

    rows = ""

    for obj in objects:
        status_class = "badge-green"

        if obj.status == "planned":
            status_class = "badge-yellow"

        if obj.status in ["inactive", "cancelled"]:
            status_class = "badge-red"

        if obj.status == "included":
            status_class = "badge-blue"

        rows += f"""
        <tr>
          <td>{html.escape(obj.reference or "")}</td>
          <td>{html.escape(obj.name or "")}</td>
          <td>{html.escape(obj.locator or "-")}</td>
          <td>{obj.latitude or "-"}</td>
          <td>{obj.longitude or "-"}</td>
          <td>
            <span class="{status_class}">
              {html.escape(obj.status or "-")}
            </span>
          </td>
          <td>
            <a class="button" href="/ylff-control/objects/{obj.reference}">
              Labot
            </a>
            <a class="button secondary" href="/object/{obj.reference}" target="_blank">
              Skatīt
            </a>

            <form
              method="POST"
              action="/ylff-control/objects/{obj.reference}/delete"
              style="display:inline;"
              onsubmit="return confirm('Tiešām dzēst objektu {obj.reference}? Ja objektam ir aktivizācijas vai QSO, dzēšana tiks bloķēta.');"
            >
              <button class="button danger" type="submit">
                Dzēst
              </button>
            </form>
          </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
          <td colspan="7">Objekti nav atrasti.</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>YLFF objekti adminā</title>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: #f4f7fb;
      color: #0f172a;
      font-family: Arial, sans-serif;
    }}

    .layout {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: 280px 1fr;
    }}

    .sidebar {{
      background: #0b1726;
      color: white;
      padding: 24px 18px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 28px;
    }}

    .brand img {{
      width: 54px;
      height: 54px;
      object-fit: contain;
    }}

    .brand-title {{
      font-size: 24px;
      font-weight: bold;
    }}

    .menu-section {{
      margin: 22px 0 10px;
      color: #94a3b8;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .7px;
    }}

    .menu-link {{
      display: block;
      padding: 12px 14px;
      border-radius: 10px;
      color: #e5e7eb;
      text-decoration: none;
      font-weight: 700;
      margin-bottom: 7px;
    }}

    .menu-link:hover,
    .menu-link.active {{
      background: #1d4ed8;
      color: white;
    }}

    .main {{
      padding: 34px;
    }}

    .top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 22px;
    }}

    h1 {{
      margin: 0;
      font-size: 32px;
    }}

    .card {{
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .06);
      overflow: hidden;
      margin-bottom: 20px;
    }}

    .card-inner {{
      padding: 20px;
    }}

    .search-row {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}

    input {{
      padding: 12px 14px;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      font-size: 15px;
    }}

    .search-row input {{
      min-width: 320px;
      flex: 1;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th,
    td {{
      padding: 13px 16px;
      border-bottom: 1px solid #e5e7eb;
      text-align: left;
      font-size: 14px;
      vertical-align: middle;
    }}

    th {{
      background: #f8fafc;
      color: #334155;
      font-weight: 800;
    }}

    .button {{
      display: inline-block;
      padding: 9px 13px;
      border-radius: 9px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      font-size: 13px;
      border: none;
      cursor: pointer;
    }}

    .secondary {{
      background: #334155;
    }}

    .logout {{
      background: #fee2e2;
      color: #991b1b;
    }}

    .badge-green,
    .badge-yellow,
    .badge-red,
    .badge-blue {{
      display: inline-block;
      padding: 5px 9px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 12px;
    }}

    .badge-green {{
      background: #dcfce7;
      color: #166534;
    }}

    .badge-yellow {{
      background: #fef3c7;
      color: #92400e;
    }}

    .badge-red {{
      background: #fee2e2;
      color: #991b1b;
    }}

    .badge-blue {{
      background: #dbeafe;
      color: #1d4ed8;
    }}
  </style>
</head>

<body>
  <div class="layout">

    <aside class="sidebar">
      <div class="brand">
        <img src="/static/img/logo-small.png" alt="YLFF">
        <div>
          <div class="brand-title">YLFF Admin</div>
          <div>Control Panel</div>
        </div>
      </div>

      <a class="menu-link" href="/ylff-control">🏠 Pārskats</a>

      <div class="menu-section">Dati</div>
      <a class="menu-link" href="/ylff-control-2026/adif">📥 ADIF imports</a>
      <a class="menu-link" href="/ylff-control-2026/activations">📡 Aktivizācijas</a>
      <a class="menu-link active" href="/ylff-control/objects">🌲 Objekti</a>
      <a class="menu-link" href="/activity">🔎 Activity pārbaude</a>

      <div class="menu-section">Saturs</div>
      <a class="menu-link" href="/ylff-control/pages">📝 Publiskās lapas</a>

      <div class="menu-section">Publiski</div>
      <a class="menu-link" href="/">🌐 Publiskā lapa</a>
      <a class="menu-link" href="/map">🗺️ Karte</a>

      <div class="menu-section">Sistēma</div>
      <a class="menu-link" href="/ylff-control/logout">🚪 Izlogoties</a>
    </aside>

    <main class="main">
      <div class="top">
        <h1>Objektu pārvaldība</h1>

        <a class="button logout" href="/ylff-control/logout">
          Izlogoties
        </a>
      </div>

      <div class="card">
        <div class="card-inner">
          <form method="GET" action="/ylff-control/objects" class="search-row">
            <input
              type="text"
              name="search"
              value="{html.escape(search)}"
              placeholder="Meklēt pēc YLFF, nosaukuma, lokatora vai statusa"
            >

            <button class="button" type="submit">
              Meklēt
            </button>

            <a class="button secondary" href="/ylff-control/objects">
              Notīrīt
            </a>

            <a class="button secondary" href="/objects-list" target="_blank">
              Publiskais katalogs
            </a>
          </form>
        </div>
      </div>

      <div class="card">
        <table>
          <thead>
            <tr>
              <th>YLFF</th>
              <th>Nosaukums</th>
              <th>Lokators</th>
              <th>Lat</th>
              <th>Lon</th>
              <th>Statuss</th>
              <th>Darbības</th>
            </tr>
          </thead>

          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </main>

  </div>
</body>
</html>
"""



@admin_objects_bp.route(
    "/ylff-control/objects/<reference>/delete",
    methods=["POST"],
)
def admin_object_delete(reference):
    obj = YLFFObject.query.filter_by(
        reference=reference,
    ).first_or_404()

    activation_count = Activation.query.filter_by(
        ylff_object_id=obj.id,
    ).count()

    qso_count = QSORecord.query.filter_by(
        ylff_object_id=obj.id,
    ).count()

    if activation_count > 0 or qso_count > 0:
        return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Dzēšana bloķēta</title>

  <style>
    body {{
      margin: 0;
      background: #f4f7fb;
      color: #0f172a;
      font-family: Arial, sans-serif;
    }}

    .container {{
      max-width: 760px;
      margin: 60px auto;
      padding: 30px;
    }}

    .card {{
      background: white;
      border: 1px solid #fecaca;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .08);
    }}

    h1 {{
      color: #991b1b;
      margin-top: 0;
    }}

    p {{
      line-height: 1.7;
      font-size: 16px;
    }}

    .button {{
      display: inline-block;
      padding: 12px 18px;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      margin-right: 10px;
    }}

    .secondary {{
      background: #334155;
    }}
  </style>
</head>

<body>
  <div class="container">
    <div class="card">
      <h1>Objektu nevar dzēst</h1>

      <p>
        Objektam <strong>{obj.reference}</strong> jau ir piesaistīti dati:
      </p>

      <p>
        Aktivizācijas: <strong>{activation_count}</strong><br>
        QSO ieraksti: <strong>{qso_count}</strong>
      </p>

      <p>
        Drošāk ir objektam uzlikt statusu <strong>cancelled</strong> vai
        <strong>inactive</strong>, nevis dzēst no datubāzes.
      </p>

      <a class="button" href="/ylff-control/objects/{obj.reference}">
        Labot objektu
      </a>

      <a class="button secondary" href="/ylff-control/objects">
        Atpakaļ uz sarakstu
      </a>
    </div>
  </div>
</body>
</html>
"""

    db.session.delete(obj)
    db.session.commit()

    return redirect("/ylff-control/objects")


@admin_objects_bp.route(
    "/ylff-control/objects/<reference>",
    methods=["GET", "POST"],
)
def admin_object_edit(reference):
    obj = YLFFObject.query.filter_by(
        reference=reference,
    ).first_or_404()

    if request.method == "POST":
        obj.name = request.form.get("name", "").strip()
        obj.locator = request.form.get("locator", "").strip()
        obj.image_url = request.form.get("image_url", "").strip()

        uploaded_image = request.files.get("object_image")
        uploaded_image_url = save_object_image_upload(uploaded_image, obj.reference)
        if uploaded_image_url:
            obj.image_url = uploaded_image_url

        obj.status = request.form.get("status", "active").strip()

        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()

        obj.latitude = float(latitude) if latitude else None
        obj.longitude = float(longitude) if longitude else None

        db.session.commit()

        return redirect("/ylff-control/objects")

    status_options = ""

    for status in STATUS_OPTIONS:
        selected = ""

        if obj.status == status:
            selected = "selected"

        status_options += f"""
        <option value="{status}" {selected}>
          {status}
        </option>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Labot {html.escape(obj.reference)}</title>

  <style>
    body {{
      margin: 0;
      background: #f4f7fb;
      color: #0f172a;
      font-family: Arial, sans-serif;
    }}

    .container {{
      max-width: 900px;
      margin: auto;
      padding: 34px;
    }}

    .card {{
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      padding: 26px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .06);
    }}

    h1 {{
      margin-top: 0;
      font-size: 32px;
    }}

    label {{
      display: block;
      margin-top: 18px;
      margin-bottom: 7px;
      font-weight: 800;
      color: #334155;
    }}

    input,
    select {{
      width: 100%;
      padding: 12px 14px;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      font-size: 15px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }}

    .actions {{
      display: flex;
      gap: 12px;
      margin-top: 24px;
      flex-wrap: wrap;
    }}

    button,
    .button {{
      display: inline-block;
      padding: 12px 18px;
      border: none;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      cursor: pointer;
      font-size: 15px;
    }}

    .secondary {{
      background: #334155;
    }}

    .public {{
      background: #16a34a;
    }}

    .danger {{
      background: #991b1b;
    }}
  </style>
</head>

<body>
  <div class="container">
    <div class="card">
      <h1>Labot objektu: {html.escape(obj.reference)}</h1>

      <form method="POST" enctype="multipart/form-data">
        <label>YLFF reference</label>
        <input value="{html.escape(obj.reference or '')}" disabled>

        <label>Nosaukums</label>
        <input name="name" value="{html.escape(obj.name or '')}" required>

        <label>Lokators</label>
        <input name="locator" value="{html.escape(obj.locator or '')}">

        <label>Objekta bilde URL</label>
        <input name="image_url" value="{html.escape(getattr(obj, 'image_url', '') or '')}" placeholder="/static/object-images/YLFF-0002.jpg">

        <label>Augšupielādēt objekta bildi</label>
        <input type="file" name="object_image" accept="image/png,image/jpeg,image/webp">

        <label>Statuss</label>
        <select name="status">
          {status_options}
        </select>

        <div class="grid">
          <div>
            <label>Latitude</label>
            <input name="latitude" value="{obj.latitude or ''}">
          </div>

          <div>
            <label>Longitude</label>
            <input name="longitude" value="{obj.longitude or ''}">
          </div>
        </div>

        <div class="actions">
          <button type="submit">
            Saglabāt
          </button>

          <a class="button secondary" href="/ylff-control/objects">
            Atpakaļ
          </a>

          <a class="button public" href="/object/{obj.reference}" target="_blank">
            Skatīt publiski
          </a>

          <a class="button secondary" href="/map" target="_blank">
            Karte
          </a>
        </div>
      </form>
    </div>
  </div>
</body>
</html>
"""
