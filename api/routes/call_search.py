from html import escape

from flask import Blueprint, redirect, request

from models.activation import Activation
from models.object import YLFFObject
from models.qso_record import QSORecord
from routes.layout import ylff_page


call_search_bp = Blueprint(
    "call_search",
    __name__,
)


def split_operators(value):
    if not value:
        return []

    return [
        item.strip().upper()
        for item in value.split(",")
        if item.strip()
    ]


def award_status(count, required):
    if count >= required:
        return "Pieejams"

    return "Nav pietiekami"


@call_search_bp.route("/call/<callsign>")
def old_call_redirect(callsign):
    return redirect(
        f"/activity/{callsign.upper().strip()}"
    )


@call_search_bp.route("/activity", methods=["GET"])
def activity_search_form():
    callsign = request.args.get(
        "call",
        "",
    ).strip().upper()

    if callsign:
        return redirect(f"/activity/{callsign}")

    content = """
    <div class="ylff-card">
      <h1 class="ylff-title">
        Activity
      </h1>

      <div class="ylff-subtitle">
        Meklē savu CALL, lai redzētu nostrādātos YLFF objektus un aktivizācijas.
      </div>

      <form method="GET" action="/activity" class="ylff-search-row">
        <input
          class="ylff-input"
          name="call"
          placeholder="Piemēram IU7KIX, ON4SPR, YL3GBC"
          required
        >

        <button class="ylff-button" type="submit">
          Meklēt
        </button>
      </form>
    </div>
    """

    return ylff_page(
        "YLFF Activity",
        content,
    )


