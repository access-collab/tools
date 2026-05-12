
import type { PageLoad } from "./$types";
export const prerender = false;
import { apiQuestionsApplicableQuestions, apiVlopseNameQuestionGetQuestions } from "@api";
import type { DsaQuestion } from "@api";
export const load: PageLoad = async ({params}) => {

  const call = await apiVlopseNameQuestionGetQuestions({
    baseUrl: "http://localhost:5173",
    path: {name: params.vlopse}
  });
  const res = call.response;

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  let questions = call.data;
  console.log(questions)
  return { questions: questions };
};
