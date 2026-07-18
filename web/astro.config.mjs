import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://vivianweidai.com',
  trailingSlash: 'always',
  // Tuck the build output inside pipeline/worker/ so it co-locates with
  // the Cloudflare Worker that serves it via the ASSETS binding.
  // Path is relative to this Astro root (web/); the worker is a sibling
  // under the repo root, hence ../pipeline.
  outDir: '../pipeline/worker/dist',
  build: {
    format: 'directory',
  },
  // Disable the dev toolbar's hover-source overlay (the "File display"
  // tooltip that appears over images and elements in dev mode). Only
  // affects local preview; production build is unaffected either way.
  devToolbar: {
    enabled: false,
  },
});
