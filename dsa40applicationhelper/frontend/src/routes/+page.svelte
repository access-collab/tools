<script lang="ts">
  import { onMount } from "svelte";
  import { healthHealthCheck, type HealthResponse } from "@api";

  let health: HealthResponse | null = null;
  let error: string | null = null;

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
        Status: <strong>{health.status}</strong> &nbsp;|&nbsp; DB:
        <strong>{health.db}</strong>
      </p>
      <p><a href="/helper">Start</a></p>
    {:else if error}
      <p style="color: red">Could not reach /health — {error}</p>
    {:else}
      <p>Checking…</p>
    {/if}
  </section>
</main>

