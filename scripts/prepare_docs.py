import os, shutil
pairs = [
  ("charts/funnel.png", "docs/shot_funnel.png"),
  ("charts/cac_vs_ltv_by_segment.png", "docs/shot_cac_ltv.png"),
  ("charts/revenue_projection_scenarios.png", "docs/shot_scenarios.png"),
]
os.makedirs("docs", exist_ok=True)
for src, dst in pairs:
    if os.path.exists(src):
        shutil.copyfile(src, dst)
print("Docs images prepared.")
