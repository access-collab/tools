<script lang="ts">
  import type { InputType, DsaQuestion } from "@api/types.gen";
  import Select from "$lib/Select.svelte";
  import { Input } from "./components/ui/input";

  type Props = {
    id: string;
    text: string;
    visible: boolean;
    input_type: InputType;
    help_text?: string | null;
    config?: DsaQuestion["config"];
    options?: string[] | null;
    value?: string;
    validation?: string | string[] | null;
  };

  let {
    id,
    text,
    visible,
    input_type,
    help_text,
    config,
    options,
    value = $bindable(""),
    validation,
  }: Props = $props();

  const selectOptions = $derived(
    config?.type === "selection" ? config.options : (options ?? []),
  );

  const validationErrors = $derived(
    Array.isArray(validation) ? validation : validation ? [validation] : [],
  );
  const hidden = $derived(!required && !visible);
</script>

  <p class="font-medium">{text}</p>
<div class={hidden ? "hidden" : "py-3"}>
  {#if help_text}
    <p class="mt-1 text-sm text-muted-foreground">{help_text}</p>
  {/if}

  <div class="mt-2">
    {#if input_type === "text"}
      <Input {id} name={id} type="text" bind:value class="max-w-xs" />
    {:else if input_type === "file_upload"}
      <Input {id} name={id} type="text" bind:value class="max-w-xs" />
    {:else if input_type === "date_select"}
      <Input {id} name={id} type="text" bind:value class="max-w-xs" />
    {:else if input_type === "selection"}
      <Select {id} bind:value options={selectOptions} />
    {:else if input_type === "multi_select"}
      <div class="flex flex-col gap-2">
        {#each selectOptions as opt}
          <label class="flex items-center gap-2 text-sm">
            <input type="checkbox" name={id} value={opt} />
            {opt}
          </label>
        {/each}
      </div>
    {:else if input_type === "iso-3166-1"}
      <Input
        {id}
        name={id}
        type="text"
        placeholder="Country name"
        bind:value
        class="max-w-xs"
      />
    {/if}
  </div>

  {#if validationErrors.length > 0}
    <div class="mt-1">
      {#each validationErrors as err}
        <p class="text-sm text-destructive">{err}</p>
      {/each}
    </div>
  {/if}
  <hr class="mt-3" />
</div>

<style>
  .hidden {
    display: none;
  }
</style>
