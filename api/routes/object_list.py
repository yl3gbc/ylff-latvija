from flask import Blueprint, request
from sqlalchemy import or_

from models.object import YLFFObject
from models.activation import Activation
from routes.layout import ylff_page


object_list_bp = Blueprint(
    "object_list",
    __name__,
)

objects_list_bp = object_list_bp


@object_list_bp.route("/objects-list")
def objects_list():
    search = request.args.get(
        "search",
        "",
    ).strip()

    query = YLFFObject.query

    if search:
        like = f"%{search}%"

        query = query.filter(
            or_(
                YLFFObject.reference.ilike(like),
                YLFFObject.name.ilike(like),
                YLFFObject.locator.ilike(like),
                YLFFObject.status.ilike(like),
            )
        )

    objects = query.order_by(
        YLFFObject.reference.asc()
    ).all()

    rows = ""

    for obj in objects:
        activation_count = Activation.query.filter_by(
            ylff_object_id=obj.id,
            status="complete",
        ).count()

        object_activation_status = (
            "Aktivizēts"
            if activation_count > 0
            else "Nav aktivizēts"
        )

        status_class = (
            "ylff-status-complete"
            if activation_count > 0
            else "ylff-status-incomplete"
        )

        rows += f"""
        <tr>
          <td>
            <a href="/object/{obj.reference}">
              {obj.reference}
            </a>
          </td>

          <td>{obj.name}</td>

          <td>{obj.locator or "-"}</td>

          <td>
            <span class="{status_class}">
              Nav aktivizēts
            </span>
          </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
          <td colspan="4">
            Objekti pēc šī meklējuma nav atrasti.
          </td>
        </tr>
        """

    content = f"""
    <div class="ylff-card">
      <h1 class="ylff-title">
        YLFF objektu katalogs
      </h1>

      <div class="ylff-subtitle">
        Meklē objektus pēc YLFF references, nosaukuma, lokatora vai statusa.
      </div>

      <form method="GET" action="/objects-list" class="ylff-search-row">
        <input
          class="ylff-input"
          type="text"
          name="search"
          value="{search}"
          placeholder="Piemēram YLFF-0368, Gauja, KO26, active"
        >

        <button class="ylff-button" type="submit">
          Meklēt
        </button>

        <a class="ylff-button ylff-button-dark" href="/objects-list">
          Notīrīt
        </a>

        <a class="ylff-button ylff-button-gold" href="/map">
          Atvērt karti
        </a>
      </form>
    </div>

    <div class="ylff-card">
      <h2 class="ylff-title">
        Atrastie objekti: {len(objects)}
      </h2>

      <table class="ylff-table">
        <thead>
          <tr>
            <th>YLFF</th>
            <th>Nosaukums</th>
            <th>Lokators</th>
            <th>Statuss</th>
          </tr>
        </thead>

        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    """

    return ylff_page(
        "YLFF objektu katalogs",
        content,
    )
