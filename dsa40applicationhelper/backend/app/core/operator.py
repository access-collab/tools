from abc import ABC, abstractmethod

from pycountry import countries
from typing_extensions import override

from app.core.models import PlatformMapping

Inputs = str | list[str] | None


        else:
            return self.func(inputs)
class AbstractOperator(ABC):
    @abstractmethod
    def _apply(self, inputs: Inputs) -> str: ...

class MakeISOOperator(AbstractOperator):
    @override
    def _apply(self, inputs: Inputs):
        if inputs is None:
            raise TypeError("Cannot create ISO from None argument.")
        if isinstance(inputs, list):
            raise TypeError("Cannot create ISO from list argument.")
        result = countries.get(name=inputs)
        if not result:
            raise ValueError(f"Unknown country {inputs}")
        return result.alpha_3


class JoinOperator(AbstractOperator):
    delimiter: str

    def __init__(self, delimiter: str):
        self.delimiter = delimiter

    @override
    def _apply(self, inputs: Inputs):
        if inputs is None:
            raise TypeError("Cannot join None type")
        if isinstance(inputs, str):
            raise TypeError("Cannot join str type")
        return self.delimiter.join(inputs)


class NoopOperator(AbstractOperator):
    @override
    def _apply(self, inputs: Inputs):
        if isinstance(inputs, list):
            raise TypeError("Cannot transform lists")
        if inputs is None:
            raise TypeError("Cannot transform None")
        return inputs


def hydrate_operator(operator: PlatformMapping):
    # FIXME: No-Op is simply a mapping. So we don't really want this here? or it's more elegant, let's see
    if isinstance(operator, str):
        print(f"DEBUG no-op {operator}")

        return NoopOperator()
    match operator.operation:
        case "make-iso":
            return MakeISOOperator()
        case "join-space":
            return JoinOperator(" ")
        case "join-comma":
            return JoinOperator(", ")
        case _:
            raise ValueError(f"Invalid operator description: {operator}")
