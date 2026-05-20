<script>
  let { children } = $props();
  import "../app.css";
</script>

<div class="flex min-h-svh flex-col">
  <header class="sticky top-0 z-10 border-b border-border/80 bg-card/90 backdrop-blur-sm">
    <div class="mx-auto flex max-w-4xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
      <a href="/" class="font-heading text-lg font-bold tracking-tight text-foreground sm:text-xl">
        DSA40 Application Helper
      </a>
      <nav class="flex items-center gap-4 text-sm">
        <a
          href="/helper"
          class="text-muted-foreground transition-colors hover:text-foreground"
        >
          Select platforms
        </a>
      </nav>
    </div>
  </header>

  <main class="flex-1">
    {@render children()}
  </main>

  <footer class="border-t border-border/80 py-6">
    <p class="text-center text-sm text-muted-foreground">
      DSA Art.&nbsp;40(12) researcher access forms
    </p>
  </footer>
</div>
