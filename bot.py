import telebot
import requests
import base64
from io import BytesIO
from deep_translator import GoogleTranslator

TELEGRAM_TOKEN = 'TOKEN'
DEEPINFRA_TOKEN = 'TOKEN'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_image(prompt):
    url = "https://api.deepinfra.com/v1/inference/stabilityai/stable-diffusion-2-1"
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        base64_image = output['images'][0]
        if base64_image.startswith('data:image'):
            base64_image = base64_image.split(",")[1]
        image_data = base64.b64decode(base64_image)
        image_file = BytesIO(image_data)
        image_file.name = "generated.png"
        return image_file
    else:
        print("Ошибка генерации:", response.text)
        return None

@bot.message_handler(content_types=['text'])
def handle_text(message):
    prompt = message.text
    prompt_en = GoogleTranslator(source='auto', target='en').translate(prompt)
    bot.reply_to(message, "Генерирую изображение, подождите... ⏳")
    image_file = generate_image(prompt_en)
    if image_file:
        bot.send_photo(message.chat.id, image_file, caption=f"Вот ваша картинка по запросу: \"{prompt}\" 🎨")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка при генерации изображения. Попробуйте позже!")

if __name__ == "__main__":
    bot.infinity_polling()
