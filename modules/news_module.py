"""
News Module for Voris
Fetches and displays news headlines from various sources
"""

import requests
from datetime import datetime

class NewsModule:
    """Handles news retrieval and headlines"""
    
    def __init__(self):
        self.user_agent = "Voris AI Assistant/1.0"
        self.headers = {"User-Agent": self.user_agent}
    
    def get_top_headlines(self, country="us", category=None, limit=5):
        """
        Get top news headlines
        Uses NewsAPI (free tier - requires API key for full access)
        Falls back to RSS feeds
        """
        # Try RSS feeds (no API key needed)
        return self.get_rss_headlines(category, limit)
    
    def get_rss_headlines(self, category=None, limit=5):
        """
        Get headlines from RSS feeds
        """
        try:
            # BBC News RSS
            if category == "technology" or category == "tech":
                url = "http://feeds.bbci.co.uk/news/technology/rss.xml"
            elif category == "business":
                url = "http://feeds.bbci.co.uk/news/business/rss.xml"
            elif category == "science":
                url = "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
            elif category == "world":
                url = "http://feeds.bbci.co.uk/news/world/rss.xml"
            else:
                url = "http://feeds.bbci.co.uk/news/rss.xml"  # Top stories
            
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            # Parse RSS XML
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            headlines = []
            for item in root.findall('.//item')[:limit]:
                title = item.find('title')
                description = item.find('description')
                link = item.find('link')
                pub_date = item.find('pubDate')
                
                headlines.append({
                    "title": title.text if title is not None else "",
                    "description": description.text if description is not None else "",
                    "url": link.text if link is not None else "",
                    "published": pub_date.text if pub_date is not None else ""
                })
            
            return {
                "success": True,
                "headlines": headlines,
                "source": "BBC News RSS",
                "category": category or "top stories"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_news(self, query, limit=5):
        """
        Search for news articles about a specific topic
        """
        try:
            # Use DuckDuckGo News search
            url = "https://api.duckduckgo.com/"
            params = {
                "q": f"{query} news",
                "format": "json",
                "no_html": 1
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            for topic in data.get("RelatedTopics", [])[:limit]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", "")
                    })
            
            return {
                "success": True,
                "results": results,
                "query": query
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tech_news(self, limit=5):
        """Get technology news specifically"""
        return self.get_rss_headlines("technology", limit)
    
    def get_business_news(self, limit=5):
        """Get business news"""
        return self.get_rss_headlines("business", limit)
    
    def get_science_news(self, limit=5):
        """Get science news"""
        return self.get_rss_headlines("science", limit)
