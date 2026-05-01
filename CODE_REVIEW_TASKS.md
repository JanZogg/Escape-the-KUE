# Vorschläge aus dem Code-Review

Diese Aufgaben sind als **kleine, klar abgrenzbare Tickets** formuliert.

## 1) Aufgabe: Tippfehler korrigieren
**Titel:** Variablenkommentar sprachlich korrigieren (`Variabeln` → `Variablen`)

**Problem:** In `Game.py` steht der Kommentar `#Variabeln`.

**Akzeptanzkriterien:**
- Der Kommentar ist auf `# Variablen` korrigiert.
- Es gibt keine weiteren offensichtlichen Tippfehler in den Abschnittsüberschriften (`# Listen`, `# Actors`, `# Programm`).

---

## 2) Aufgabe: Programmierfehler beheben
**Titel:** Zimmerwechsel nur bei tatsächlichem Tastendruck auslösen und Indexfehler verhindern

**Problem:** In `on_key_down` wird `if keyboard.P:` verwendet. Das prüft den globalen Tastaturzustand statt den übergebenen `key`. Außerdem kann `aktueller_zimmer_index` über das Ende der Liste laufen und dann bei `zimmer[...]` abstürzen.

**Vorschlag zur Umsetzung:**
- `if keyboard.P:` auf `if key == keys.P:` umstellen.
- Den Zimmerindex beim Erhöhen robust behandeln (z. B. zyklisch per Modulo oder mit Boundary-Check).

**Akzeptanzkriterien:**
- Ein Zimmerwechsel passiert nur beim P-Keydown-Event.
- Wiederholtes Drücken von `P` verursacht keinen `IndexError`.

---

## 3) Aufgabe: Kommentar-/Doku-Unstimmigkeit bereinigen
**Titel:** Unpräzisen ChatGPT-Kommentar durch technische Erklärung ersetzen

**Problem:** Der Inline-Kommentar `#ChatGPT hat mir die Formel %= gegeben` erklärt nicht, **warum** die Zeile notwendig ist.

**Vorschlag zur Umsetzung:**
- Kommentar ersetzen durch eine fachliche Erklärung, z. B. dass `offset_x` per Modulo auf die Hintergrundbreite normalisiert wird, damit endloses Scrollen möglich bleibt.

**Akzeptanzkriterien:**
- Kommentar beschreibt Zweck und Effekt der Logik.
- Kein tool-/personenbezogener Kommentar mehr im Produktionscode.

---

## 4) Aufgabe: Test verbessern
**Titel:** Minimale Regressionstests für Eingabelogik und Scrolling einführen

**Problem:** Es gibt aktuell keine automatisierten Tests.

**Vorschlag zur Umsetzung:**
- Logik aus `update`/`on_key_down` in testbare Hilfsfunktionen auslagern (reine Python-Funktionen).
- Pytest-Tests ergänzen für:
  1. Startzustand → Spielstart mit `S`.
  2. Zimmerwechsel mit `P` inklusive Wrap-around.
  3. `offset_x`-Normalisierung mit Modulo bei positiver und negativer Bewegung.

**Akzeptanzkriterien:**
- Testdatei ist vorhanden und läuft mit `pytest` lokal grün.
- Mindestens ein Test deckt den früheren Indexfehler beim Zimmerwechsel ab.
