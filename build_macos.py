"""Build and validate a macOS application, then zip it with links intact."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    if sys.platform != "darwin":
        raise SystemExit("Mac-Apps müssen auf macOS erstellt werden, z. B. mit GitHub Actions.")
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-arch", choices=("arm64", "x86_64"), required=True)
    args = parser.parse_args()
    arch = platform.machine()
    if arch != args.expected_arch:
        raise SystemExit("Unexpected Python architecture: " + arch)
    output = root / "dist" / "macos"
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        sys.executable, "-m", "PyInstaller", "--noconfirm",
        "--distpath", str(output), "--workpath", str(root / "build" / arch),
        str(root / "Escape-the-KUE.spec"),
    ], check=True, cwd=root)
    app = output / "Escape-the-KUE.app"
    executable = app / "Contents" / "MacOS" / "Escape-the-KUE"
    report = output / "self-test.json"
    report.unlink(missing_ok=True)
    subprocess.run([
        str(executable), "--self-test", "--self-test-output", str(report),
    ], check=True, cwd=tempfile.gettempdir(), timeout=180)
    results = json.loads(report.read_text(encoding="utf-8"))
    if not results.get("passed") or not results.get("frozen"):
        raise RuntimeError("The macOS application failed its packaging test.")
    subprocess.run(["codesign", "--verify", "--deep", "--strict", str(app)], check=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    label = "Apple-Silicon" if arch == "arm64" else "Intel"
    folder_name = "Escape-the-KUE-macOS-" + label
    with tempfile.TemporaryDirectory(prefix="escape-kue-package-") as temp:
        delivery = Path(temp) / folder_name
        delivery.mkdir()
        shutil.copytree(app, delivery / app.name, symlinks=True)
        shutil.copy2(root / "PLAY-MAC.txt", delivery / "BITTE-LESEN.txt")
        licenses = delivery / "licenses"
        licenses.mkdir()
        python_license = Path(sys.base_prefix) / "LICENSE.txt"
        if python_license.exists():
            shutil.copy2(python_license, licenses / "Python-LICENSE.txt")
        for package in ("pgzero", "numpy", "pyinstaller", "pygame"):
            dist = importlib.metadata.distribution(package)
            for relative in dist.files or []:
                path = str(relative).replace("\\", "/")
                if ".dist-info/" in path and any(word in relative.name.lower() for word in ("license", "copying")):
                    dest = licenses / package / path.split(".dist-info/", 1)[-1]
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dist.locate_file(relative), dest)
        pygame_dist = importlib.metadata.distribution("pygame")
        lgpl = pygame_dist.locate_file("pygame/docs/generated/LGPL.txt")
        if lgpl.exists():
            shutil.copy2(lgpl, licenses / "Pygame-LGPL.txt")
        metadata = {
            "source_commit": commit, "platform": "macOS", "architecture": arch,
            "build_macos": platform.mac_ver()[0], "python": platform.python_version(),
            "self_test": results, "developer_id_signed": False, "notarized": False,
        }
        (delivery / "build-info.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        archive = output / (folder_name + "-" + commit[:7] + ".zip")
        subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", str(delivery), str(archive)], check=True)
    # Test the extracted ZIP as well: the app contains essential symbolic links.
    with tempfile.TemporaryDirectory(prefix="escape-kue-extract-") as extracted:
        subprocess.run(["ditto", "-x", "-k", str(archive), extracted], check=True)
        extracted_app = Path(extracted) / folder_name / app.name
        subprocess.run(["codesign", "--verify", "--deep", "--strict", str(extracted_app)], check=True)
        extraction_report = Path(extracted) / "self-test-extracted.json"
        subprocess.run([
            str(extracted_app / "Contents" / "MacOS" / "Escape-the-KUE"),
            "--self-test", "--self-test-output", str(extraction_report),
        ], check=True, cwd=tempfile.gettempdir(), timeout=180)
        if not json.loads(extraction_report.read_text(encoding="utf-8")).get("passed"):
            raise RuntimeError("The extracted ZIP failed its packaging test.")
    with archive.open("rb") as archive_file:
        digest = hashlib.file_digest(archive_file, "sha256").hexdigest()
    archive.with_suffix(".zip.sha256").write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
    print("Mac-Download: " + str(archive))


if __name__ == "__main__":
    main()
