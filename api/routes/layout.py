from routes.translations import (
    get_lang,
    lang_url,
    switch_lang_url,
    tr,
)


def ylff_navbar():
    return f"""
    <div class="ylff-topbar">
      <a class="ylff-brand" href="{lang_url('/')}">
        <img
          class="ylff-brand-logo"
          src="/static/img/logo-small.png"
          alt="YLFF logo"
        >

        <div>
          <div class="ylff-brand-title">YLFF</div>
          <div class="ylff-brand-subtitle">LATVIAN FLORA & FAUNA</div>
        </div>
      </a>

      <div class="ylff-nav">
        <a href="{lang_url('/')}">{tr('home')}</a>
        <a href="{lang_url('/objects-list')}">{tr('objects')}</a>
        <a href="{lang_url('/top-operators')}">{tr('activators')}</a>
        <a href="{lang_url('/activity')}">{tr('activity')}</a>
        <a href="{lang_url('/awards')}">{tr('awards')}</a>
        <a href="{lang_url('/rules')}">{tr('rules')}</a>
        <a href="{lang_url('/about')}">{tr('about')}</a>
        <a href="{lang_url('/map')}">{tr('map')}</a>

              <!--
      AI mistake record, 2026-06-20:
      The public layout language flag patch removed the visible LV/EN/RU text labels,
      but left the old vertical separator character "|" after the flag group.
      The mistake was in this original source file: api/routes/layout.py.
      Correct fix: remove the leftover literal "|" from the public language switch area.
      -->
<span class="ylff-lang-switch">
        <a href="{switch_lang_url('lv')}" title="Latviski">
          <img src="https://flagcdn.com/w40/lv.png" alt="LV">
        </a>
        <a href="{switch_lang_url('en')}" title="English">
          <img src="https://flagcdn.com/w40/gb.png" alt="EN">
        </a>
        <a href="{switch_lang_url('ru')}" title="Русский">
          <img src="https://flagcdn.com/w40/ru.png" alt="RU">
        </a>
      </span>
      </div>
    </div>
    """


def ylff_footer():
    return f"""
    <div class="ylff-footer">
      <div>🌐 www.ylff.id.lv</div>
      <div>📧 info@ylff.id.lv</div>
      <div>📡 {tr('footer_radio')}</div>
      <div>© 2026 YLFF Programma</div>
    </div>
    """


def ylff_page(title, content):
    lang = get_lang()

    return f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="/static/ylff-theme.css">
</head>

<body>
  <div class="ylff-page">
    {ylff_navbar()}

    <main class="ylff-container">
      {content}
    </main>

    {ylff_footer()}
  </div>
</body>
</html>
"""
