import requests
from dotenv import load_dotenv
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path = os.path.join(base_dir, '../../.env'))
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

def fetch_articles(query, from_date, to_date, num_articles):
    all_articles = []
    page = 1
    per_page = 100  # max number of articles per request for Newscatcher
    headers = {"x-api-key": NEWS_API_KEY}

    while len(all_articles) < num_articles:
        params = {
            "q": query,
            "lang": "en",
            "from": from_date,
            "to": to_date,
            "page": page,
            "page_size": per_page,
            "sort_by": "relevancy"
        }

        response = requests.get("https://api.newscatcherapi.com/v2/search", params=params, headers=headers)

        if response.status_code != 200:
            print(f"Failed to get data: {response.content}")
            break

        articles = response.json().get('articles', [])
        all_articles.extend(articles)

        if len(articles) < per_page:
            break  # No more articles available

        page += 1

    articles = pd.DataFrame(all_articles)

    columns_to_keep = ['title', 'excerpt', 'published_date', 'topic', 'link']
    articles = articles.loc[:, columns_to_keep]

    articles.dropna(subset=['excerpt'], inplace=True)
    articles = articles[articles['excerpt'].str.strip() != '']

    return articles
