import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      // During dev, proxy API calls to the FastAPI backend
      "/health": "http://localhost:8000",
      "/api": "http://localhost:8000",
      "/admin": "http://localhost:8000",
    },
  },
});
