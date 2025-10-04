"use client";

import type React from "react";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { SendIcon, MessageSquare, Loader2 as Loader2Icon } from "lucide-react";
import { ScrollArea } from "../ui/scroll-area";
import { Input } from "../ui/input";
import { AIChatProps } from "@/types";
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import { Message, MessageContent } from "@/components/ai-elements/message";

export function AIChat({ dateRange, selectedTickers }: AIChatProps) {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "streaming" | "error">("idle");
  const [error, setError] = useState<Error | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    let context = "";
    if (dateRange?.from && dateRange?.to) {
      context += `Период: ${dateRange.from.toLocaleDateString()} - ${dateRange.to.toLocaleDateString()}. `;
    }
    if (selectedTickers?.length > 0) {
      context += `Выбранные тикеры: ${selectedTickers.join(", ")}. `;
    }

    const fullMessage = context ? `${context}\n${input.trim()}` : input.trim();

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      parts: [{ type: "text", text: fullMessage }],
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setStatus("streaming");
    setError(null);
    setInput("");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [userMessage],
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "API error");
      }

      const assistantMessage = await response.json();
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error("Error sending message:", err);
      setError(err as Error);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          parts: [{ type: "text", text: `Ошибка: ${(err as Error).message}` }],
        },
      ]);
    } finally {
      setIsLoading(false);
      setStatus("idle");
    }
  };

  return (
    <div className="flex flex-col h-[560px]">
      <div className="space-y-4">
        <Conversation className="relative w-full" style={{ height: "500px" }}>
          <ConversationContent>
            {messages.length === 0 ? (
              <ConversationEmptyState
                icon={<MessageSquare className="size-12" />}
                title="Сообщений пока нет!"
                description="Начните общение с AI-ассистеном."
              />
            ) : (
              messages.map((message) => {

                let content = "";

                if (Array.isArray(message.parts)) {
                  content = message.parts
                    .filter((part: any) => part.type === "text")
                    .map((part: any) => part.text)
                    .join("");
                }

                return (
                  <Message
                    from={message.role === "user" ? "user" : "assistant"}
                    key={message.id}
                  >
                    <MessageContent>
                      {content ||
                        "AI не смог сгенерировать ответ. Попробуйте еще раз."}
                    </MessageContent>
                  </Message>
                );
              })
            )}
            {status === "streaming" && (
              <div className="flex justify-start animate-fade-in">
                <div className="bg-muted rounded-lg px-4 py-3">
                  <Loader2Icon className="w-5 h-5 animate-spin text-[#F56E0F]" />
                </div>
              </div>
            )}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>
      </div>

      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <Input
          value={input}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setInput(e.target.value)
          }
          placeholder="Задайте вопрос..."
          disabled={isLoading}
          className="flex-1 focus-visible:ring-lava transition-all duration-300"
        />
        <Button
          type="submit"
          disabled={isLoading || !input.trim()}
          size="icon"
          className="bg-lava hover:bg-lava transition-all duration-300"
        >
          <SendIcon className="w-4 h-4" />
        </Button>
      </form>
    </div>
  );
}
