from flask import Flask, render_template, request, jsonify
import feedparser
from transformers import pipeline

app = Flask(__name__)

# Initialize Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# RSS Feed URLs
RSS_FEEDS = {
    "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "world": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
}

# Fetch and summarize news
def fetch_and_summarize(feed_url, max_articles=5):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:max_articles]:
        title = entry.title
        link = entry.link
        description = entry.description

        # Generate summary
        try:
            summary = summarizer(description, max_length=50, min_length=25, do_sample=False)
            summary_text = summary[0]["summary_text"]
        except Exception:
            summary_text = "Could not generate summary."

        articles.append({"title": title, "link": link, "summary": summary_text})
    return articles

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-news", methods=["POST"])
def get_news():
    category = request.json.get("category", "technology")
    feed_url = RSS_FEEDS.get(category.lower(), RSS_FEEDS["technology"])
    news = fetch_and_summarize(feed_url)
    return jsonify(news)

if __name__ == "__main__":
    app.run(debug=True)
