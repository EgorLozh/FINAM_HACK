import { convertToModelMessages, UIMessage } from "ai";

const API_KEY = process.env.OPENROUTER_API_KEY as string;
const BASE_URL = "https://openrouter.ai/api/v1";

export async function POST(req: Request) {
  try {
    const { messages }: { messages: UIMessage[] } = await req.json();


    if (!API_KEY) {
      console.error("OPENROUTER_API_KEY не найден");
      return Response.json(
        { error: "OpenRouter API ключ не настроен" },
        { status: 500 }
      );
    }

    const sysPrompt = `Вы - профессиональный финансовый аналитик, специализирующийся на российском рынке MOEX. 
Отвечайте на русском языке, предоставляйте полезную информацию о тикерах, рыночных трендах и инвестиционных стратегиях.
Будьте конкретны!`;

    const modelMessages = convertToModelMessages(messages);
    const fullMessages = [
      { role: "system" as const, content: sysPrompt },
      ...modelMessages,
    ];


    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    const response = await fetch(`${BASE_URL}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Finam AI Chat",
      },
      body: JSON.stringify({
        model: "openai/gpt-4o-mini",
        messages: fullMessages,
        temperature: 0.7,
        max_tokens: 1024,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("OpenRouter error:", response.status, errorText);
      return Response.json(
        {
          error: `OpenRouter API error: ${response.status}`,
          details: errorText,
        },
        { status: 500 }
      );
    }

    const data = await response.json();
    const text = data.choices[0]?.message?.content || "No response generated";

    const responseData = {
      id: crypto.randomUUID(),
      role: "assistant",
      parts: [{ type: "text", text }],
    };


    return Response.json(responseData);
  } catch (error) {
    console.error("AI_API error:", error);
    
    let errorMessage = "Failed to generate response";
    let statusCode = 500;
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        errorMessage = "Запрос превысил время ожидания (30 секунд)";
        statusCode = 408;
      } else if (error.message.includes('fetch failed')) {
        errorMessage = "Ошибка подключения к AI сервису. Проверьте интернет-соединение";
        statusCode = 503;
      } else {
        errorMessage = error.message;
      }
    }
    
    return Response.json(
      {
        error: errorMessage,
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: statusCode }
    );
  }
}
