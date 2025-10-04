#!/usr/bin/env python3
"""
Простой тест для проверки работы MOEX RSS парсера
"""
import asyncio
import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_parsing.parsers.moex_rss import MoexRssParser


async def test_moex_parser():
    """Тестируем парсер MOEX RSS"""
    print("Тестирование MOEX RSS парсера...")
    
    parser = MoexRssParser(max_articles=5)  # Ограничиваем количество для теста
    
    try:
        results = await parser.parse()
        
        print(f"\nПолучено {len(results)} новостей:")
        print("=" * 50)
        
        for i, news in enumerate(results, 1):
            print(f"\n{i}. {news.headline}")
            print(f"   Источник: {news.source}")
            print(f"   Дата: {news.created_at}")
            print(f"   URL: {news.url}")
            print(f"   Описание: {news.body[:200]}..." if len(news.body) > 200 else f"   Описание: {news.body}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Ошибка при тестировании парсера: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_moex_parser())
    if success:
        print("\n✅ Тест завершен успешно!")
    else:
        print("\n❌ Тест завершен с ошибками!")
        sys.exit(1)
