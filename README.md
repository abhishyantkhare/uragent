# Reading Room

A Vite app for a public, read-only collection of books and essays.

The app lives in `apps/reading-room`. It replaces the previous Next.js app.
Install dependencies at the repository root with `npm install`. Run it with
`npm run dev --workspace @uragent/reading-room` and build it with
`npm run build --workspace @uragent/reading-room`.

The app reads `public.reading_room_books_retry` from Supabase. Its schema and sample
collection are in `database/schema.sql`. The browser needs
`VITE_SUPABASE_URL` and `VITE_SUPABASE_PUBLISHABLE_KEY` at build time.
Use only a public/publishable key in browser configuration, never a service key.
The table deliberately permits public reads only. No user accounts or private
data are needed by this app.
