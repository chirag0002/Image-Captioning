from transformers import pipeline

# Create the image-to-text pipeline
pipe = pipeline("image-to-text", model="microsoft/git-large-coco", max_new_tokens=100)

# Process an image and extract text
image_path = "two.jpg"  # Replace with the path to your image file
results = pipe(image_path)

# Check the structure of the results dictionary
print(results)
