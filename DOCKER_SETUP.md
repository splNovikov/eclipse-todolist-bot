# Установка Docker на сервере Timeweb

Эта инструкция поможет вам установить Docker и Docker Compose на вашем сервере Timeweb.

## Шаг 1: Подключение к серверу

Подключитесь к вашему серверу через SSH:

```bash
ssh ваш_пользователь@ваш_сервер_ip
```

## Шаг 2: Обновление системы

```bash
sudo apt update
sudo apt upgrade -y
```

## Шаг 3: Установка необходимых пакетов

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

## Шаг 4: Добавление официального GPG ключа Docker

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

> Если у вас Debian, замените `ubuntu` на `debian` в команде выше.

## Шаг 5: Добавление репозитория Docker

Для Ubuntu:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Для Debian:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## Шаг 6: Установка Docker

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

## Шаг 7: Проверка установки Docker

```bash
sudo docker --version
sudo docker run hello-world
```

Вы должны увидеть версию Docker и успешное выполнение тестового контейнера.

## Шаг 8: Установка Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Шаг 9: Проверка установки Docker Compose

```bash
docker-compose --version
```

## Шаг 10: Настройка прав для запуска Docker без sudo (опционально, но рекомендуется)

```bash
sudo usermod -aG docker $USER
```

**Важно:** После этой команды нужно выйти и снова войти в систему, чтобы изменения вступили в силу:

```bash
exit
```

Подключитесь снова:
```bash
ssh ваш_пользователь@ваш_сервер_ip
```

Проверьте, что Docker работает без sudo:
```bash
docker ps
```

## Шаг 11: Клонирование репозитория

Теперь клонируйте ваш репозиторий бота:

```bash
cd ~
git clone https://github.com/ваш-username/eclipse-todolist-bot.git
cd eclipse-todolist-bot
```

## Шаг 12: Настройка переменных окружения

Создайте файл `.env`:

```bash
nano .env
```

Добавьте ваш токен бота:
```
BOT_TOKEN=ваш_токен_бота
PYTHONUNBUFFERED=1
```

Сохраните файл (Ctrl+O, Enter, Ctrl+X).

## Шаг 13: Первый запуск

```bash
docker-compose up -d
```

Проверьте статус:
```bash
docker-compose ps
docker-compose logs -f
```

## Готово! ✅

Docker установлен и бот запущен. Теперь при каждом push в ветку `main` GitHub Actions будет автоматически обновлять бота на сервере.

## Полезные команды

- Просмотр логов: `docker-compose logs -f`
- Перезапуск бота: `docker-compose restart`
- Остановка бота: `docker-compose down`
- Запуск бота: `docker-compose up -d`
- Обновление бота вручную: `git pull && docker-compose up -d --build`
