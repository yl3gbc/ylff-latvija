import html

from flask import Blueprint

from models.page_content import PageContent
from routes.layout import ylff_page
from routes.translations import get_lang, lang_url


public_pages_bp = Blueprint(
    "public_pages",
    __name__,
)


DEFAULT_CONTENT = {
    "rules": {
        "lv": {
            "title": "YLFF programmas nolikums",
            "content": """
<p>
  YLFF programma ir Latvijas Flora un Fauna amatieru radio aktivitāšu programma,
  kuras mērķis ir popularizēt Latvijas dabas teritorijas, radioamatieru aktivitāti
  un starptautiskus sakarus no dabas objektiem.
</p>

<h2>1. Programmas mērķis</h2>
<p>
  Programmas mērķis ir veicināt radioamatieru darbību no Latvijas dabas teritorijām,
  popularizēt aizsargājamos objektus un apkopot aktivizācijas, QSO ierakstus,
  aktivizatoru un hunter statistiku.
</p>

<h2>2. YLFF objekti</h2>
<ul>
  <li>Katram objektam tiek piešķirta YLFF reference.</li>
  <li>Reference tiek lietota formātā YLFF-0001, YLFF-0035, YLFF-0368.</li>
  <li>Objekti ir publiski redzami objektu katalogā un kartē.</li>
</ul>

<h2>3. Aktivizācija</h2>
<ul>
  <li>Aktivizācija tiek veikta no YLFF objekta teritorijas.</li>
  <li>Ekspedīcijas CALL ir tas izsaukuma signāls, kas lietots ēterā.</li>
  <li>Aktivizatori ir operatori, kuriem aktivizācija tiek ieskaitīta.</li>
</ul>

<h2>4. 100 QSO prasība</h2>
<ul>
  <li>Pabeigta aktivizācija ir aktivizācija ar vismaz 100 QSO.</li>
  <li>Ja ADIF logā ir mazāk par 100 QSO, aktivizācija saglabājas kā nepabeigta.</li>
  <li>Nepabeigtas aktivizācijas QSO saglabājas sistēmā.</li>
</ul>
""",
        },
        "en": {
            "title": "YLFF Rules",
            "content": """
<p>
  The YLFF programme is the Latvian Flora and Fauna amateur radio activity programme.
  Its purpose is to promote Latvian nature areas, amateur radio activity and
  international contacts from YLFF references.
</p>

<h2>1. Programme purpose</h2>
<p>
  The programme encourages amateur radio operation from Latvian nature areas and
  maintains activation, QSO, activator and hunter statistics.
</p>

<h2>2. YLFF references</h2>
<ul>
  <li>Each object has a unique YLFF reference.</li>
  <li>The reference format is YLFF-0001, YLFF-0035, YLFF-0368.</li>
  <li>Objects are visible in the public catalogue and map.</li>
</ul>

<h2>3. Activation</h2>
<ul>
  <li>An activation is made from the territory of a YLFF object.</li>
  <li>The expedition callsign is the callsign used on air.</li>
  <li>Operators listed for the activation receive activator credit.</li>
</ul>

<h2>4. 100 QSO requirement</h2>
<ul>
  <li>A completed activation requires at least 100 QSOs.</li>
  <li>If an ADIF log has fewer than 100 QSOs, it is stored as incomplete.</li>
  <li>Incomplete activation QSOs are still stored in the system.</li>
</ul>
""",
        },
        "ru": {
            "title": "Положение YLFF",
            "content": """
<p>
  Программа YLFF — это латвийская программа радиолюбительской активности
  Flora and Fauna. Цель программы — популяризация природных территорий Латвии,
  радиолюбительской активности и международных связей с объектов YLFF.
</p>

<h2>1. Цель программы</h2>
<p>
  Программа поддерживает работу радиолюбителей с природных территорий Латвии
  и ведёт статистику активаций, QSO, активаторов и hunter.
</p>

<h2>2. Объекты YLFF</h2>
<ul>
  <li>Каждому объекту присваивается уникальный YLFF reference.</li>
  <li>Формат reference: YLFF-0001, YLFF-0035, YLFF-0368.</li>
  <li>Объекты доступны в публичном каталоге и на карте.</li>
</ul>

<h2>3. Активация</h2>
<ul>
  <li>Активация выполняется с территории объекта YLFF.</li>
  <li>Экспедиционный CALL — это позывной, используемый в эфире.</li>
  <li>Операторы, указанные в активации, получают зачёт активатора.</li>
</ul>

<h2>4. Требование 100 QSO</h2>
<ul>
  <li>Завершённая активация требует минимум 100 QSO.</li>
  <li>Если в ADIF меньше 100 QSO, активация сохраняется как незавершённая.</li>
  <li>QSO незавершённой активации всё равно сохраняются в системе.</li>
</ul>
""",
        },
    },
    "awards": {
        "lv": {
            "title": "YLFF Diplomi / Awards",
            "content": """
<p>
  Šajā sadaļā tiek publicēti YLFF diplomu veidi, nosacījumi un diplomu paraugi.
  Activity sadaļā katrs radioamatieris var pārbaudīt savu statusu pēc CALL.
</p>

<h2>Hunter diplomi</h2>
<table class="ylff-table">
  <thead>
    <tr>
      <th>Diploms</th>
      <th>Nosacījums</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bronze Hunter Award</td><td>10 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>Silver Hunter Award</td><td>25 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>Gold Hunter Award</td><td>50 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>YLFF15 Hunter</td><td>15 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>YLFF25 Hunter</td><td>25 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>YLFF35 Hunter</td><td>35 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>YLFF50 Hunter</td><td>50 unikāli nostrādāti YLFF objekti</td></tr>
    <tr><td>Honor Roll Hunter</td><td>100 vai vairāk unikāli nostrādāti YLFF objekti</td></tr>
  </tbody>
</table>

<h2>Aktivizatoru diplomi</h2>
<table class="ylff-table">
  <thead>
    <tr>
      <th>Diploms</th>
      <th>Nosacījums</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bronze Activator Award</td><td>3 pabeigti YLFF objekti</td></tr>
    <tr><td>Silver Activator Award</td><td>5 pabeigti YLFF objekti</td></tr>
    <tr><td>Gold Activator Award</td><td>10 pabeigti YLFF objekti</td></tr>
    <tr><td>YLFF10 Activator</td><td>10 pabeigti YLFF objekti</td></tr>
    <tr><td>YLFF15 Activator</td><td>15 pabeigti YLFF objekti</td></tr>
    <tr><td>YLFF20 Activator</td><td>20 pabeigti YLFF objekti</td></tr>
    <tr><td>YLFF25 Activator</td><td>25 pabeigti YLFF objekti</td></tr>
    <tr><td>Honor Roll Activator</td><td>100 vai vairāk pabeigti YLFF objekti</td></tr>
  </tbody>
</table>
""",
        },
        "en": {
            "title": "YLFF Awards",
            "content": """
<p>
  This section contains YLFF award types, requirements and sample diplomas.
  Each radio amateur can check their status by callsign in the Activity section.
</p>

<h2>Hunter awards</h2>
<table class="ylff-table">
  <thead>
    <tr>
      <th>Award</th>
      <th>Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bronze Hunter Award</td><td>10 unique worked YLFF references</td></tr>
    <tr><td>Silver Hunter Award</td><td>25 unique worked YLFF references</td></tr>
    <tr><td>Gold Hunter Award</td><td>50 unique worked YLFF references</td></tr>
    <tr><td>YLFF15 Hunter</td><td>15 unique worked YLFF references</td></tr>
    <tr><td>YLFF25 Hunter</td><td>25 unique worked YLFF references</td></tr>
    <tr><td>YLFF35 Hunter</td><td>35 unique worked YLFF references</td></tr>
    <tr><td>YLFF50 Hunter</td><td>50 unique worked YLFF references</td></tr>
    <tr><td>Honor Roll Hunter</td><td>100 or more unique worked YLFF references</td></tr>
  </tbody>
</table>

<h2>Activator awards</h2>
<table class="ylff-table">
  <thead>
    <tr>
      <th>Award</th>
      <th>Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bronze Activator Award</td><td>3 completed YLFF references</td></tr>
    <tr><td>Silver Activator Award</td><td>5 completed YLFF references</td></tr>
    <tr><td>Gold Activator Award</td><td>10 completed YLFF references</td></tr>
    <tr><td>YLFF10 Activator</td><td>10 completed YLFF references</td></tr>
    <tr><td>YLFF15 Activator</td><td>15 completed YLFF references</td></tr>
    <tr><td>YLFF20 Activator</td><td>20 completed YLFF references</td></tr>
    <tr><td>YLFF25 Activator</td><td>25 completed YLFF references</td></tr>
    <tr><td>Honor Roll Activator</td><td>100 or more completed YLFF references</td></tr>
  </tbody>
</table>
""",
        },
        "ru": {
            "title": "Дипломы YLFF",
            "content": """
<p>
  В этом разделе публикуются виды дипломов YLFF, условия и образцы дипломов.
  Каждый радиолюбитель может проверить свой статус по CALL в разделе Activity.
</p>

<h2>Дипломы Hunter</h2>
<table class="ylff-table">
  <thead>
    <tr>
      <th>Диплом</th>
      <th>Условие</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bronze Hunter Award</td><td>10 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>Silver Hunter Award</td><td>25 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>Gold Hunter Award</td><td>50 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>YLFF15 Hunter</td><td>15 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>YLFF25 Hunter</td><td>25 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>YLFF35 Hunter</td><td>35 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>YLFF50 Hunter</td><td>50 уникальных сработанных объектов YLFF</td></tr>
    <tr><td>Honor Roll Hunter</td><td>100 или больше уникальных сработанных объектов YLFF</td></tr>
  </tbody>
</table>

<h2>Дипломы Activator</h2>
<table class="ylff-table">
  <thead>
    <tr>
      <th>Диплом</th>
      <th>Условие</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Bronze Activator Award</td><td>3 завершённых объекта YLFF</td></tr>
    <tr><td>Silver Activator Award</td><td>5 завершённых объектов YLFF</td></tr>
    <tr><td>Gold Activator Award</td><td>10 завершённых объектов YLFF</td></tr>
    <tr><td>YLFF10 Activator</td><td>10 завершённых объектов YLFF</td></tr>
    <tr><td>YLFF15 Activator</td><td>15 завершённых объектов YLFF</td></tr>
    <tr><td>YLFF20 Activator</td><td>20 завершённых объектов YLFF</td></tr>
    <tr><td>YLFF25 Activator</td><td>25 завершённых объектов YLFF</td></tr>
    <tr><td>Honor Roll Activator</td><td>100 или больше завершённых объектов YLFF</td></tr>
  </tbody>
</table>
""",
        },
    },
    "about": {
        "lv": {
            "title": "Par projektu",
            "content": """
<p>
  YLFF Latvija ir Latvijas Flora un Fauna amatieru radio statistikas,
  aktivizāciju, objektu un diplomu platforma.
</p>

<p>
  Projekta mērķis ir apkopot YLFF objektus, aktivizācijas, ADIF logus,
  hunter statistiku, aktivizatoru rezultātus un diplomu statusus vienā
  kopīgā publiskā sistēmā.
</p>

<ul>
  <li>YLFF objektu katalogs un karte;</li>
  <li>ADIF logu imports;</li>
  <li>aktivizatoru statistika;</li>
  <li>hunter / Activity meklēšana pēc CALL;</li>
  <li>diplomu noteikumi un statuss;</li>
  <li>programmas nolikums.</li>
</ul>
""",
        },
        "en": {
            "title": "About the project",
            "content": """
<p>
  YLFF Latvia is a platform for Latvian Flora and Fauna amateur radio statistics,
  activations, objects and awards.
</p>

<p>
  The goal is to collect YLFF objects, activations, ADIF logs, hunter statistics,
  activator results and award status in one public system.
</p>

<ul>
  <li>YLFF object catalogue and map;</li>
  <li>ADIF log import;</li>
  <li>activator statistics;</li>
  <li>hunter / Activity callsign search;</li>
  <li>award rules and status;</li>
  <li>programme rules.</li>
</ul>
""",
        },
        "ru": {
            "title": "О проекте",
            "content": """
<p>
  YLFF Latvia — это платформа для статистики латвийской Flora and Fauna,
  активаций, объектов и дипломов.
</p>

<p>
  Цель проекта — собрать объекты YLFF, активации, ADIF логи, статистику hunter,
  результаты активаторов и статус дипломов в одной публичной системе.
</p>

<ul>
  <li>каталог объектов YLFF и карта;</li>
  <li>импорт ADIF логов;</li>
  <li>статистика активаторов;</li>
  <li>поиск hunter / Activity по CALL;</li>
  <li>условия и статус дипломов;</li>
  <li>положение программы.</li>
</ul>
""",
        },
    },
}


