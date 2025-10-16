import os, yaml
def load_config():
    here = os.path.dirname(__file__)
    cfg_path = os.path.join(here, "..", "config.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
