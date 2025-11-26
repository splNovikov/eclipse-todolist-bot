# Настройка GitHub Secrets для автоматического деплоя

Для работы автоматического деплоя необходимо настроить секреты в GitHub.

## Шаг 1: Откройте настройки репозитория

1. Перейдите в ваш репозиторий на GitHub
2. Нажмите на вкладку **Settings** (Настройки)
3. В левом меню выберите **Secrets and variables** → **Actions**

## Шаг 2: Добавьте необходимые секреты

Нажмите **New repository secret** и добавьте следующие секреты:

### SSH_HOST
- **Имя:** `SSH_HOST`
- **Значение:** IP-адрес или доменное имя вашего сервера Timeweb
- **Пример:** `123.45.67.89` или `your-server.timeweb.ru`

### SSH_USERNAME
- **Имя:** `SSH_USERNAME`
- **Значение:** Имя пользователя для SSH-подключения
- **Пример:** `root` или `user`

### SSH_PRIVATE_KEY
- **Имя:** `SSH_PRIVATE_KEY`
- **Значение:** Приватный SSH-ключ для подключения к серверу

#### Как получить SSH-ключ:

Если у вас еще нет SSH-ключа:

1. **На вашем локальном компьютере** создайте новую пару ключей:
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/timeweb_deploy
   ```
   
   Или используйте RSA (если ed25519 не поддерживается):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-actions-deploy" -f ~/.ssh/timeweb_deploy
   ```

2. **Скопируйте публичный ключ на сервер:**
   ```bash
   ssh-copy-id -i ~/.ssh/timeweb_deploy.pub ваш_пользователь@ваш_сервер
   ```
   
   Или вручную:
   ```bash
   cat ~/.ssh/timeweb_deploy.pub
   ```
   
   Затем на сервере выполните:
   ```bash
   mkdir -p ~/.ssh
   echo "ваш_публичный_ключ" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   chmod 700 ~/.ssh
   ```

3. **Скопируйте приватный ключ в GitHub Secret:**
   ```bash
   cat ~/.ssh/timeweb_deploy
   ```
   
   Скопируйте весь вывод (включая `-----BEGIN ... KEY-----` и `-----END ... KEY-----`) и вставьте в значение секрета `SSH_PRIVATE_KEY`.

### SSH_PORT (опционально)
- **Имя:** `SSH_PORT`
- **Значение:** Порт SSH
- **Пример:** `22` или `2222`
- **Примечание:** Если не указан, будет использован порт 22 по умолчанию. Можно не создавать этот секрет, если используется стандартный порт 22.

### SSH_DEPLOY_PATH (опционально)
- **Имя:** `SSH_DEPLOY_PATH`
- **Значение:** Путь к директории проекта на сервере
- **Пример:** `$HOME/eclipse-todolist-bot` или `/home/user/eclipse-todolist-bot`
- **По умолчанию:** `$HOME/eclipse-todolist-bot`
- **Важно:** Используйте `$HOME` вместо `~`, так как тильда не всегда расширяется в скриптах
- **Примечание:** Если директория не существует, workflow автоматически клонирует репозиторий в указанный путь

### GIT_REPOSITORY_URL (опционально)
- **Имя:** `GIT_REPOSITORY_URL`
- **Значение:** URL репозитория для клонирования (если директория не существует)
- **Примеры:**
  - SSH (рекомендуется для приватных): `git@github.com:username/eclipse-todolist-bot.git`
  - HTTPS с токеном: `https://USERNAME:TOKEN@github.com/username/eclipse-todolist-bot.git`
  - HTTPS публичный: `https://github.com/username/eclipse-todolist-bot.git`
- **По умолчанию:** Автоматически определяется из текущего репозитория в SSH формате (`git@github.com:...`)
- **Примечание:** 
  - Для приватных репозиториев требуется настроить SSH-ключ на сервере для доступа к GitHub
  - Или использовать HTTPS URL с Personal Access Token
  - Обычно не требуется, если репозиторий уже настроен на сервере

## Шаг 3: Проверка подключения

После настройки всех секретов:

1. Сделайте тестовый коммит и push в ветку `main`
2. Перейдите во вкладку **Actions** в вашем репозиторий
3. Проверьте, что workflow выполнился успешно

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте приватные ключи в репозиторий
- Используйте отдельный SSH-ключ только для деплоя
- Регулярно обновляйте ключи
- Ограничьте права доступа SSH-ключа на сервере (если возможно)

## Устранение проблем

### Ошибка "Permission denied (publickey)"
- Убедитесь, что публичный ключ добавлен в `~/.ssh/authorized_keys` на сервере
- Проверьте права доступа: `chmod 600 ~/.ssh/authorized_keys`

### Ошибка "git: command not found"
- Установите git на сервере: `sudo apt install git`

### Ошибка "docker-compose: command not found"
- Убедитесь, что docker-compose установлен и доступен в PATH
- Проверьте установку: `docker-compose --version`

### Ошибка "Could not read from remote repository" или "could not read Username"
- **Для приватных репозиториев:** Настройте SSH-ключ на сервере для доступа к GitHub:
  
  1. Создайте SSH-ключ на сервере (если еще нет):
     ```bash
     ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/github_deploy
     ```
  
  2. Добавьте публичный ключ в GitHub:
     - Перейдите в Settings → SSH and GPG keys → New SSH key
     - Или для конкретного репозитория: Settings → Deploy keys → Add deploy key
     - Скопируйте содержимое: `cat ~/.ssh/github_deploy.pub`
  
  3. Настройте SSH config (опционально):
     ```bash
     cat >> ~/.ssh/config << EOF
     Host github.com
       IdentityFile ~/.ssh/github_deploy
       IdentitiesOnly yes
     EOF
     chmod 600 ~/.ssh/config
     ```
  
  4. Проверьте подключение:
     ```bash
     ssh -T git@github.com
     ```
  
- **Альтернатива:** Используйте секрет `GIT_REPOSITORY_URL` с HTTPS URL и токеном:
  - Формат: `https://USERNAME:TOKEN@github.com/username/repo.git`
  - Создайте Personal Access Token в GitHub: Settings → Developer settings → Personal access tokens
