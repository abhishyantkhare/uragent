import test, { afterEach } from 'node:test';
import assert from 'node:assert/strict';
import handler from '../api/reading-insight.js';
const originalKey = process.env.READING_ROOM_AI_API_KEY;
const originalFetch = globalThis.fetch;
afterEach(() => {
  if (originalKey === undefined) delete process.env.READING_ROOM_AI_API_KEY;
  else process.env.READING_ROOM_AI_API_KEY = originalKey;
  globalThis.fetch = originalFetch;
});
test('reports the original provider credential requirement honestly', async () => {
  delete process.env.READING_ROOM_AI_API_KEY;
  const response = await handler.fetch(new Request('https://example.test/api/reading-insight', { method: 'POST' }));
  assert.equal(response.status, 503);
  assert.match((await response.json()).error, /READING_ROOM_AI_API_KEY/);
});
test('retains the original OpenAI integration without a fallback recommendation', async () => {
  process.env.READING_ROOM_AI_API_KEY = 'server-test-credential';
  globalThis.fetch = async (url, init) => {
    assert.equal(url, 'https://api.openai.com/v1/responses');
    assert.equal(init.headers.Authorization, 'Bearer server-test-credential');
    const body = JSON.parse(init.body);
    assert.equal(body.store, false);
    assert.match(body.input, /A Room of One/);
    return Response.json({ output: [{ content: [{ type: 'output_text', text: 'A provider response.' }] }] });
  };
  const response = await handler.fetch(new Request('https://example.test/api/reading-insight', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ titles: ["A Room of One's Own"] }),
  }));
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { text: 'A provider response.' });
});
