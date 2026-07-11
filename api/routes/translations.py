from flask import request


AVAILABLE_LANGS = [
    "lv",
    "en",
    "ru",
]


DEFAULT_LANG = "lv"


TRANSLATIONS = {
    "lv": {
        "home": "Sākumlapa",
        "objects": "Objekti",
        "activators": "Aktivizatori",
        "activity": "Activity",
        "awards": "Diplomi",
        "rules": "Nolikums",
        "about": "Par projektu",
        "map": "Karte",
        "search": "Meklēt",
        "clear": "Notīrīt",
        "open_map": "Atvērt karti",
        "footer_radio": "Amatieru radio — mūsu tilts uz dabu!",
        "objects_catalog": "YLFF objektu katalogs",
        "objects_catalog_help": "Meklē objektus pēc YLFF references, nosaukuma, lokatora vai statusa.",
        "found_objects": "Atrastie objekti",
        "reference": "YLFF",
        "name": "Nosaukums",
        "locator": "Lokators",
        "status": "Statuss",
        "not_found": "Ieraksti nav atrasti.",
    },
    "en": {
        "home": "Home",
        "objects": "Objects",
        "activators": "Activators",
        "activity": "Activity",
        "awards": "Awards",
        "rules": "Rules",
        "about": "About",
        "map": "Map",
        "search": "Search",
        "clear": "Clear",
        "open_map": "Open map",
        "footer_radio": "Amateur radio — our bridge to nature!",
        "objects_catalog": "YLFF object catalogue",
        "objects_catalog_help": "Search objects by YLFF reference, name, locator or status.",
        "found_objects": "Found objects",
        "reference": "YLFF",
        "name": "Name",
        "locator": "Locator",
        "status": "Status",
        "not_found": "No records found.",
    },
    "ru": {
        "home": "Главная",
        "objects": "Объекты",
        "activators": "Активаторы",
        "activity": "Activity",
        "awards": "Дипломы",
        "rules": "Положение",
        "about": "О проекте",
        "map": "Карта",
        "search": "Искать",
        "clear": "Очистить",
        "open_map": "Открыть карту",
        "footer_radio": "Любительское радио — наш мост к природе!",
        "objects_catalog": "Каталог объектов YLFF",
        "objects_catalog_help": "Поиск объектов по YLFF reference, названию, локатору или статусу.",
        "found_objects": "Найдено объектов",
        "reference": "YLFF",
        "name": "Название",
        "locator": "Локатор",
        "status": "Статус",
        "not_found": "Записи не найдены.",
    },
}


def get_lang():
    lang = request.args.get(
        "lang",
        DEFAULT_LANG,
    ).lower()

    if lang not in AVAILABLE_LANGS:
        return DEFAULT_LANG

    return lang


def tr(key):
    lang = get_lang()

    return TRANSLATIONS.get(
        lang,
        TRANSLATIONS[DEFAULT_LANG],
    ).get(
        key,
        TRANSLATIONS[DEFAULT_LANG].get(key, key),
    )


def lang_url(path):
    lang = get_lang()

    return f"{path}?lang={lang}"


def switch_lang_url(lang):
    path = request.path

    if lang not in AVAILABLE_LANGS:
        lang = DEFAULT_LANG

    return f"{path}?lang={lang}"
