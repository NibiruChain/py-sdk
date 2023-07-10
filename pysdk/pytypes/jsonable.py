import abc
import copy
import json
from datetime import datetime
from typing import Any, Mapping


def to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "to_jsonable"):
        return obj.to_jsonable()
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, datetime):
        return to_iso(obj)
    if isinstance(obj, list):
        return [to_jsonable(g) for g in obj]
    if isinstance(obj, dict):
        return dict_to_jsonable(obj)
    if isinstance(obj, datetime):
        return to_iso(obj)
    return obj


def to_iso(dt: datetime) -> str:
    return (
        dt.isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
        .replace(".000Z", "Z")
    )


def dict_to_jsonable(d: Mapping) -> Mapping[str, "Jsonable"]:
    """Recursively calls to_jsonable on each element of the given map."""
    return {key: to_jsonable(val) for key, val in d.items()}


class Jsonable(abc.ABC):
    def to_jsonable(self) -> Any:
        """Returns a JSON-serializable Python representation"""
        return dict_to_jsonable(copy.deepcopy(self.__dict__))

    def to_json_str(self) -> str:
        return json.dumps(
            obj=self.to_jsonable(),
            sort_keys=True,
            separators=(",", ":"),
        )

    def __repr__(self):
        return self.to_json_str()

    def __str__(self):
        return self.to_json_str()
