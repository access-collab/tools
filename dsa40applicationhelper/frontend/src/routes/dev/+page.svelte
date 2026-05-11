<script lang="ts">
  import Question from "$lib/Question.svelte";
  import { type DsaQuestion } from "@api/types.gen";
  // export type InputType = 'text' | 'file_upload' | 'date_select' | 'selection' | 'multi_select' | 'iso-3166-1';

  const question: DsaQuestion = {
    id: "test",
    text: "This is what I'm asking for: ",
    input_type: "text",
    visible: true,
  };
  const invalid: DsaQuestion = { validation: ["error"], ...question };
  const with_help_text: DsaQuestion = {
    help_text:
      "Please be very speicfic in how you answer this. Use your keyboard to type the input, ideally. If not you might be able to use your voice to text",
    ...question,
  };
  const file_upload: DsaQuestion = { ...question, input_type: "file_upload" };
  const selection: DsaQuestion = {
    ...question,
    input_type: "selection",
    config: { type: "selection", options: ["Apple", "Pear", "Banana"] },
  };
  const boolean: DsaQuestion = {
    ...question,
    input_type: "selection",
    config: { type: "selection", options: ["true", "false"] },
  };
</script>

<h2>Free Text</h2>
<Question {...question} />

<h2>With Help Text</h2>
<Question {...with_help_text} />

<h2>file_upload</h2>
<Question {...file_upload} />
<h2>selection</h2>
<Question {...selection} />

<h2>boolean</h2>
<Question {...boolean} />

<h2>Error during validation</h2>
<Question {...invalid} />
