<script lang="ts">
  import * as Select from "$lib/components/ui/select/index.ts";

  type Props = {
    id: string;
    value: string;
    options: string[];
  };

  let { id, value = $bindable(""), options }: Props = $props();
  const triggerContent = $derived(
    options.find((o) => o === value) ?? "Select an option",
  );
</script>

<Select.Root type="single" name={id} bind:value>
  <Select.Trigger class="w-[180px]">
    {triggerContent}
  </Select.Trigger>
  <Select.Content>
    <Select.Group>
      {#each options as opt}
        <Select.Item value={opt} label={opt}>
          {opt}
        </Select.Item>
      {/each}
    </Select.Group>
  </Select.Content>
</Select.Root>
