# 🌀 CryptoMixer | Анонимные криптовалютные транзакции

**Децентрализованный миксер для анонимизации криптовалютных транзакций** с поддержкой BTC, ETH и USDT. Полная прозрачность комиссий и нулевое хранение логов.

## 🔑 Особенности

- 🛡️ **Мультивалютная поддержка**: Bitcoin, Ethereum, USDT
- 📊 **Динамические комиссии**: Авторасчет gas fee + service fee
- 🔄 **Интуитивный интерфейс**: Процесс микширования за 3 шага
- 📜 **Полная история операций**: Последние 10 транзакций
- 🔒 **Безопасность**: 
  - Хеширование паролей (SHA-256)
  - Сессионная аутентификация

## 🛠️ Технологии

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-lightgrey)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3-purple)

- **Backend**: Flask + SQLite3
- **Frontend**: Tailwind CSS + Vanilla JS
- **Дополнительно**: QRCode.js, hashlib

## 🚀 Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/gwadsfwascawfwga/CryptoMixer.git
cd CryptoMixer

# Установить зависимости
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Запустить приложение
flask run --debug
