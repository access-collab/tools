<script lang="ts">
  import type { PageProps } from "./$types";

  import { enhance } from "$app/forms";
  import Question from "$lib/Question.svelte";
    import ResultViewer from "$lib/ResultViewer.svelte";
  let { data, form }: PageProps = $props();
</script>

<h1>VLOPSE selection: {data.vlopses}</h1>
<form method="POST" use:enhance>
  {#each data.questions as question}
    <Question
      id={question.id}
      text={question.text}
      type={question.type}
      help_text={question.help_text}
      options={question.options}
      value={question.value}
      validation={form?.validation_errors?.find((item) => {
        return item.question_id == question.id;
      })?.description}
    />
  {/each}
  <button>Submit</button>
</form>
{#if form?.success}
  <h1 style:color="green">Result</h1>
  <ResultViewer results={form.by_vlopse}/>
{:else}
  <p style:color="red">No Success</p>
{/if}
{#if form?.transformation_errors}
  <h3>Transformation Errors</h3>
  {#each Object.entries(form.transformation_errors) as [key, errors]}
    <h4>Vlopse Question {key}</h4>
    {#each errors as { type, message }}
      {message}
    {/each}
  {/each}
{/if}
