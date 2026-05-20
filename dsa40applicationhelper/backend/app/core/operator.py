from abc import ABC, abstractmethod
from datetime import datetime

from pycountry import countries
from typing_extensions import override

from app.core.models import PlatformMapping

Inputs = str | list[str] | None


class OperatorExecutionError(Exception):
    def __init__(self, message: str, inputs: Inputs) -> None:
        if isinstance(inputs, list):
            list_inputs = inputs
        else:
            list_inputs = [inputs]
        super().__init__({"message": message, "inputs": list_inputs})


class AbstractOperator(ABC):
    @abstractmethod
    def _apply(self, inputs: Inputs) -> str: ...

    def apply(self, inputs: Inputs):
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


class JoinParagraphOperator(AbstractOperator):
    """Join multiple text answers into one platform field (e.g. combined research description)."""

    @override
    def _apply(self, inputs: Inputs):
        if not isinstance(inputs, list):
            raise TypeError("Expected a list of text values")
        parts = [part.strip() for part in inputs if part and str(part).strip()]
        if not parts:
            raise ValueError("No text values to combine")
        return "\n\n".join(parts)


class JoinDateRangeOperator(AbstractOperator):
    """Format two dates as a single access timeframe string (free-form platform fields)."""

    @override
    def _apply(self, inputs: Inputs):
        if not isinstance(inputs, list) or len(inputs) != 2:
            raise TypeError("Expected exactly two date values")
        start, end = (str(v).strip() for v in inputs)
        if not start or not end:
            raise ValueError("Both start and end dates are required")
        return f"{start} to {end}"


def _parse_date(value: str) -> datetime:
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {value}")


def _duration_bucket(days: int) -> str:
    if days <= 1:
        return "24 hours"
    if days <= 7:
        return "1 - 7 days"
    if days <= 28:
        return "1 - 4 weeks"
    if days <= 90:
        return "30 - 90 days"
    if days <= 365:
        return "3 - 12 months"
    return ">12 months"


class MakeDurationOperator(AbstractOperator):
    """Map a storage/access date range to a duration bucket (e.g. YouTube Y19)."""

    @override
    def _apply(self, inputs: Inputs):
        if not isinstance(inputs, list) or len(inputs) != 2:
            raise TypeError("Expected exactly two date values")
        start = _parse_date(str(inputs[0]))
        end = _parse_date(str(inputs[1]))
        if end < start:
            raise ValueError("End date must not be before start date")
        days = (end - start).days
        return _duration_bucket(days)


class MakeReportOperator(AbstractOperator):
    """Alias for joining narrative sections (summary + systemic risk, etc.)."""

    def __init__(self) -> None:
        self._join = JoinParagraphOperator()

    @override
    def _apply(self, inputs: Inputs):
        return self._join._apply(inputs)


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
        case "join-paragraph":
            return JoinParagraphOperator()
        case "join-date-range":
            return JoinDateRangeOperator()
        case "make-duration":
            return MakeDurationOperator()
        case "make-report":
            return MakeReportOperator()
        case _:
            raise ValueError(f"Invalid operator description: {operator}")
