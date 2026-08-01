import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({
    pattern: '*/index.md',
    base: './public/projects',
    // Preserve the original folder name as the id so URLs like
    // /projects/20260420%20UV-Vis%20Spectroscopy/ keep working.
    generateId: ({ entry }) => entry.replace(/\/index\.md$/, ''),
  }),
  schema: z.object({
    project: z.string(),
    // H1 prose title. Rendered by Project.astro at the top of the page.
    title: z.string(),
    // Full science name(s) — drives chip rendering at the title row and
    // project-page subject coloring.
    sciences: z.array(z.string()),
    // Vestigial. Every project still declares this and the schema still
    // accepts it, but the tech pages it fed were deleted 2026-07-30 and
    // nothing reads it now. Kept optional so the 7 existing files validate.
    tech: z.array(z.string()).optional(),
  }),
});


export const collections = { projects };
