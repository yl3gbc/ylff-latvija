from collections import defaultdict

from flask import Blueprint

from models.activation import Activation


top_operators_bp = Blueprint(
    "top_operators",
    __name__,
)


@top_operators_bp.route("/top-operators")
def top_operators():
    activations = Activation.query.all()

    stats = defaultdict(
        lambda: {
            "activations": 0,
            "objects": set(),
            "qso": 0,
        }
    )

    for activation in activations:
        if not activation.operators:
            continue

        operators = [
            item.strip().upper()
            for item in activation.operators.split(",")
            if item.strip()
        ]

        for operator in operators:
            stats[operator]["activations"] += 1
            stats[operator]["objects"].add(activation.ylff_object_id)
            stats[operator]["qso"] += activation.qso_count or 0

    rows = ""

    sorted_stats = sorted(
        stats.items(),
        key=lambda item: item[1]["qso"],
        reverse=True,
    )

    for index, (operator, data) in enumerate(sorted_stats, start=1):
        rows += f"""
          <tr>
            <td>{index}</td>
            <td>
              <a href="/operator/{operator}">
                {operator}
              </a>
            </td>
            <td>{data["activations"]}</td>
            <td>{len(data["objects"])}</td>
            <td>{data["qso"]}</td>
          </tr>
        """

    if not rows:
        rows = """
          <tr>
            <td colspan="5">Operatoru statistikas vēl nav.</td>
          </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>TOP operatori</title>

  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      background: #0f172a;
      color: white;
    }}

    .container {{
      max-width: 1100px;
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
      font-size: 36px;
      margin-top: 0;
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

    a {{
      color: #4ade80;
      text-decoration: none;
      font-weight: bold;
    }}
  </style>
</head>

<body>
  <div class="container">
    <div class="card">
      <h1>TOP operatori</h1>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Operators</th>
            <th>Aktivizācijas</th>
            <th>Objekti</th>
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
