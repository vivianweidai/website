import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeMathjax from 'rehype-mathjax/svg';

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
  // Math is typeset at BUILD time into inline SVG PATHS. $...$ inline, $$...$$
  // display. Safe to enable globally -- no report contains a bare $ that could
  // be mistaken for a delimiter (checked across all 11 before switching it on).
  //
  // ⚠️ SVG output, not KaTeX and not MathJax's CHTML. Both of those position
  // glyphs using metrics that only hold if their own web fonts load, and when a
  // font 404s the browser substitutes a serif whose metrics are different --
  // fraction bars then cut through the letters instead of sitting above them.
  // KaTeX hit exactly that here: Vite inlines an imported stylesheet into a
  // <style> tag in dev, which re-bases its relative url(fonts/...) against the
  // PAGE url, so every font missed. SVG paths carry their own outlines, need no
  // font file, and cannot fail that way in dev or in the build.
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeMathjax],
  },
});
