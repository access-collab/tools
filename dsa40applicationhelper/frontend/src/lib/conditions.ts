// conditions.ts
export type Operator = "eq" | "neq";

export interface Condition {
  question_id: string;
  operator: Operator;
  value: string;
}

export type ConditionsMap = Record<string, Condition[]>;
export type FormValues = Record<string, string | undefined>;

export function evaluateCondition(c: Condition, values: FormValues): boolean {
  const actual = values[c.question_id];
  switch (c.operator) {
    case "eq":
      return actual === c.value;
    case "neq":
      return actual !== c.value;
    default: {
      // exhaustiveness check — TS errors here if you add an operator and forget a case
      const _exhaustive: never = c.operator;
      return _exhaustive;
    }
  }
}

export function isVisible(
  questionId: string,
  conditions: ConditionsMap,
  values: FormValues,
): boolean {
  const rules = conditions[questionId];
  if (!rules || rules.length === 0) return false; // no rules = always visible
  return rules.every((r) => evaluateCondition(r, values));
}
