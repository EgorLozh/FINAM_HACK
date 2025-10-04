// Тикеры
export interface TickerSelectorProps {
  selectedTickers: string[];
  onTickersChange: (tickers: string[]) => void;
}

// DateRangePicker
export interface DateRangePickerProps {
  dateRange: { from: Date | undefined; to: Date | undefined };
  onDateRangeChange: (range: {
    from: Date | undefined;
    to: Date | undefined;
  }) => void;
  news?: NewsItem[];
}

// AIChat
export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface AIChatProps {
  dateRange: { from: Date | undefined; to: Date | undefined };
  selectedTickers: string[];
}

// Новости
export interface NewsItem {
  headline: string;
  hotness: string;
  why_now: string;
  entities: string;
  sources: string;
  timeline: string;
  draft: string;
}