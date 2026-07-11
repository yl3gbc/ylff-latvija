from collections import defaultdict

from flask import Blueprint

from models.activation import Activation
from models.object import YLFFObject


top_objects_bp = Blueprint(
    "top_objects",
    __name__,
)


@top_objects_bp.route("/top-objects")
def top_objects():
    activations = Activation.query.all()

    stats = defaultdict(
        lambda: {
            "activations": 0,
            "qso": 0,
        }
    )

    for activation in activations:
        stats[activation.ylff_object_id]["activations"] += 1
        stats[activation.ylff_object_id]["qso"] += (
            activation.qso_count or 0
        )

    rows = ""

    sorted_stats = sorted(
        stats.items(),
        key=lambda item: item[1]["qso"],
        reverse=True,
    )

    for index, (object_id, data) in enumerate(sorted_stats, start=1):
        obj = YLFFObject.query.get(object_id)

        if not obj:
            continue

        rows += f"""
          <tr>
            <td>{index}</td>

            <td>
              <a href="/object/{obj.reference}">
                {obj.reference}
              </a>
            </td>

            <td>{obj.name}</td>

            <td>{data["activations"]}</td>

            <td>{data["qso"]}</td>
          </tr>
        """

    if not rows:
        rows = """
          <tr>
            <td colspan="5">
              Objektu statistikas vēl nav.
            </td>
          </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>TOP objekti</title>

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

      <h1>TOP objekti</h1>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Reference</th>
            <th>Objekts</th>
            <th>Aktivizācijas</th>
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