def get_page(slug):
    page = PageContent.query.filter_by(
        slug=slug,
    ).first()

    return page


def get_default(slug, lang):
    return DEFAULT_CONTENT.get(
        slug,
        {},
    ).get(
        lang,
        DEFAULT_CONTENT.get(slug, {}).get("lv", {}),
    )


def pick_page_text(page, slug, lang):
    default = get_default(slug, lang)

    if not page:
        return (
            default.get("title", slug.title()),
            default.get("content", ""),
        )

    title = getattr(page, f"title_{lang}", None)
    content = getattr(page, f"content_{lang}", None)

    if not title:
        title = default.get("title", slug.title())

    if not content:
        content = default.get("content", "")

    return title, content


def render_public_page(slug):
    lang = get_lang()
    page = get_page(slug)

    title, content_html = pick_page_text(
        page,
        slug,
        lang,
    )

    edit_link = ""

    content = f"""
    <div class="ylff-card">
      <h1 class="ylff-title">{html.escape(title)}</h1>

      <div class="ylff-subtitle">
        {content_html}
      </div>
    </div>

    <div class="ylff-card">
      <a class="ylff-button" href="{lang_url('/activity')}">
        Activity
      </a>

      <a class="ylff-button ylff-button-gold" href="{lang_url('/objects-list')}">
        Objekti
      </a>

      <a class="ylff-button ylff-button-dark" href="{lang_url('/map')}">
        Karte
      </a>
    </div>
    """

    return ylff_page(
        title,
        content,
    )


@public_pages_bp.route("/rules")
def rules_page():
    return render_public_page("rules")


@public_pages_bp.route("/awards")
def awards_page():
    return render_public_page("awards")


@public_pages_bp.route("/about")
def about_page():
    return render_public_page("about")
