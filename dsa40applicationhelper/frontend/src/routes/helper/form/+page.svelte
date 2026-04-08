<script lang="ts">
  import type { PageProps } from "./$types";

  import Question from "$lib/Question.svelte";
  let { data, form }: PageProps = $props();
  let error = $state(undefined);
</script>

<h1>VLOPSE selection: {data.vlopses}</h1>
{#if error}
  {error}
{/if}
<form method="POST" use:enhance>
  {#each data.questions as question}
    <Question
      id={question.id}
      text={question.text_en}
      help_text={question.help_text}
      value={question.value}
      validation={question.validation}
    />
  {/each}
  <button>Submit</button>
</form>
