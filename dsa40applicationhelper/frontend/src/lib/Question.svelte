<script lang="ts">
  import type { InputType, DsaQuestion } from "@api/types.gen";
  import Select from "$lib/Select.svelte";
  import { Input } from "./components/ui/input";

  type Props = {
    id: string;
    text: string;
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
    input_type,
    help_text,
    value = $bindable(""),
    validation,
  }: Props = $props();
</script>

<div>
  <label>Q ({id}): {text} <input name={id} {id} type="text" bind:value /></label>
  <p class="font-medium">{text}</p>
  {#if help_text}
    {help_text}
  {/if}
  {#if validation}
    <p style:color="red">Err: {validation}</p>
    {#if input_type === "text"}
      <Input {id} name={id} type="text" bind:value class="max-w-xs" />
    {:else if input_type === "file_upload"}
      <Input {id} name={id} type="text" bind:value class="max-w-xs" />
    {:else if input_type === "date_select"}
      <Input {id} name={id} type="text" bind:value class="max-w-xs" />
    {:else if input_type === "iso-3166-1"}
      <Input
        {id}
        name={id}
        type="text"
        placeholder="Country name"
        bind:value
      />
    {/if}
  {/if}
  <hr />
</div>
