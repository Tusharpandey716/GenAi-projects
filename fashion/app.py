import openai

# Set your OpenAI API key
openai.api_key = "sk-5678mnopqrstuvwx5678mnopqrstuvwx5678mnop"

# Generate an image based on a fashion-related prompt
response = openai.Image.create(
    prompt="A modern outfit inspired by vintage Parisian fashion, combining classic elegance with contemporary flair. Featuring chic details like a tailored trench coat, high-waisted trousers, and stylish accessories like a beret and vintage handbag.",
    n=1,  # Number of images to generate
    size="1024x1024"  # Image size (e.g., 256x256, 512x512, 1024x1024)
)

# Save or display the image URL
image_url = response['data'][0]['url']
print(f"Generated Image URL: {image_url}")
