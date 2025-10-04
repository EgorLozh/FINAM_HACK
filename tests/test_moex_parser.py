#!/usr/bin/env python3
"""
Тест для парсера MOEX RSS с записью результатов в файл
"""
import asyncio
import sys
import os
import json
from datetime import datetime

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_parsing.parsers.moex_rss import MoexRssParser


async def test_moex_parser():
    """Тестируем парсер MOEX RSS и записываем результаты в файл"""
    print("🚀 Запуск тестирования парсера MOEX RSS...")
    print("📊 Парсер настроен на получение новостей за последние 100 часов")
    
    # Создаем экземпляр парсера
    parser = MoexRssParser(max_articles=50)  # Ограничиваем для теста
    
    try:
        # Запускаем парсинг
        print("⏳ Парсинг новостей...")
        results = await parser.parse()
        
        print(f"✅ Получено {len(results)} новостей")
        
        if not results:
            print("❌ Новостей не найдено")
            return False
        
        # Подготавливаем данные для записи
        output_data = []
        for i, news in enumerate(results, 1):
            news_data = {
                "index": i,
                "headline": news.headline,
                "source": news.source,
                "created_at": news.created_at.isoformat(),
                "url": news.url,
                "body_length": len(news.body),
                "body_preview": news.body[:200] + "..." if len(news.body) > 200 else news.body,
                "full_body": news.body
            }
            output_data.append(news_data)
        
        # Создаем имя файла с временной меткой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test/moex_news_{timestamp}.json"
        
        # Записываем результаты в JSON файл
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Результаты сохранены в файл: {output_file}")
        
        # Также создаем текстовый файл с кратким отчетом
        report_file = f"test/moex_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"ОТЧЕТ О ПАРСИНГЕ MOEX RSS\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Количество новостей: {len(results)}\n")
            f.write(f"=" * 50 + "\n\n")
            
            for i, news in enumerate(results, 1):
                f.write(f"{i}. {news.headline}\n")
                f.write(f"   Источник: {news.source}\n")
                f.write(f"   Дата: {news.created_at}\n")
                f.write(f"   URL: {news.url}\n")
                f.write(f"   Длина текста: {len(news.body)} символов\n")
                f.write(f"   Превью: {news.body[:150]}...\n")
                f.write("-" * 50 + "\n\n")
        
        print(f"📋 Краткий отчет сохранен в файл: {report_file}")
        
        # Выводим статистику
        print("\n📈 СТАТИСТИКА:")
        print(f"   • Всего новостей: {len(results)}")
        print(f"   • Средняя длина текста: {sum(len(n.body) for n in results) // len(results)} символов")
        print(f"   • Самая длинная новость: {max(len(n.body) for n in results)} символов")
        print(f"   • Самая короткая новость: {min(len(n.body) for n in results)} символов")
        
        # Показываем примеры заголовков
        print(f"\n📰 ПРИМЕРЫ ЗАГОЛОВКОВ:")
        for i, news in enumerate(results[:5], 1):
            print(f"   {i}. {news.headline}")
        
        if len(results) > 5:
            print(f"   ... и еще {len(results) - 5} новостей")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании парсера: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 ТЕСТИРОВАНИЕ ПАРСЕРА MOEX RSS")
    print("=" * 50)
    
    success = asyncio.run(test_moex_parser())
    
    if success:
        print("\n✅ Тест завершен успешно!")
        print("📁 Проверьте папку test/ для просмотра результатов")
    else:
        print("\n❌ Тест завершен с ошибками!")
        sys.exit(1)
