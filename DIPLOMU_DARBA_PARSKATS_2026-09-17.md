# YLFF diplomu darba pārskats — 2026-09-17

## Apstiprinātā loģika
- Katrs ADIF žurnāls tiek saglabāts atsevišķi.
- Sistēma summē viena cilvēka QSO vienā YLFF objektā no visiem žurnāliem.
- Pie 100+ QSO objekts ir pilnībā aktivizēts.
- Komandas dalībniekam ieskaita pilnu QSO skaitu no žurnāliem, kuros viņš norādīts.
- Nepabeigtie objekti paliek sarakstā un kartē, bet aktivizatoru pakāpēs netiek ieskaitīti.
- Medniekam skaita unikālus objektus neatkarīgi no aktivizācijas statusa.
- Aktivizatoru Honor Roll ir 25+, mednieku Honor Roll ir 50+.

## Pašreizējais stāvoklis
- DiplomaRecord modelis ir izveidots un importēts, bet vēl netiek izmantots.
- call_search un ADIF augšupielāde jau rāda QSO un pilnu vai nepilnu statusu katram žurnālam.
- Vairāku žurnālu QSO summēšana vēl nav ieviesta.
- Honor Roll sliekšņi call_search.py izlaboti no 100 uz 25 un 50.
- PDF izveide un lejupielāde tiks veikta pēc atsevišķas instrukcijas.

## Nākamais darbs
- Ieviest kopējo QSO aprēķinu, nesapludinot žurnālu ierakstus.
- Meklēšanā parādīt objekta kopējo QSO, statusu un tekstu “Nav sasniegti 100 QSO”.
- Pārbaudīt YL3GBC individuālos un komandas objektus.
- Tikai pēc tam pieslēgt DiplomaRecord; PDF daļu atstāt vēlākam laikam.
