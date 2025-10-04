import { api } from "@/shared/api";

class NewsService {
  public async getNews(body: any) {
    const response = await api.post<any>("generate/", body);
    return response;
  }

}

export const newsService = new NewsService();