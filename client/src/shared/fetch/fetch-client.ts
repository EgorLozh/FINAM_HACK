import { FetchError } from "./fetch-error";
import { RequestOptions, TypeSearchParams } from "./fetch-types";

export class FetchClient {
  private baseUrl: string;
  public headers?: Record<string, string>;
  public params?: TypeSearchParams;
  public options?: RequestOptions;

  public constructor(init: {
    baseUrl: string;
    headers?: Record<string, string>;
    params?: TypeSearchParams;
    options?: RequestOptions;
  }) {
    this.baseUrl = init.baseUrl;
    this.headers = init.headers;
    this.params = init.params;
    this.options = init.options;
  }

  private createSearchParams(params: TypeSearchParams) {
    const searchParams = new URLSearchParams();

    for (const key in { ...this.params, ...params }) {
      if (Object.prototype.hasOwnProperty.call(params, key)) {
        const value = params[key];

        if (Array.isArray(value)) {
          value.forEach((currentValue) => {
            searchParams.append(key, currentValue?.toString() ?? "");
          });
        } else {
          searchParams.append(key, value?.toString() ?? "");
        }
      }
    }

    return `?${searchParams.toString()}`;
  }

  private async request<T>(
    endpoint: string,
    method: RequestInit["method"],
    options: RequestOptions = {}
  ) {
    let url = `${this.baseUrl}/${endpoint}`;

    if (options.params) {
      url += this.createSearchParams(options.params);
    }

    const config: RequestInit = {
      ...options,
      ...(!!this.options && { ...this.options }),
      method,
      headers: {
        ...(!!options?.headers && options.headers),
      },
    };

    const response: Response = await fetch(url, config);

    if (!response.ok) {
      const error = (await response.json()) as { message: string } | undefined;

      throw new FetchError(
        response.status,
        error?.message ?? response.statusText
      );
    }

    const headers: Record<string, string> = {};
    response.headers.forEach((value, key) => {
      headers[key] = value;
    });

    const text = await response.text();
    let data = null;
    if (text) {
      try {
        data = JSON.parse(text);
      } catch (e) {
        data = text;
      }
    }

    return {
      data,
      headers
    } as unknown as T;
  }

  public async get<T>(
    endpoint: string,
    options: Omit<RequestOptions, "body"> = {}
  ) {
    return this.request<T>(endpoint, "GET", options);
  }

  public async post<T>(
    endpoint: string,
    body: Record<string, string>,
    options: Omit<RequestOptions, "body"> = {}
  ) {
    return this.request<T>(endpoint, "POST", {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
      ...(!!body && { body: JSON.stringify(body) }),
    });
  }

}
