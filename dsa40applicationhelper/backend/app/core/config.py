from pathlib import Path

from pydantic import BaseModel

from app.models import Condition

from .models import PlatformMapping

_VLOPSE_CONFIG_DIR = Path(__file__).parent.parent / "data" / "vlopses"


class VLOPSEConfiguration(BaseModel):
    mappings: dict[str, PlatformMapping]
    conditions: dict[str, Condition]


def _load_json(filename: str) -> VLOPSEConfiguration:
    path = _VLOPSE_CONFIG_DIR / filename
    data = path.read_text()
    return VLOPSEConfiguration.model_validate_json(data)


def _write_json(filename: str, value: VLOPSEConfiguration):
    path = _VLOPSE_CONFIG_DIR / filename
    serialized = value.model_dump_json()
    with open(path, "w") as f:
        f.write(serialized)


def get_vlopse_configuration_for(platform_name: str) -> VLOPSEConfiguration:
    return _load_json(f"{platform_name}.json")


def write_vlopse_configuration_for(platform_name: str, config: VLOPSEConfiguration):
    return _write_json(f"{platform_name}.json", config)
