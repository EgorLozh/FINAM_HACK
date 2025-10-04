"use client";

import { useState } from "react";
import { DateRangePicker } from "@/components/layouts/DateRangePicker";
import { TickerSelector } from "@/components/layouts/TickerSelector";
import { AIChat } from "@/components/layouts/AiChat";
import { ThemeSwitcher } from "@/components/layouts/ThemeSwitcher";
import { Card } from "@/components/ui/card";
import { CalendarIcon, TrendingUpIcon, MessageSquareIcon } from "lucide-react";
import { NewsItem } from "@/types";

export default function Home() {
  const [dateRange, setDateRange] = useState<{
    from: Date | undefined;
    to: Date | undefined;
  }>({
    from: undefined,
    to: undefined,
  });
  const [selectedTickers, setSelectedTickers] = useState<string[]>([]);

  // Тестовые данные новостей
  const sampleNews: NewsItem[] = [
    {
      headline: "Сбербанк объявил о рекордных дивидендах - акции выросли на 8%",
      hotness: "Критическая",
      why_now: "Совет директоров одобрил выплату дивидендов в размере 28 рублей на акцию, что на 40% больше прошлогодних выплат",
      entities: "SBER, Сбербанк, Греф, дивиденды, MOEX, ЦБ РФ",
      sources: "РБК, Интерфакс, Московская биржа, Коммерсантъ",
      timeline: "14:00 - заседание совета директоров, 14:30 - объявление о дивидендах, 15:00 - рост на 3%, 16:00 - пик +8%, 17:00 - закрытие торгов",
      draft: "Сбербанк установил новый рекорд по дивидендным выплатам, объявив о выплате 28 рублей на акцию за 2024 год. Это решение привело к историческому росту котировок на 8% в течение торговой сессии. Аналитики отмечают, что такая щедрость может сигнализировать о высоких ожиданиях банка относительно будущих доходов."
    },
    {
      headline: "Газпром потерял 12% после новостей о сокращении экспорта в Европу",
      hotness: "Высокая",
      why_now: "Европейские партнеры объявили о планах полного отказа от российского газа к 2027 году",
      entities: "GAZP, Газпром, Миллер, Европа, СПГ, трубопроводы",
      sources: "Bloomberg, Reuters, Ведомости, ТАСС",
      timeline: "09:00 - открытие торгов, 10:15 - новости из Европы, 11:00 - падение на 5%, 14:30 - минимум -12%, 16:00 - частичное восстановление",
      draft: "Акции Газпрома обрушились на 12% после заявления европейских энергетических компаний о планах полного отказа от российского газа. Это решение может серьезно ударить по экспортным доходам компании, которые составляют основу ее прибыли."
    },
    {
      headline: "Лукойл инвестирует 50 млрд рублей в цифровизацию производства",
      hotness: "Средняя",
      why_now: "Компания запускает масштабную программу модернизации для повышения эффективности добычи",
      entities: "LKOH, Лукойл, Алекперов, цифровизация, добыча, инвестиции",
      sources: "РБК, Коммерсантъ, Нефтегазовая вертикаль",
      timeline: "11:00 - пресс-конференция, 11:30 - презентация планов, 12:00 - рост на 2%, 13:00 - стабилизация",
      draft: "Лукойл объявил о запуске программы цифровой трансформации с инвестициями 50 млрд рублей. Проект направлен на внедрение ИИ-технологий в процессы добычи и переработки нефти, что должно повысить эффективность на 15-20%."
    },
    {
      headline: "Роснефть подписала контракт на поставку нефти в Индию на $2 млрд",
      hotness: "Средняя",
      why_now: "Расширение сотрудничества с азиатскими партнерами на фоне санкций",
      entities: "ROSN, Роснефть, Сечин, Индия, экспорт, контракт",
      sources: "ТАСС, РИА Новости, Economic Times",
      timeline: "08:00 - подписание контракта, 09:30 - пресс-релиз, 10:00 - рост на 1.5%, 11:00 - стабилизация",
      draft: "Роснефть заключила долгосрочный контракт с индийскими партнерами на поставку 10 млн тонн нефти в год. Сделка оценивается в $2 млрд и поможет компании диверсифицировать экспортные потоки."
    },
    {
      headline: "МТС показал рост выручки на 15% благодаря развитию экосистемы",
      hotness: "Низкая",
      why_now: "Компания успешно развивает новые направления бизнеса в сфере финтеха и e-commerce",
      entities: "MTSS, МТС, Корнеев, финтех, экосистема, мобильные платежи",
      sources: "Ведомости, Коммерсантъ, CNews",
      timeline: "09:00 - публикация отчетности, 09:30 - конференц-звонок, 10:00 - рост на 0.8%, 11:00 - стабилизация",
      draft: "МТС продемонстрировал устойчивый рост выручки на 15% благодаря успешному развитию экосистемных сервисов. Особенно выделяется рост в сегменте финтех-услуг и мобильных платежей."
    },
    {
      headline: "Норникель снизил производство никеля на 8% из-за технических работ",
      hotness: "Низкая",
      why_now: "Плановые ремонтные работы на основных производственных мощностях",
      entities: "GMKN, Норникель, Потанин, никель, производство, ремонт",
      sources: "Интерфакс, РБК, Металл-Экспо",
      timeline: "10:00 - пресс-релиз, 10:30 - техническая пауза, 11:00 - падение на 1.2%, 12:00 - восстановление",
      draft: "Норникель временно снизил производство никеля на 8% в связи с плановыми техническими работами на Норильском комбинате. Компания ожидает восстановления полной мощности к концу квартала."
    },
    {
      headline: "Яндекс запустил новый сервис для бизнеса - акции выросли на 5%",
      hotness: "Умеренная",
      why_now: "Компания расширяет B2B-направление, что может стать новым драйвером роста",
      entities: "YNDX, Яндекс, Аркадий Волож, B2B, облачные сервисы, ИИ",
      sources: "CNews, РБК, Коммерсантъ, TechCrunch",
      timeline: "12:00 - презентация продукта, 12:30 - пресс-релиз, 13:00 - рост на 2%, 14:00 - пик +5%, 15:00 - стабилизация",
      draft: "Яндекс представил новый комплексный сервис для корпоративных клиентов, включающий облачные решения и ИИ-инструменты. Аналитики отмечают потенциал этого направления для диверсификации доходов компании."
    },
    {
      headline: "Аэрофлот отменил 15% рейсов из-за нехватки запчастей",
      hotness: "Средняя",
      why_now: "Санкции ограничивают доступ к западным комплектующим для авиатехники",
      entities: "AFLT, Аэрофлот, Полуянов, запчасти, санкции, авиация",
      sources: "ТАСС, РИА Новости, АвиаПорт",
      timeline: "08:00 - внутренний меморандум, 09:00 - уведомление пассажиров, 10:00 - падение на 3%, 11:00 - минимум -4%, 12:00 - частичное восстановление",
      draft: "Аэрофлот вынужден сократить количество рейсов на 15% из-за нехватки запчастей для западных самолетов. Компания работает над локализацией поставок, но процесс займет несколько месяцев."
    }
  ];

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
            <AIChat dateRange={dateRange} selectedTickers={selectedTickers} />
          </Card>
        </div>
      </div>
    </div>
  );
}
