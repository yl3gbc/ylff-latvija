import html
from datetime import datetime

from flask import Blueprint, redirect, request

from extensions import db
from models.activation import Activation
from models.object import YLFFObject
from models.qso_record import QSORecord


admin_activations_manage_bp = Blueprint(
    "admin_activations_manage",
    __name__,
)


@admin_activations_manage_bp.route("/ylff-control/activations")
def admin_activations_list():
    search = request.args.get("search", "").strip()

    query = Activation.query

    if search:
        like = f"%{search}%"
        query = query.filter(
            Activation.callsign.ilike(like)
            | Activation.operators.ilike(like)
            | Activation.status.ilike(like)
        )

    activations = query.order_by(
        Activation.id.desc()
    ).all()

    rows = ""

    for activation in activations:
        obj = YLFFObject.query.get(activation.ylff_object_id)

        reference = obj.reference if obj else "-"
        object_name = obj.name if obj else "-"

        status_class = "badge-green"
        if activation.status == "incomplete":
            status_class = "badge-yellow"

        rows += f"""
        <tr>
          <td>{activation.id}</td>
          <td>{html.escape(activation.callsign or "-")}</td>
          <td>
            <strong>{html.escape(reference)}</strong><br>
            {html.escape(object_name)}
          </td>
          <td>{html.escape(activation.operators or "-")}</td>
          <td>{activation.qso_count or 0}</td>
          <td><span class="{status_class}">{html.escape(activation.status or "-")}</span></td>
          <td>{activation.activation_start or "-"}</td>
          <td>
            <a class="button secondary" href="/ylff-control/activations/{activation.id}">Skatīt</a>
            <a class="button" href="/ylff-control/activations/{activation.id}/edit">Labot</a>

            <form method="POST" action="/ylff-control/activations/{activation.id}/recount" style="display:inline;">
              <button class="button green" type="submit">Pārrēķināt</button>
            </form>

            <form method="POST" action="/ylff-control/activations/{activation.id}/delete" style="display:inline;"
              onsubmit="return confirm('Tiešām dzēst aktivizāciju #{activation.id} un visus tās QSO?');">
              <button class="button danger" type="submit">Dzēst</button>
            </form>
          </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
          <td colspan="8">Aktivizācijas nav atrastas.</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Aktivizācijas</title>

  <style>
    body {{ margin:0; background:#f4f7fb; color:#0f172a; font-family:Arial,sans-serif; }}
    .layout {{ min-height:100vh; display:grid; grid-template-columns:280px 1fr; }}
    .sidebar {{ background:#0b1726; color:white; padding:24px 18px; }}
    .brand {{ display:flex; align-items:center; gap:12px; margin-bottom:28px; }}
    .brand img {{ width:54px; height:54px; object-fit:contain; }}
    .brand-title {{ font-size:24px; font-weight:bold; }}
    .menu-section {{ margin:22px 0 10px; color:#94a3b8; font-size:12px; text-transform:uppercase; letter-spacing:.7px; }}
    .menu-link {{ display:block; padding:12px 14px; border-radius:10px; color:#e5e7eb; text-decoration:none; font-weight:700; margin-bottom:7px; }}
    .menu-link:hover,.menu-link.active {{ background:#1d4ed8; color:white; }}
    .main {{ padding:34px; }}
    .top {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:22px; }}
    h1 {{ margin:0; font-size:32px; }}
    .card {{ background:white; border:1px solid #e5e7eb; border-radius:16px; box-shadow:0 6px 18px rgba(15,23,42,.06); overflow:hidden; margin-bottom:20px; }}
    .card-inner {{ padding:20px; }}
    .search-row {{ display:flex; gap:10px; flex-wrap:wrap; }}
    input,select {{ padding:12px 14px; border:1px solid #cbd5e1; border-radius:10px; font-size:15px; }}
    .search-row input {{ min-width:320px; flex:1; }}
    table {{ width:100%; border-collapse:collapse; }}
    th,td {{ padding:13px 16px; border-bottom:1px solid #e5e7eb; text-align:left; font-size:14px; vertical-align:top; }}
    th {{ background:#f8fafc; color:#334155; font-weight:800; }}
    .button {{ display:inline-block; padding:8px 11px; border-radius:9px; background:#2563eb; color:white; text-decoration:none; font-weight:800; font-size:12px; border:none; cursor:pointer; margin:2px; }}
    .secondary {{ background:#334155; }}
    .green {{ background:#16a34a; }}
    .danger {{ background:#dc2626; }}
    .logout {{ background:#fee2e2; color:#991b1b; }}
    .badge-green,.badge-yellow {{ display:inline-block; padding:5px 9px; border-radius:999px; font-weight:800; font-size:12px; }}
    .badge-green {{ background:#dcfce7; color:#166534; }}
    .badge-yellow {{ background:#fef3c7; color:#92400e; }}
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
      <a class="menu-link active" href="/ylff-control/activations">📡 Aktivizācijas</a>
      <a class="menu-link" href="/ylff-control/expeditions">🗓️ Plānotās ekspedīcijas</a>
      <a class="menu-link" href="/ylff-control/objects">🌲 Objekti</a>

      <div class="menu-section">Saturs</div>
      <a class="menu-link" href="/ylff-control/pages">📝 Publiskās lapas</a>

      <div class="menu-section">Sistēma</div>
      <a class="menu-link" href="/ylff-control/logout">🚪 Izlogoties</a>
    </aside>

    <main class="main">
      <div class="top">
        <h1>Aktivizāciju pārvaldība</h1>
        <a class="button logout" href="/ylff-control/logout">Izlogoties</a>
      </div>

      <div class="card">
        <div class="card-inner">
          <form method="GET" action="/ylff-control/activations" class="search-row">
            <input
              type="text"
              name="search"
              value="{html.escape(search)}"
              placeholder="Meklēt pēc CALL, operatora vai statusa"
            >
            <button class="button" type="submit">Meklēt</button>
            <a class="button secondary" href="/ylff-control/activations">Notīrīt</a>
          </form>
        </div>
      </div>

      <div class="card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>CALL</th>
              <th>Objekts</th>
              <th>Operatori</th>
              <th>QSO</th>
              <th>Statuss</th>
              <th>Datums</th>
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


@admin_activations_manage_bp.route("/ylff-control/activations/<int:activation_id>")
def admin_activation_detail(activation_id):
    activation = Activation.query.get_or_404(activation_id)
    obj = YLFFObject.query.get(activation.ylff_object_id)

    qso_count = QSORecord.query.filter_by(
        activation_id=activation.id,
    ).count()

    qso_rows = ""

    qsos = QSORecord.query.filter_by(
        activation_id=activation.id,
    ).order_by(
        QSORecord.qso_date.asc()
    ).limit(100).all()

    for qso in qsos:
        qso_rows += f"""
        <tr>
          <td>{html.escape(qso.worked_call or "-")}</td>
          <td>{qso.qso_date or "-"}</td>
          <td>{html.escape(qso.band or "-")}</td>
          <td>{html.escape(qso.mode or "-")}</td>
        </tr>
        """

    if not qso_rows:
        qso_rows = "<tr><td colspan='4'>QSO nav atrasti.</td></tr>"

    reference = obj.reference if obj else "-"
    object_name = obj.name if obj else "-"

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Aktivizācija #{activation.id}</title>
  <style>
    body {{ margin:0; background:#f4f7fb; color:#0f172a; font-family:Arial,sans-serif; }}
    .container {{ max-width:1100px; margin:auto; padding:34px; }}
    .card {{ background:white; border:1px solid #e5e7eb; border-radius:16px; padding:26px; box-shadow:0 6px 18px rgba(15,23,42,.06); margin-bottom:20px; }}
    h1 {{ margin-top:0; }}
    .row {{ padding:11px 0; border-bottom:1px solid #e5e7eb; }}
    .label {{ color:#64748b; font-weight:800; margin-bottom:4px; }}
    .value {{ font-size:16px; }}
    .actions {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:22px; }}
    .button {{ display:inline-block; padding:11px 15px; border-radius:10px; background:#2563eb; color:white; text-decoration:none; font-weight:800; border:none; cursor:pointer; }}
    .secondary {{ background:#334155; }}
    .green {{ background:#16a34a; }}
    .danger {{ background:#dc2626; }}
    table {{ width:100%; border-collapse:collapse; }}
    th,td {{ padding:11px; border-bottom:1px solid #e5e7eb; text-align:left; }}
    th {{ background:#f8fafc; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>Aktivizācija #{activation.id}</h1>

      <div class="row"><div class="label">CALL</div><div class="value">{html.escape(activation.callsign or "-")}</div></div>
      <div class="row"><div class="label">Operatori</div><div class="value">{html.escape(activation.operators or "-")}</div></div>
      <div class="row"><div class="label">Objekts</div><div class="value">{html.escape(reference)} - {html.escape(object_name)}</div></div>
      <div class="row"><div class="label">QSO</div><div class="value">{activation.qso_count or 0} / DB QSO: {qso_count}</div></div>
      <div class="row"><div class="label">Statuss</div><div class="value">{html.escape(activation.status or "-")}</div></div>
      <div class="row"><div class="label">Datums</div><div class="value">{activation.activation_start or "-"} līdz {activation.activation_end or "-"}</div></div>

      <div class="actions">
        <a class="button" href="/ylff-control/activations/{activation.id}/edit">Labot</a>

        <form method="POST" action="/ylff-control/activations/{activation.id}/recount">
          <button class="button green" type="submit">Pārrēķināt QSO</button>
        </form>

        <a class="button secondary" href="/ylff-control/activations">Atpakaļ</a>
        <a class="button secondary" href="/activity/{activation.callsign}" target="_blank">Activity</a>
      </div>
    </div>

    <div class="card">
      <h2>Pirmie 100 QSO</h2>
      <table>
        <thead>
          <tr>
            <th>Worked CALL</th>
            <th>Datums</th>
            <th>Band</th>
            <th>Mode</th>
          </tr>
        </thead>
        <tbody>
          {qso_rows}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""


@admin_activations_manage_bp.route(
    "/ylff-control/activations/<int:activation_id>/edit",
    methods=["GET", "POST"],
)
def admin_activation_edit(activation_id):
    activation = Activation.query.get_or_404(activation_id)

    if request.method == "POST":
        activation.callsign = request.form.get("callsign", "").strip().upper()
        activation.operators = request.form.get("operators", "").strip().upper()
        activation.status = request.form.get("status", "complete").strip()
        activation.qso_count = int(request.form.get("qso_count", "0") or 0)

        object_reference = request.form.get("ylff_reference", "").strip().upper()
        obj = YLFFObject.query.filter_by(reference=object_reference).first()

        if obj:
            activation.ylff_object_id = obj.id

            QSORecord.query.filter_by(
                activation_id=activation.id,
            ).update(
                {"ylff_object_id": obj.id}
            )

        start_raw = request.form.get("activation_start", "").strip()
        end_raw = request.form.get("activation_end", "").strip()

        activation.activation_start = datetime.strptime(start_raw, "%Y-%m-%d").date() if start_raw else None
        activation.activation_end = datetime.strptime(end_raw, "%Y-%m-%d").date() if end_raw else None

        db.session.commit()

        return redirect(f"/ylff-control/activations/{activation.id}")

    obj = YLFFObject.query.get(activation.ylff_object_id)

    reference = obj.reference if obj else ""

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Labot aktivizāciju</title>
  <style>
    body {{ margin:0; background:#f4f7fb; color:#0f172a; font-family:Arial,sans-serif; }}
    .container {{ max-width:900px; margin:auto; padding:34px; }}
    .card {{ background:white; border:1px solid #e5e7eb; border-radius:16px; padding:26px; box-shadow:0 6px 18px rgba(15,23,42,.06); }}
    h1 {{ margin-top:0; }}
    label {{ display:block; margin-top:18px; margin-bottom:7px; font-weight:800; color:#334155; }}
    input,select {{ width:100%; padding:12px 14px; border:1px solid #cbd5e1; border-radius:10px; font-size:15px; }}
    .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
    .actions {{ display:flex; gap:12px; margin-top:24px; flex-wrap:wrap; }}
    button,.button {{ display:inline-block; padding:12px 18px; border:none; border-radius:10px; background:#2563eb; color:white; text-decoration:none; font-weight:800; cursor:pointer; }}
    .secondary {{ background:#334155; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>Labot aktivizāciju #{activation.id}</h1>

      <form method="POST">
        <label>CALL</label>
        <input name="callsign" value="{html.escape(activation.callsign or '')}" required>

        <label>Operatori</label>
        <input name="operators" value="{html.escape(activation.operators or '')}">

        <label>YLFF reference</label>
        <input name="ylff_reference" value="{html.escape(reference)}" required>

        <div class="grid">
          <div>
            <label>QSO count</label>
            <input name="qso_count" value="{activation.qso_count or 0}">
          </div>

          <div>
            <label>Statuss</label>
            <select name="status">
              <option value="complete" {"selected" if activation.status == "complete" else ""}>complete</option>
              <option value="incomplete" {"selected" if activation.status == "incomplete" else ""}>incomplete</option>
            </select>
          </div>
        </div>

        <div class="grid">
          <div>
            <label>Sākuma datums</label>
            <input type="date" name="activation_start" value="{activation.activation_start or ''}">
          </div>

          <div>
            <label>Beigu datums</label>
            <input type="date" name="activation_end" value="{activation.activation_end or ''}">
          </div>
        </div>

        <div class="actions">
          <button type="submit">Saglabāt</button>
          <a class="button secondary" href="/ylff-control/activations/{activation.id}">Atpakaļ</a>
        </div>
      </form>
    </div>
  </div>
</body>
</html>
"""


@admin_activations_manage_bp.route(
    "/ylff-control/activations/<int:activation_id>/recount",
    methods=["POST"],
)
def admin_activation_recount(activation_id):
    activation = Activation.query.get_or_404(activation_id)

    qso_count = QSORecord.query.filter_by(
        activation_id=activation.id,
    ).count()

    activation.qso_count = qso_count
    activation.status = "complete" if qso_count >= 100 else "incomplete"

    db.session.commit()

    return redirect(f"/ylff-control/activations/{activation.id}")


@admin_activations_manage_bp.route(
    "/ylff-control/activations/<int:activation_id>/delete",
    methods=["POST"],
)
def admin_activation_delete(activation_id):
    activation = Activation.query.get_or_404(activation_id)

    QSORecord.query.filter_by(
        activation_id=activation.id,
    ).delete()

    db.session.delete(activation)
    db.session.commit()

    return redirect("/ylff-control/activations")
