import os

from flask import Blueprint, redirect, request, session


admin_auth_bp = Blueprint(
    "admin_auth",
    __name__,
)


def parse_admin_users():
    raw_users = os.getenv(
        "YLFF_ADMIN_USERS",
        "",
    )

    users = {}

    for item in raw_users.split(","):
        item = item.strip()

        if not item or ":" not in item:
            continue

        username, password = item.split(":", 1)

        username = username.strip()
        password = password.strip()

        if username and password:
            users[username] = password

    return users


@admin_auth_bp.route("/ylff-control/login", methods=["GET", "POST"])
def admin_login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        users = parse_admin_users()

        if not users:
            error = "Admin lietotāji nav iestatīti servera .env failā."

        elif username in users and password == users[username]:
            session["ylff_admin_logged_in"] = True
            session["ylff_admin_username"] = username

            next_url = request.args.get("next") or "/ylff-control"

            return redirect(next_url)

        else:
            error = "Nepareizs lietotājvārds vai parole."

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>YLFF Admin Login</title>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      font-family: Arial, sans-serif;
      background:
        linear-gradient(
          rgba(3, 7, 18, 0.35),
          rgba(3, 7, 18, 0.75)
        ),
        url("/static/img/hero_bg.png");
      background-size: cover;
      background-position: center;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}

    .login-card {{
      width: 100%;
      max-width: 430px;
      background: rgba(8, 28, 12, .86);
      border: 1px solid rgba(245, 200, 93, .28);
      border-radius: 20px;
      padding: 34px;
      box-shadow: 0 18px 48px rgba(0,0,0,.50);
      backdrop-filter: blur(7px);
      text-align: center;
    }}

    .logo {{
      width: 96px;
      height: 96px;
      object-fit: contain;
      margin-bottom: 14px;
      filter: drop-shadow(0 8px 18px rgba(0,0,0,.65));
    }}

    h1 {{
      margin: 0 0 8px;
      color: #facc15;
      font-family: Georgia, serif;
      font-size: 34px;
    }}

    .subtitle {{
      color: #e5e7eb;
      margin-bottom: 24px;
    }}

    input {{
      width: 100%;
      padding: 14px 16px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,.22);
      background: rgba(15, 23, 42, .74);
      color: white;
      font-size: 16px;
      outline: none;
      margin-bottom: 14px;
    }}

    button {{
      width: 100%;
      padding: 14px 16px;
      border: none;
      border-radius: 12px;
      background: #16a34a;
      color: white;
      font-weight: bold;
      font-size: 16px;
      cursor: pointer;
    }}

    button:hover {{
      background: #15803d;
    }}

    .error {{
      background: rgba(127, 29, 29, .86);
      border: 1px solid rgba(248, 113, 113, .45);
      color: #fee2e2;
      padding: 12px;
      border-radius: 12px;
      margin-bottom: 16px;
      font-weight: bold;
    }}

    .back {{
      margin-top: 18px;
    }}

    .back a {{
      color: #86efac;
      text-decoration: none;
      font-weight: bold;
    }}
  </style>
</head>

<body>
  <div class="login-card">
    <img class="logo" src="/static/img/logo-main.png" alt="YLFF">

    <h1>YLFF Admin</h1>

    <div class="subtitle">
      Ievadi lietotājvārdu un paroli, lai piekļūtu vadības panelim.
    </div>

    {"<div class='error'>" + error + "</div>" if error else ""}

    <form method="POST">
      <input
        type="text"
        name="username"
        placeholder="Lietotājvārds"
        autofocus
        required
      >

      <input
        type="password"
        name="password"
        placeholder="Parole"
        required
      >

      <button type="submit">
        Ielogoties
      </button>
    </form>

    <div class="back">
      <a href="/">← Atpakaļ uz publisko lapu</a>
    </div>
  </div>
</body>
</html>
"""


@admin_auth_bp.route("/ylff-control/logout")
def admin_logout():
    session.pop("ylff_admin_logged_in", None)
    session.pop("ylff_admin_username", None)

    return redirect("/ylff-control/login")
