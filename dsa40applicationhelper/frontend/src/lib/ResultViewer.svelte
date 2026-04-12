<script lang="ts">
  import * as Tabs from "$lib/components/ui/tabs/index.ts";

  type Props = {
    results: string[];
  };

  let { results }: Props = $props();
  let tabs = $derived(results?.map((e) => e.name));
</script>

<div class="-mb-4 flex w-full max-w-sm flex-col gap-6">
  <Tabs.Root value={tabs[0]}>
    <Tabs.List>
      {#each tabs as tab}
        <Tabs.Trigger value={tab}>{tab}</Tabs.Trigger>
      {/each}
    </Tabs.List>
    {#each results as vlopse}
      <h2>{vlopse.name}</h2>
      <Tabs.Content value={vlopse.name}>
        {#each vlopse.answers as answer}
          <div class="grid gap-3">
            <p>{answer.question_id}</p><p>{answer.text}</p><p>{answer.value}</p>
          </div>
        {/each}
      </Tabs.Content>
    {/each}
  </Tabs.Root>
</div>
