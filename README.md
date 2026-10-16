# Reading Room

A Vite app for a public, read-only collection of books and essays.

The app lives in `apps/reading-room`. It replaces the previous Next.js app.
Install dependencies at the repository root with `npm install`. Run it with
`npm run dev --workspace @uragent/reading-room` and build it with
`npm run build --workspace @uragent/reading-room`.

The app reads `public.reading_room_books_retry` from Supabase. Its schema and sample
collection are in `database/schema.sql`. The browser needs
`READING_ROOM_PUBLIC_DATABASE_ENDPOINT` and
`READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY` at build time. Vite exposes only the
`READING_ROOM_PUBLIC_` prefix. `READING_ROOM_PUBLIC_COLLECTION_NAME` controls the
collection label.
Use only a public/publishable key in browser configuration, never a service key.
The table deliberately permits public reads only. No user accounts or private
data are needed by this app.

The reading guide uses an existing OpenAI account through the Vercel function
`api/reading-insight.js`. Its server-only `READING_ROOM_AI_API_KEY` is not stored
in this repository. Preserve that integration and use the original provider
credential. `READING_ROOM_AI_MODEL` is a non-secret model setting. Neither server
variable may be exposed through Vite's public prefix. The book-selection button
requires a successful provider response; a placeholder recommendation does not
provide this feature.
