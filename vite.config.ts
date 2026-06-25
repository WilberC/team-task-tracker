import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "static",
    emptyOutDir: false,
    sourcemap: true,
    manifest: false,
    rollupOptions: {
      input: {
        main: "src/assets/ts/main.ts"
      },
      output: {
        entryFileNames: "js/[name].js",
        chunkFileNames: "js/[name].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            return "css/main.css";
          }
          return "assets/[name][extname]";
        }
      }
    }
  }
});
