<script lang="ts">
  import type { PageProps } from "./$types";

  import { enhance } from "$app/forms";
  import Question from "$lib/Question.svelte";
  import ResultViewer from "$lib/ResultViewer.svelte";
  import { Button } from "$lib/components/ui/button/index.js";
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

  const visibleCount = $derived(
    data.questions.filter((q) => visibility[q.id] || q.required).length,
  );
</script>

<svelte:head>
  <title>Application form · DSA40 Application Helper</title>
</svelte:head>

<div class="mx-auto max-w-3xl px-4 py-10 sm:px-6 sm:py-12">
  <div class="mb-8">
    <a href="/helper" class="text-sm text-muted-foreground transition-colors hover:text-foreground">
      ← Change platforms
    </a>
    <h1 class="font-heading mt-3 text-2xl font-bold tracking-tight sm:text-3xl">
      Application form
    </h1>
    <p class="mt-2 text-muted-foreground">
      {visibleCount} question{visibleCount === 1 ? "" : "s"} for your selection. Optional fields
      appear when relevant.
    </p>
  </div>

  <form
    method="POST"
    use:enhance
    enctype="multipart/form-data"
    class="rounded-xl border border-border bg-card shadow-sm"
  >
    <div class="divide-y divide-border px-4 sm:px-6">
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
    </div>

    <div class="flex items-center justify-end gap-4 border-t border-border bg-muted/30 px-4 py-4 sm:px-6">
      <Button type="submit" size="lg">Submit answers</Button>
    </div>
  </form>

  {#if form?.success}
    <section class="mt-12">
      <h2 class="font-heading text-xl font-bold text-primary">Platform answers</h2>
      <p class="mt-1 text-sm text-muted-foreground">
        Copy each answer into the corresponding platform form.
      </p>
      <div class="mt-6">
        <ResultViewer results={form.by_vlopse} />
      </div>
    </section>
  {:else if form?.validation_errors?.length}
    <p class="mt-6 rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
      Please fix the highlighted fields and submit again.
    </p>
  {/if}

  {#if form?.transformation_errors}
    <section class="mt-8 rounded-xl border border-destructive/30 bg-destructive/5 p-4">
      <h3 class="font-heading font-bold text-destructive">Transformation errors</h3>
      <ul class="mt-3 space-y-4 text-sm">
        {#each Object.entries(form.transformation_errors) as [key, errors]}
          <li>
            <p class="font-medium">VLOPSE question {key}</p>
            <ul class="mt-1 list-inside list-disc text-muted-foreground">
              {#each errors as { message }}
                <li>{message}</li>
              {/each}
            </ul>
          </li>
        {/each}
      </ul>
    </section>
  {/if}
</div>
