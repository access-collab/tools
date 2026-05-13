import type { PageLoad } from "./$types";
export const prerender = false;
export const ssr = false;
import {
  apiQuestionsApplicableQuestions,
  apiConditionGetConditions,
} from "@api";

const loadConditions = async (vlopses: string[]) => {
  const call = await apiConditionGetConditions({
    query: { vlopse: vlopses },
  });
  const res = call.response;

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return call.data;
};

export const load: PageLoad = async ({ url }) => {
  const vlopses = url.searchParams.getAll("vlopses");

  const call = await apiQuestionsApplicableQuestions({
    query: { vlopse: vlopses },
  });
  const res = call.response;

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  let questions = call.data?.map((e) => e && { validation: null, ...e }) ?? [];
  let conditions = await loadConditions(vlopses);
  return { questions: questions, conditions: conditions };
};
