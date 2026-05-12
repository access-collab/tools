<script lang="ts">
  import type { PageProps } from "./$types";

  let { data, params }: PageProps = $props();
  let { questions } = data;
</script>

<svelte:head>
  <title>DSA40 Application Helper</title>
</svelte:head>

<main>
  <h1>{params.vlopse}</h1>
  {#if questions}
    {#each questions as question}
      <div class="question">
        <h2>
          {question.id}
        </h2>
        {question.text}
        {question.input_type}
      </div>
    {/each}
  {/if}
</main>

<style>
  main {
    font-family: system-ui, sans-serif;
    max-width: 600px;
    margin: 4rem auto;
    padding: 0 1rem;
  }
  h1 {
    font-size: 1.75rem;
  }
</style>
