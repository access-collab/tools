// conditions.ts
export type Operator = "eq" | "neq";

export interface Condition {
  question_id: string;
  operator: Operator;
  value: string;
}

/** OR of AND-groups: show when any inner group fully matches. */
export type ConditionRuleGroups = Condition[] | Condition[][];
export type ConditionsMap = Record<string, ConditionRuleGroups>;
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

function isAndGroup(group: Condition[], values: FormValues): boolean {
  return group.every((r) => evaluateCondition(r, values));
}

export function isVisible(
  questionId: string,
  conditions: ConditionsMap,
  values: FormValues,
): boolean {
  const rules = conditions[questionId];
  if (!rules || rules.length === 0) return true;
  if (Array.isArray(rules[0])) {
    return (rules as Condition[][]).some((group) => isAndGroup(group, values));
  }
  return isAndGroup(rules as Condition[], values);
}
