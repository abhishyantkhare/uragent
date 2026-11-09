import test, { beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import configure from '../vite.config.js';

const keys = ['READING_ROOM_PUBLIC_DATABASE_ENDPOINT', 'READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY',
  'NEXT_PUBLIC_SUPABASE_URL', 'NEXT_PUBLIC_SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY',
  'READING_ROOM_AI_API_KEY'];
let saved;
beforeEach(() => { saved = Object.fromEntries(keys.map(k => [k, process.env[k]])); for (const k of keys) delete process.env[k]; });
afterEach(() => { for (const k of keys) { if (saved[k] === undefined) delete process.env[k]; else process.env[k] = saved[k]; } });
const read = () => configure({ mode: 'test' });

test('maps the managed public database variables into existing app names', () => {
  process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://example.supabase.co';
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'public-test-key';
  const config = read();
  assert.equal(JSON.parse(config.define['import.meta.env.READING_ROOM_PUBLIC_DATABASE_ENDPOINT']), process.env.NEXT_PUBLIC_SUPABASE_URL);
  assert.equal(JSON.parse(config.define['import.meta.env.READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY']), 'public-test-key');
});

test('preserves explicit original app settings', () => {
  process.env.READING_ROOM_PUBLIC_DATABASE_ENDPOINT = 'https://original.supabase.co';
  process.env.READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY = 'original-public-key';
  process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://fallback.supabase.co';
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'fallback-public-key';
  const config = read();
  assert.equal(JSON.parse(config.define['import.meta.env.READING_ROOM_PUBLIC_DATABASE_ENDPOINT']), 'https://original.supabase.co');
  assert.equal(JSON.parse(config.define['import.meta.env.READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY']), 'original-public-key');
});

test('does not expose server credentials or widen the public prefix', () => {
  process.env.SUPABASE_SERVICE_ROLE_KEY = 'SERVER_ONLY_TEST_MARKER';
  process.env.READING_ROOM_AI_API_KEY = 'AI_SERVER_ONLY_TEST_MARKER';
  const config = read();
  assert.equal(config.envPrefix, 'READING_ROOM_PUBLIC_');
  assert.equal(JSON.parse(config.define['import.meta.env.READING_ROOM_PUBLIC_DATABASE_BROWSER_KEY']), '');
  assert.ok(!JSON.stringify(config).includes('SERVER_ONLY_TEST_MARKER'));
});
