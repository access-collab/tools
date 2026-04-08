import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "./openapi.json",
  output: "src/api",

  plugins: [
    {
      name: "@hey-api/sdk",
      validator: true,
    },
    {
      name: "zod",
    },
    {
      name: "@hey-api/schemas",
      type: "json",
    },
  ],
});
