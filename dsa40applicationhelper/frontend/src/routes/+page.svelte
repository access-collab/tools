<script lang="ts">
  import { onMount } from "svelte";
  import { healthHealthCheck, type HealthResponse } from "@api";
  import { Button } from "$lib/components/ui/button/index.js";

  let health: HealthResponse | undefined = $state(undefined);
  let error: string | undefined = $state(undefined);

  onMount(async () => {
    try {
      const call = await healthHealthCheck();
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

<div class="mx-auto max-w-2xl px-4 py-12 sm:px-6 sm:py-16">
  <p class="text-sm font-medium uppercase tracking-wider text-primary">DSA Art. 40(12)</p>
  <h1 class="font-heading mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
    Application Helper
  </h1>
  <p class="mt-4 text-lg leading-relaxed text-muted-foreground">
    Answer cross-platform questions once, then get platform-specific answers for your VLOPSE
    access applications.
  </p>

  <section class="mt-10 rounded-xl border border-border bg-card p-6 shadow-sm">
    <h2 class="font-heading text-lg font-bold">System status</h2>

    {#if health}
      <dl class="mt-4 grid gap-3 text-sm sm:grid-cols-2">
        <div class="rounded-lg bg-muted/60 px-3 py-2">
          <dt class="text-muted-foreground">API</dt>
          <dd class="mt-0.5 font-medium capitalize">{health.api}</dd>
        </div>
        <div class="rounded-lg bg-muted/60 px-3 py-2">
          <dt class="text-muted-foreground">Database</dt>
          <dd class="mt-0.5 font-medium capitalize">{health.db}</dd>
        </div>
        <div class="rounded-lg bg-muted/60 px-3 py-2">
          <dt class="text-muted-foreground">DSA questions</dt>
          <dd class="mt-0.5 font-medium capitalize">{health.dsa_status}</dd>
        </div>
        <div class="rounded-lg bg-muted/60 px-3 py-2">
          <dt class="text-muted-foreground">Mappings</dt>
          <dd class="mt-0.5 font-medium capitalize">{health.mapping_status}</dd>
        </div>
      </dl>

      <div class="mt-8">
        <Button href="/helper" size="lg">Start application</Button>
      </div>
    {:else if error}
      <p class="mt-4 text-sm text-destructive">Could not reach the API — {error}</p>
    {:else}
      <p class="mt-4 text-sm text-muted-foreground">Checking backend…</p>
    {/if}
  </section>
</div>
