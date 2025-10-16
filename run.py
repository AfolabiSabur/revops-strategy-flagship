import os, subprocess, sys

CMDS = [
    [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
    ["pip", "install", "-r", "requirements.txt"],
    [sys.executable, "src/generate_data.py"],
    [sys.executable, "src/build_charts.py"],
    [sys.executable, "src/scenario_planner.py"],
    [sys.executable, "src/deal_model.py"],
    [sys.executable, "src/portfolio_optimizer.py"],
    [sys.executable, "src/compute_kpis.py"],
    [sys.executable, "src/build_sparklines.py"],
    [sys.executable, "src/build_report.py"],
    [sys.executable, "src/build_zip.py"],
]

def run(cmd):
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for c in CMDS:
        run(c)
    print("Done. Open exports/flagship_strategy_report.html")
