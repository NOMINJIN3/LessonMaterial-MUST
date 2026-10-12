import torch
from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

# VQA Загвар ачаалах
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

image = Image.open("sample_image.jpg").convert("RGB")

# Асуулт асуух
text = "What is in the image?"
inputs = processor(image, text, return_tensors="pt")

# Үр дүн боловсруулах
outputs = model(**inputs)
logits = outputs.logits
idx = logits.argmax(-1).item()
print("Question:", text)
print("Answer:", model.config.id2label[idx])
