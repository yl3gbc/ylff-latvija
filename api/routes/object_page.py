import html
from flask import Blueprint

from models.activation import Activation
from models.object import YLFFObject


object_page_bp = Blueprint(
    "object_page",
    __name__,
)


@object_page_bp.route("/object/<reference>")
def object_page(reference):
    item = YLFFObject.query.filter_by(
        reference=reference,
    ).first()

    if not item:
        return "<h1>Objekts nav atrasts</h1>", 404

    activations = Activation.query.filter_by(
        ylff_object_id=item.id,
    ).order_by(
        Activation.activation_start.desc()
    ).all()

    activation_count = len(activations)
    activation_status = "Aktivizēts" if activation_count > 0 else "Nav aktivizēts"
    status_active_class = "status-active" if activation_count > 0 else "status-not-active"
    qso_total = sum(activation.qso_count or 0 for activation in activations)

    activator_calls = sorted(
        {
            activation.callsign
            for activation in activations
            if activation.callsign
        }
    )

    activators_text = ", ".join(activator_calls) if activator_calls else "-"

    activation_rows = ""

    for activation in activations:
        activation_rows += f"""
          <tr>
            <td>{activation.callsign}</td>
            <td>{activation.operators or "-"}</td>
            <td>{activation.activation_start or "-"}</td>
            <td>{activation.activation_end or "-"}</td>
            <td>{activation.qso_count}</td>
          </tr>
        """

    if not activation_rows:
        activation_rows = """
          <tr>
            <td colspan="5">Aktivizāciju vēl nav.</td>
          </tr>
        """

    image_url = html.escape(getattr(item, "image_url", "") or "")

    object_image_html = ""
    if image_url:
        object_image_html = f"""
        <div class="card object-image-card">
          <img class="object-image" src="{image_url}" alt="{html.escape(item.reference)}">
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>{item.reference}</title>

  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css">

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
      margin-bottom: 24px;
      box-shadow: 0 8px 24px rgba(0,0,0,.35);
    }}

    h1 {{
      margin-top: 0;
      color: #22c55e;
      font-size: 36px;
    }}

    h2 {{
      color: #e5e7eb;
      margin-top: 0;
    }}

    #map {{
      height: 420px;
      border-radius: 16px;
    }}

    .info {{
      line-height: 1.9;
      font-size: 16px;
    }}

    .status {{
      display: inline-block;
      padding: 6px 12px;
      border-radius: 999px;
      background: #16803a;
      font-weight: bold;
    }}

    .btn {{
      display: inline-block;
      padding: 10px 14px;
      color: white;
      text-decoration: none;
      border-radius: 10px;
      font-weight: bold;
      margin-right: 10px;
      margin-top: 14px;
    }}

    .btn-blue {{
      background: #2563eb;
    }}

    .btn-orange {{
      background: #ea580c;
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
      font-weight: bold;
    }}

      .object-image-card {{
        margin-top: 20px;
        padding: 0;
        overflow: hidden;
      }}

      .object-image {{
        width: 100%;
        max-height: 420px;
        display: block;
        object-fit: cover;
        border-radius: 12px;
      }}

    </style>
</head>

<body>
  <div class="container">

    <div class="card">
      <h1>{item.reference}</h1>

      {object_image_html}

      <div class="info">
        <strong>Nosaukums:</strong> {item.name}<br>

        <strong>Aktivizācijas statuss:</strong>
        <span class="{status_active_class}">{activation_status}</span><br>

        <strong>Aktivizāciju skaits:</strong>
        {activation_count}<br>

        <strong>Koordinātas:</strong>
        {item.latitude}, {item.longitude}<br>

        <strong>Lokators:</strong>
        {item.locator or "-"}<br>

        <strong>Apraksts:</strong>
        {item.description or "-"}<br>

        <a
          class="btn btn-blue"
          href="https://www.google.com/maps?q={item.latitude},{item.longitude}"
          target="_blank"
        >
          Atvērt Google Maps
        </a>

        <a
          class="btn btn-orange"
          href="https://www.google.com/maps/dir/?api=1&destination={item.latitude},{item.longitude}"
          target="_blank"
        >
          Navigācija
        </a>
      </div>
    </div>

    <div class="card">
      <div id="map"></div>
    </div>

    <div class="card">
      <h2>Aktivizāciju statistika</h2>

      <div class="info">
        Aktivizāciju skaits: {activation_count}<br>
        QSO skaits: {qso_total}<br>
        Aktivatori: {activators_text}
      </div>
    </div>

    <div class="card">
      <h2>Aktivizāciju vēsture</h2>

      <table>
        <thead>
          <tr>
            <th>CALL</th>
            <th>Operatori</th>
            <th>Sākums</th>
            <th>Beigas</th>
            <th>QSO</th>
          </tr>
        </thead>

        <tbody>
          {activation_rows}
        </tbody>
      </table>
    </div>

  </div>

  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

  <script>
    const map = L.map("map").setView(
      [{item.latitude}, {item.longitude}],
      11
    );

    L.tileLayer(
      "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",
      {{
        maxZoom: 19,
        attribution: "© OpenStreetMap"
      }}
    ).addTo(map);

    L.marker(
      [{item.latitude}, {item.longitude}]
    ).addTo(map);
  </script>
</body>
</html>
"""