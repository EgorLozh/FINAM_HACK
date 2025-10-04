"use client"

import { useState, useMemo } from "react"
import { Check, ChevronsUpDown, X } from "lucide-react"
import { Button } from "@/components/ui/button"
// import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { TickerSelectorProps } from "@/types"
import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover"

// MOEX тикеры
const MOEX_TICKERS = [
  { value: "SBER", label: "SBER - Сбербанк" },
  { value: "GAZP", label: "GAZP - Газпром" },
  { value: "LKOH", label: "LKOH - Лукойл" },
  { value: "GMKN", label: "GMKN - Норникель" },
  { value: "YNDX", label: "YNDX - Яндекс" },
  { value: "ROSN", label: "ROSN - Роснефть" },
  { value: "NVTK", label: "NVTK - Новатэк" },
  { value: "TATN", label: "TATN - Татнефть" },
  { value: "MGNT", label: "MGNT - Магнит" },
  { value: "MTSS", label: "MTSS - МТС" },
  { value: "ALRS", label: "ALRS - Алроса" },
  { value: "SNGS", label: "SNGS - Сургутнефтегаз" },
  { value: "NLMK", label: "NLMK - НЛМК" },
  { value: "CHMF", label: "CHMF - Северсталь" },
  { value: "VTBR", label: "VTBR - ВТБ" },
  { value: "PLZL", label: "PLZL - Полюс" },
  { value: "AFLT", label: "AFLT - Аэрофлот" },
  { value: "PHOR", label: "PHOR - ФосАгро" },
  { value: "MOEX", label: "MOEX - Московская биржа" },
  { value: "RUAL", label: "RUAL - РУСАЛ" },
]


export function TickerSelector({ selectedTickers, onTickersChange }: TickerSelectorProps) {
  const [open, setOpen] = useState(false)

  const handleSelect = (value: string) => {
    if (selectedTickers.includes(value)) {
      const newTickers = selectedTickers.filter((t) => t !== value)
      onTickersChange(newTickers)
    } else {
      const newTickers = [...selectedTickers, value]
      onTickersChange(newTickers)
    }
  }

  const handleRemove = (value: string) => {
    onTickersChange(selectedTickers.filter((t) => t !== value))
  }

  const selectedLabels = useMemo(() => {
    return selectedTickers.map((ticker) => {
      const found = MOEX_TICKERS.find((t) => t.value === ticker)
      return found ? found.label : ticker
    })
  }, [selectedTickers])

  return (
    <div className="space-y-3">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between bg-transparent hover:border-lava transition-all duration-300"
          >
            {selectedTickers.length > 0 ? `Выбрано: ${selectedTickers.length}` : "Выберите тикеры"}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-full p-2" align="start">
          <div className="max-h-[300px] overflow-y-auto">
            <div className="space-y-1">
              {MOEX_TICKERS.map((ticker) => (
                <div
                  key={ticker.value}
                  className={cn(
                    "flex items-center space-x-2 rounded-sm px-2 py-1.5 text-sm cursor-pointer hover:bg-accent hover:text-accent-foreground",
                    selectedTickers.includes(ticker.value) && "bg-accent text-accent-foreground"
                  )}
                  onClick={() => {
                    handleSelect(ticker.value)
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4 text-lava",
                      selectedTickers.includes(ticker.value) ? "opacity-100" : "opacity-0",
                    )}
                  />
                  {ticker.label}
                </div>
              ))}
            </div>
          </div>
        </PopoverContent>
      </Popover>

      {selectedTickers.length > 0 && (
        <div className="flex flex-wrap gap-2 animate-fade-in">
          {selectedTickers.map((ticker) => {
            const label = MOEX_TICKERS.find((t) => t.value === ticker)?.label || ticker
            return (
              <Badge
                key={ticker}
                variant="secondary"
                className="gap-1 bg-lava hover:bg-lava/20 transition-colors duration-300"
              >
                {label.split(" - ")[0]}
                <button
                  onClick={() => handleRemove(ticker)}
                  className="ml-1 hover:text-lava transition-colors duration-200"
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )
          })}
        </div>
      )}
    </div>
  )
}
