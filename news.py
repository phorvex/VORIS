import requests
import xml.etree.ElementTree as ET

NEWS_SOURCES = {
    # General
    "general": "https://feeds.bbci.co.uk/news/rss.xml",
    "bbc": "https://feeds.bbci.co.uk/news/rss.xml",
    "reuters": "https://feeds.reuters.com/reuters/topNews",
    "ap": "https://feeds.apnews.com/rss/apf-topnews",
    "npr": "https://feeds.npr.org/1001/rss.xml",
    "cnn": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "fox": "https://moxie.foxnews.com/google-publisher/latest.xml",
    "guardian": "https://www.theguardian.com/world/rss",
    "al jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "abc": "https://feeds.abcnews.com/abcnews/topstories",
    "nbc": "https://feeds.nbcnews.com/nbcnews/public/news",
    "cbsnews": "https://www.cbsnews.com/latest/rss/main",
    "usatoday": "https://rssfeeds.usatoday.com/UsatodaycomNation-TopStories",
    "newsweek": "https://www.newsweek.com/rss",
    # Tech
    "tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "techcrunch": "https://techcrunch.com/feed/",
    "wired": "https://www.wired.com/feed/rss",
    "verge": "https://www.theverge.com/rss/index.xml",
    "ars": "https://feeds.arstechnica.com/arstechnica/index",
    "arstechnica": "https://feeds.arstechnica.com/arstechnica/index",
    "engadget": "https://www.engadget.com/rss.xml",
    "zdnet": "https://www.zdnet.com/news/rss.xml",
    "hackernews": "https://news.ycombinator.com/rss",
    "hacker news": "https://news.ycombinator.com/rss",
    "mit tech": "https://www.technologyreview.com/feed/",
    # Science
    "science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "nasa": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "scientific american": "https://rss.sciam.com/ScientificAmerican-Global",
    "nature": "https://www.nature.com/nature.rss",
    "space": "https://www.space.com/feeds/all",
    # Health
    "health": "https://feeds.bbci.co.uk/news/health/rss.xml",
    "medscape": "https://www.medscape.com/cx/rss/professional.xml",
    "webmd": "https://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
    # Business
    "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
    "wsj": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "financial times": "https://www.ft.com/?format=rss",
    "economist": "https://www.economist.com/finance-and-economics/rss.xml",
    "forbes": "https://www.forbes.com/real-time/feed2/",
    "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
    # Entertainment
    "entertainment": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    "variety": "https://variety.com/feed/",
    "hollywood reporter": "https://www.hollywoodreporter.com/feed/",
    "rolling stone": "https://www.rollingstone.com/feed/",
    # Sports
    "sports": "https://www.espn.com/espn/rss/news",
    "espn": "https://www.espn.com/espn/rss/news",
    "nfl": "https://www.espn.com/espn/rss/nfl/news",
    "nba": "https://www.espn.com/espn/rss/nba/news",
    "mlb": "https://www.espn.com/espn/rss/mlb/news",
    "nhl": "https://www.espn.com/espn/rss/nhl/news",
    "soccer": "https://www.espn.com/espn/rss/soccer/news",
    # World
    "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "us": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
    "europe": "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
    "asia": "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "middle east": "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "africa": "https://feeds.bbci.co.uk/news/world/africa/rss.xml",
    "latin america": "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml",
    # Politics
    "politics": "https://feeds.npr.org/1014/rss.xml",
    "politico": "https://rss.politico.com/politics-news.xml",
    "hill": "https://thehill.com/news/feed/",
    "axios": "https://api.axios.com/feed/",
    # Security/Hacking
    "security": "https://feeds.feedburner.com/TheHackersNews",
    "hacking": "https://feeds.feedburner.com/TheHackersNews",
    "cybersecurity": "https://feeds.feedburner.com/TheHackersNews",
    "krebs": "https://krebsonsecurity.com/feed/",
    "darknet": "https://www.darknet.org.uk/feed/",
    "threatpost": "https://threatpost.com/feed/",
    # Gaming
    "gaming": "https://www.gamespot.com/feeds/mashup/",
    "ign": "https://feeds.ign.com/ign/all",
    "kotaku": "https://kotaku.com/rss",
    # Crypto
    "crypto": "https://cointelegraph.com/rss",
    "bitcoin": "https://cointelegraph.com/rss",
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    # AI
    "ai": "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "artificial intelligence": "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "openai": "https://techcrunch.com/tag/openai/feed/",
}

def get_news(category="general", count=5):
    category_lower = category.lower().strip()
    url = NEWS_SOURCES.get(category_lower)
    if not url:
        for key in NEWS_SOURCES:
            if category_lower in key or key in category_lower:
                url = NEWS_SOURCES[key]
                break
    if not url:
        url = NEWS_SOURCES["general"]
    try:
        headers = {"User-Agent": "VORIS/1.0"}
        response = requests.get(url, timeout=10, headers=headers)
        root = ET.fromstring(response.content)
        headlines = []
        for item in root.findall(".//item")[:count]:
            title = item.find("title")
            if title is not None and title.text:
                headlines.append(title.text.strip())
        if not headlines:
            return "I couldn't find any news right now."
        result = f"Here are the top {len(headlines)} headlines:\n"
        for i, h in enumerate(headlines, 1):
            result += f"{i}. {h}\n"
        return result.strip()
    except Exception as e:
        return "I couldn't reach the news right now."

def get_news_brief():
    return get_news(category="general", count=5)

def list_sources():
    categories = sorted(set(NEWS_SOURCES.keys()))
    return "Available news sources: " + ", ".join(categories)