import { FetchClient } from "../fetch/fetch-client";

const SERVER_URL = process.env.SERVER_URL as string;

export const api = new FetchClient({
  baseUrl: SERVER_URL,
  headers: {},
  params: {},
});

