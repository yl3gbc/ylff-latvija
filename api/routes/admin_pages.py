import html

from flask import Blueprint, redirect, request

from extensions import db
from models.page_content import PageContent


admin_pages_bp = Blueprint(
    "admin_pages",
    __name__,
)


PAGE_LABELS = {
    "rules": "Nolikums",
    "awards": "Diplomi",
    "about": "Par projektu",
}


def get_or_create_page(slug):
    page = PageContent.query.filter_by(
        slug=slug,
    ).first()

    if page:
        return page

    page = PageContent(
        slug=slug,
        title_lv=PAGE_LABELS.get(slug, slug),
        title_en=slug.title(),
        title_ru=PAGE_LABELS.get(slug, slug),
        content_lv="",
        content_en="",
        content_ru="",
    )

    db.session.add(page)
    db.session.commit()

    return page


@admin_pages_bp.route("/ylff-control/pages")
def admin_pages_list():
    for slug in PAGE_LABELS:
        get_or_create_page(slug)

    pages = PageContent.query.order_by(
        PageContent.slug.asc()
    ).all()

    rows = ""

    for page in pages:
        rows += f"""
        <tr>
          <td>{html.escape(page.slug)}</td>
          <td>{html.escape(page.title_lv or "-")}</td>
          <td>{html.escape(page.title_en or "-")}</td>
          <td>{html.escape(page.title_ru or "-")}</td>
          <td>
            <a class="button" href="/ylff-control/pages/{page.slug}">
              Rediģēt
            </a>
          </td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Admin lapas</title>

  <style>
    body {{
      margin: 0;
      background: #f4f7fb;
      color: #0f172a;
      font-family: Arial, sans-serif;
    }}

    .layout {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: 280px 1fr;
    }}

    .sidebar {{
      background: #0b1726;
      color: white;
      padding: 24px 18px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 28px;
    }}

    .brand img {{
      width: 54px;
      height: 54px;
      object-fit: contain;
    }}

    .brand-title {{
      font-size: 24px;
      font-weight: bold;
    }}

    .menu-link {{
      display: block;
      padding: 12px 14px;
      border-radius: 10px;
      color: #e5e7eb;
      text-decoration: none;
      font-weight: 700;
      margin-bottom: 7px;
    }}

    .menu-link:hover,
    .menu-link.active {{
      background: #1d4ed8;
      color: white;
    }}

    .main {{
      padding: 34px;
    }}

    .top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 22px;
    }}

    h1 {{
      margin: 0;
      font-size: 32px;
    }}

    .card {{
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .06);
      overflow: hidden;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th,
    td {{
      padding: 14px 18px;
      border-bottom: 1px solid #e5e7eb;
      text-align: left;
      font-size: 14px;
    }}

    th {{
      background: #f8fafc;
      color: #334155;
      font-weight: 800;
    }}

    .button {{
      display: inline-block;
      padding: 9px 13px;
      border-radius: 9px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      font-size: 13px;
    }}

    .logout {{
      background: #fee2e2;
      color: #991b1b;
    }}
  </style>
</head>

<body>
  <div class="layout">

    <aside class="sidebar">
      <div class="brand">
        <img src="/static/img/logo-small.png" alt="YLFF">
        <div>
          <div class="brand-title">YLFF Admin</div>
          <div>Control Panel</div>
        </div>
      </div>

      <a class="menu-link" href="/ylff-control">🏠 Pārskats</a>
      <a class="menu-link" href="/ylff-control-2026/adif">📥 ADIF imports</a>
      <a class="menu-link" href="/ylff-control-2026/activations">📡 Aktivizācijas</a>
      <a class="menu-link active" href="/ylff-control/pages">📝 Publiskās lapas</a>
      <a class="menu-link" href="/">🌐 Publiskā lapa</a>
      <a class="menu-link" href="/ylff-control/logout">🚪 Izlogoties</a>
    </aside>

    <main class="main">
      <div class="top">
        <h1>Publisko lapu rediģēšana</h1>

        <a class="button logout" href="/ylff-control/logout">
          Izlogoties
        </a>
      </div>

      <div class="card">
        <table>
          <thead>
            <tr>
              <th>Slug</th>
              <th>LV virsraksts</th>
              <th>EN virsraksts</th>
              <th>RU virsraksts</th>
              <th>Darbība</th>
            </tr>
          </thead>

          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </main>

  </div>
</body>
</html>
"""


