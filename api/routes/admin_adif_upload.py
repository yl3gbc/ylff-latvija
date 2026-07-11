from datetime import datetime
import html
import json
import re

from flask import Blueprint, request

from extensions import db
from models.activation import Activation
from models.object import YLFFObject
from models.qso_record import QSORecord


admin_adif_upload_bp = Blueprint(
    "admin_adif_upload",
    __name__,
)


def normalize_reference(value):
    if not value:
        return None

    value = value.strip().upper()

    match = re.search(r"YLFF[- ]?(\d+)", value)

    if not match:
        return None

    return f"YLFF-{match.group(1).zfill(4)}"


def read_adif_field(record, field_name):
    pattern = rf"<{field_name}:\d+[^>]*>([^<]*)"
    match = re.search(pattern, record, re.IGNORECASE)

    if not match:
        return None

    return match.group(1).strip()


def parse_adif(content):
    records = re.split(r"<eor>", content, flags=re.IGNORECASE)

    qso_count = 0
    dates = []
    callsign = None
    operators = None
    reference = None
    qso_records = []

    for record in records:
        if "<qso_date" not in record.lower():
            continue

        worked_call = read_adif_field(record, "CALL")

        if not worked_call:
            continue

        qso_count += 1

        qso_date_value = read_adif_field(record, "QSO_DATE")
        qso_date = None

        if qso_date_value:
            try:
                qso_date = datetime.strptime(
                    qso_date_value,
                    "%Y%m%d",
                ).date()

                dates.append(qso_date)

            except ValueError:
                qso_date = None

        band = read_adif_field(record, "BAND")
        mode = read_adif_field(record, "MODE")

        qso_records.append(
            {
                "worked_call": worked_call.upper(),
                "qso_date": (
                    qso_date.isoformat()
                    if qso_date
                    else ""
                ),
                "band": band or "",
                "mode": mode or "",
            }
        )

        if not callsign:
            callsign = read_adif_field(
                record,
                "STATION_CALLSIGN",
            )

        if not operators:
            operators = read_adif_field(
                record,
                "OPERATOR",
            )

        if not reference:
            for field in [
                "QTH",
                "COMMENT",
                "NOTES",
                "ADDRESS",
            ]:
                value = read_adif_field(record, field)
                reference = normalize_reference(value or "")

                if reference:
                    break

    return {
        "qso_count": qso_count,
        "activation_start": min(dates) if dates else None,
        "activation_end": max(dates) if dates else None,
        "callsign": callsign,
        "operators": operators,
        "reference": reference,
        "qso_records": qso_records,
    }


