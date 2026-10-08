# Mac-Version erstellen

GitHub Actions erstellt zwei Downloads: Apple-Silicon und Intel.
Die ZIPs enthalten eine `.app`, Python, Pygame Zero und alle Spielressourcen.

## Mit GitHub

Wenn der Workflow in `main` übernommen wurde:

1. Im Repository auf **Actions** klicken.
2. **Mac-Spiel erstellen** auswählen.
3. **Run workflow** klicken, den gewünschten Spielstand auswählen und bestätigen.
4. Nach den beiden grünen Ergebnissen den abgeschlossenen Lauf öffnen.
5. Unter **Artifacts** die Dateien für Apple-Silicon und Intel herunterladen.
6. Die äußere GitHub-Artifact-ZIP entpacken. Darin liegt die eigentliche
   `Escape-the-KUE-macOS-...zip`, die als Datei am GitHub Release hochgeladen wird.

Der Workflow baut auch Änderungen in Pull Requests, damit die Mac-Version
vor der Übernahme geprüft werden kann. Er veröffentlicht keine Releases.
Normale Commits auf `main` erzeugen keinen automatischen Download.

## Prüfungen

Der Build prüft alle Bilder, Sounds und Schriftarten sowie Startbildschirm,
Intro, sechs Räume, Gegenstände, Rätselansichten und Endbildschirme.
Er prüft die lokale Signatur der `.app`, packt mit macOS `ditto` und testet
auch die App aus der wieder entpackten ZIP, damit symbolische Links und
Ausführungsrechte erhalten bleiben.

Die Tests verwenden virtuelle Bildschirm- und Audioausgabe. Vollbild,
echte Tonausgabe, Maus und Tastatur sowie das erste Öffnen eines Downloads
müssen zusätzlich auf einem echten Mac getestet werden.

## Direkt auf einem Mac

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-build.txt
.venv/bin/python build_macos.py --expected-arch arm64
```

Auf einem Intel-Mac lautet das letzte Argument `x86_64`.
Das Ergebnis liegt unter `dist/macos/`.

## Erstes Öffnen

Diese Ausgaben sind lokal ad hoc signiert, haben jedoch keine Developer-ID-
Signatur und sind nicht bei Apple notarisiert. macOS kann einen Download
deshalb zunächst blockieren. Eine Anleitung liegt in `PLAY-MAC.txt`.
Für einen Download ohne diese zusätzliche Freigabe wären eine Apple-
Entwicklersignatur und Notarisierung ein weiterer Schritt.

Referenzen:
- https://support.apple.com/de-ch/102445
- https://pyinstaller.org/en/stable/feature-notes.html
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
