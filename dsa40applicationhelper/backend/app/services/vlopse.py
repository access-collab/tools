from pathlib import Path
from app.services.mapping import (
    CustomStuffs,
    get_custom_stuffs_for,
    write_custom_stuffs_for,
)

_DATA_DIR = Path(__file__).parent.parent / "data"


class VlopseExistsException(BaseException):
    pass


class VlopseDoesNotExistException(BaseException):
    pass


class VlopseConfigService:
    def add(self, name):
        current = self.get(name)
        if current:
            raise VlopseExistsException()
        stuff = {"mappings": {}, "conditions": []}
        write_custom_stuffs_for(name, stuff)

    def get(self, name):
        try:
            return get_custom_stuffs_for(name)
        except FileNotFoundError:
            return None

    def get_all(self):
        return [p.stem for p in _DATA_DIR.glob("*.json")]

    def delete(self, name):
        path = [p for p in _DATA_DIR.glob("*json") if p.stem == name]

        if not len(path):
            raise VlopseDoesNotExistException()
        else:
            path[0].unlink()

    def rename(self, old_name: str, new_name: str):
        current = self.get(old_name)
        if current is None:
            raise VlopseDoesNotExistException()
        new = self.get(new_name)
        if new:
            raise VlopseExistsException()
        self.delete(old_name)
        self.add(new_name)
        self.update(new_name, current)

    def update(self, name, value: CustomStuffs):
        if self.get(name) is None:
            raise VlopseDoesNotExistException()
        write_custom_stuffs_for(name, value)
