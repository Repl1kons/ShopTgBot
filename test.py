import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import time

def create_product_image(product_name, quantity, price, choose_product_url, output_path, ava):
    # Запускаем счетчик времени
    start_time = time.time()

    product_image = Image.open("data/img/object.jpg")
    # product_image.

    choose_product_response = requests.get(choose_product_url)
    choose_product_image = Image.open(io.BytesIO(choose_product_response.content))

    width = 100
    height = 100
    card = Image.new("RGB",(width,height),"#EEC3EE")

    # Получаем изображение аватара пользователя
    ava_image = Image.open(ava)
    ava_width = 50  # Выберите подходящую ширину
    ava_height = 50  # Выберите подходящую высоту
    ava_resized = ava_image.resize((ava_width,ava_height),Image.LANCZOS)

    # Создаем маску для круглой формы
    mask_1 = Image.new("L",ava_resized.size,0)
    draw = ImageDraw.Draw(mask_1)
    draw.ellipse((0,0,ava_width,ava_height),fill = 255)
    position = (690,90)

    """ПОКАЗ УСПЕШНОЙ ОПЛАТЫ"""
    success_image = Image.open("data/img/object.jpg")
    success_width = 350  # Выберите подходящую ширину
    success_height = 60  # Выберите подходящую высоту
    success_resized = success_image.resize((success_width,success_height),Image.LANCZOS)

    # Создаем маску для круглой формы
    mask_success = Image.new("L",success_resized.size,0)
    draw_success = ImageDraw.Draw(mask_success)
    radius = min(ava_width,ava_height) // 2  # Радиус закругления, равный половине минимальной стороны изображения
    draw_success.rounded_rectangle((0, 0, success_width, success_height), radius, fill=255)
    position_success = (365, 520)


    """БЛОКИ ДЛЯ ХАР-ИК ТОВАРОВ"""
    block_image = Image.open("data/img/object.jpg")
    block_width = 150  # Выберите подходящую длину
    block_height = 70  # Выберите подходящую шир
    block_resized = block_image.resize((block_width,block_height),Image.LANCZOS)

    # Создаем маску для круглой формы
    mask_block = Image.new("L",block_resized.size,0)
    draw_block = ImageDraw.Draw(mask_block)
    radius = min(block_width,block_height) // 2  # Радиус закругления, равный половине минимальной стороны изображения
    draw_block.rounded_rectangle((0,0,block_width,block_height),radius,fill = 255)
    position_block_amount = (365,420)
    position_block_price = (565,420)



    image = product_image.copy()
    draw = ImageDraw.Draw(image)
    font_size = 22
    font = ImageFont.truetype("sfns-display-bold.ttf", font_size)


    """ БЕЛАЯ КАРТОЧКА"""
    new_width = 450
    new_height = 530
    card_resized = card.resize((new_width, new_height), Image.LANCZOS)

    mask_card = Image.new("L",card_resized.size,0)
    draw_mask = ImageDraw.Draw(mask_card)
    radius = 20
    draw_mask.rounded_rectangle((0,0,new_width,new_height),radius,fill = 255)

    # Вставляем изображение товара на основное изображение с закругленными углами
    image.paste(card_resized,(315,product_image.height-600),mask = mask_card)


    """ ФОТО ЕЖЕДНЕВНИКА """
    new_width = 200
    new_height = 200
    choose_product_resized = choose_product_image.resize((new_width, new_height), Image.LANCZOS)

    # Создаем маску для скругления углов
    mask = Image.new("L", choose_product_resized.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    radius = 20
    draw_mask.rounded_rectangle((0, 0, new_width, new_height), radius, fill=255)

    # Вставляем изображение товара на основное изображение с закругленными углами
    image.paste(choose_product_resized, (440, card_resized.height - 400), mask=mask)

    image.paste(ava_resized,position,mask = mask_1)
    image.paste(success_resized,position_success,mask = mask_success)



    text_name = f"{product_name}\n"
    text_position_name = (435, card_resized.height - 190)
    draw.text(text_position_name,text_name,fill = "#6A6A6A",font = font)



    text_success = "Успешно добавлено в корзину"
    text_position_success = (375, 535)
    draw.text(text_position_success,text_success,fill = "#6D6C64",font = font)



    image.paste(block_resized, position_block_amount,mask = mask_block)
    text_block_amount = f"Кол-во: {quantity}"
    text_position_block_amount = (390,440)
    draw.text(text_position_block_amount,text_block_amount,fill = "#4B4B4B",font = font)




    image.paste(block_resized,position_block_price,mask = mask_block)
    text_block_price = f"Цена: {price}"
    text_position_block_price = (590,440)
    draw.text(text_position_block_price,text_block_price,fill = "#4B4B4B",font = font)



    image.save(output_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)






#
# choose_product_url = 'https://sun9-27.userapi.com/et34ZHyRMg7Okk0XSGqBPdfJaXrtqV767P9JDw/q5qcPRcYf60.jpg'
# create_product_image("Ежедневник TO-DO", 1, 490, choose_product_url, "output_image.jpg", "ava.png")