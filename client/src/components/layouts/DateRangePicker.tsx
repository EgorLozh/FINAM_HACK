"use client";

import { useState } from "react";
import { Calendar } from "@/components/ui/calendar";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover";
import { CalendarIcon, AlertCircleIcon, Flame, Clock, Users, ExternalLink, FileText } from "lucide-react";
import { format } from "date-fns";
import { ru } from "date-fns/locale";
import { cn } from "@/lib/utils";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { DateRangePickerProps, NewsItem } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import NewsModal from "@/components/modals/NewsModal";
import { getHotnessColor } from "@/utils/getHotnessColor";

export function DateRangePicker({
  dateRange,
  onDateRangeChange,
  news = [],
}: DateRangePickerProps) {
  const [showNews, setShowNews] = useState(false);
  const [selectedNewsItem, setSelectedNewsItem] = useState<NewsItem | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSelect = (range: any) => {
    if (range) {
      onDateRangeChange(range);
      if (range.from && range.to) {
        setShowNews(true);
      } else {
        setShowNews(false);
      }
    }
  };

  const handleNewsItemClick = (newsItem: NewsItem) => {
    setSelectedNewsItem(newsItem);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedNewsItem(null);
  };

  return (
    <div className="space-y-4">
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={cn(
              "w-full justify-start text-left font-normal transition-all duration-300",
              !dateRange.from && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {dateRange.from ? (
              dateRange.to ? (
                <>
                  {format(dateRange.from, "dd MMM yyyy", { locale: ru })} -{" "}
                  {format(dateRange.to, "dd MMM yyyy", { locale: ru })}
                </>
              ) : (
                format(dateRange.from, "dd MMM yyyy", { locale: ru })
              )
            ) : (
              <span>Выберите период</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="range"
            selected={dateRange}
            onSelect={handleSelect}
            numberOfMonths={2}
            locale={ru}
          />
        </PopoverContent>
      </Popover>

      {showNews && dateRange.from && dateRange.to && news.length > 0 && (
        <div className="space-y-4 animate-fade-in">
          <Alert className="bg-lava/10 border-lava">
            <AlertCircleIcon className="h-4 w-4 text-lava" />
            <AlertDescription className="text-foreground">
              <strong className="text-lava">Горячие новости за период:</strong> С{" "}
              {format(dateRange.from, "dd.MM.yyyy")} по{" "}
              {format(dateRange.to, "dd.MM.yyyy")} найдено {news.length} новостей
            </AlertDescription>
          </Alert>
          
          <div className="flex flex-col gap-3 h-[300px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
            {news.map((item, index) => (
              <Card
                key={index}
                className="cursor-pointer hover:shadow-lg transition-all duration-300 border-l-4 border-l-lava/50 hover:border-l-lava"
                onClick={() => handleNewsItemClick(item)}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-4">
                    <CardTitle className="text-base font-semibold text-foreground leading-tight line-clamp-2">
                      {item.headline}
                    </CardTitle>
                    <Badge
                      className={`${getHotnessColor(
                        item.hotness
                      )} font-medium`}
                    >
                      <Flame className="w-3 h-3 mr-1" />
                      {item.hotness}
                    </Badge>
                  </div>
                </CardHeader>
                
                <CardContent className="pt-0">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <ExternalLink className="w-4 h-4" />
                    <span className="truncate">{item.sources}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
      
      <NewsModal
        newsItem={selectedNewsItem}
        isOpen={isModalOpen}
        onClose={handleModalClose}
      />
    </div>
  );
}
