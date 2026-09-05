import type { ApiResponse } from "../types/api";
const base = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, "");
export const apiConnected = Boolean(base);
export async function ask(message: string, signal?: AbortSignal): Promise<ApiResponse> {
  if (!base) throw new Error("API_NOT_CONNECTED");
  const r = await fetch(`${base}/v1/orchestrate`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({message}), signal });
  if (!r.ok) throw new Error(`API_ERROR_${r.status}`);
  const data = await r.json();
  if (!data || typeof data.status !== "string" || typeof data.answer !== "string" || !Array.isArray(data.citations) || typeof data.trace_id !== "string") throw new Error("NON_CANONICAL_RESPONSE");
  return data as ApiResponse;
}