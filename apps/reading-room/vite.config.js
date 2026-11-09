import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  // Map only public database settings. Never expose a server/service credential.
  const endpoint = env.READING_ROOM_PUBLIC_DATABASE_ENDPOINT || env.NEXT_PUBLIC_SUPABASE_URL || '';
  const browserKey = env.READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY || env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
  return {
    envPrefix: 'READING_ROOM_PUBLIC_',
    define: {
      'import.meta.env.READING_ROOM_PUBLIC_DATABASE_ENDPOINT': JSON.stringify(endpoint),
      'import.meta.env.READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY': JSON.stringify(browserKey),
    },
  };
});
