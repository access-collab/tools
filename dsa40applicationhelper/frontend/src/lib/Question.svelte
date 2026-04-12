<script lang="ts">
  import type { InputType } from "@api";
  import Select from "$lib/Select.svelte";

  type Props = {
    id: string;
    text: string;
    type: InputType;
    help_text: string | null | undefined;
    value: string;
    validation: string | undefined;
  };

  let {
    id,
    text,
    type,
    help_text,
    value = $bindable(),
    validation,
    // TODO: Ensure the default value is null not '' in FORM
  }: Props = $props();
</script>

<div>
  <label>Q: {text} <input name={id} {id} type="text" bind:value /></label>
  {#if help_text}
    {help_text}
  {/if}
  {#if validation}
    <p style:color="red">Err: {validation}</p>
  {/if}
  <hr />
</div>
