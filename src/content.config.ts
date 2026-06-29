import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({
    pattern: '*/index.md',
    base: './public/research/projects',
    // Preserve the original folder name as the id so URLs like
    // /research/projects/20260420%20UV-Vis%20Spectroscopy/ keep working.
    generateId: ({ entry }) => entry.replace(/\/index\.md$/, ''),
  }),
  schema: z.object({
    project: z.string(),
    // H1 prose title. Rendered by Project.astro at the top of the page.
    title: z.string(),
    // Full science name(s) — drives chip rendering at the title row,
    // tech-page reverse-lookup, and project-page subject coloring.
    sciences: z.array(z.string()),
    // Render the Mi cat icon next to the H1 — only the two cat-themed
    // projects use this.
    mi: z.boolean().optional(),
    data_photos: z.array(z.string()).optional(),
    // Techs this project uses. Drives the auto-populated Projects section
    // on each /research/technology/<sci>/<Tech>/ page.
    tech: z.array(z.string()).optional(),
  }),
});

// Per-tech template pages — one folder per tech under
// public/research/technology/<science_slug>/<Tech Name>/index.md.
// id is "<science_slug>/<tech>" so the dynamic route can split params.
const tech = defineCollection({
  loader: glob({
    pattern: '*/*/index.md',
    base: './public/research/technology',
    generateId: ({ entry }) => entry.replace(/\/index\.md$/, ''),
  }),
  schema: z.object({
    tech: z.string(),
    science: z.string(),
    science_slug: z.string(),
    topic: z.string(),
    category: z.string(),
    hero: z.string().optional(),
    // Optional CSS object-position override for cropping the hero (e.g.
    // "top" or "center 30%"). Default is center; tweak when the
    // important part of the image is off-center.
    hero_position: z.string().optional(),
    // Physical Toys this Tech maps to. Rendered as the Toys list on the
    // tech page; if the tech is referenced by any project, each toy's
    // name links to the most recent matching project.
    toys: z.array(z.object({
      name: z.string(),
      description: z.string(),
      // Optional link target for the toy name (e.g. the project that used it).
      url: z.string().optional(),
      // Optional per-toy image (relative to the tech folder). When a tech
      // bundles several toys, hovering a toy in the list swaps the hero to
      // this image.
      image: z.string().optional(),
    })).optional(),
  }),
});

export const collections = { projects, tech };
