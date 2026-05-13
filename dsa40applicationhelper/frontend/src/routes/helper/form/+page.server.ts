import { fail } from "@sveltejs/kit";
import type { Actions } from "./$types";
import { apiTransformTransformAnswers, apiValidateValidateAnswers } from "@api";
import { apiQuestionsApplicableQuestions } from "@api";
import type { DsaQuestion } from "@api";
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";
const validate = async ({ answers, vlopses }) => {
  const call = await apiValidateValidateAnswers({
    baseUrl: "http://localhost:5173",
    body: { answers: answers },
    query: { vlopse: vlopses },
  });
  const res = call.response;

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  let { ok, errors, kind } = call.data;
  if (ok) {
    return { ok: true, errors: [] };
  }

  let err =
    kind == "validation"
      ? {
          validation_errors: Object.entries(errors).map(([key, value]) => ({
            question_id: key,
            description: value,
          })),
        }
      : { transformation_errors: errors };

  return { ok: false, ...err };
};
const transform = async ({ answers, vlopses }) => {
  const call = await apiTransformTransformAnswers({
    baseUrl: "http://localhost:5173",
    body: { answers: answers },
    query: { vlopse: vlopses },
  });
  const res = call.response;

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  let by_vlopse = call.data.by_vlopse;
  return { ok: true, by_vlopse };
};
export const actions = {
  default: async ({ url, cookies, request, fetch }) => {
    // TODO log the user in
    const vlopses = url.searchParams.getAll("vlopses");
    const data = await request.formData();
    const uploadDir = "/tmp/dsa_uploads";
    await mkdir(uploadDir, { recursive: true });
    const answers = await Promise.all(
      [...data.entries()].map(async ([key, value]) => {
        if (value instanceof File) {
          if (value.size > 0) {
            const filename = `${Date.now()}_${value.name}`;
            await writeFile(
              join(uploadDir, filename),
              Buffer.from(await value.arrayBuffer()),
            );
            return { question_id: key, value: join(uploadDir, filename) };
          }
          return { question_id: key, value: "" };
        }
        return { question_id: key, value: value as string };
      }),
    );

    var { ok, ...rest } = await validate({ answers, vlopses });
    if (!ok) {
      console.log("error validating DSA answers.");
      console.log(rest);
      return fail(400, { ...rest });
    }

    var { ok, by_vlopse } = await transform({ answers, vlopses });
    if (!ok) {
      console.log("error transforming to VLOPSE questions.");
      return fail(400, { errors: by_vlopse });
    }

    return { success: true, by_vlopse };

    // if (!email) {
    // 	return fail(400, { email, missing: true });
    // }
  },
} satisfies Actions;
