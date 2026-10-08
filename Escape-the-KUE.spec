from pathlib import Path
import sys
from PyInstaller.utils.hooks import collect_data_files

root = Path(SPECPATH)
datas = [(str(root / folder), folder) for folder in ("images", "sounds", "fonts")]
datas += [(str(root / "Game.py"), ".")]
datas += collect_data_files("pgzero")

a = Analysis(
    [str(root / "launch_game.py")],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=["quiz", "Panorama", "Hotspot"],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "pandas", "scipy"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="Escape-the-KUE",
    debug=False,
    strip=False,
    upx=False,
    console=False,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="Escape-the-KUE")
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="Escape-the-KUE.app",
        bundle_identifier="ch.escape-the-kue.game",
        info_plist={"CFBundleDisplayName": "Escape the KUE", "NSHighResolutionCapable": True},
    )
