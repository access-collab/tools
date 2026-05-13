import { env } from "$env/dynamic/private";

export async function handle({ event, resolve }) {
  const { pathname } = event.url;
  if (pathname.startsWith("/api") || pathname === "/health") {
    const search = event.url.search;
    const target = `${env.BACKEND_URL ?? "http://localhost:8000"}${pathname}${search}`;
    const body = ["GET", "HEAD"].includes(event.request.method)
      ? undefined
      : event.request.body;
    return fetch(target, {
      method: event.request.method,
      headers: event.request.headers,
      body,
      // @ts-expect-error — Node fetch requires duplex for streamed request bodies
      duplex: "half",
    });
  }
  return resolve(event);
}
