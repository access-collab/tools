<script lang="ts">
  import type { InputType } from "@api";
  import Select from "$lib/Select.svelte";

  type Props = {
    id: string;
    text: string;
    input_type: InputType;
    help_text?: string | null;
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
  {#if help_text}
    {help_text}
  {/if}
  {#if validation}
    <p style:color="red">Err: {validation}</p>
  {/if}
  <hr />
</div>
