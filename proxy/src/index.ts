/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.jsonc`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

// actually, Env code isn't required
export interface Env {
	Proxy: KVNamespace
}

export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
	  const url = new URL(request.url);

	  if (url.pathname==='/kv') {
		let value = await env.Proxy.get("meme");		
		return new Response(value, {
		  headers: { 'Content-Type': 'text/plain' }
		});
	  }

	  let sbs = await env.Proxy.get("sb");
	  if (sbs !== null) {
		sbs = JSON.parse(sbs);
	  } else {
		sbs = "msg:\"error\""; 
	  }
	  if (url.pathname === '/subscribe') {
		const token = url.searchParams.get('token');
		
		if (!token) {
		  return new Response('Token is required', { status: 400 });
		}
		let tokenValid = await env.Proxy.get(token);
		if (tokenValid === 'true') {
		  return new Response(JSON.stringify(sbs), {
			headers: { 'Content-Type': 'application/json' }
		  });
		} else {
		  return new Response('Invalid token', { status: 401 });
		}
	  }
  
	  // 对其他路径的请求，直接返回一个简单的响应
	  return new Response('Not Found', { status: 404 });
	}
  } satisfies ExportedHandler<Env>;
   
