from flask import Blueprint, request
from routes.translations import switch_lang_url

from models.activation import Activation
from models.object import YLFFObject
from models.expedition_plan import ExpeditionPlan


home_page_bp = Blueprint(
    "home_page",
    __name__,
)


@home_page_bp.route("/")
def home_page():
    objects_count = YLFFObject.query.count()

    activations = Activation.query.order_by(
        Activation.created_at.desc()
    ).all()

    activation_count = len(activations)

    qso_total = sum(
        activation.qso_count or 0
        for activation in activations
    )

    activator_set = set()

    for activation in activations:
        if activation.operators:
            for item in activation.operators.split(","):
                call = item.strip().upper()

                if call:
                    activator_set.add(call)

        elif activation.callsign:
            activator_set.add(
                activation.callsign.strip().upper()
            )

    activator_count = len(activator_set)


    planned_rows = ""

    planned = ExpeditionPlan.query.filter_by(
        status="approved"
    ).order_by(
        ExpeditionPlan.planned_date.asc()
    ).limit(8).all()

    for plan in planned:
        obj = YLFFObject.query.filter_by(
            reference=plan.ylff_reference
        ).first()

        object_name = "-"

        if obj:
            object_name = obj.name

        planned_rows += f"""
          <tr>
            <td>{plan.callsign}</td>
            <td>
              <a href="/object/{plan.ylff_reference}">
                {plan.ylff_reference}
              </a>
            </td>
            <td>{object_name}</td>
            <td>{plan.planned_date or "-"}</td>
            <td>{plan.planned_time_utc or "-"}</td>
            <td>{plan.mode or "-"}</td>
          </tr>
        """

    latest_rows = ""

    latest = activations[:8]

    for activation in latest:
        obj = YLFFObject.query.get(
            activation.ylff_object_id
        )

        if not obj:
            continue

        status = getattr(
            activation,
            "status",
            "complete",
        )

        if status == "incomplete":
            status_text = "Nepabeigta"
            status_class = "status-incomplete"
        else:
            status_text = "Pabeigta"
            status_class = "status-complete"

        latest_rows += f"""
          <tr>
            <td>{activation.callsign}</td>

            <td>
              <a href="/object/{obj.reference}">
                {obj.reference}
              </a>
            </td>

            <td>{obj.name}</td>

            <td>{activation.operators or "-"}</td>

            <td>{activation.qso_count}</td>

            <td>
              <span class="{status_class}">
                {status_text}
              </span>
            </td>
          </tr>
        """

    if not latest_rows:
        latest_rows = """
          <tr>
            <td colspan="6">
              {txt["no_activations"]}
            </td>
          </tr>
        """

    lang = request.args.get("lang", "lv")
    if lang not in {"lv", "en", "ru"}:
        lang = "lv"

    homepage_i18n = {
        "lv": {
            "nav_home": "SĀKUMLAPA",
            "nav_objects": "OBJEKTI",
            "nav_activators": "AKTIVIZATORI",
            "nav_activity": "ACTIVITY",
            "nav_awards": "DIPLOMI",
            "nav_rules": "NOLIKUMS",
            "nav_about": "PAR PROJEKTU",
            "nav_map": "KARTE",
            "hero_line_1": "Atklāj un aktivizē Latvijas dabas dārgumus!",
            "hero_line_2": "Apvieno radio, dabu un piedzīvojumu viena kopīgā programmā.",
            "btn_objects": "Apskatīt objektus",
            "btn_latest": "Jaunākās aktivizācijas",
            "btn_search": "Meklēt",
            "search_placeholder": "Meklēt CALL vai objektu, piemēram IU7KIX vai YLFF-0368",
            "stat_objects": "Objekti",
            "stat_activations": "Aktivizācijas",
            "stat_activators": "Aktivizatori",
            "stat_award_countries": "Diplomu valstis",
            "planned_title": "Plānotās ekspedīcijas",
            "latest_title": "Pēdējās aktivizācijas",
            "no_plans": "Pašlaik nav apstiprinātu plānoto ekspedīciju.",
            "no_activations": "Aktivizāciju vēl nav.",
            "btn_plan": "Pieteikt plānoto ekspedīciju",
            "table_object": "OBJEKTS",
            "table_date": "DATUMS",
            "table_activators": "AKTIVIZATORI",
            "table_status": "STATUSS",
        },
        "en": {
            "nav_home": "HOME",
            "nav_objects": "OBJECTS",
            "nav_activators": "ACTIVATORS",
            "nav_activity": "ACTIVITY",
            "nav_awards": "AWARDS",
            "nav_rules": "RULES",
            "nav_about": "ABOUT",
            "nav_map": "MAP",
            "hero_line_1": "Discover and activate Latvia's natural treasures!",
            "hero_line_2": "Bringing together radio, nature and adventure in one shared program.",
            "btn_objects": "View objects",
            "btn_latest": "Latest activations",
            "btn_search": "Search",
            "search_placeholder": "Search CALL or object, for example IU7KIX or YLFF-0368",
            "stat_objects": "Objects",
            "stat_activations": "Activations",
            "stat_activators": "Activators",
            "stat_award_countries": "Award countries",
            "planned_title": "Planned expeditions",
            "latest_title": "Latest activations",
            "no_plans": "There are no approved planned expeditions yet.",
            "no_activations": "There are no activations yet.",
            "btn_plan": "Submit planned expedition",
            "table_object": "OBJECT",
            "table_date": "DATE",
            "table_activators": "ACTIVATORS",
            "table_status": "STATUS",
        },
        "ru": {
            "nav_home": "ГЛАВНАЯ",
            "nav_objects": "ОБЪЕКТЫ",
            "nav_activators": "АКТИВАТОРЫ",
            "nav_activity": "АКТИВНОСТЬ",
            "nav_awards": "ДИПЛОМЫ",
            "nav_rules": "ПРАВИЛА",
            "nav_about": "О ПРОЕКТЕ",
            "nav_map": "КАРТА",
            "hero_line_1": "Открывайте и активируйте природные сокровища Латвии!",
            "hero_line_2": "Радио, природа и приключения в одной общей программе.",
            "btn_objects": "Посмотреть объекты",
            "btn_latest": "Последние активации",
            "btn_search": "Поиск",
            "search_placeholder": "Искать CALL или объект, например IU7KIX или YLFF-0368",
            "stat_objects": "Объекты",
            "stat_activations": "Активации",
            "stat_activators": "Активаторы",
            "stat_award_countries": "Страны дипломов",
            "planned_title": "Планируемые экспедиции",
            "latest_title": "Последние активации",
            "no_plans": "Пока нет утверждённых планируемых экспедиций.",
            "no_activations": "Активаций пока нет.",
            "btn_plan": "Подать планируемую экспедицию",
            "table_object": "ОБЪЕКТ",
            "table_date": "ДАТА",
            "table_activators": "АКТИВАТОРЫ",
            "table_status": "СТАТУС",
        },
    }

    txt = homepage_i18n[lang]

    return f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>YLFF Latvija</title>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #07110b;
      color: white;
    }}

    .page {{
      min-height: 100vh;
      background:
        linear-gradient(
          rgba(3, 7, 18, 0.02),
          rgba(3, 7, 18, 0.38)
        ),
        url("/static/img/hero_bg.png");
      background-size: cover;
      background-position: center top;
      background-repeat: no-repeat;
      background-attachment: fixed;
    }}

    .topbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      min-height: 86px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 46px;
      background: rgba(3, 7, 18, 0.68);
      border-bottom: 1px solid rgba(255,255,255,.12);
      backdrop-filter: blur(7px);
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      flex-shrink: 0;
    }}

    .brand-logo {{
      width: 58px;
      height: 58px;
      object-fit: contain;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,.55));
    }}

    .brand-title {{
      font-size: 34px;
      font-weight: bold;
      letter-spacing: 2px;
      color: #f8f4dc;
      line-height: 1;
      text-shadow: 0 3px 8px rgba(0,0,0,.65);
    }}

    .brand-subtitle {{
      margin-top: 4px;
      font-size: 13px;
      color: #e5d9a8;
      letter-spacing: 1px;
      text-shadow: 0 3px 8px rgba(0,0,0,.65);
    }}

    .nav {{
      display: flex;
      gap: 22px;
      align-items: center;
      flex-wrap: wrap;
      justify-content: flex-end;
    }}

    .nav a {{
      color: #f8f4dc;
      text-decoration: none;
      font-weight: bold;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .5px;
      text-shadow: 0 3px 8px rgba(0,0,0,.65);
      white-space: nowrap;
    }}

    .lang-switch {{
      display: inline-flex;
      gap: 7px;
      align-items: center;
      margin-left: 18px;
      padding-left: 14px;
      border-left: 1px solid rgba(255,255,255,.25);
      font-size: 13px;
      font-weight: 900;
    }}

    .lang-switch a {{
      color: #facc15 !important;
      text-decoration: none;
    }}

    .lang-switch span {{
      color: rgba(255,255,255,.5);
    }}

    .top-lang-switch {{
      display: inline-flex;
      gap: 7px;
      align-items: center;
      margin-left: 14px;
      padding-left: 12px;
      border-left: 1px solid rgba(255,255,255,.25);
      font-size: 12px;
      font-weight: 900;
    }}

    .top-lang-switch a {{
      color: #facc15 !important;
      text-decoration: none;
    }}

    .top-lang-switch span {{
      color: rgba(255,255,255,.55);
    }}

    .nav a:hover {{
      color: #facc15;
    }}

    .hero {{
      max-width: 1400px;
      margin: auto;
      padding: 44px 46px 22px;
      display: grid;
      grid-template-columns: 1.08fr .92fr;
      gap: 34px;
      align-items: center;
    }}

    .hero-left {{
      min-width: 0;
    }}

    .ylff-title-img {{
      width: min(620px, 100%);
      display: block;
      filter:
        drop-shadow(0 5px 8px rgba(0,0,0,.65))
        drop-shadow(0 14px 24px rgba(0,0,0,.45));
    }}

    .hero-text {{
      margin-top: 28px;
      font-size: 18px;
      line-height: 1.6;
      max-width: 650px;
      color: #ffffff;
      text-shadow:
        0 3px 7px rgba(0,0,0,.85),
        0 8px 18px rgba(0,0,0,.45);
    }}

    .hero-actions {{
      display: flex;
      gap: 14px;
      margin-top: 26px;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-block;
      padding: 14px 22px;
      border-radius: 10px;
      text-decoration: none;
      color: white;
      font-weight: bold;
      border: 1px solid rgba(255,255,255,.18);
      box-shadow: 0 10px 24px rgba(0,0,0,.35);
    }}

    .btn-green {{
      background: rgba(22, 101, 52, .92);
    }}

    .btn-gold {{
      background: rgba(146, 94, 18, .92);
    }}

    .btn-dark {{
      background: rgba(15, 23, 42, .82);
    }}

    .search-box {{
      display: flex;
      gap: 10px;
      margin-top: 24px;
      max-width: 650px;
    }}

    .search-input {{
      flex: 1;
      padding: 14px 16px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,.28);
      background: rgba(15, 23, 42, .72);
      color: white;
      font-size: 16px;
      outline: none;
    }}

    .search-input::placeholder {{
      color: rgba(255,255,255,.58);
    }}

    .search-button {{
      padding: 14px 20px;
      border: none;
      border-radius: 10px;
      background: #16a34a;
      color: white;
      font-weight: bold;
      cursor: pointer;
      font-size: 16px;
    }}

    .hero-logo-wrap {{
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    .hero-logo {{
      width: min(510px, 100%);
      object-fit: contain;
      filter:
        drop-shadow(0 10px 18px rgba(0,0,0,.68))
        drop-shadow(0 18px 30px rgba(0,0,0,.45));
    }}

    .stats {{
      max-width: 1120px;
      margin: 8px auto 0;
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid rgba(245, 200, 93, .28);
      background: rgba(8, 28, 12, .76);
      backdrop-filter: blur(5px);
      box-shadow: 0 10px 32px rgba(0,0,0,.38);
    }}

    .stat {{
      padding: 22px 18px;
      border-right: 1px solid rgba(245, 200, 93, .20);
      text-align: center;
    }}

    .stat:last-child {{
      border-right: none;
    }}

    .stat-icon {{
      font-size: 31px;
      color: #facc15;
      margin-bottom: 8px;
    }}

    .stat-value {{
      font-size: 32px;
      font-weight: bold;
      color: #fff7d6;
    }}

    .stat-label {{
      margin-top: 5px;
      color: #f5e8b0;
      font-size: 15px;
    }}

    .lower {{
      max-width: 1400px;
      margin: 24px auto 0;
      padding: 0 46px 34px;
      display: grid;
      grid-template-columns: 1.45fr 1fr;
      gap: 18px;
    }}

    .card {{
      background: rgba(8, 28, 12, .78);
      border: 1px solid rgba(245, 200, 93, .24);
      border-radius: 14px;
      padding: 24px;
      box-shadow: 0 10px 32px rgba(0,0,0,.38);
      backdrop-filter: blur(5px);
    }}

    h2 {{
      margin-top: 0;
      color: #facc15;
      letter-spacing: 1px;
      font-family: Georgia, serif;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th,
    td {{
      padding: 10px 8px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      text-align: left;
      font-size: 14px;
    }}

    th {{
      color: #86efac;
      text-transform: uppercase;
      font-size: 13px;
    }}

    a {{
      color: #86efac;
      text-decoration: none;
      font-weight: bold;
    }}

    .status-complete {{
      color: #86efac;
      font-weight: bold;
    }}

    .status-incomplete {{
      color: #facc15;
      font-weight: bold;
    }}

    .about-text {{
      line-height: 1.7;
      color: #f3f4f6;
    }}

    .footer {{
      max-width: 1400px;
      margin: auto;
      padding: 18px 46px 28px;
      color: #f8f4dc;
      display: flex;
      justify-content: space-between;
      gap: 20px;
      flex-wrap: wrap;
      font-size: 14px;
      text-shadow: 0 3px 8px rgba(0,0,0,.75);
    }}

    @media (max-width: 1050px) {{
      .topbar {{
        position: sticky;
        top: 0;
        min-height: auto;
        padding: 18px;
        flex-direction: column;
        gap: 16px;
      }}

      .nav {{
        justify-content: center;
        gap: 14px;
      }}

      .hero {{
        grid-template-columns: 1fr;
        padding: 36px 24px 20px;
        text-align: center;
      }}

      .ylff-title-img {{
        margin-left: auto;
        margin-right: auto;
      }}

      .hero-text {{
        margin-left: auto;
        margin-right: auto;
      }}

      .hero-actions,
      .search-box {{
        justify-content: center;
        margin-left: auto;
        margin-right: auto;
      }}

      .hero-logo {{
        max-width: 360px;
      }}

      .stats {{
        grid-template-columns: repeat(2, 1fr);
        margin-left: 24px;
        margin-right: 24px;
      }}

      .lower {{
        grid-template-columns: 1fr;
        padding: 0 24px 30px;
      }}
    }}


    .top-lang-switch .top-lang-label {{
      color: #ffffff;
      font-weight: 800;
      font-size: 12px;
      letter-spacing: .03em;
      line-height: 1;
    }}

    .top-lang-switch img {{
      width: 26px;
      height: 18px;
      border-radius: 3px;
      display: block;
      object-fit: cover;
    }}

    .top-lang-switch a {{
      width: 32px;
      min-width: 32px;
      height: 28px;
      padding: 0;
      gap: 0;
    }}

  </style>
</head>

<body>
  <div class="page">

    <div class="topbar">
      <a class="brand" href="/">
        <img
          class="brand-logo"
          src="/static/img/logo-small.png"
          alt="YLFF logo"
        >

        <div>
          <div class="brand-title">
            YLFF
          </div>

          <div class="brand-subtitle">
            LATVIAN FLORA & FAUNA
          </div>
        </div>
      </a>

      <div class="nav">
        <a href="/">{txt["nav_home"]}</a>
        <a href="/objects-list">{txt["stat_objects"]}</a>
        <a href="/top-operators">{txt["stat_activators"]}</a>
        <a href="/activity">{txt["nav_activity"]}</a>
        <a href="/awards">{txt["nav_awards"]}</a>
        <a href="/rules">{txt["nav_rules"]}</a>
        <a href="/about">Par projektu</a>
        <a href="/map">Karte</a>

          <!--
          AI mistake record, 2026-06-20:
          The first patch tried to insert the language flags after this exact line:
            <a href="/map">Karte</a>
          That exact line did not exist in this homepage source file, so the patch failed.
          The correct insertion point was found in the existing homepage navigation near:
            <a href="/activity">{txt["nav_activity"]}</a>
          Requirement: assistant source-file mistakes must be visible in the original affected source file and committed.
          -->
          <span class="top-lang-switch">
            <a href="/?lang=lv" title="Latviski">
              <img src="https://flagcdn.com/w40/lv.png" alt="LV">
            </a>
            <a href="/?lang=en" title="English">
              <img src="https://flagcdn.com/w40/gb.png" alt="EN">
            </a>
            <a href="/?lang=ru" title="Русский">
              <img src="https://flagcdn.com/w40/ru.png" alt="RU">
            </a>
          </span>
</div>
    </div>

    <section class="hero">
      <div class="hero-left">
        <img
          class="ylff-title-img"
          src="/static/img/ylff-title.png"
          alt="YLFF"
        >

        <div class="hero-text">
          {txt["hero_line_1"]}<br>
          Apvieno radio, dabu un piedzīvojumu vienā kopīgā programmā.
        </div>

        <div class="hero-actions">
          <a class="btn btn-green" href="/objects-list">
            {txt["btn_objects"]}
          </a>

          <a class="btn btn-gold" href="#latest">
            {txt["btn_latest"]}
          </a>

          <a class="btn btn-dark" href="/awards">
            Diplomi
          </a>

          <a class="btn btn-dark" href="/rules">
            Nolikums
          </a>
        </div>

        <div class="search-box">
          <input
            id="searchInput"
            class="search-input"
            type="text"
            placeholder="{txt["search_placeholder"]}"
          >

          <button
            class="search-button"
            onclick="goSearch()"
          >
            Meklēt
          </button>
        </div>
      </div>

      <div class="hero-logo-wrap">
        <img
          class="hero-logo"
          src="/static/img/logo-main.png"
          alt="YLFF main logo"
        >
      </div>
    </section>

    <section class="stats">
      <div class="stat">
        <div class="stat-icon">🌲</div>
        <div class="stat-value">{objects_count}</div>
        <div class="stat-label">{txt["stat_objects"]}</div>
      </div>

      <div class="stat">
        <div class="stat-icon">📡</div>
        <div class="stat-value">{activation_count}</div>
        <div class="stat-label">{txt["stat_activations"]}</div>
      </div>

      <div class="stat">
        <div class="stat-icon">👥</div>
        <div class="stat-value">{activator_count}</div>
        <div class="stat-label">{txt["stat_activators"]}</div>
      </div>

      <div class="stat">
        <div class="stat-icon">🤝</div>
        <div class="stat-value">{qso_total}</div>
        <div class="stat-label">QSO</div>
      </div>

      <div class="stat">
        <div class="stat-icon">🌍</div>
        <div class="stat-value">0</div>
        <div class="stat-label">{txt["stat_award_countries"]}</div>
      </div>
    </section>

    <section class="lower">
      <div class="card">
        <h2>{txt["planned_title"]}</h2>

        <table>
          <thead>
            <tr>
              <th>CALL</th>
              <th>YLFF</th>
              <th>Objekts</th>
              <th>Datums</th>
              <th>UTC</th>
              <th>Mode</th>
            </tr>
          </thead>

          <tbody>
            {planned_rows}
          </tbody>
        </table>

        <p>
          <a class="btn btn-green" href="/plan-expedition">
            {txt["btn_plan"]}
          </a>
        </p>
      </div>

      <div class="card" id="latest">
        <h2>{txt["latest_title"]}</h2>

        <table>
          <thead>
            <tr>
              <th>CALL</th>
              <th>YLFF</th>
              <th>Objekts</th>
              <th>{txt["stat_activators"]}</th>
              <th>QSO</th>
              <th>Statuss</th>
            </tr>
          </thead>

          <tbody>
            {latest_rows}
          </tbody>
        </table>
      </div>

      <div class="card">
        <h2>Par programmu</h2>

        <div class="about-text">
          YLFF programma veicina Latvijas dabas objektu iepazīšanu
          un aktivizēšanu ar amatieru radio palīdzību.
          Sistēma apkopo aktivizācijas, nostrādātos objektus,
          statistiku, nolikumu un nākotnē arī diplomus.
        </div>

        <p>
          <a class="btn btn-green" href="/activity">
            {txt["nav_activity"]} meklēšana
          </a>
        </p>

        <p>
          <a href="/awards">Diplomu sadaļa</a>
          &nbsp; | &nbsp;
          <a href="/rules">{txt["nav_rules"]}</a>
        </p>
      </div>
    </section>

    <div class="footer">
      <div>🌐 www.ylff.id.lv</div>
      <div>📧 info@ylff.id.lv</div>
      <div>📡 Amatieru radio — mūsu tilts uz dabu!</div>
      <div>© 2026 YLFF Programma</div>
    </div>

  </div>

  <script>
    function goSearch() {{
      const value = document
        .getElementById("searchInput")
        .value
        .trim()
        .toUpperCase();

      if (!value) {{
        return;
      }}

      if (value.startsWith("YLFF-")) {{
        window.location.href = "/object/" + value;
      }} else {{
        window.location.href = "/activity/" + value;
      }}
    }}

    document
      .getElementById("searchInput")
      .addEventListener("keydown", function(event) {{
        if (event.key === "Enter") {{
          goSearch();
        }}
      }});
  </script>
</body>
</html>
"""
