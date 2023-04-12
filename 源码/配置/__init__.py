from dynaconf import Dynaconf
from pathlib import Path

基本目录 = Path(__file__).parent.parent.parent

配置文件列表 = [
    "config.yaml",
    "config.dev.yaml",
]

配置 = Dynaconf(envvar_prefix="ARIA2BOT", settings_files=配置文件列表, base_dir=基本目录)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
