#!/usr/bin/env python3
"""
Хук для команды /ct (create task) - добавляет project_index.json в контекст
для обеспечения планировщика задач полной информацией о структуре проекта
"""

import json
import logging
import os
import sys
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ct-hook")


def load_project_index(project_dir: str) -> dict:
    """Загружает project_index.json"""
    index_path = Path(project_dir) / "project_index.json"

    if not index_path.exists():
        logger.warning(f"Индекс проекта не найден: {index_path}")
        return None

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки индекса: {e}")
        return None


def format_context_summary(index_data: dict) -> str:
    """Форматирует краткое резюме проекта для контекста"""
    if not index_data:
        return "❌ Project index unavailable"

    # Извлекаем данные из актуальной структуры индекса
    metadata = index_data.get("project_overview", {})
    key_modules = index_data.get("key_modules", {})
    architecture_patterns = index_data.get("architecture_patterns", [])
    key_features = index_data.get("key_features", [])
    project_stats = index_data.get("project_statistics", {})
    current_context = index_data.get("current_development_context", {})

    # Получаем статистику файлов
    python_files = project_stats.get("python_files", 0)
    total_files = project_stats.get("total_files", 0)

    # Извлекаем архитектурные слои из key_modules
    architecture_layers = []
    for module_category, modules in key_modules.items():
        architecture_layers.append(module_category)

    # Подсчет файлов по модулям
    file_types = {}
    for category, modules in key_modules.items():
        if isinstance(modules, list):
            file_types[category] = len(modules)
        elif isinstance(modules, dict):
            file_types[category] = len(modules)

    context = f"""# 📋 Project Structure Context (Auto-injected for /ct)

## Project Overview
- **Name**: {metadata.get('name', 'Unknown')}
- **Description**: {metadata.get('description', 'No description available')}
- **Architecture**: {metadata.get('architecture', 'Not specified')}
- **Last Updated**: {metadata.get('last_updated', 'Unknown')}
- **Python Files**: {python_files}/{total_files}

## Architecture Layers
{', '.join(sorted(architecture_layers)) if architecture_layers else 'Not analyzed'}

## Module Distribution
"""

    for category, count in sorted(file_types.items()):
        context += f"- **{category}**: {count} modules\n"

    # Архитектурные паттерны
    if architecture_patterns:
        context += f"\n## Architecture Patterns\n"
        patterns_list = (
            list(architecture_patterns)
            if hasattr(architecture_patterns, "__iter__")
            else [str(architecture_patterns)]
        )
        for pattern in patterns_list[:5]:
            context += f"- {pattern}\n"

    # Ключевые функции
    if key_features:
        context += f"\n## Key Features\n"
        if isinstance(key_features, dict):
            items = list(key_features.items())
            for feature, details in items[:5]:
                desc = (
                    details.get("description", str(details))
                    if isinstance(details, dict)
                    else str(details)
                )
                context += f"- **{feature}** - {desc}\n"
        elif isinstance(key_features, list):
            for feature in key_features[:5]:
                context += f"- {feature}\n"
        else:
            context += f"- {str(key_features)}\n"

    # Ключевые модули по категориям
    for category, modules in key_modules.items():
        if modules:
            context += f"\n## {category.replace('_', ' ').title()}\n"
            if isinstance(modules, list):
                module_list = list(modules)
                for module in module_list[:5]:
                    context += f"- `{module}`\n"
            elif isinstance(modules, dict):
                items = list(modules.items())
                for module, desc in items[:5]:
                    context += f"- `{module}` - {desc}\n"
            else:
                context += f"- {str(modules)}\n"

    # Текущий контекст разработки
    if current_context:
        context += f"\n## Current Development Context\n"
        for key, value in current_context.items():
            if isinstance(value, list) and value:
                value_list = list(value)
                context += f"- **{key.replace('_', ' ').title()}**: {', '.join(value_list[:3])}\n"
            elif isinstance(value, str):
                context += f"- **{key.replace('_', ' ').title()}**: {value}\n"

    context += f"\n---\n*This context was automatically injected by ct-context-injector hook*\n"

    return context


def main():
    try:
        # Читаем входные данные от Claude Code
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        project_dir = input_data.get("cwd", "")

        # Проверяем, что это вызов Task tool (используется командой /ct)
        if tool_name != "Task":
            logger.debug(f"Хук не для Task tool: {tool_name}")
            sys.exit(0)

        # Проверяем CLAUDE_PROJECT_DIR
        claude_project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
        if claude_project_dir:
            project_dir = claude_project_dir

        if not project_dir:
            logger.warning("Не удалось определить директорию проекта")
            sys.exit(0)

        logger.info(f"🎯 /ct команда обнаружена, добавляю контекст проекта...")
        logger.info(f"📁 Project dir: {project_dir}")

        # Загружаем индекс проекта
        index_data = load_project_index(project_dir)

        # Формируем контекст
        context_summary = format_context_summary(index_data)

        # Выводим контекст в stdout для добавления в сессию Claude
        print(context_summary)

        logger.info("✅ Контекст проекта добавлен для /ct команды")

    except Exception as e:
        logger.error(f"❌ Ошибка в ct-context-injector: {e}")
        sys.exit(0)  # Не блокируем выполнение при ошибке


if __name__ == "__main__":
    main()
