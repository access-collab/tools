<script lang="ts">
  import { onMount } from "svelte";
  import { apiVlopseGetVlopse } from "@api";
  import { Button } from "$lib/components/ui/button/index.js";
  import { goto } from "$app/navigation";

  let vlopses: string[] = $state([]);
  let error: string | null = null;

  let selected = $state([]);

  onMount(async () => {
    try {
      const call = await apiVlopseGetVlopse({
        baseUrl: "http://localhost:5173",
      });
      const response = call.response;

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      vlopses = call.data;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  });
  function submit(vlopse: string) {
    goto(`/admin/${vlopse}`);
  }
</script>

<svelte:head>
  <title>DSA40 Application Helper</title>
</svelte:head>

<main>
  <h1>VLOPSE selection</h1>
  <p>select Vlopse to edit</p>

  <section>
    {#if vlopses}
      {#each vlopses as vlopse}
        <Button onclick={() => submit(vlopse)}>
          {vlopse}
        </Button>
      {/each}
    {/if}
  </section>
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
