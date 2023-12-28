FROM python:latest

# Копируем наш проект в ./app
COPY ./ ./app

# Переходим в ./app
WORKDIR ./app

# Устанавливаем тайм зону
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Устанавливаем локаль
RUN apt update && apt install -y --no-install-recommends locales; rm -rf /var/lib/apt/lists/*; sed -i '/^#.* ru_RU.UTF-8 /s/^#//' /etc/locale.gen; locale-gen


# Обновляем pip и устанавливаем зависимости от проекта
RUN pip install --upgrade pip && pip install -r requirements.txt

# Запускаем программу
ENTRYPOINT [ "python", "./main.py" ]