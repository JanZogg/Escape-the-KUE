# Mac-Download für Apple-Chips erstellen

Diese Ausgabe unterstützt Macs mit M1 oder neuer. Intel-Macs sind ausgeschlossen.
Die ZIP enthält Escape-the-KUE.app, Python, Pygame Zero, alle Bilder, Sounds
und Schriftarten sowie eine kurze Startanleitung.

Nach der Übernahme des Workflows in main:
1. Im Repository Actions öffnen.
2. Mac-Spiel erstellen auswählen.
3. Run workflow anklicken und den gewünschten Spielstand auswählen.
4. Nach dem erfolgreichen Lauf unter Artifacts die Spiel-ZIP herunterladen.
5. Diese ZIP unverändert als Datei an ein GitHub Release anhängen.

Es wird nur die Apple-Silicon-Version auf macOS 14 (arm64) gebaut.
Der Workflow prüft auch Pull Requests. Er veröffentlicht keine Releases.
Ein Commit auf main allein erzeugt noch keine neue Spiel-ZIP.

Die erstellte App lädt alle Ressourcen und zeichnet wesentliche Spielansichten.
Danach werden die lokale Signatur und die aus der ZIP wieder entpackte App
geprüft. Die Tests verwenden virtuelle Bildschirm- und Audioausgabe.
Ein manueller Spieltest auf einem echten Mac ergänzt diese Prüfung
(Vollbild, Ton, Eingabe und erstes Öffnen eines heruntergeladenen Programms).

Direkt auf einem Mac mit Apple-Chip:
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-build.txt
.venv/bin/python build_macos.py --expected-arch arm64

Das Ergebnis liegt unter dist/macos/.

Die App ist ad hoc signiert. Sie hat keine Apple-Developer-ID-Signatur und
ist nicht bei Apple notarisiert. Deshalb kann macOS beim ersten Öffnen
zusätzliche Freigabe verlangen. Eine Anleitung liegt in der ZIP.

Referenzen:
https://support.apple.com/de-ch/102445
https://pyinstaller.org/en/stable/feature-notes.html
https://docs.github.com/en/actions/reference/runners/github-hosted-runners
