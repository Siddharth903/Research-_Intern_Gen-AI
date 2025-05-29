from flask import Flask, render_template, request
from huggingface_hub import InferenceClient
import requests
import os

app = Flask(__name__)

# Set your API keys as environment variables or directly here        ## Write your own API key in here
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 's,.dfmsklsg,fmc;l,akjlf,vmwklsg,cf.ls/kdf,ax.c,s.lfkc,.kfslvkc,m,skl;gk')
HF_TOKEN = os.getenv('HF_API_KEY', '14785236987456321456987456')

NEWS_SOURCES = 'bbc-news,cnn,reuters'

def get_trending_news():
    url = f'https://newsapi.org/v2/top-headlines?sources={NEWS_SOURCES}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json().get('articles', [])[:5]

def generate_video(prompt):
    client = InferenceClient(token=HF_TOKEN)
    try:
        # Adjust model name and parameters as per DeepSeek's documentation
        response = client.text_to_video(
            prompt,
            model="deepseek-ai/DeepSeek-Video",  # Check actual model name
            negative_prompt="low quality, blurry",
            num_frames=24,
            fps=12,
            height=512,
            width=512
        )
        video_path = f"static/output.mp4"
        with open(video_path, "wb") as f:
            f.write(response)
        return video_path
    except Exception as e:
        print(f"Error generating video: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = get_trending_news()
    video_path = None
    selected_idx = None

    if request.method == 'POST':
        selected_idx = int(request.form.get('article_idx'))
        selected = articles[selected_idx]
        prompt = selected['title'] + (". " + selected.get('description', '') if selected.get('description') else "")
        video_path = generate_video(prompt)

    return render_template('index.html', articles=articles, video_path=video_path, selected_idx=selected_idx)

if __name__ == '__main__':
    app.run(debug=True)
