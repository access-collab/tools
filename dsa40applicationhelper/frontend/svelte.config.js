import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    "alias": {
      "@api": "./src/api",
    },
    adapter: adapter({
      // Output to backend/static so FastAPI can serve it
      pages: "../backend/static",
      assets: "../backend/static",
      fallback: "index.html",
      precompress: false,
      strict: false,
    }),
  },
};

export default config;
