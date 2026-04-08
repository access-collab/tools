<script lang="ts">
  import type { PageProps } from "./$types";

  import { enhance } from "$app/forms";
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
{#if form?.success}
  <h1>Result</h1>
  {#each form.answers as vlopse}
    <h2>{vlopse.name}</h2>
    {#each vlopse.answers as answer}
      <p>{answer.question_id}</p>
      :
      {#if answer.errors}
        <p>{answer.errors[0].msg}</p>
      {:else}
        <p>{answer.value}</p>
      {/if}
    {/each}
  {/each}
{:else}
  No Success
{/if}
