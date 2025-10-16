import os, zipfile
ROOT = os.path.abspath(".")
EXPORTS_DIR = os.path.join(ROOT, "exports")
ZIP_PATH = os.path.join(EXPORTS_DIR, "strategy_flagship_pack.zip")
SKIP_DIRS = {".venv", ".git", "__pycache__", ".vscode", "node_modules"}
SKIP_FILES = {os.path.basename(ZIP_PATH)}
def add_dir(z, root):
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f in SKIP_FILES: continue
            src = os.path.join(folder, f)
            if os.path.abspath(src) == os.path.abspath(ZIP_PATH): continue
            z.write(src, arcname=os.path.relpath(src, root))
os.makedirs(EXPORTS_DIR, exist_ok=True)
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as z: add_dir(z, ROOT)
print(f"ZIP built at {ZIP_PATH}")
