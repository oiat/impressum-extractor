# Impressum Extractor

Ein Tool zum Auffinden und Extrahieren von Impressumsdaten auf Webseiten mithilfe eines Web-Crawlers und eines LLMs (Google Gemini).

**Funktionen**
- **Extraktion:** Sucht nach Impressum-/Kontakt-Seiten und extrahiert strukturierte Angaben.
- **Crawling:** Lädt Seiten, bereinigt HTML und sammelt potenziell relevante Links.
- **LLM-Auswertung:** Nutzt einen Prompt und ein JSON-Schema, um Ergebnisse als valides JSON zurückzugeben.

**Voraussetzungen**
- Python 3.9+ empfohlen
- Abhängigkeiten in `requirements.txt`

**Installation**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Konfiguration**
- Standard-Konfiguration: `settings.toml`.
- Kopiere `example.settings.toml` nach `settings.toml` und fülle `gemini.api_key` mit deinem API-Key.
- Wichtige Einstellungen:
  - `gemini.model` — zu verwendendes LLM-Modell
  - `gemini.api_key` — API-Key für das LLM
  - `impressum.prompt_path` — Pfad zur Prompt-Vorlage (Standard: `prompts/prompt.txt`)
  - `impressum.scheme_path` — Pfad zum JSON-Schema (Standard: `schemas/scheme.json`)
  - `impressum.output_path` — Ausgabe-Datei (Standard: `result.json`)

**Nutzung**
- Einfache Ausführung für eine URL:
```bash
python main.py --url "https://example.com"
```
- Das Ergebnis wird in der Datei gespeichert, die in `settings.toml` unter `impressum.output_path` konfiguriert ist (Standard: `result.json`).

**Projektstruktur (wichtigste Dateien)**
- `main.py` — Einstiegspunkt, initialisiert den `ImpressumExtractor` und schreibt das Ergebnis.
- `services/impressum_extractor.py` — Logik zur Suche, Vorverarbeitung und LLM-Auswertung.
- `services/website_crawler.py` — HTTP-Requests und HTML-Bereinigung.
- `prompts/prompt.txt` — Prompt-Template für das LLM.
- `schemas/scheme.json` — Erwartetes JSON-Schema für die LLM-Ausgabe.
- `settings.toml` / `example.settings.toml` — Konfiguration.
- `requirements.txt` — benötigte Python-Pakete.

**Entwicklungshinweise**
- Prompt und Schema anpassen, wenn sich das Ausgabeformat ändern soll.
- Für Debugging: `settings.toml` log-level auf `DEBUG` setzen.

**Beispiel Ausgaben bei Standard nutzung**
- https://agi-akku.de
```json
{
  "company_name": "AGI Angela Gutzeit Industrievertretungen GmbH",
  "address": "Curslacker Deich 194a 21039 Hamburg Deutschland",
  "email": "verkauf@agi-akku.de",
  "phone": "04152 / 887690",
  "vat_id": "DE 118634419",
  "found": true,
  "notes": "Alle relevanten Impressumsdaten wurden erfolgreich aus dem Text extrahiert."
}
```
----
- https://shop.orf.at
```json
{
  "company_name": "ORF Marketing & Creation GmbH & Co KG",
  "address": "1136 Wien, Hugo-Portisch-Gasse 1",
  "email": "shop@orf.at",
  "phone": null,
  "vat_id": "ATU 66572924",
  "found": true,
  "notes": "Die Daten wurden erfolgreich aus dem Abschnitt 'Offenlegung und Informationen gem. § 25 MedienG, § 5 ECG und § 14 UGB' extrahiert. Eine Telefonnummer war im Text nicht explizit angegeben, lediglich E-Mail-Adressen für den Support."
}
```
---
- https://keycity.com/
```json
{
  "company_name": "E&R Software GmbH",
  "address": "Franz-Baumann-Weg 22/18, 6020 Innsbruck, Österreich",
  "email": "office@er-games.at",
  "phone": "+43 720 519517",
  "vat_id": "ATU72245368",
  "found": true,
  "notes": "Die Daten wurden aus dem Impressums-Abschnitt extrahiert. Es wird zusätzlich eine Support-E-Mail (office@keycity.com) und eine leicht abweichende Adresse im Footer (ohne Top-Nummer) erwähnt."
}
```
- https://mooris.de/
```json
{
  "company_name": "Mooris.de",
  "address": null,
  "email": "hallo@mooris.de",
  "phone": "+49 30 22011808",
  "vat_id": null,
  "found": true,
  "notes": "Ein Firmenname (Mooris.de), eine Telefonnummer und eine E-Mail-Adresse wurden im Text gefunden. Eine vollständige physische Adresse sowie eine Umsatzsteuer-Identifikationsnummer fehlen in diesem Website-Auszug. Der Text deutet darauf hin, dass das Unternehmen ursprünglich aus der Schweiz stammt, aber eine deutsche Support-Nummer nutzt."
}
```