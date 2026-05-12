<script lang="ts">
  import type { PageProps } from "./$types";

  import { enhance } from "$app/forms";
  import Question from "$lib/Question.svelte";
  import ResultViewer from "$lib/ResultViewer.svelte";
  import { isVisible, type FormValues } from "$lib/conditions";
  let { data, form }: PageProps = $props();

  let values = $state<FormValues>(
    Object.fromEntries(data.questions.map((q) => [q.id, ""])),
  );

  let visibility = $derived(
    Object.fromEntries(
      data.questions.map((q) => [
        q.id,
        isVisible(q.id, data.conditions, values),
      ]),
    ),
  );
</script>

<form method="POST" use:enhance enctype="multipart/form-data">
  {#each data.questions as question (question.id)}
    <Question
      id={question.id}
      text={question.text}
      required={question.required}
      visible={visibility[question.id]}
      bind:value={values[question.id]}
      input_type={question.input_type}
      help_text={question.help_text}
      config={question.config}
      options={question.options}
      validation={form?.validation_errors?.find((item) => {
        return item.question_id == question.id;
      })?.description}
    />
  {/each}
  <button>Submit</button>
</form>
{#if form?.success}
  <h1 style:color="green">Result</h1>
  <ResultViewer results={form.by_vlopse} />
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
