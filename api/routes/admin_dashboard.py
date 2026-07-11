from flask import Blueprint
from sqlalchemy import func

from extensions import db
from models.activation import Activation
from models.object import YLFFObject
from models.qso_record import QSORecord


admin_dashboard_bp = Blueprint(
    "admin_dashboard",
    __name__,
)


@admin_dashboard_bp.route("/ylff-control")
def admin_dashboard():
    objects_count = YLFFObject.query.count()
    activations_count = Activation.query.count()
    qso_records_count = QSORecord.query.count()

    complete_count = Activation.query.filter_by(
        status="complete"
    ).count()

    incomplete_count = Activation.query.filter_by(
        status="incomplete"
    ).count()

    activated_objects_count = db.session.query(
        func.count(func.distinct(Activation.ylff_object_id))
    ).filter(
        Activation.status == "complete"
    ).scalar() or 0

    not_activated_objects_count = objects_count - activated_objects_count

    activated_percent = 0

    if objects_count:
        activated_percent = round(
            activated_objects_count / objects_count * 100,
            2,
        )

    latest = Activation.query.order_by(
        Activation.id.desc()
    ).limit(6).all()

    latest_rows = ""

    for activation in latest:
        obj = YLFFObject.query.get(
            activation.ylff_object_id
        )

        reference = "-"
        object_name = "-"

        if obj:
            reference = obj.reference
            object_name = obj.name

        status_class = "badge-green"
        status_text = "Pabeigta"

        if activation.status == "incomplete":
            status_class = "badge-yellow"
            status_text = "Nepabeigta"

        latest_rows += f"""
        <tr>
          <td>{activation.id}</td>
          <td>{activation.callsign}</td>
          <td>{reference}</td>
          <td>{object_name}</td>
          <td>{activation.qso_count}</td>
          <td><span class="{status_class}">{status_text}</span></td>
        </tr>
        """

    if not latest_rows:
        latest_rows = """
        <tr>
          <td colspan="6">Aktivizāciju vēl nav.</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>YLFF Admin</title>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f4f7fb;
      color: #0f172a;
    }}

    .admin-layout {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: 280px 1fr;
    }}

    .sidebar {{
      background: #0b1726;
      color: white;
      padding: 24px 18px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 30px;
    }}

    .brand img {{
      width: 54px;
      height: 54px;
      object-fit: contain;
    }}

    .brand-title {{
      font-size: 24px;
      font-weight: bold;
      line-height: 1.1;
    }}

    .brand-subtitle {{
      color: #cbd5e1;
      font-size: 13px;
      margin-top: 4px;
    }}

    .menu-section {{
      margin: 22px 0 10px;
      color: #94a3b8;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .7px;
    }}

    .menu-link {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 10px;
      color: #e5e7eb;
      text-decoration: none;
      font-weight: 600;
      margin-bottom: 6px;
    }}

    .menu-link:hover {{
      background: rgba(255,255,255,.08);
    }}

    .menu-link.active {{
      background: #1d4ed8;
      color: white;
    }}

    .sidebar-footer {{
      margin-top: 34px;
      padding-top: 18px;
      border-top: 1px solid rgba(255,255,255,.12);
      color: #94a3b8;
      font-size: 13px;
    }}

    .main {{
      min-width: 0;
    }}

    .topbar {{
      height: 78px;
      background: white;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 34px;
      position: sticky;
      top: 0;
      z-index: 10;
    }}

    .topbar-title {{
      display: flex;
      align-items: center;
      gap: 18px;
    }}

    .hamburger {{
      font-size: 26px;
      color: #0f172a;
    }}

    h1 {{
      margin: 0;
      font-size: 30px;
    }}

    .admin-user {{
      display: flex;
      align-items: center;
      gap: 12px;
      color: #0f172a;
      font-weight: 600;
    }}

    .avatar {{
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
    }}

    .content {{
      padding: 28px 34px 44px;
    }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 18px;
      margin-bottom: 24px;
    }}

    .stat-card {{
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      padding: 22px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .06);
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .stat-icon {{
      width: 58px;
      height: 58px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 28px;
      flex-shrink: 0;
    }}

    .blue {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }}

    .green {{
      background: linear-gradient(135deg, #22c55e, #16a34a);
    }}

    .purple {{
      background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    }}

    .yellow {{
      background: linear-gradient(135deg, #facc15, #f59e0b);
    }}

    .teal {{
      background: linear-gradient(135deg, #14b8a6, #0891b2);
    }}

    .stat-label {{
      color: #64748b;
      font-size: 14px;
      margin-bottom: 5px;
    }}

    .stat-value {{
      font-size: 28px;
      font-weight: 800;
      color: #0f172a;
    }}

    .panel-grid {{
      display: grid;
      grid-template-columns: 1.35fr .85fr;
      gap: 20px;
      margin-bottom: 20px;
    }}

    .panel {{
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .06);
      overflow: hidden;
    }}

    .panel-header {{
      padding: 20px 22px;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .panel-title {{
      font-size: 20px;
      font-weight: 800;
    }}

    .small-button {{
      display: inline-block;
      padding: 9px 12px;
      border: 1px solid #e5e7eb;
      border-radius: 9px;
      color: #0f172a;
      background: white;
      text-decoration: none;
      font-weight: 600;
      font-size: 13px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th,
    td {{
      padding: 13px 18px;
      border-bottom: 1px solid #e5e7eb;
      text-align: left;
      font-size: 14px;
    }}

    th {{
      color: #334155;
      font-weight: 800;
      background: #f8fafc;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    .badge-green {{
      display: inline-block;
      background: #dcfce7;
      color: #166534;
      padding: 5px 9px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 12px;
    }}

    .badge-yellow {{
      display: inline-block;
      background: #fef3c7;
      color: #92400e;
      padding: 5px 9px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 12px;
    }}

    .quick-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      padding: 18px;
    }}

    .quick-card {{
      min-height: 112px;
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      text-decoration: none;
      color: #0f172a;
      font-weight: 700;
      gap: 10px;
    }}

    .quick-card:hover {{
      border-color: #2563eb;
      box-shadow: 0 8px 18px rgba(37, 99, 235, .12);
    }}

    .quick-icon {{
      font-size: 32px;
    }}

    .system-list {{
      padding: 8px 18px 18px;
    }}

    .system-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 13px 0;
      border-bottom: 1px solid #e5e7eb;
      color: #0f172a;
    }}

    .system-row:last-child {{
      border-bottom: none;
    }}

    .system-ok {{
      color: #16a34a;
      font-weight: 800;
    }}

    .note {{
      background: #fff7ed;
      border: 1px solid #fed7aa;
      color: #92400e;
      border-radius: 16px;
      padding: 18px 20px;
      font-weight: 600;
    }}

    @media (max-width: 1100px) {{
      .admin-layout {{
        grid-template-columns: 1fr;
      }}

      .sidebar {{
        position: relative;
        height: auto;
      }}

      .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}

      .panel-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>

<body>
  <div class="admin-layout">

    <aside class="sidebar">
      <div class="brand">
        <img src="/static/img/logo-small.png" alt="YLFF">

        <div>
          <div class="brand-title">YLFF Admin</div>
          <div class="brand-subtitle">Control Panel</div>
        </div>
      </div>

      <a class="menu-link active" href="/ylff-control">🏠 Pārskats</a>

      <div class="menu-section">Dati</div>
      <a class="menu-link" href="/ylff-control-2026/adif">📥 ADIF imports</a>
      <a class="menu-link" href="/ylff-control-2026/activations">📡 Aktivizācijas</a>
      <a class="menu-link" href="/ylff-control/expeditions">🗓️ Plānotās ekspedīcijas</a>
      <a class="menu-link" href="/ylff-control/objects">🌲 Objekti</a>
      <a class="menu-link" href="/activity">🔎 Activity pārbaude</a>

      <div class="menu-section">Saturs</div>
      <a class="menu-link" href="/awards">🏆 Diplomi</a>
      <a class="menu-link" href="/rules">📜 Nolikums</a>
      <a class="menu-link" href="/about">ℹ️ Par projektu</a>
      <a class="menu-link" href="/uploads">🖼️ Mediji</a>

      <div class="menu-section">Publiski</div>
      <a class="menu-link" href="/">🌐 Publiskā lapa</a>
      <a class="menu-link" href="/map">🗺️ Karte</a>
      <a class="menu-link" href="/top-operators">👥 TOP aktivizatori</a>
      <a class="menu-link" href="/top-objects">📊 TOP objekti</a>

      <div class="menu-section">Sistēma</div>
      <a class="menu-link" href="/ylff-control">⚙️ Iestatījumi</a>

      <div class="sidebar-footer">
        v0.1 alfa<br>
        YLFF Latvija
      </div>
    </aside>

    <main class="main">
      <div class="topbar">
        <div class="topbar-title">
          <div class="hamburger">☰</div>
          <h1>Pārskats</h1>
        </div>

        <div class="admin-user">
          <span>🔔</span>
          <div class="avatar">A</div>
          <span>Administrators</span>
          <a class="logout-link" href="/ylff-control/logout">Izlogoties</a>
        </div>
      </div>

      <div class="content">

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon green">🌲</div>
            <div>
              <div class="stat-label">Objekti</div>
              <div class="stat-value">{objects_count}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon blue">📡</div>
            <div>
              <div class="stat-label">Aktivizācijas</div>
              <div class="stat-value">{activations_count}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon purple">🤝</div>
            <div>
              <div class="stat-label">QSO ieraksti</div>
              <div class="stat-value">{qso_records_count}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon green">✅</div>
            <div>
              <div class="stat-label">Pabeigtas</div>
              <div class="stat-value">{complete_count}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon yellow">⏳</div>
            <div>
              <div class="stat-label">Nepabeigtas</div>
              <div class="stat-value">{incomplete_count}</div>
            </div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">YLFF objektu aktivizācijas pārklājums</div>
          </div>

          <div style="padding: 22px;">
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:18px;">
              <div class="stat-card">
                <div class="stat-icon green">🌲</div>
                <div>
                  <div class="stat-label">Objekti kopā</div>
                  <div class="stat-value">{objects_count}</div>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon blue">📡</div>
                <div>
                  <div class="stat-label">Aktivizēti objekti</div>
                  <div class="stat-value">{activated_objects_count}</div>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon yellow">⏳</div>
                <div>
                  <div class="stat-label">Neaktivizēti</div>
                  <div class="stat-value">{not_activated_objects_count}</div>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon teal">%</div>
                <div>
                  <div class="stat-label">Pārklājums</div>
                  <div class="stat-value">{activated_percent}%</div>
                </div>
              </div>
            </div>

            <div style="background:#e5e7eb;border-radius:999px;height:24px;overflow:hidden;">
              <div style="background:linear-gradient(90deg,#16a34a,#22c55e);height:24px;width:{activated_percent}%;border-radius:999px;"></div>
            </div>

            <div style="margin-top:10px;color:#64748b;font-weight:700;">
              Aktivizēti {activated_objects_count} no {objects_count} YLFF objektiem.
              Šis rādītājs palīdz saprast, kad programmai vajag pievienot jaunus objektus.
            </div>
          </div>
        </div>

        <br>

        <div class="panel-grid">
          <div class="panel">
            <div class="panel-header">
              <div class="panel-title">Pēdējās aktivizācijas</div>
              <a class="small-button" href="/activity">Skatīt Activity</a>
            </div>

            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>CALL</th>
                  <th>YLFF</th>
                  <th>Objekts</th>
                  <th>QSO</th>
                  <th>Statuss</th>
                </tr>
              </thead>

              <tbody>
                {latest_rows}
              </tbody>
            </table>
          </div>

          <div class="panel">
            <div class="panel-header">
              <div class="panel-title">Ātrās darbības</div>
            </div>

            <div class="quick-grid">
              <a class="quick-card" href="/ylff-control-2026/adif">
                <div class="quick-icon">📥</div>
                <div>Importēt ADIF</div>
              </a>

              <a class="quick-card" href="/ylff-control-2026/activations">
                <div class="quick-icon">📡</div>
                <div>Pievienot aktivizāciju</div>
              </a>

              <a class="quick-card" href="/ylff-control/objects">
                <div class="quick-icon">🌲</div>
                <div>Objektu pārvaldība</div>
              </a>

              <a class="quick-card" href="/map">
                <div class="quick-icon">🗺️</div>
                <div>Atvērt karti</div>
              </a>

              <a class="quick-card" href="/awards">
                <div class="quick-icon">🏆</div>
                <div>Diplomi</div>
              </a>

              <a class="quick-card" href="/rules">
                <div class="quick-icon">📜</div>
                <div>Nolikums</div>
              </a>
            </div>
          </div>
        </div>

        <div class="panel-grid">
          <div class="panel">
            <div class="panel-header">
              <div class="panel-title">Sistēmas statuss</div>
            </div>

            <div class="system-list">
              <div class="system-row">
                <span>🌐 Vietne</span>
                <span class="system-ok">Tiešsaistē ●</span>
              </div>

              <div class="system-row">
                <span>🗄️ Datubāze</span>
                <span class="system-ok">Savienota ●</span>
              </div>

              <div class="system-row">
                <span>📥 ADIF imports</span>
                <span class="system-ok">Darbojas ●</span>
              </div>

              <div class="system-row">
                <span>🗺️ Karte</span>
                <span class="system-ok">Aktīva ●</span>
              </div>
            </div>
          </div>

          <div class="note">
            Šis ir YLFF admin paneļa alfa pārskats. Nākamajos soļos pieslēgsim
            login aizsardzību, objektu rediģēšanu, lapu satura rediģēšanu un diplomu pārvaldību.
          </div>
        </div>

      </div>
    </main>

  </div>
</body>
</html>
"""