@admin_adif_upload_bp.route(
    "/ylff-control-2026/adif",
    methods=["GET", "POST"],
)
def admin_adif_upload():
    result = None
    message = ""

    objects = YLFFObject.query.order_by(
        YLFFObject.reference.asc()
    ).all()

    if request.method == "POST":
        save_action = request.form.get("save_action")

        if save_action == "1":
            callsign = request.form.get(
                "callsign",
                "",
            ).strip().upper()

            operators = request.form.get(
                "operators",
                "",
            ).strip().upper()

            reference = request.form.get(
                "reference",
                "",
            ).strip().upper()

            qso_count = int(
                request.form.get(
                    "qso_count",
                    "0",
                )
            )

            activation_start = (
                request.form.get("activation_start")
                or None
            )

            activation_end = (
                request.form.get("activation_end")
                or None
            )

            qso_records_json = request.form.get(
                "qso_records_json",
                "[]",
            )

            try:
                parsed_qso_records = json.loads(
                    qso_records_json
                )

            except json.JSONDecodeError:
                parsed_qso_records = []

            start_date = (
                datetime.strptime(
                    activation_start,
                    "%Y-%m-%d",
                ).date()
                if activation_start
                else None
            )

            end_date = (
                datetime.strptime(
                    activation_end,
                    "%Y-%m-%d",
                ).date()
                if activation_end
                else None
            )

            ylff_object = YLFFObject.query.filter_by(
                reference=reference
            ).first()

            if not ylff_object:
                message = "Kļūda: objekts nav atrasts."

            elif not callsign:
                message = "Kļūda: CALL nav atrasts."

            elif not parsed_qso_records:
                message = "Kļūda: QSO ieraksti nav atrasti."

            else:
                activation_status = "complete"

                if qso_count < 100:
                    activation_status = "incomplete"

                activation = Activation(
                    callsign=callsign,
                    ylff_object_id=ylff_object.id,
                    operators=operators or callsign,
                    qso_count=qso_count,
                    activation_start=start_date,
                    activation_end=end_date,
                    status=activation_status,
                )

                db.session.add(activation)
                db.session.flush()

                saved_qso_count = 0

                for qso in parsed_qso_records:
                    worked_call = (
                        qso.get("worked_call", "")
                        .strip()
                        .upper()
                    )

                    if not worked_call:
                        continue

                    qso_date_value = qso.get("qso_date") or None

                    qso_date = (
                        datetime.strptime(
                            qso_date_value,
                            "%Y-%m-%d",
                        ).date()
                        if qso_date_value
                        else None
                    )

                    record = QSORecord(
                        activation_id=activation.id,
                        ylff_object_id=ylff_object.id,
                        worked_call=worked_call,
                        qso_date=qso_date,
                        band=qso.get("band") or None,
                        mode=qso.get("mode") or None,
                    )

                    db.session.add(record)
                    saved_qso_count += 1

                db.session.commit()

                if activation_status == "complete":
                    status_text = "pabeigta"
                else:
                    status_text = "nepabeigta"

                message = (
                    f"Aktivizācija saglabāta: "
                    f"{callsign} / {reference} / "
                    f"{qso_count} QSO. "
                    f"Statuss: {status_text}. "
                    f"QSO ieraksti saglabāti: "
                    f"{saved_qso_count}"
                )

        else:
            uploaded_file = request.files.get("adif_file")

            if not uploaded_file:
                message = "Kļūda: ADIF fails nav izvēlēts."

            else:
                content = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore",
                )

                result = parse_adif(content)

                callsign = (
                    request.form.get(
                        "callsign",
                        "",
                    ).strip().upper()
                    or (result.get("callsign") or "").upper()
                )

                operators = (
                    request.form.get(
                        "operators",
                        "",
                    ).strip().upper()
                    or (result.get("operators") or callsign).upper()
                )

                reference = (
                    request.form.get(
                        "reference",
                        "",
                    ).strip().upper()
                    or result.get("reference")
                )

                result["callsign"] = callsign
                result["operators"] = operators
                result["reference"] = reference

    object_options = ""

    for item in objects:
        selected = ""

        if result and result.get("reference") == item.reference:
            selected = "selected"

        object_options += f"""
          <option value="{item.reference}" {selected}>
            {item.reference} — {item.name}
          </option>
        """

    preview_html = ""

    if result:
        start_value = (
            result["activation_start"].isoformat()
            if result.get("activation_start")
            else ""
        )

        end_value = (
            result["activation_end"].isoformat()
            if result.get("activation_end")
            else ""
        )

        qso_records_json = html.escape(
            json.dumps(
                result.get("qso_records", []),
                ensure_ascii=False,
            ),
            quote=True,
        )

        if result.get("qso_count", 0) >= 100:
            preview_status = "Pabeigta aktivizācija"
        else:
            preview_status = "Nepabeigta aktivizācija"

        preview_html = f"""
          <div class="preview">
            <h2>ADIF priekšskatījums</h2>

            <p>
              <strong>CALL:</strong>
              {result.get("callsign") or "-"}
            </p>

            <p>
              <strong>Aktivizatori:</strong>
              {result.get("operators") or "-"}
            </p>

            <p>
              <strong>Objekts:</strong>
              {result.get("reference") or "-"}
            </p>

            <p>
              <strong>QSO:</strong>
              {result.get("qso_count")}
            </p>

            <p>
              <strong>Statuss:</strong>
              {preview_status}
            </p>

            <p>
              <strong>Sākums:</strong>
              {result.get("activation_start") or "-"}
            </p>

            <p>
              <strong>Beigas:</strong>
              {result.get("activation_end") or "-"}
            </p>

            <form method="POST">
              <input
                type="hidden"
                name="save_action"
                value="1"
              >

              <input
                type="hidden"
                name="callsign"
                value="{result.get("callsign") or ""}"
              >

              <input
                type="hidden"
                name="operators"
                value="{result.get("operators") or ""}"
              >

              <input
                type="hidden"
                name="reference"
                value="{result.get("reference") or ""}"
              >

              <input
                type="hidden"
                name="qso_count"
                value="{result.get("qso_count") or 0}"
              >

              <input
                type="hidden"
                name="activation_start"
                value="{start_value}"
              >

              <input
                type="hidden"
                name="activation_end"
                value="{end_value}"
              >

              <input
                type="hidden"
                name="qso_records_json"
                value="{qso_records_json}"
              >

              <button type="submit">
                Saglabāt aktivizāciju
              </button>
            </form>
          </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>ADIF imports</title>

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

    h1,
    h2 {{
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

    .preview {{
      margin-top: 24px;
      padding: 16px;
      border-radius: 14px;
      background: #0f172a;
      border: 1px solid #374151;
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

    <p>
      <a href="/">← Sākumlapa</a>
    </p>

    <div class="card">

      <h1>ADIF imports</h1>

      {f'<div class="message">{message}</div>' if message else ''}

      <form method="POST" enctype="multipart/form-data">

        <label>ADIF fails</label>
        <input
          type="file"
          name="adif_file"
          accept=".adi,.adif"
          required
        >

        <label>Ekspedīcijas CALL</label>
        <input
          name="callsign"
          placeholder="Ja ADIF nenolasa automātiski"
        >

        <label>Aktivizatori</label>
        <input
          name="operators"
          placeholder="Piemēram YL3GBC,YL2SW"
        >

        <label>YLFF objekts</label>
        <select name="reference">
          <option value="">
            Mēģināt nolasīt no ADIF
          </option>
          {object_options}
        </select>

        <div class="help">
          QSO skaits, datumi un nostrādātie CALL tiek nolasīti no ADIF faila automātiski.
          Ja QSO ir mazāk par 100, aktivizācija saglabājas kā nepabeigta.
        </div>

        <button type="submit">
          Pārbaudīt ADIF
        </button>

      </form>

      {preview_html}

    </div>

  </div>
</body>
</html>
"""
