from datetime import datetime

from flask import Blueprint, request

from extensions import db
from models.activation import Activation
from models.object import YLFFObject


admin_activations_page_bp = Blueprint(
    "admin_activations_page",
    __name__,
)


@admin_activations_page_bp.route(
    "/ylff-control-2026/activations",
    methods=["GET", "POST"],
)
def admin_activations_page():
    message = ""

    objects = YLFFObject.query.order_by(
        YLFFObject.reference.asc()
    ).all()

    if request.method == "POST":
        callsign = request.form.get("callsign", "").strip().upper()
        reference = request.form.get("reference", "").strip().upper()
        operators = request.form.get("operators", "").strip().upper()
        qso_count = request.form.get("qso_count", "0").strip()
        activation_start = request.form.get("activation_start", "").strip()
        activation_end = request.form.get("activation_end", "").strip()

        ylff_object = YLFFObject.query.filter_by(
            reference=reference
        ).first()

        if not callsign or not reference:
            message = "Kļūda: CALL un objekts ir obligāti."

        elif not ylff_object:
            message = "Kļūda: objekts nav atrasts."

        else:
            start_date = None
            end_date = None

            if activation_start:
                start_date = datetime.strptime(
                    activation_start,
                    "%Y-%m-%d",
                ).date()

            if activation_end:
                end_date = datetime.strptime(
                    activation_end,
                    "%Y-%m-%d",
                ).date()

            activation = Activation(
                callsign=callsign,
                ylff_object_id=ylff_object.id,
                operators=operators or callsign,
                qso_count=int(qso_count or 0),
                activation_start=start_date,
                activation_end=end_date,
            )

            db.session.add(activation)
            db.session.commit()

            message = f"Aktivizācija saglabāta: {callsign} / {reference}"

    object_options = ""

    for item in objects:
        object_options += f"""
          <option value="{item.reference}">
            {item.reference} — {item.name}
          </option>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>YLFF aktivizācijas</title>

  <style>
    body {{
      margin: 0;
      background: #0f172a;
      color: white;
      font-family: Arial, sans-serif;
    }}

    .container {{
      max-width: 900px;
      margin: auto;
      padding: 30px;
    }}

    .card {{
      background: #111827;
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 8px 24px rgba(0,0,0,.35);
    }}

    h1 {{
      color: #22c55e;
      margin-top: 0;
    }}

    label {{
      display: block;
      margin-top: 16px;
      margin-bottom: 6px;
      color: #d1d5db;
      font-weight: bold;
    }}

    input,
    select {{
      width: 100%;
      padding: 12px;
      border-radius: 10px;
      border: 1px solid #374151;
      background: #0f172a;
      color: white;
      font-size: 16px;
      box-sizing: border-box;
    }}

    button {{
      margin-top: 22px;
      padding: 12px 18px;
      border: none;
      border-radius: 10px;
      background: #16a34a;
      color: white;
      font-weight: bold;
      font-size: 16px;
      cursor: pointer;
    }}

    .message {{
      margin-bottom: 18px;
      padding: 12px;
      border-radius: 10px;
      background: #064e3b;
      color: #d1fae5;
    }}

    .top-links {{
      margin-bottom: 20px;
    }}

    a {{
      color: #4ade80;
      text-decoration: none;
      font-weight: bold;
    }}

    .help {{
      color: #9ca3af;
      font-size: 14px;
      margin-top: 4px;
    }}
  </style>
</head>

<body>
  <div class="container">

    <div class="top-links">
      <a href="/">← Sākumlapa</a>
    </div>

    <div class="card">

      <h1>Pievienot aktivizāciju</h1>

      {f'<div class="message">{message}</div>' if message else ''}

      <form method="POST">

        <label>Ekspedīcijas CALL</label>
        <input
          name="callsign"
          placeholder="Piemēram YL44WFF vai YL3GBC/P"
          required
        >

        <label>YLFF objekts</label>
        <select name="reference" required>
          {object_options}
        </select>

        <label>Aktivizatori</label>
        <input
          name="operators"
          placeholder="Piemēram YL3GBC,YL2SW,YL3AUG"
        >
        <div class="help">
          Ja ir viens aktivizators, ieraksti viņa pamata CALL.
        </div>

        <label>QSO skaits</label>
        <input
          name="qso_count"
          type="number"
          min="0"
          value="0"
          required
        >

        <label>Sākuma datums</label>
        <input
          name="activation_start"
          type="date"
        >

        <label>Beigu datums</label>
        <input
          name="activation_end"
          type="date"
        >

        <button type="submit">
          Saglabāt aktivizāciju
        </button>

      </form>

    </div>

  </div>
</body>
</html>
"""
