<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button/index.js";

  import { goto } from "$app/navigation";
  import { apiVlopseGetVlopse, type PlatformInformation } from "@api";

  let vlopses: { id: string; info: PlatformInformation }[] = $state([]);
  let error: string | null = null;

  let selected = $state([]);

  onMount(async () => {
    try {
      const call = await apiVlopseGetVlopse();
      const response = call.response;

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      vlopses = call.data ?? [];
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  });

  function submit() {
    if (selected.length === 0) return;
    const params = new URLSearchParams(selected.map((v) => ["vlopses", v]));
    goto(`/helper/form?${params}`);
  }
</script>

<svelte:head>
  <title>DSA40 Application Helper</title>
</svelte:head>

<main>
  <h1>VLOPSE selection</h1>
  <p>Select the vlopses you want to apply to</p>

  <section>
    {#if vlopses}
      {#each vlopses as vlopse (vlopse.id)}
        <div>
          {vlopse.info.name}
          {vlopse.info.platform_information}
          {vlopse.info.account_required}
          {vlopse.info.application_link}
        </div>
        <label
          ><input
            type="checkbox"
            name="vlopses"
            value={vlopse.id}
            bind:group={selected}
          />
        </label>
      {/each}

      <Button onclick={submit} disabled={selected.length === 0}>
        Continue
      </Button>
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
