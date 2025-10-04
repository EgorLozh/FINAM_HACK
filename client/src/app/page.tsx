"use client";

import { useEffect, useState } from "react";
import { DateRangePicker } from "@/components/layouts/DateRangePicker";
import { TickerSelector } from "@/components/layouts/TickerSelector";
import { AIChat } from "@/components/layouts/AiChat";
import { ThemeSwitcher } from "@/components/layouts/ThemeSwitcher";
import { Card } from "@/components/ui/card";
import { CalendarIcon, TrendingUpIcon, MessageSquareIcon } from "lucide-react";
import { NewsItem } from "@/types";
import { useGetNewsMutation } from "@/hooks/useGetNewsMutation";

export default function Home() {
  const [dateRange, setDateRange] = useState<{
    from: Date | undefined;
    to: Date | undefined;
  }>({
    from: undefined,
    to: undefined,
  });

  const [selectedTickers, setSelectedTickers] = useState<string[]>([]);
  const [sampleNews, setSampleNews] = useState<any>([]);
  
  const { getNews, isLoadingGetNews } = useGetNewsMutation(setSampleNews);

  useEffect(() => {
    if (!dateRange.from && !dateRange.to) return;
  
    getNews({
      values: {
        date_from: dateRange.from,
        date_to: dateRange.to,
      },
    });
  }, [dateRange.from, dateRange.to]);

  const handleTickersChange = (tickers: string[]) => {
    setSelectedTickers(tickers);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8 flex items-start justify-between animate-fade-in">
          <div>
            <h1 className="text-4xl font-bold text-foreground mb-2">
              NPE <span className="text-lava">FINAM HACKATON</span>
            </h1>
            <p className="text-muted-foreground text-lg">
              Выберите даты, тикеры и задайте вопросы AI-ассистенту
            </p>
          </div>
          <ThemeSwitcher />
        </div>

        {/* Main */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-6 flex flex-col justify-between">
            <Card className="p-6 animate-scale-in hover:shadow-lg transition-shadow duration-300">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-lava/10 rounded-lg">
                  <CalendarIcon className="w-5 h-5 text-lava" />
                </div>
                <h2 className="text-xl font-semibold">Выбор периода</h2>
              </div>
              <DateRangePicker
                dateRange={dateRange}
                onDateRangeChange={setDateRange}
                news={sampleNews}
              />
            </Card>

            <Card
              className="p-6 animate-scale-in hover:shadow-lg transition-shadow duration-300"
              style={{ animationDelay: "0.1s" }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-lava/10 rounded-lg">
                  <TrendingUpIcon className="w-5 h-5 text-lava" />
                </div>
                <h2 className="text-xl font-semibold">Выбор тикеров</h2>
              </div>
              <TickerSelector
                selectedTickers={selectedTickers}
                onTickersChange={handleTickersChange}
              />
            </Card>
          </div>

          <Card
            className="p-6 lg:row-span-2 animate-scale-in hover:shadow-lg transition-shadow duration-300"
            style={{ animationDelay: "0.2s" }}
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-lava/10 rounded-lg">
                <MessageSquareIcon className="w-5 h-5 text-lava" />
              </div>
              <h2 className="text-xl font-semibold">AI Ассистент</h2>
            </div>
            <AIChat
              dateRange={dateRange}
              selectedTickers={selectedTickers}
              sampleNews={sampleNews}
            />
          </Card>
        </div>
      </div>
    </div>
  );
}
