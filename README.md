# Документация по проекту
# Учебный конфигурационный язык

Этот проект реализует инструмент командной строки для преобразования текста из учебного конфигурационного языка в формат TOML. Инструмент обрабатывает комментарии, константы, структуры (включая вложенные структуры) и поддерживает ссылки на константы.

## Возможности
- Объявление и использование констант
- Поддержка вложенных структур произвольной глубины
- Комментарии в формате `(comment текст комментария)`
- Преобразование в формат TOML
- Проверка синтаксиса и типов данных

## Структура проекта
```
HW3/
├── translator.py          # Основной парсер
├── tests_translator.py    # Модульные тесты            
└── test.toml         # Выходной TOML файл
```

## Использование

### Парсинг конфигурационного файла
```sh
python HW3/config3.py <input_file> <output_file>
```

Например:
```sh
python HW3/config3.py HW3/example/config1_example.txt HW3/output.toml
```

### Запуск тестов
```sh
python -m unittest HW3/tests_config3.py
```

## Примеры конфигураций

### Конфигурация для сетевых настроек
```
' Это конфигурация для сетевых настроек
var port 8080;
var timeout 30;
var max_connections 100;
var server_name "example.com";

' Это однострочный комментарий

#( "192.168.1.1", "192.168.1.2", "192.168.1.3" )

table([
    ip = "192.168.1.1",
    mask = "255.255.255.0",
    gateway = "192.168.1.254"
])

var new_port @{+ port 1};
var new_timeout @{- timeout 5};
var new_max_connections @{* max_connections 2};
var min_value @{min port timeout};
var max_value @{max port max_connections};ы
```

### Конфигурация для мониторинга системы
```
var monitoring_service "HealthCheckService";
var check_interval 5;  # in minutes

table([
    endpoints = #("http://localhost:8080/health", "http://localhost:8080/status"),
    notifications = table([
        email = "admin@example.com",
        sms = "1234567890",
        alert_threshold = @{ + check_interval 10 }
    ]),
    status = table([
        last_check = "2023-10-01T12:00:00Z",
        is_up = true,
        response_time = @{ max 200 150 }
    ])
])
```
