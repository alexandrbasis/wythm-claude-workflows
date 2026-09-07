# OPS-17: Normalize greeting names

Состояние: реализовано, проверки пройдены.

## Цель
Перед приветствием удалять пробелы с обоих краёв имени. Внутренние пробелы сохранять. Текущий формат Hello, <name>! не менять.

## Проверка
- [x] Имя "  Alex Basis  " даёт "Hello, Alex Basis!".
- [x] Имя без крайних пробелов даёт прежний результат.
- [x] `python3 -m unittest discover -s tests -q` — OK, пройдено 2 теста.

## Шаги
Добавить поведенческую проверку крайних и внутренних пробелов, исправить greeting.py, записать результаты сюда.

## Фактические проверки
- Добавлена поведенческая проверка `test_trims_outer_whitespace_and_preserves_inner_spaces` в `tests/test_greeting.py`.
- RED: до исправления проверка падала с результатом `Hello,   Alex Basis  !` вместо `Hello, Alex Basis!`.
- GREEN: после изменения `greet` использует `name.strip()`; команда `python3 -m unittest discover -s tests -q` завершилась успешно (`Ran 2 tests`, `OK`).
