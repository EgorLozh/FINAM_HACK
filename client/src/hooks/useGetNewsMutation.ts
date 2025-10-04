import { newsService } from "@/services/news.service";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";

export function useGetNewsMutation(setSampleNews: (data: any) => void) {
  const { mutate: getNews, isPending: isLoadingGetNews } = useMutation({
    mutationKey: ["get news"],
    mutationFn: ({ values }: { values: any }) => {
      return newsService.getNews(values);
    },
    onSuccess: (response: any) => {
      setSampleNews(response);
      toast.success("Новости успешно получены", {
        duration: 3000,
      });
    },
    onError: () => {
      toast.error("Новости не найдены :(", {
        duration: 3000,
      });
    },
  });

  return { getNews, isLoadingGetNews };
}