@admin_pages_bp.route(
    "/ylff-control/pages/<slug>",
    methods=["GET", "POST"],
)
def admin_page_edit(slug):
    if slug not in PAGE_LABELS:
        return redirect("/ylff-control/pages")

    page = get_or_create_page(slug)

    if request.method == "POST":
        page.title_lv = request.form.get("title_lv", "").strip()
        page.title_en = request.form.get("title_en", "").strip()
        page.title_ru = request.form.get("title_ru", "").strip()

        page.content_lv = request.form.get("content_lv", "")
        page.content_en = request.form.get("content_en", "")
        page.content_ru = request.form.get("content_ru", "")

        db.session.commit()

        return redirect("/ylff-control/pages")

    title_lv = html.escape(page.title_lv or "")
    title_en = html.escape(page.title_en or "")
    title_ru = html.escape(page.title_ru or "")

    content_lv = html.escape(page.content_lv or "")
    content_en = html.escape(page.content_en or "")
    content_ru = html.escape(page.content_ru or "")

    return f"""
<!DOCTYPE html>
<html lang="lv">
<head>
  <meta charset="UTF-8">
  <title>Rediģēt {html.escape(slug)}</title>

  <style>
    body {{
      margin: 0;
      background: #f4f7fb;
      color: #0f172a;
      font-family: Arial, sans-serif;
    }}

    .container {{
      max-width: 1180px;
      margin: auto;
      padding: 34px;
    }}

    .card {{
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      padding: 26px;
      box-shadow: 0 6px 18px rgba(15, 23, 42, .06);
      margin-bottom: 20px;
    }}

    h1 {{
      margin-top: 0;
      font-size: 32px;
    }}

    .hint {{
      color: #64748b;
      margin-bottom: 22px;
      line-height: 1.6;
    }}

    label {{
      display: block;
      margin-top: 20px;
      margin-bottom: 7px;
      font-weight: 800;
      color: #334155;
    }}

    input,
    textarea {{
      width: 100%;
      padding: 12px 14px;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      font-size: 15px;
      font-family: Arial, sans-serif;
    }}

    textarea {{
      min-height: 220px;
      resize: vertical;
      line-height: 1.6;
    }}

    .language-block {{
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      padding: 18px;
      margin-top: 22px;
      background: #f8fafc;
    }}

    .language-title {{
      font-size: 20px;
      font-weight: 900;
      color: #0f172a;
      margin-bottom: 10px;
    }}

    .actions {{
      display: flex;
      gap: 12px;
      margin-top: 26px;
      flex-wrap: wrap;
    }}

    button,
    .button {{
      display: inline-block;
      padding: 12px 18px;
      border: none;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      text-decoration: none;
      font-weight: 800;
      cursor: pointer;
      font-size: 15px;
    }}

    .secondary {{
      background: #334155;
    }}

    .public {{
      background: #16a34a;
    }}

    .ck-editor__editable {{
      min-height: 280px;
      line-height: 1.6;
      color: #0f172a;
      font-size: 15px;
      background: white;
    }}

    .ck-toolbar {{
      border-radius: 10px 10px 0 0 !important;
    }}

    .ck-editor__main > .ck-editor__editable {{
      border-radius: 0 0 10px 10px !important;
    }}
  </style>
</head>

<body>
  <div class="container">

    <div class="card">
      <h1>Rediģēt: {html.escape(PAGE_LABELS.get(slug, slug))}</h1>

      <div class="hint">
        Šeit var labot publisko lapu tekstus trīs valodās.
        Teksts tiek saglabāts datubāzē un publiskā lapa to rādīs pēc
        <strong>?lang=lv</strong>, <strong>?lang=en</strong> vai <strong>?lang=ru</strong>.
      </div>

      <form method="POST">

        <div class="language-block">
          <div class="language-title">Latviešu valoda</div>

          <label>LV virsraksts</label>
          <input name="title_lv" value="{title_lv}">

          <label>LV teksts</label>
          <textarea class="rich-editor" id="content_lv" name="content_lv">{content_lv}</textarea>
        </div>

        <div class="language-block">
          <div class="language-title">English</div>

          <label>EN title</label>
          <input name="title_en" value="{title_en}">

          <label>EN content</label>
          <textarea class="rich-editor" id="content_en" name="content_en">{content_en}</textarea>
        </div>

        <div class="language-block">
          <div class="language-title">Русский</div>

          <label>RU заголовок</label>
          <input name="title_ru" value="{title_ru}">

          <label>RU текст</label>
          <textarea class="rich-editor" id="content_ru" name="content_ru">{content_ru}</textarea>
        </div>

        <div class="actions">
          <button type="submit">
            Saglabāt
          </button>

          <a class="button secondary" href="/ylff-control/pages">
            Atpakaļ
          </a>

          <a class="button public" href="/{slug}" target="_blank">
            Skatīt publiski
          </a>
        </div>

      </form>
    </div>

  </div>

  <script src="https://cdn.ckeditor.com/ckeditor5/41.4.2/classic/ckeditor.js"></script>

  <script>
    const editorConfig = {{
      toolbar: [
        "heading",
        "|",
        "bold",
        "italic",
        "link",
        "bulletedList",
        "numberedList",
        "|",
        "blockQuote",
        "insertTable",
        "undo",
        "redo"
      ]
    }};

    document
      .querySelectorAll(".rich-editor")
      .forEach(function(element) {{
        ClassicEditor
          .create(element, editorConfig)
          .catch(function(error) {{
            console.error(error);
          }});
      }});
  </script>
</body>
</html>
"""
