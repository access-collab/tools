from pathlib import Path

from pydantic import TypeAdapter

from app.models import UnifiedQuestion

someadapter = TypeAdapter(list[UnifiedQuestion])


_DATA_DIR = Path(__file__).parent.parent / "data"
