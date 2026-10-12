import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
from gtts import gTTS
import os

def main():
    image_path = "sample_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"Алдаа: '{image_path}' файл олдсонгүй!")
        return

    print("Загварыг ачаалж байна, түр хүлээнэ үү...")
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 1. Дүрсийг боловсруулах
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    # 2. Текстэн тайлбар үүсгэх
    output_ids = model.generate(inputs["pixel_values"], max_length=16, num_beams=4)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    print("\n--- Үр дүн ---")
    print(f"Generated Caption: {caption}")

    # 3. Тайлбарыг дуу болгон хувиргаж хадгалах (Дүрс + Дуу хоолой даалгавар)
    print("\nТайлбарыг аудио файл руу хувиргаж байна...")
    tts = gTTS(text=caption, lang='en')
    tts.save("caption_audio.mp3")
    print("Аудио файл 'caption_audio.mp3' нэртэйгээр амжилттай хадгалагдлаа.")

if __name__ == "__main__":
    main()
