<script lang="ts">
  import { onMount } from "svelte";
  import { healthHealthCheck, type HealthResponse } from "@api";

  let health: HealthResponse | undefined = $state(undefined);
  let error: string | undefined = $state(undefined);

  onMount(async () => {
    try {
      const call = await healthHealthCheck({
        baseUrl: "http://localhost:5173",
      });
      const response = call.response;

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      health = call.data;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  });
</script>

<svelte:head>
  <title>DSA40 Application Helper</title>
</svelte:head>
<main>
  <h1>DSA40 Application Helper</h1>
  <p>Skeleton scaffold — both backend and frontend are running.</p>

  <section>
    <h2>Backend health</h2>
    {#if health}
      <p>
        API: <strong>{health.api}</strong> &nbsp;|&nbsp; DB:
        <strong>{health.db}</strong>
        DSA Questions: <strong>{health.dsa_status}</strong>
        Mappings: <strong>{health.mapping_status}</strong>
      </p>
      <p><a href="/helper">Start</a></p>
    {:else if error}
      <p style="color: red">Could not reach /health — {error}</p>
    {:else}
      <p>Checking…</p>
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
