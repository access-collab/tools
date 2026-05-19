from abc import ABC, abstractmethod

from pycountry import countries
from typing_extensions import override

from app.core.models import PlatformMapping

Inputs = str | list[str] | None


class OperatorExecutionError(Exception):
    """Raised when an operator cannot process its inputs.

    Wraps both ``TypeError`` (wrong input shape) and ``ValueError`` (invalid
    input value) so callers only need to handle one exception type. The
    ``inputs`` field preserves the original value(s) for error reporting.
    """

    def __init__(self, message: str, inputs: Inputs) -> None:
        if isinstance(inputs, list):
            list_inputs = inputs
        else:
            list_inputs = [inputs]
        super().__init__({"message": message, "inputs": list_inputs})


class AbstractOperator(ABC):
    @abstractmethod
    def _apply(self, inputs: Inputs) -> str:
        """Transform *inputs* into a single output string.

        Raise ``TypeError`` when the input shape is wrong (e.g. a list where a
        string is expected). Raise ``ValueError`` when the value itself is
        invalid (e.g. an unrecognised country name).
        """
        ...

    def apply(self, inputs: Inputs) -> str:
        """Public entry point; delegates to ``_apply`` with uniform error handling."""
        try:
            result = self._apply(inputs)
            return result
        except TypeError as e:
            message = e.args[0]
            raise OperatorExecutionError(message, inputs) from None

        except ValueError as e:
            message = e.args[0]
            raise OperatorExecutionError(message, inputs) from None


class MakeISOOperator(AbstractOperator):
    """Convert a country name string to its ISO 3166-1 alpha-3 code.

    Accepts a single string (e.g. ``"Germany"``), returns the three-letter code
    (``"DEU"``). Currently supports English names only.
    """

    @override
    def _apply(self, inputs: Inputs) -> str:
        if inputs is None:
            raise TypeError("Cannot create ISO from None argument.")
        if isinstance(inputs, list):
            raise TypeError("Cannot create ISO from list argument.")
        result = countries.get(name=inputs)
        if not result:
            raise ValueError(f"Unknown country {inputs}")
        return result.alpha_3


class JoinOperator(AbstractOperator):
    """Join a list of strings into one using a fixed delimiter.

    Accepts a ``list[str]`` (e.g. ``["Jane", "Doe"]``), returns the joined
    string (``"Jane Doe"`` for a space delimiter).
    """

    delimiter: str

    def __init__(self, delimiter: str):
        self.delimiter = delimiter

    @override
    def _apply(self, inputs: Inputs) -> str:
        if inputs is None:
            raise TypeError("Cannot join None type")
        if isinstance(inputs, str):
            raise TypeError("Cannot join str type")
        return self.delimiter.join(inputs)


class NoopOperator(AbstractOperator):
    """Pass a single string through unchanged.

    Used for direct field mappings that require no transformation.
    """

    @override
    def _apply(self, inputs: Inputs) -> str:
        if isinstance(inputs, list):
            raise TypeError("Cannot transform lists")
        if inputs is None:
            raise TypeError("Cannot transform None")
        return inputs


def hydrate_operator(operator: PlatformMapping) -> AbstractOperator:
    """Instantiate the correct operator for a VLOPSE mapping entry.

    *operator* is either a bare string (direct field mapping -> ``NoopOperator``)
    or a ``PlatformMappingComplex`` whose ``operation`` field selects the
    operator:

    - ``"make-iso"``:   ``MakeISOOperator``: country name -> ISO 3166-1 alpha-3
    - ``"join-space"``: ``JoinOperator(" ")``: list of strings joined by a space
    - ``"join-comma"``: ``JoinOperator(", ")``: list of strings joined by ``", "``

    Raises ``ValueError`` for unrecognised operation strings.
    """
    if isinstance(operator, str):
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
