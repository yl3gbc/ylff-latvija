from datetime import datetime

from flask import Blueprint, request

from extensions import db
from models.expedition_plan import ExpeditionPlan
from models.object import YLFFObject
from routes.layout import ylff_page


expedition_plan_bp = Blueprint("expedition_plan", __name__)


@expedition_plan_bp.route("/plan-expedition", methods=["GET", "POST"])
def plan_expedition():
    message = ""

    if request.method == "POST":
        planned_date_raw = request.form.get("planned_date", "").strip()
        planned_date = None

        if planned_date_raw:
            planned_date = datetime.strptime(planned_date_raw, "%Y-%m-%d").date()

        plan = ExpeditionPlan(
            callsign=request.form.get("callsign", "").strip().upper(),
            operators=request.form.get("operators", "").strip().upper(),
            ylff_reference=request.form.get("ylff_reference", "").strip().upper(),
            planned_date=planned_date,
            planned_time_utc=request.form.get("planned_time_utc", "").strip(),
            mode=request.form.get("mode", "").strip().upper(),
            whatsapp=request.form.get("whatsapp", "").strip(),
            email=request.form.get("email", "").strip(),
            notes=request.form.get("notes", "").strip(),
            status="pending",
        )

        db.session.add(plan)
        db.session.commit()

        message = """
        <div class="ylff-card">
          <h2 class="ylff-title">Pieteikums nosūtīts</h2>
          <p>Plānotā ekspedīcija saglabāta ar statusu <strong>pending</strong>.</p>
        </div>
        """

    objects = YLFFObject.query.order_by(YLFFObject.reference.asc()).all()

    options = ""
    for obj in objects:
        options += f'<option value="{obj.reference}">{obj.reference} - {obj.name}</option>'

    content = f"""
    {message}

    <div class="ylff-card">
      <h1 class="ylff-title">Plānot ekspedīciju</h1>

      <div class="ylff-subtitle">
        Aizpildi informāciju par plānoto YLFF aktivizāciju.
      </div>

      <form method="POST" class="ylff-form">
        <label>CALLSIGN</label>
        <input class="ylff-input" name="callsign" placeholder="YL3GBC" required>

        <label>Operatori</label>
        <input class="ylff-input" name="operators" placeholder="YL3GBC, YL2SW">

        <label>YLFF objekts</label>
        <select class="ylff-input" name="ylff_reference" required>
          {options}
        </select>

        <label>Datums</label>
        <input class="ylff-input" type="date" name="planned_date">

        <label>Sākuma laiks UTC</label>
        <input class="ylff-input" name="planned_time_utc" placeholder="08:00">

        <label>Mode</label>
        <input class="ylff-input" name="mode" placeholder="SSB, CW, DIGI">

        <label>WhatsApp</label>
        <input class="ylff-input" name="whatsapp" placeholder="+371...">

        <label>E-pasts</label>
        <input class="ylff-input" type="email" name="email" placeholder="callsign@example.com">

        <label>Piezīmes</label>
        <textarea class="ylff-input" name="notes" rows="6"></textarea>

        <br><br>

        <button class="ylff-button" type="submit">
          Nosūtīt pieteikumu
        </button>
      </form>
    </div>
    """

    return ylff_page("Plānot ekspedīciju", content)
