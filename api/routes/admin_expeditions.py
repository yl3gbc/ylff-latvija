import html

from flask import Blueprint, redirect

from extensions import db
from models.expedition_plan import ExpeditionPlan
from models.object import YLFFObject


admin_expeditions_bp = Blueprint(
    "admin_expeditions",
    __name__,
)


@admin_expeditions_bp.route("/ylff-control/expeditions")
def admin_expeditions_list():
    plans = ExpeditionPlan.query.order_by(
        ExpeditionPlan.created_at.desc()
    ).all()

    rows = ""

    for plan in plans:
        obj = YLFFObject.query.filter_by(
            reference=plan.ylff_reference,
        ).first()

        object_name = obj.name if obj else "-"

        badge = "badge-yellow"

        if plan.status == "approved":
            badge = "badge-green"

        if plan.status == "rejected":
            badge = "badge-red"

        rows += f"""
        <tr>
          <td>{plan.id}</td>
          <td>{html.escape(plan.callsign or "-")}</td>
          <td>{html.escape(plan.operators or "-")}</td>
          <td>
            <strong>{html.escape(plan.ylff_reference or "-")}</strong><br>
            {html.escape(object_name)}
          </td>
          <td>{plan.planned_date or "-"}</td>
          <td>{html.escape(plan.planned_time_utc or "-")}</td>
          <td>{html.escape(plan.mode or "-")}</td>
          <td>
            <span class="{badge}">
              {html.escape(plan.status or "-")}
            </span>
          </td>
          <td>
            <a class="button secondary" href="/ylff-control/expeditions/{plan.id}">
              Skatīt
            </a>

            <form method="POST" action="/ylff-control/expeditions/{plan.id}/approve" style="display:inline;">
              <button class="button green" type="submit">
                Apstiprināt
              </button>
            </form>

            <form method="POST" action="/ylff-control/expeditions/{plan.id}/reject" style="display:inline;">
              <button class="button danger" type="submit">
                Noraidīt
              </button>
            </form>
          </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
          <td colspan="9">Plānoto ekspedīciju pieteikumu vēl nav.</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Plānotās ekspedīcijas</title>

  <style>
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
      vertical-align: top;
    }}

    th {{
      background: #f8fafc;
      color: #334155;
      font-weight: 800;
    }}

    .button {{
      display: inline-block;
      padding: 8px 11px;
      border-radius: 9px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      font-size: 12px;
      border: none;
      cursor: pointer;
      margin: 2px;
    }}

    .secondary {{
      background: #334155;
    }}

    .green {{
      background: #16a34a;
    }}

    .danger {{
      background: #dc2626;
    }}

    .logout {{
      background: #fee2e2;
      color: #991b1b;
    }}

    .badge-green,
    .badge-yellow,
    .badge-red {{
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
      <a class="menu-link active" href="/ylff-control/expeditions">🗓️ Plānotās ekspedīcijas</a>
      <a class="menu-link" href="/ylff-control/objects">🌲 Objekti</a>

      <div class="menu-section">Saturs</div>
      <a class="menu-link" href="/ylff-control/pages">📝 Publiskās lapas</a>

      <div class="menu-section">Publiski</div>
      <a class="menu-link" href="/">🌐 Publiskā lapa</a>
      <a class="menu-link" href="/plan-expedition">📨 Pieteikt ekspedīciju</a>

      <div class="menu-section">Sistēma</div>
      <a class="menu-link" href="/ylff-control/logout">🚪 Izlogoties</a>
    </aside>

    <main class="main">
      <div class="top">
        <h1>Plānotās ekspedīcijas</h1>

        <a class="button logout" href="/ylff-control/logout">
          Izlogoties
        </a>
      </div>

      <div class="card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>CALL</th>
              <th>Operatori</th>
              <th>Objekts</th>
              <th>Datums</th>
              <th>UTC</th>
              <th>Mode</th>
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


@admin_expeditions_bp.route("/ylff-control/expeditions/<int:plan_id>")
def admin_expedition_detail(plan_id):
    plan = ExpeditionPlan.query.get_or_404(plan_id)

    obj = YLFFObject.query.filter_by(
        reference=plan.ylff_reference,
    ).first()

    object_name = obj.name if obj else "-"

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Ekspedīcijas pieteikums</title>

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
    }}

    .row {{
      padding: 12px 0;
      border-bottom: 1px solid #e5e7eb;
    }}

    .label {{
      color: #64748b;
      font-weight: 800;
      margin-bottom: 4px;
    }}

    .value {{
      font-size: 16px;
    }}

    .actions {{
      margin-top: 22px;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .button {{
      display: inline-block;
      padding: 11px 15px;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      border: none;
      cursor: pointer;
    }}

    .green {{
      background: #16a34a;
    }}

    .danger {{
      background: #dc2626;
    }}

    .secondary {{
      background: #334155;
    }}
  </style>
</head>

<body>
  <div class="container">
    <div class="card">
      <h1>Ekspedīcijas pieteikums #{plan.id}</h1>

      <div class="row">
        <div class="label">CALL</div>
        <div class="value">{html.escape(plan.callsign or "-")}</div>
      </div>

      <div class="row">
        <div class="label">Operatori</div>
        <div class="value">{html.escape(plan.operators or "-")}</div>
      </div>

      <div class="row">
        <div class="label">Objekts</div>
        <div class="value">{html.escape(plan.ylff_reference or "-")} - {html.escape(object_name)}</div>
      </div>

      <div class="row">
        <div class="label">Datums / UTC</div>
        <div class="value">{plan.planned_date or "-"} {html.escape(plan.planned_time_utc or "")}</div>
      </div>

      <div class="row">
        <div class="label">Mode</div>
        <div class="value">{html.escape(plan.mode or "-")}</div>
      </div>

      <div class="row">
        <div class="label">WhatsApp</div>
        <div class="value">{html.escape(plan.whatsapp or "-")}</div>
      </div>

      <div class="row">
        <div class="label">E-pasts</div>
        <div class="value">{html.escape(plan.email or "-")}</div>
      </div>

      <div class="row">
        <div class="label">Piezīmes</div>
        <div class="value">{html.escape(plan.notes or "-")}</div>
      </div>

      <div class="row">
        <div class="label">Statuss</div>
        <div class="value">{html.escape(plan.status or "-")}</div>
      </div>

      <div class="actions">
        <form method="POST" action="/ylff-control/expeditions/{plan.id}/approve">
          <button class="button green" type="submit">Apstiprināt</button>
        </form>

        <form method="POST" action="/ylff-control/expeditions/{plan.id}/reject">
          <button class="button danger" type="submit">Noraidīt</button>
        </form>

        <a class="button secondary" href="/ylff-control/expeditions">
          Atpakaļ
        </a>
      </div>
    </div>
  </div>
</body>
</html>
"""


@admin_expeditions_bp.route(
    "/ylff-control/expeditions/<int:plan_id>/approve",
    methods=["POST"],
)
def admin_expedition_approve(plan_id):
    plan = ExpeditionPlan.query.get_or_404(plan_id)
    plan.status = "approved"
    db.session.commit()

    return redirect("/ylff-control/expeditions")


@admin_expeditions_bp.route(
    "/ylff-control/expeditions/<int:plan_id>/reject",
    methods=["POST"],
)
def admin_expedition_reject(plan_id):
    plan = ExpeditionPlan.query.get_or_404(plan_id)
    plan.status = "rejected"
    db.session.commit()

    return redirect("/ylff-control/expeditions")
