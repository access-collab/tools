from typing import Any, Callable, Generic, TypeVar

from pycountry import countries
from app.core.models import PlatformMapping, PlatformMappingComplex

A = TypeVar("A")
B = TypeVar("B")


class Operator(Generic[A, B]):
    name: str
    func: Callable[A, B]
    inputs: A

    def __init__(self, src: A, operation: str) -> None:
        self.name = operation
        if operation == "join-space":
            self.func = lambda x: " ".join(x)
            self.inputs = src
        elif operation == "no-op":
            self.func = lambda x: x
            self.inputs = src

        elif operation == "make-iso":
            self.func = lambda x: countries.get(name=x).alpha_3
            self.inputs = src
        else:
            raise NotImplementedError(f"Operation {operation} not implemented yet.")

    def _validate_args(self, args: dict[str, A]):
        if isinstance(args, dict):
            missing = [i for i in self.inputs if i not in args.keys()]
            if len(missing):
                raise TypeError(f"Missing argument(s) {missing} for {self.name}")

    def __repr__(self) -> str:
        args = (
            ", ".join(self.inputs.keys())
            if isinstance(self.inputs, dict)
            else self.inputs
        )
        return f"{self.name}({args})"

    @property
    def arguments(self) -> list[str]:
        if isinstance(self.inputs, dict):
            return self.inputs.keys()
        elif isinstance(self.inputs, str):
            return [self.inputs]
        else:
            return self.inputs

    def apply(self, inputs: dict[str, Any] | A) -> Any:
        self._validate_args(inputs)
        if isinstance(inputs, dict):
            return self.func([v for k, v in inputs.items()])
        else:
            return self.func(inputs)


def hydrate_operator(operator: PlatformMapping):
    if isinstance(operator, str):
        return Operator[str, str](operator, "no-op")
    elif isinstance(operator, PlatformMappingComplex):
        if isinstance(operator.src, list):
            return Operator[list[str], str](operator.src, operator.operation)
            ...
        elif isinstance(operator.src, str):
            return Operator[str, str](operator.src, operator.operation)
            ...
        else:
            raise TypeError(f"unknown operator {operator}")

    else:
        raise TypeError(f"unknown operator {operator}")
