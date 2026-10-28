
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>YLFF Latvija</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #07110b;
      color: white;
    }

    .page {
      min-height: 100vh;
      background:
        linear-gradient(
          rgba(3, 7, 18, 0.02),
          rgba(3, 7, 18, 0.38)
        ),
        url("/img/hero_bg.png");
      background-size: cover;
      background-position: center top;
      background-repeat: no-repeat;
      background-attachment: fixed;
    }

    .topbar {
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
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      flex-shrink: 0;
    }

    .brand-logo {
      width: 58px;
      height: 58px;
      object-fit: contain;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,.55));
    }

    .brand-title {
      font-size: 34px;
      font-weight: bold;
      letter-spacing: 2px;
      color: #f8f4dc;
      line-height: 1;
      text-shadow: 0 3px 8px rgba(0,0,0,.65);
    }

    .brand-subtitle {
      margin-top: 4px;
      font-size: 13px;
      color: #e5d9a8;
      letter-spacing: 1px;
      text-shadow: 0 3px 8px rgba(0,0,0,.65);
    }

    .nav {
      display: flex;
      gap: 22px;
      align-items: center;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .nav a {
      color: #f8f4dc;
      text-decoration: none;
      font-weight: bold;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .5px;
      text-shadow: 0 3px 8px rgba(0,0,0,.65);
      white-space: nowrap;
    }

    .lang-switch {
      display: inline-flex;
      gap: 7px;
      align-items: center;
      margin-left: 18px;
      padding-left: 14px;
      border-left: 1px solid rgba(255,255,255,.25);
      font-size: 13px;
      font-weight: 900;
    }

    .lang-switch a {
      color: #facc15 !important;
      text-decoration: none;
    }

    .lang-switch span {
      color: rgba(255,255,255,.5);
    }

    .top-lang-switch {
      display: inline-flex;
      gap: 7px;
      align-items: center;
      margin-left: 14px;
      padding-left: 12px;
      border-left: 1px solid rgba(255,255,255,.25);
      font-size: 12px;
      font-weight: 900;
    }

    .top-lang-switch a {
      color: #facc15 !important;
      text-decoration: none;
    }

    .top-lang-switch span {
      color: rgba(255,255,255,.55);
    }

    .nav a:hover {
      color: #facc15;
    }

    .hero {
      max-width: 1400px;
      margin: auto;
      padding: 44px 46px 22px;
      display: grid;
      grid-template-columns: 1.08fr .92fr;
      gap: 34px;
      align-items: center;
    }

    .hero-left {
      min-width: 0;
    }

    .ylff-title-img {
      width: min(620px, 100%);
      display: block;
      filter:
        drop-shadow(0 5px 8px rgba(0,0,0,.65))
        drop-shadow(0 14px 24px rgba(0,0,0,.45));
    }

    .hero-text {
      margin-top: 28px;
      font-size: 18px;
      line-height: 1.6;
      max-width: 650px;
      color: #ffffff;
      text-shadow:
        0 3px 7px rgba(0,0,0,.85),
        0 8px 18px rgba(0,0,0,.45);
    }

    .hero-actions {
      display: flex;
      gap: 14px;
      margin-top: 26px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-block;
      padding: 14px 22px;
      border-radius: 10px;
      text-decoration: none;
      color: white;
      font-weight: bold;
      border: 1px solid rgba(255,255,255,.18);
      box-shadow: 0 10px 24px rgba(0,0,0,.35);
    }

    .btn-green {
      background: rgba(22, 101, 52, .92);
    }

    .btn-gold {
      background: rgba(146, 94, 18, .92);
    }

    .btn-dark {
      background: rgba(15, 23, 42, .82);
    }

    .search-box {
      display: flex;
      gap: 10px;
      margin-top: 24px;
      max-width: 650px;
    }

    .search-input {
      flex: 1;
      padding: 14px 16px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,.28);
      background: rgba(15, 23, 42, .72);
      color: white;
      font-size: 16px;
      outline: none;
    }

    .search-input::placeholder {
      color: rgba(255,255,255,.58);
    }

    .search-button {
      padding: 14px 20px;
      border: none;
      border-radius: 10px;
      background: #16a34a;
      color: white;
      font-weight: bold;
      cursor: pointer;
      font-size: 16px;
    }

    .hero-logo-wrap {
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .hero-logo {
      width: min(510px, 100%);
      object-fit: contain;
      filter:
        drop-shadow(0 10px 18px rgba(0,0,0,.68))
        drop-shadow(0 18px 30px rgba(0,0,0,.45));
    }

    .stats {
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
    }

    .stat {
      padding: 22px 18px;
      border-right: 1px solid rgba(245, 200, 93, .20);
      text-align: center;
    }

    .stat:last-child {
      border-right: none;
    }

    .stat-icon {
      font-size: 31px;
      color: #facc15;
      margin-bottom: 8px;
    }

    .stat-value {
      font-size: 32px;
      font-weight: bold;
      color: #fff7d6;
    }

    .stat-label {
      margin-top: 5px;
      color: #f5e8b0;
      font-size: 15px;
    }

    .lower {
      max-width: 1400px;
      margin: 24px auto 0;
      padding: 0 46px 34px;
      display: grid;
      grid-template-columns: 1.45fr 1fr;
      gap: 18px;
    }

    .card {
      background: rgba(8, 28, 12, .78);
      border: 1px solid rgba(245, 200, 93, .24);
      border-radius: 14px;
      padding: 24px;
      box-shadow: 0 10px 32px rgba(0,0,0,.38);
      backdrop-filter: blur(5px);
    }

    h2 {
      margin-top: 0;
      color: #facc15;
      letter-spacing: 1px;
      font-family: Georgia, serif;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    th,
    td {
      padding: 10px 8px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      text-align: left;
      font-size: 14px;
    }

    th {
      color: #86efac;
      text-transform: uppercase;
      font-size: 13px;
    }

    a {
      color: #86efac;
      text-decoration: none;
      font-weight: bold;
    }

    .status-complete {
      color: #86efac;
      font-weight: bold;
    }

    .status-incomplete {
      color: #facc15;
      font-weight: bold;
    }

    .about-text {
      line-height: 1.7;
      color: #f3f4f6;
    }

    .footer {
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
    }

    @media (max-width: 1050px) {
      .topbar {
        position: sticky;
        top: 0;
        min-height: auto;
        padding: 18px;
        flex-direction: column;
        gap: 16px;
      }

      .nav {
        justify-content: center;
        gap: 14px;
      }

      .hero {
        grid-template-columns: 1fr;
        padding: 36px 24px 20px;
        text-align: center;
      }

      .ylff-title-img {
        margin-left: auto;
        margin-right: auto;
      }

      .hero-text {
        margin-left: auto;
        margin-right: auto;
      }

      .hero-actions,
      .search-box {
        justify-content: center;
        margin-left: auto;
        margin-right: auto;
      }

      .hero-logo {
        max-width: 360px;
      }

      .stats {
        grid-template-columns: repeat(2, 1fr);
        margin-left: 24px;
        margin-right: 24px;
      }

      .lower {
        grid-template-columns: 1fr;
        padding: 0 24px 30px;
      }
    }


    .top-lang-switch .top-lang-label {
      color: #ffffff;
      font-weight: 800;
      font-size: 12px;
      letter-spacing: .03em;
      line-height: 1;
    }

    .top-lang-switch img {
      width: 26px;
      height: 18px;
      border-radius: 3px;
      display: block;
      object-fit: cover;
    }

    .top-lang-switch a {
      width: 32px;
      min-width: 32px;
      height: 28px;
      padding: 0;
      gap: 0;
    }

  </style>
  <link rel="stylesheet" href="/ylff-modern.css">
</head>

<body>
  <div class="page">

    <div class="topbar">
      <a class="brand" href="/">
        <img
          class="brand-logo"
          src="/img/logo-small.png"
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
        <a href="/">SĀKUMLAPA</a>
        <a href="/objects-list">Objekti</a>
        <a href="/top-operators">Aktivizatori</a>
        <a href="/activity">ACTIVITY</a>
        <a href="/awards">DIPLOMI</a>
        <a href="/rules">NOLIKUMS</a>
        <a href="/about">Par projektu</a>
        <a href="/map">Karte</a>

          <!--
          AI mistake record, 2026-06-20:
          The first patch tried to insert the language flags after this exact line:
            <a href="/map">Karte</a>
          That exact line did not exist in this homepage source file, so the patch failed.
          The correct insertion point was found in the existing homepage navigation near:
            <a href="/activity">ACTIVITY</a>
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
        <div class="ylff-wordmark">YLFF</div>
        <div class="ylff-program-name">LATVIAN FLORA &amp; FAUNA</div>
        <div class="ylff-program-subtitle">AMATEUR RADIO AWARD PROGRAM</div>

        <div class="hero-text">
          Atklāj un aktivizē Latvijas dabas dārgumus!<br>
          Apvieno radio, dabu un piedzīvojumu vienā kopīgā programmā.
        </div>

        <div class="hero-actions">
          <a class="btn btn-green" href="/objects-list">
            <svg viewBox="0 0 24 24"><path d="m17 14 3 3h-5v4H9v-4H4l3-3H5l4-4H7l5-7 5 7h-2l4 4h-2Z"/></svg> Apskatīt objektus
          </a>

          <a class="btn btn-gold" href="#latest">
            <svg viewBox="0 0 24 24"><path d="M4 10a7.3 7.3 0 0 0 10 10Z"/><path d="m9 15 3-3M17 13a6 6 0 0 0-6-6M21 13A10 10 0 0 0 11 3"/></svg> Jaunākās aktivizācijas
          </a>

          <a class="btn btn-dark" href="/awards">
            <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="5"/><path d="m8.5 12-1.5 9 5-3 5 3-1.5-9"/></svg> Diplomi
          </a>

          <a class="btn btn-dark" href="/rules">
            <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h8"/></svg> Nolikums
          </a>
        </div>

        <div class="search-box">
          <input
            id="searchInput"
            class="search-input"
            type="text"
            placeholder="Meklēt CALL vai objektu, piemēram IU7KIX vai YLFF-0368"
          >

          <button
            class="search-button"
            onclick="goSearch()"
          >
            <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg> Meklēt
          </button>
        </div>
      </div>

      <div class="hero-logo-wrap">
        <img
          class="hero-logo"
          src="/img/logo-main.png"
          alt="YLFF main logo"
        >
      </div>
    </section>

    <section class="stats">
      <div class="stat">
        <div class="stat-icon"><svg viewBox="0 0 24 24"><path d="m17 14 3 3h-5v4H9v-4H4l3-3H5l4-4H7l5-7 5 7h-2l4 4h-2Z"/></svg></div>
        <div class="stat-value">408</div>
        <div class="stat-label">Objekti</div>
      </div>

      <div class="stat">
        <div class="stat-icon"><svg viewBox="0 0 24 24"><path d="M4 10a7.3 7.3 0 0 0 10 10Z"/><path d="m9 15 3-3M17 13a6 6 0 0 0-6-6M21 13A10 10 0 0 0 11 3"/></svg></div>
        <div class="stat-value">42</div>
        <div class="stat-label">Aktivizācijas</div>
      </div>

      <div class="stat">
        <div class="stat-icon"><svg viewBox="0 0 24 24"><circle cx="9" cy="7" r="4"/><path d="M2 21v-2a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v2M16 3.2a4 4 0 0 1 0 7.6M22 21v-2a4 4 0 0 0-3-3.9"/></svg></div>
        <div class="stat-value">13</div>
        <div class="stat-label">Aktivizatori</div>
      </div>

      <div class="stat">
        <div class="stat-icon"><svg viewBox="0 0 24 24"><path d="M5 9a7 7 0 0 1 14 0M8.5 12.5a4 4 0 0 1 7 0"/><circle cx="12" cy="17" r="2"/><path d="M12 19v2"/></svg></div>
        <div class="stat-value">5549</div>
        <div class="stat-label">QSO</div>
      </div>

      <div class="stat">
        <div class="stat-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="5"/><path d="m8.5 12-1.5 9 5-3 5 3-1.5-9"/></svg></div>
        <div class="stat-value">0</div>
        <div class="stat-label">Diplomi</div>
      </div>
    </section>

    <section class="lower">
      <div class="card">
        <h2><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg> Plānotās ekspedīcijas</h2>

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

          </tbody>
        </table>

        <p>
          <a class="btn btn-green" href="/plan-expedition">
            Pieteikt plānoto ekspedīciju
          </a>
        </p>
      </div>

      <div class="card" id="latest">
        <h2><svg viewBox="0 0 24 24"><path d="M5 12a7 7 0 0 1 14 0M8 15a4 4 0 0 1 8 0"/><circle cx="12" cy="19" r="1"/></svg> Pēdējās aktivizācijas</h2>

        <table>
          <thead>
            <tr>
              <th>CALL</th>
              <th>YLFF</th>
              <th>Objekts</th>
              <th>Aktivizatori</th>
              <th>QSO</th>
              <th>Statuss</th>
            </tr>
          </thead>

          <tbody>

          <tr>
            <td>YL/DL7XJ/P</td>

            <td>
              <a href="/object/YLFF-0004">
                YLFF-0004
              </a>
            </td>

            <td>Slitere National Park</td>

            <td>DL7XJ</td>

            <td>11</td>

            <td>
              <span class="status-incomplete">
                Nepabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL/LY1CM/P</td>

            <td>
              <a href="/object/YLFF-0002">
                YLFF-0002
              </a>
            </td>

            <td>Kemeru National Park</td>

            <td>LY1CM</td>

            <td>126</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL3GBC/P</td>

            <td>
              <a href="/object/YLFF-0002">
                YLFF-0002
              </a>
            </td>

            <td>Kemeru National Park</td>

            <td>YL3GBC</td>

            <td>164</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL3GBC/P</td>

            <td>
              <a href="/object/YLFF-0002">
                YLFF-0002
              </a>
            </td>

            <td>Kemeru National Park</td>

            <td>YL3GBC</td>

            <td>109</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL/LY2BIS/P</td>

            <td>
              <a href="/object/YLFF-0040">
                YLFF-0040
              </a>
            </td>

            <td>Silene Nature Park</td>

            <td>LY2BIS</td>

            <td>204</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL/LY2BIS/P</td>

            <td>
              <a href="/object/YLFF-0040">
                YLFF-0040
              </a>
            </td>

            <td>Silene Nature Park</td>

            <td>LY2BIS</td>

            <td>207</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL/DL5WW/P</td>

            <td>
              <a href="/object/YLFF-0025">
                YLFF-0025
              </a>
            </td>

            <td>Dolessala Nature Park</td>

            <td>DL5WW</td>

            <td>140</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          <tr>
            <td>YL/DL5WW/P</td>

            <td>
              <a href="/object/YLFF-0169">
                YLFF-0169
              </a>
            </td>

            <td>Raunas Staburags Nature Reserve</td>

            <td>DL5WW</td>

            <td>180</td>

            <td>
              <span class="status-complete">
                Pabeigta
              </span>
            </td>
          </tr>

          </tbody>
        </table>
      </div>

      <div class="card">
        <h2><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/></svg> Par programmu</h2>

        <div class="about-text">
          YLFF programma veicina Latvijas dabas objektu iepazīšanu
          un aktivizēšanu ar amatieru radio palīdzību.
          Sistēma apkopo aktivizācijas, nostrādātos objektus,
          statistiku, nolikumu un nākotnē arī diplomus.
        </div>

        <p>
          <a class="btn btn-green" href="/activity">
            ACTIVITY meklēšana
          </a>
        </p>

        <p>
          <a href="/awards">Diplomu sadaļa</a>
          &nbsp; | &nbsp;
          <a href="/rules">NOLIKUMS</a>
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
    function goSearch() {
      const value = document
        .getElementById("searchInput")
        .value
        .trim()
        .toUpperCase();

      if (!value) {
        return;
      }

      if (value.startsWith("YLFF-")) {
        window.location.href = "/object/" + value;
      } else {
        window.location.href = "/activity/" + value;
      }
    }

    document
      .getElementById("searchInput")
      .addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
          goSearch();
        }
      });
  </script>
</body>
</html>
