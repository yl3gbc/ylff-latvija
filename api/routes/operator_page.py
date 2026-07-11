from flask import Blueprint

from models.activation import Activation
from models.object import YLFFObject


operator_page_bp = Blueprint(
    "operator_page",
    __name__,
)


@operator_page_bp.route("/operator/<callsign>")
def operator_page(callsign):
    callsign = callsign.upper()

    activations = Activation.query.all()

    matched = [
        activation
        for activation in activations
        if (
            activation.callsign == callsign
            or (
                activation.operators
                and callsign in [
                    item.strip().upper()
                    for item in activation.operators.split(",")
                ]
            )
        )
    ]

    qso_total = sum(
        activation.qso_count or 0
        for activation in matched
    )

    object_ids = {
        activation.ylff_object_id
        for activation in matched
    }

    rows = ""

    for activation in matched:
        obj = YLFFObject.query.get(activation.ylff_object_id)

        rows += f"""
          <tr>
            <td>{activation.callsign}</td>
            <td>{activation.operators or "-"}</td>
            <td>{obj.reference if obj else "-"}</td>
            <td>{obj.name if obj else "-"}</td>
            <td>{activation.activation_start or "-"}</td>
            <td>{activation.qso_count}</td>
          </tr>
        """

    if not rows:
        rows = """
          <tr>
            <td colspan="6">Šim operatoram aktivizāciju vēl nav.</td>
          </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>{callsign}</title>

  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      background: #0f172a;
      color: white;
    }}

    .container {{
      max-width: 1200px;
      margin: auto;
      padding: 30px;
    }}

    .card {{
      background: #111827;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 8px 24px rgba(0,0,0,.35);
    }}

    h1 {{
      color: #22c55e;
      font-size: 36px;
      margin-top: 0;
    }}

    h2 {{
      color: #e5e7eb;
      margin-top: 0;
    }}

    .stats {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}

    .stat {{
      background: #0f172a;
      border-radius: 14px;
      padding: 18px;
      border: 1px solid #1f2937;
    }}

    .stat-value {{
      font-size: 28px;
      color: #22c55e;
      font-weight: bold;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
    }}

    th, td {{
      padding: 12px;
      border-bottom: 1px solid #374151;
      text-align: left;
    }}

    th {{
      color: #22c55e;
    }}
  </style>
</head>

<body>
  <div class="container">

    <div class="card">
      <h1>{callsign}</h1>

      <div class="stats">
        <div class="stat">
          <div>Aktivizācijas</div>
          <div class="stat-value">{len(matched)}</div>
        </div>

        <div class="stat">
          <div>Unikāli objekti</div>
          <div class="stat-value">{len(object_ids)}</div>
        </div>

        <div class="stat">
          <div>Kopā QSO</div>
          <div class="stat-value">{qso_total}</div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Aktivizāciju vēsture</h2>

      <table>
        <thead>
          <tr>
            <th>CALL</th>
            <th>Operatori</th>
            <th>YLFF</th>
            <th>Objekts</th>
            <th>Datums</th>
            <th>QSO</th>
          </tr>
        </thead>

        <tbody>
          {rows}
        </tbody>
      </table>
    </div>

  </div>
</body>
</html>
"""
