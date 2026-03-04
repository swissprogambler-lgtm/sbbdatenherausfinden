# Start hier (für Laien): SBB-Check auf „verkürzt geführt“

Du musst **nicht programmieren können**. Folge einfach diesen Schritten.

## Ziel
Du möchtest prüfen, ob bei einer konkreten Verbindung im SBB-Fahrplan der Hinweis
**„verkürzt geführt“** auftaucht – und das Ergebnis als Datei speichern.

---

## 1) Einmalig installieren

Öffne ein Terminal und gib nacheinander ein:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

Wenn das ohne Fehlermeldung durchläuft, ist alles bereit.

---

## 2) Fahrplan-Link vorbereiten

- Öffne den SBB-Onlinefahrplan im Browser.
- Suche z. B. Luzern → Zürich, Datum/Uhrzeit nach Wunsch.
- Kopiere die URL aus der Adresszeile.

---

## 3) Probe-Script starten

Im Projektordner ausführen:

```bash
python3 tools/probe_sbb_verkurzt.py --url "DEINE_KOPIERTE_URL"
```

Beispiel mit eigener Ausgabedatei:

```bash
python3 tools/probe_sbb_verkurzt.py --url "DEINE_KOPIERTE_URL" --out artifacts/luzern_zuerich_0935.json
```

---

## 4) Ergebnis verstehen

Nach dem Lauf findest du eine JSON-Datei, z. B.:

- `artifacts/sbb_probe.json`

Wichtiges Feld:

- `"match": true` → Hinweis wurde gefunden
- `"match": false` → Hinweis wurde nicht gefunden

Wenn `true`, wird zusätzlich ein Screenshot gespeichert (gleicher Dateiname, `.png`).

---

## 5) Typische Probleme

## Problem: `No module named playwright`
Dann war Schritt 1 nicht vollständig. Bitte nochmal:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

## Problem: Seite lädt nicht / Timeout
Dann blockt evtl. Netzwerk/Proxy oder die URL ist nicht mehr gültig.
Einfach mit einer frischen URL erneut probieren.

---

## 6) Was du als Nächstes machen kannst

Wenn das funktioniert, kann ich dir im nächsten Schritt ein **vollautomatisches Script** bauen,
das viele Verbindungen im Intervall prüft und alles in eine Tabelle (CSV/SQLite) sammelt.


---

## GitHub-Hilfe
Wenn du unsicher bist, wie du das auf GitHub hochlädst: siehe `GITHUB_SCHRITT_FUER_SCHRITT.md`.
