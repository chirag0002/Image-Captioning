from transformers import AutoProcessor, AutoModelForCausalLM
import torch
from PIL import Image
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

git_processor_large_coco = AutoProcessor.from_pretrained("microsoft/git-large-coco")
git_model_large_coco = AutoModelForCausalLM.from_pretrained("microsoft/git-large-coco").to(device)

def generate_caption(processor, model, image, use_float_16=False):
    
    image = Image.open(image)
    
    image = image.convert("RGB")
    
    inputs = processor(images=image, return_tensors="pt").to(device)

    if use_float_16:
        inputs = inputs.to(torch.float16)
    
    generated_ids = model.generate(pixel_values=inputs.pixel_values, num_beams=3, max_length=20, min_length=5) 

    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
   
    return generated_caption

@app.route("/generate_caption", methods=["POST"])
def generate_caption_api():
    try:
        image = request.files["image"]
        if image:
            image.save("temp.jpg") 
            caption = generate_caption(git_processor_large_coco, git_model_large_coco, "temp.jpg")
            os.remove("temp.jpg") 
            return jsonify({"caption": caption})
        else:
            return jsonify({"error": "No image provided"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
