import { fail } from "@sveltejs/kit";
import type { Actions } from "./$types";
import { apiTransformTransformAnswers } from "@api";
import { apiQuestionsApplicableQuestions } from "@api";
import type { UnifiedQuestion } from "@api";
export const actions = {
  default: async ({ url, cookies, request, fetch }) => {
    // TODO log the user in
    const vlopses = url.searchParams.getAll("vlopses");
    const data = await request.formData();

    console.log(data);

    // @router.post("/api/transform")
    // async def transform_answers(answers: AnswerRequest, vlopse: list[str] = Query(...)):
    //     response = {klops: [] for klops in vlopse}
    // for klops in vlopse:

    // import { applicableQuestionsApiQuestionsGet } from "../../../client/sdk.gen";
    const answers = [...data.entries()].map(([key, value]) => ({
      question_id: key,
      value: value,
    }));
    const call = await apiTransformTransformAnswers({
      baseUrl: "http://localhost:5173",
      body: { answers: answers },
      query: { vlopse: vlopses },
    });
    console.log(response);
    if (response.status != 200) {
      return fail(response.status, data);
      // return fail(400, { email, missing: true });
    }
    const res = call.response;

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    console.log(res);
    // const call = await healthCheckHealthGet({
    //   baseUrl: "http://localhost:5173",
    // });
    // const response = call.response;
    //
    // if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // health = call.data;
    // const call = await transformAnswersApiTransformPost({
    //   baseUrl: "http://localhost:5173",
    // });
    // const response = call.response;
    // const result = await response.json();
    // console.log(result)
    let validated = call.data.by_vlopse;

    return { success: true, answers: result };
    return { success: true, answers: validated };

    // if (!email) {
    // 	return fail(400, { email, missing: true });
    // }
  },
} satisfies Actions;