@call_search_bp.route("/activity/<callsign>")
def activity_result(callsign):
    callsign = escape(
        callsign.upper().strip()
    )

    all_activations = Activation.query.order_by(
        Activation.activation_start.desc()
    ).all()

    activator_activations = []

    for activation in all_activations:
        operators = split_operators(
            activation.operators
        )

        if (
            activation.callsign == callsign
            or callsign in operators
        ):
            activator_activations.append(activation)

    activator_rows = ""
    activator_object_ids = set()
    complete_object_ids = set()

    for activation in activator_activations:
        obj = YLFFObject.query.get(
            activation.ylff_object_id
        )

        if not obj:
            continue

        activator_object_ids.add(obj.reference)

        status = getattr(
            activation,
            "status",
            "complete",
        )

        if status == "complete":
            complete_object_ids.add(obj.reference)
            status_text = "Pabeigta"
            status_class = "ylff-status-complete"
        else:
            status_text = "Nepabeigta"
            status_class = "ylff-status-incomplete"

        activator_rows += f"""
        <tr>
          <td>
            <a href="/object/{obj.reference}">
              {obj.reference}
            </a>
          </td>

          <td>{activation.callsign}</td>

          <td>{activation.operators or "-"}</td>

          <td>{activation.qso_count}</td>

          <td>
            <span class="{status_class}">
              {status_text}
            </span>
          </td>
        </tr>
        """

    if not activator_rows:
        activator_rows = """
        <tr>
          <td colspan="5">
            Šis CALL nav atrasts kā aktivizators.
          </td>
        </tr>
        """

    hunter_qsos = QSORecord.query.filter_by(
        worked_call=callsign
    ).order_by(
        QSORecord.qso_date.desc()
    ).all()

    hunter_references = {}

    for qso in hunter_qsos:
        obj = YLFFObject.query.get(
            qso.ylff_object_id
        )

        activation = Activation.query.get(
            qso.activation_id
        )

        if not obj or not activation:
            continue

        if obj.reference not in hunter_references:
            hunter_references[obj.reference] = {
                "object": obj,
                "activation": activation,
                "qso": qso,
            }

    hunter_rows = ""

    for reference in sorted(hunter_references.keys()):
        item = hunter_references[reference]
        obj = item["object"]
        activation = item["activation"]
        qso = item["qso"]

        hunter_rows += f"""
        <tr>
          <td>
            <a href="/object/{obj.reference}">
              {obj.reference}
            </a>
          </td>

          <td>{obj.name}</td>

          <td>{activation.callsign}</td>

          <td>{activation.operators or "-"}</td>

          <td>{qso.qso_date or "-"}</td>

          <td>{qso.band or "-"}</td>

          <td>{qso.mode or "-"}</td>
        </tr>
        """

    if not hunter_rows:
        hunter_rows = """
        <tr>
          <td colspan="7">
            Šis CALL nav atrasts kā YLFF meklētājs.
          </td>
        </tr>
        """

    hunter_count = len(hunter_references)
    activator_count = len(complete_object_ids)

    content = f"""
    <div class="ylff-card">
      <h1 class="ylff-title">
        Activity: {callsign}
      </h1>

      <div class="ylff-subtitle">
        Šeit redzams, ko CALL ir aktivizējis un kādus YLFF objektus nostrādājis kā hunter.
      </div>

      <form method="GET" action="/activity" class="ylff-search-row">
        <input
          class="ylff-input"
          name="call"
          value="{callsign}"
          placeholder="Your call"
        >

        <button class="ylff-button" type="submit">
          Meklēt
        </button>

        <a class="ylff-button ylff-button-dark" href="/">
          Sākumlapa
        </a>
      </form>
    </div>

    <div class="ylff-card">
      <h2 class="ylff-title">
        Kā aktivizators
      </h2>

      <div class="ylff-subtitle">
        Pabeigti objekti aktivizatoram skaitās tikai tad, ja aktivizācija ir ar 100+ QSO.
      </div>

      <h3>
        Atrastas pabeigtas references kā aktivizatoram: {activator_count}
      </h3>

      <table class="ylff-table">
        <thead>
          <tr>
            <th>Reference</th>
            <th>CALL</th>
            <th>Aktivizatori</th>
            <th>QSO</th>
            <th>Statuss</th>
          </tr>
        </thead>

        <tbody>
          {activator_rows}
        </tbody>
      </table>

      <h3>Status of activators award</h3>

      <table class="ylff-table">
        <thead>
          <tr>
            <th>Bronze</th>
            <th>Silver</th>
            <th>Gold</th>
            <th>For 10</th>
            <th>For 15</th>
            <th>For 20</th>
            <th>For 25</th>
            <th>Honor Roll</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>{award_status(activator_count, 3)}</td>
            <td>{award_status(activator_count, 5)}</td>
            <td>{award_status(activator_count, 10)}</td>
            <td>{award_status(activator_count, 10)}</td>
            <td>{award_status(activator_count, 15)}</td>
            <td>{award_status(activator_count, 20)}</td>
            <td>{award_status(activator_count, 25)}</td>
            <td>{award_status(activator_count, 100)}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="ylff-card">
      <h2 class="ylff-title">
        Kā YLFF meklētājs / Hunter
      </h2>

      <div class="ylff-subtitle">
        Hunter diplomiem skaitās unikāli nostrādātie YLFF objekti no ADIF QSO ierakstiem.
      </div>

      <h3>
        Atrastas nostrādātas references: {hunter_count}
      </h3>

      <table class="ylff-table">
        <thead>
          <tr>
            <th>Reference</th>
            <th>Objekts</th>
            <th>Aktivizēja</th>
            <th>Aktivizatori</th>
            <th>Datums</th>
            <th>Band</th>
            <th>Mode</th>
          </tr>
        </thead>

        <tbody>
          {hunter_rows}
        </tbody>
      </table>

      <h3>Status of hunter award</h3>

      <table class="ylff-table">
        <thead>
          <tr>
            <th>Bronze</th>
            <th>Silver</th>
            <th>Gold</th>
            <th>YLFF15</th>
            <th>YLFF25</th>
            <th>YLFF35</th>
            <th>YLFF50</th>
            <th>Honor Roll</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>{award_status(hunter_count, 10)}</td>
            <td>{award_status(hunter_count, 25)}</td>
            <td>{award_status(hunter_count, 50)}</td>
            <td>{award_status(hunter_count, 15)}</td>
            <td>{award_status(hunter_count, 25)}</td>
            <td>{award_status(hunter_count, 35)}</td>
            <td>{award_status(hunter_count, 50)}</td>
            <td>{award_status(hunter_count, 100)}</td>
          </tr>
        </tbody>
      </table>
    </div>
    """

    return ylff_page(
        f"Activity {callsign}",
        content,
    )
