// Cloudflare Worker — CORS proxy for Anthropic API
// Deployed at: https://anthropic-proxy.work-specious.workers.dev
//
// Handles the CORS preflight problem that blocks direct browser-to-Anthropic
// calls from GitHub Pages. The browser talks to this Worker; the Worker calls
// Anthropic server-to-server (no CORS restrictions); the Worker returns the
// response with Access-Control-Allow-Origin added.

export default {
  async fetch(request) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, x-api-key, anthropic-version, anthropic-dangerous-direct-browser-calls',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': request.headers.get('x-api-key') || '',
        'anthropic-version': request.headers.get('anthropic-version') || '2023-06-01',
      },
      body: request.body,
    });

    return new Response(response.body, {
      status: response.status,
      headers: { 'content-type': 'application/json', ...corsHeaders },
    });
  },
};
