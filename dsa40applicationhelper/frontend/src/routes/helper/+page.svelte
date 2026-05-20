<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button/index.js";

  import { goto } from "$app/navigation";
  import { apiVlopseGetVlopse, type PlatformInformation } from "@api";

  let vlopses: { id: string; info: PlatformInformation }[] = $state([]);
  let error: string | null = $state(null);

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
  <title>Select platforms · DSA40 Application Helper</title>
</svelte:head>

<div class="mx-auto max-w-2xl px-4 py-10 sm:px-6 sm:py-12">
  <h1 class="font-heading text-2xl font-bold tracking-tight sm:text-3xl">
    Select platforms
  </h1>
  <p class="mt-2 text-muted-foreground">
    Choose the VLOPSE platforms you are applying to. You will answer shared questions once.
  </p>

  {#if error}
    <p class="mt-6 rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
      {error}
    </p>
  {:else if vlopses.length === 0}
    <p class="mt-6 text-sm text-muted-foreground">Loading platforms…</p>
  {:else}
    <ul class="mt-8 flex flex-col gap-3" role="list">
      {#each vlopses as vlopse (vlopse.id)}
        <li>
          <label
            class="flex cursor-pointer items-start gap-4 rounded-xl border border-border bg-card p-4 shadow-sm transition-[border-color,box-shadow] hover:border-primary/30 hover:shadow-md has-[:checked]:border-primary has-[:checked]:ring-2 has-[:checked]:ring-primary/20"
          >
            <input
              type="checkbox"
              name="vlopses"
              value={vlopse.id}
              bind:group={selected}
              class="mt-1 size-4 shrink-0 accent-primary"
            />
            <span class="min-w-0 flex-1 font-heading font-bold">{vlopse.info.name}</span>
          </label>
        </li>
      {/each}
    </ul>

    <div class="mt-8 flex flex-wrap items-center gap-4">
      <Button onclick={submit} disabled={selected.length === 0} size="lg">
        Continue to form
      </Button>
      {#if selected.length > 0}
        <p class="text-sm text-muted-foreground">
          {selected.length} platform{selected.length === 1 ? "" : "s"} selected
        </p>
      {/if}
    </div>
  {/if}
</div>
