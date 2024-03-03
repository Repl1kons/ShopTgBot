FROM python:3.9-alpine

WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/

# Устанавливаем локаль

# Обновляем pip и устанавливаем зависимости от проекта
RUN pip install --upgrade pip && pip install -r requirements.txt


# run app
CMD ["python", "main.py"]