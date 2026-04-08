import type { PageLoad } from "./$types";
export const prerender = false;
import { fail } from "@sveltejs/kit";
import type { Actions } from "./$types";
import { apiQuestionsApplicableQuestions } from "@api";
import type { UnifiedQuestion } from "@api";
export const load: PageLoad = async ({ url }) => {
  const vlopses = url.searchParams.getAll("vlopses");
  // vlopses is string[] → ["tiktok", "meta"]

  const call = await apiQuestionsApplicableQuestions({
    baseUrl: "http://localhost:5173",
    query: { vlopse: vlopses },
  });
  const res = call.response;

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  type ValidationResponse = { success: boolean; detail: String };
  type TrackedUnifiedQuestion = UnifiedQuestion & {
    validation: ValidationResponse | null;
  };
  let questions: TrackedUnifiedQuestion[] = call.data?.map(
    (e) => e && { validation: null, ...e },
  );
  return { questions: questions };
};
