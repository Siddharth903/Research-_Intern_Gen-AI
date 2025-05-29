# app.py
import os
from flask import Flask, render_template, request
from huggingface_hub import InferenceClient

app = Flask(__name__)

# Set your Hugging Face API key
HF_API_KEY = os.getenv("HF_API_KEY", "hf_xxxxxxxxxxxxxxxxxxxxxxxx")

# Initialize the InferenceClient with the novita provider
client = InferenceClient(
    provider="novita",
    api_key=HF_API_KEY,
)

# Demo product list (replace with your scraping logic)
def get_trending_products():
    return [
        {
            "name": "Wireless Earbuds Pro",               ##Provide your product Details here and Also Give parameter that you want to give !!
            "description": "High-fidelity sound, noise-cancelling, 24h battery.",
            "url": "https://example.com/wireless-earbuds-pro",
            "image": "https://example.com/images/earbuds.jpg"
        },
        {
            "name": "Smart Fitness Watch",
            "description": "Track your health, steps, and sleep with style.",
            "url": "https://example.com/smart-fitness-watch",
            "image": "https://example.com/images/fitness-watch.jpg"
        }
    ]

# Demo keyword research (replace with your keyword research logic)
def get_seo_keywords(product_name):
    keywords_map = {
        "Wireless Earbuds Pro": ["wireless earbuds", "bluetooth headphones", "noise cancelling earbuds", "best wireless earbuds"],
        "Smart Fitness Watch": ["fitness watch", "smartwatch", "health tracker", "best fitness watch"]
    }
    return keywords_map.get(product_name, ["best product", "top rated", "buy online", "review"])

def generate_blog_post(product, keywords):
    prompt = (
        f"Write a 150-200 word SEO blog post about {product['name']}."
        f" Include these keywords: {', '.join(keywords[:4])}."
        f" Highlight the main features: {product['description']}."
        f" Make it engaging, informative, and naturally incorporate the keywords."
    )
    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating blog post: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    products = get_trending_products()
    if request.method == 'POST':
        product_idx = int(request.form['product'])
        product = products[product_idx]
        keywords = get_seo_keywords(product['name'])
        blog_content = generate_blog_post(product, keywords)
        return render_template('result.html', product=product, keywords=keywords, content=blog_content)
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
