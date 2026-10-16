export default {
  async fetch(request) {
    const apiKey = process.env.READING_ROOM_AI_API_KEY;
    if (!apiKey) {
      return Response.json(
        { error: 'The reading guide needs its original provider credential: READING_ROOM_AI_API_KEY.' },
        { status: 503 },
      );
    }
    if (request.method !== 'POST') {
      return Response.json({ error: 'Use POST to request a reading recommendation.' }, { status: 405 });
    }
    const { titles } = await request.json();
    if (!Array.isArray(titles) || titles.length === 0 || titles.some((title) => typeof title !== 'string')) {
      return Response.json({ error: 'Provide at least one book title.' }, { status: 400 });
    }
    const upstream = await fetch('https://api.openai.com/v1/responses', {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: process.env.READING_ROOM_AI_MODEL || 'gpt-4.1-mini',
        input: `Recommend one book for a quiet evening from this list and explain why in two sentences:\n${titles.join('\n')}`,
        max_output_tokens: 160,
        store: false,
      }),
    });
    if (!upstream.ok) {
      return Response.json({ error: 'The reading guide provider rejected the request. Check its credential and account.' }, { status: 502 });
    }
    const result = await upstream.json();
    const text = result.output.flatMap((item) => item.content || [])
      .filter((item) => item.type === 'output_text').map((item) => item.text).join('\n');
    return Response.json({ text });
  },
};
