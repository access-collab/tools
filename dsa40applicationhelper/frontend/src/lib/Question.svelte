<script lang="ts">
  import type { InputType, DsaQuestion } from "@api/types.gen";
  import Select from "$lib/Select.svelte";
  import { Input } from "./components/ui/input";

  type Props = {
    id: string;
    text: string;
    required: boolean;
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
    required,
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

  function parseMultiValue(raw: string): string[] {
    return raw
      .split(/;\s*/)
      .map((part) => part.trim())
      .filter(Boolean);
  }

  function toggleMultiOption(option: string, checked: boolean) {
    const current = parseMultiValue(value);
    const next = checked
      ? current.includes(option)
        ? current
        : [...current, option]
      : current.filter((item) => item !== option);
    value = next.join("; ");
  }

  const validationErrors = $derived(
    Array.isArray(validation) ? validation : validation ? [validation] : [],
  );
  const hidden = $derived(!required && !visible);
</script>

{#if !hidden}
  <fieldset class="py-5">
    <legend class="font-heading text-base font-bold leading-snug text-foreground">
      {text}
      <span
        class="ml-1.5 text-xs font-normal uppercase tracking-wide {required
          ? 'text-primary'
          : 'text-muted-foreground'}"
      >
        {required ? "Required" : "Optional"}
      </span>
    </legend>

    {#if help_text}
      <p class="mt-1.5 text-sm leading-relaxed text-muted-foreground">{help_text}</p>
    {/if}

    <div class="mt-3 max-w-lg">
      {#if input_type === "text"}
        <Input {id} name={id} type="text" bind:value class="w-full" />
      {:else if input_type === "file_upload"}
        <Input {id} name={id} type="file" class="w-full max-w-md" />
      {:else if input_type === "date_select"}
        <Input {id} name={id} type="text" bind:value class="w-full" placeholder="YYYY-MM-DD" />
      {:else if input_type === "selection"}
        <Select {id} bind:value options={selectOptions} />
      {:else if input_type === "multi_select"}
        {#if selectOptions.length > 0}
          <div class="flex flex-col gap-2.5 rounded-lg border border-border bg-muted/30 p-3">
            {#each selectOptions as opt (opt)}
              <label class="flex cursor-pointer items-center gap-2.5 text-sm">
                <input
                  type="checkbox"
                  name={id}
                  value={opt}
                  checked={parseMultiValue(value).includes(opt)}
                  onchange={(e) => toggleMultiOption(opt, e.currentTarget.checked)}
                  class="size-4 accent-primary"
                />
                {opt}
              </label>
            {/each}
          </div>
        {:else}
          <textarea
            {id}
            name={id}
            bind:value
            rows="3"
            placeholder="Enter keywords or topics, separated by semicolons"
            class="border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex min-h-[80px] w-full rounded-md border px-3 py-2 text-sm focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none"
          ></textarea>
        {/if}
      {:else if input_type === "iso-3166-1"}
        <Input
          {id}
          name={id}
          type="text"
          placeholder="Country name"
          bind:value
          class="w-full"
        />
      {/if}
    </div>

    {#if validationErrors.length > 0}
      <ul class="mt-2 space-y-0.5" role="alert">
        {#each validationErrors as err}
          <li class="text-sm text-destructive">{err}</li>
        {/each}
      </ul>
    {/if}
  </fieldset>
{/if}
