import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const briefings = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../dist/briefings' }),
  schema: z.object({
    schema_version: z.string().optional(),
    persona_id: z.string().optional(),
    persona_name: z.string().optional(),
    brief_type: z.string().optional(),
    brief_mode: z.string().optional(),
    upcoming_meeting_date: z.string().optional(),
    generated_date: z.string().optional(),
    has_agenda: z.boolean().optional(),
    last_cumulative_meeting: z.string().optional(),
    inter_meeting_evidence_count: z.number().optional(),
  }),
});

const personas = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../docs/persona/Active' }),
  schema: z.object({
    title: z.string(),
    artifact: z.string(),
    status: z.string().optional(),
    author: z.string().optional(),
    created: z.coerce.string().optional(),
    'last-updated': z.coerce.string().optional(),
    'linked-journeys': z.array(z.string()).optional(),
    'linked-stories': z.array(z.string()).optional(),
    'depends-on': z.array(z.string()).optional(),
  }),
});

export const collections = { briefings, personas };
