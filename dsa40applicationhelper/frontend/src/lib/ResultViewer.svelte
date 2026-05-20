<script lang="ts">
  import * as Tabs from "$lib/components/ui/tabs/index.ts";
  import { Separator } from "$lib/components/ui/separator/index.ts";
  import { Button } from "$lib/components/ui/button/index.ts";
  import { Checkmark, Clipboard } from "./components/icons/Icons.svelte";

  type Answer = {
    question_id: string;
    text: string;
    value: string;
  };

  type Result = {
    name: string;
    answers: Answer[];
  };

  type Props = {
    results: Result[];
  };

  let { results }: Props = $props();
  let tabs = $derived(results?.map((e) => e.name));

  let copiedId = $state<string | null>(null);

  async function copyToClipboard(value: string, uniqueId: string) {
    await navigator.clipboard.writeText(value);
    copiedId = uniqueId;
    setTimeout(() => {
      copiedId = null;
    }, 1500);
  }
</script>

<div class="flex w-full max-w-2xl flex-col gap-6">
  <Tabs.Root value={tabs[0]}>
    <Tabs.List variant="line">
      {#each tabs as tab (tab)}
        <Tabs.Trigger value={tab}>{tab}</Tabs.Trigger>
      {/each}
    </Tabs.List>

    {#each results as vlopse (vlopse.name)}
      <Tabs.Content value={vlopse.name}>
        {#each vlopse.answers as answer, i (answer.question_id)}
          {#if i > 0}
            <Separator />
          {/if}
          <div class="flex items-start justify-between gap-4 py-3">
            <div class="flex min-w-0 flex-col gap-2">
              <p class="text-xs text-muted-foreground">{answer.question_id}</p>
              <p class="font-heading text-base font-bold">{answer.text}</p>
              <p class="text-sm text-foreground/80">{answer.value}</p>
            </div>
            <Button
              variant="ghost"
              size="icon-sm"
              onclick={() =>
                copyToClipboard(
                  answer.value,
                  vlopse.name + ":" + answer.question_id,
                )}
              aria-label="Copy {answer.value}"
              class="mt-0.5 shrink-0"
            >
              {#if copiedId === vlopse.name + ":" + answer.question_id}
                {@render Clipboard()}
              {:else}
                {@render Checkmark()}
              {/if}
            </Button>
          </div>
        {/each}
      </Tabs.Content>
    {/each}
  </Tabs.Root>
</div>
