"""
Web Integration Module for Voris
Handles web searches, general knowledge, weather data, and API integrations
"""

import requests
import json
from datetime import datetime
import re

class WebModule:
    """Handles web-based operations and API integrations"""
    
    def __init__(self):
        self.user_agent = "Voris AI Assistant/1.0"
        self.headers = {"User-Agent": self.user_agent}
        self.weather_api_key = None  # Users can add their own API key
    
    def search_web(self, query, num_results=5):
        """
        Perform web search using DuckDuckGo Instant Answer API
        """
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            result = {
                "success": True,
                "query": query,
                "abstract": data.get("Abstract", ""),
                "abstract_source": data.get("AbstractSource", ""),
                "abstract_url": data.get("AbstractURL", ""),
                "answer": data.get("Answer", ""),
                "definition": data.get("Definition", ""),
                "definition_source": data.get("DefinitionSource", ""),
                "related_topics": []
            }
            
            # Add related topics
            for topic in data.get("RelatedTopics", [])[:num_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    result["related_topics"].append({
                        "text": topic.get("Text", ""),
                        "url": topic.get("FirstURL", "")
                    })
            
            return result
            
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Search failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_wikipedia_summary(self, topic):
        """
        Get Wikipedia summary for a topic
        """
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
            
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "title": data.get("title", ""),
                "summary": data.get("extract", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "thumbnail": data.get("thumbnail", {}).get("source", "") if "thumbnail" in data else None
            }
            
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Wikipedia lookup failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_weather(self, location=None):
        """
        Get weather information using wttr.in (no API key needed)
        """
        try:
            # Clean up location - remove time references
            if location:
                import re
                location = re.sub(r'\s+(tonight|today|tomorrow|this\s+week|this\s+weekend)\s*$', '', location, flags=re.IGNORECASE)
                location = location.strip()
            
            # Use wttr.in which provides weather without API key
            # Clean location for URL
            if location:
                # Remove any trailing question marks or spaces
                location = location.rstrip('? ').strip()
                url = f"https://wttr.in/{location}?format=j1"
            else:
                url = "https://wttr.in/?format=j1"
            
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            current = data["current_condition"][0]
            
            return {
                "success": True,
                "location": data["nearest_area"][0]["areaName"][0]["value"],
                "region": data["nearest_area"][0].get("region", [{}])[0].get("value", ""),
                "country": data["nearest_area"][0]["country"][0]["value"],
                "temperature_c": current["temp_C"],
                "temperature_f": current["temp_F"],
                "condition": current["weatherDesc"][0]["value"],
                "humidity": current["humidity"],
                "wind_speed": current["windspeedKmph"],
                "wind_dir": current["winddir16Point"],
                "feels_like_c": current["FeelsLikeC"],
                "feels_like_f": current["FeelsLikeF"]
            }
            
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Weather lookup failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def answer_question(self, question):
        """
        Attempt to answer a general knowledge question
        Uses multiple sources to find the best answer
        """
        question_lower = question.lower()
        
        # For current/time-sensitive questions, prioritize DuckDuckGo instant answers
        is_current_query = any(word in question_lower for word in ["current", "who is the", "latest", "today", "now", "2024", "2025"])
        
        # Try DuckDuckGo first
        search_result = self.search_web(question)
        
        if search_result["success"]:
            # Check for instant answer
            if search_result["answer"]:
                return {
                    "success": True,
                    "answer": search_result["answer"],
                    "source": "DuckDuckGo Instant Answer"
                }
            
            # For current queries, prefer related topics (more likely to have current info)
            if is_current_query and search_result["related_topics"]:
                # Get the first related topic which is usually most relevant
                first_topic = search_result["related_topics"][0]["text"]
                return {
                    "success": True,
                    "answer": first_topic,
                    "source": "DuckDuckGo",
                    "url": search_result["related_topics"][0]["url"]
                }
            
            # Check for abstract
            if search_result["abstract"]:
                # For current queries, only use abstract if it seems specific enough
                if is_current_query and len(search_result["abstract"]) < 300:
                    return {
                        "success": True,
                        "answer": search_result["abstract"],
                        "source": search_result["abstract_source"],
                        "url": search_result["abstract_url"]
                    }
                elif not is_current_query:
                    return {
                        "success": True,
                        "answer": search_result["abstract"],
                        "source": search_result["abstract_source"],
                        "url": search_result["abstract_url"]
                    }
            
            # Check for definition
            if search_result["definition"]:
                return {
                    "success": True,
                    "answer": search_result["definition"],
                    "source": search_result["definition_source"]
                }
            
            # Use related topics as fallback
            if search_result["related_topics"] and not is_current_query:
                return {
                    "success": True,
                    "answer": search_result["related_topics"][0]["text"],
                    "source": "DuckDuckGo",
                    "url": search_result["related_topics"][0]["url"]
                }
        
        # If DuckDuckGo doesn't have an answer and it's NOT a current query, try Wikipedia
        # Extract potential topic from question
        if not is_current_query:
            topic = self.extract_topic_from_question(question)
            if topic:
                wiki_result = self.get_wikipedia_summary(topic)
                if wiki_result["success"]:
                    return {
                        "success": True,
                        "answer": wiki_result["summary"],
                        "source": "Wikipedia",
                        "url": wiki_result["url"]
                    }
        else:
            # For current queries where we couldn't get specific info, provide helpful guidance
            return {
                "success": True,
                "answer": "I apologize, but I don't have access to real-time information or current events. My knowledge may be limited for time-sensitive questions. For the most up-to-date information, I recommend checking a news website or search engine.",
                "source": "Voris"
            }
        
        return {
            "success": False,
            "error": "Could not find a reliable answer"
        }
    
    def extract_topic_from_question(self, question):
        """
        Extract the main topic from a question
        """
        # Handle special current event queries
        question_lower = question.lower()
        
        # For current president queries, be more specific
        if "president" in question_lower:
            if "current" in question_lower or "who is the" in question_lower:
                # Extract country if mentioned
                if "usa" in question_lower or "united states" in question_lower or "america" in question_lower:
                    return "President of the United States"
                return "current president"
        
        # Remove only articles and basic question words, keep important context words
        question_words = ["who", "what", "when", "where", "why", "how", "is", "are", "was", "were", 
                         "the", "a", "an", "of"]
        
        words = question.lower().split()
        filtered_words = [w for w in words if w not in question_words]
        
        if filtered_words:
            return " ".join(filtered_words)
        return None
    
    def get_location_info(self):
        """
        Get current location information based on IP with Google Maps integration
        """
        try:
            # Using ip-api.com (free, no key needed)
            url = "http://ip-api.com/json/"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data["status"] == "success":
                lat = data["lat"]
                lon = data["lon"]
                city = data["city"]
                region = data["regionName"]
                country = data["country"]
                
                # Generate Google Maps URLs
                maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                maps_search_url = f"https://www.google.com/maps/search/{city},+{region},+{country}".replace(" ", "+")
                
                return {
                    "success": True,
                    "country": country,
                    "region": region,
                    "city": city,
                    "timezone": data["timezone"],
                    "latitude": lat,
                    "longitude": lon,
                    "coordinates": f"{lat}, {lon}",
                    "isp": data["isp"],
                    "maps_url": maps_url,
                    "maps_search_url": maps_search_url
                }
            else:
                return {
                    "success": False,
                    "error": "Could not determine location"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Location lookup failed: {str(e)}"
            }
    
    def get_current_president(self, country="United States"):
        """
        Get current president/leader of a country
        """
        query = f"current president of {country}"
        return self.answer_question(query)
    
    def get_specific_info(self, query):
        """
        Get specific current information (like current president, current events)
        Uses more targeted queries
        """
        # For very specific current queries, try DuckDuckGo instant answer first
        search_result = self.search_web(query)
        
        if search_result["success"] and search_result["answer"]:
            return {
                "success": True,
                "answer": search_result["answer"],
                "source": "DuckDuckGo"
            }
        
        # If no instant answer, provide best available info
        return self.answer_question(query)
    
    def search_maps(self, query):
        """
        Generate Google Maps search URL for a location or place
        """
        try:
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            maps_url = f"https://www.google.com/maps/search/{encoded_query}"
            
            return {
                "success": True,
                "query": query,
                "maps_url": maps_url,
                "message": f"Google Maps search for: {query}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_directions(self, origin, destination):
        """
        Generate Google Maps directions URL
        """
        try:
            import urllib.parse
            origin_encoded = urllib.parse.quote(origin)
            dest_encoded = urllib.parse.quote(destination)
            
            directions_url = f"https://www.google.com/maps/dir/{origin_encoded}/{dest_encoded}"
            
            return {
                "success": True,
                "origin": origin,
                "destination": destination,
                "directions_url": directions_url,
                "message": f"Directions from {origin} to {destination}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }    
    def get_ip_info(self, ip_address=None):
        """
        Get detailed information about an IP address
        If no IP provided, shows info about current public IP
        """
        try:
            if ip_address:
                url = f"http://ip-api.com/json/{ip_address}"
            else:
                url = "http://ip-api.com/json/"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data["status"] == "success":
                return {
                    "success": True,
                    "ip": data["query"],
                    "country": data["country"],
                    "country_code": data["countryCode"],
                    "region": data["regionName"],
                    "city": data["city"],
                    "zip": data.get("zip", "N/A"),
                    "latitude": data["lat"],
                    "longitude": data["lon"],
                    "timezone": data["timezone"],
                    "isp": data["isp"],
                    "org": data.get("org", "N/A"),
                    "as": data.get("as", "N/A")
                }
            else:
                return {
                    "success": False,
                    "error": "Could not retrieve IP information"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_website_status(self, url):
        """
        Check if a website is online and get response time
        """
        try:
            import time
            
            # Add http:// if not present
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            start_time = time.time()
            response = requests.head(url, timeout=5, allow_redirects=True)
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                "success": True,
                "url": url,
                "status_code": response.status_code,
                "status_text": "Online" if response.status_code < 400 else "Error",
                "response_time_ms": round(response_time, 2),
                "online": response.status_code < 400
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "online": False,
                "error": str(e)
            }
    
    def get_cryptocurrency_price(self, crypto="bitcoin"):
        """
        Get current cryptocurrency prices
        """
        try:
            # Using CoinGecko API (free, no key needed)
            crypto_ids = {
                "bitcoin": "bitcoin",
                "btc": "bitcoin",
                "ethereum": "ethereum",
                "eth": "ethereum",
                "dogecoin": "dogecoin",
                "doge": "dogecoin",
                "litecoin": "litecoin",
                "ltc": "litecoin",
                "ripple": "ripple",
                "xrp": "ripple",
                "cardano": "cardano",
                "ada": "cardano"
            }
            
            crypto_id = crypto_ids.get(crypto.lower(), crypto.lower())
            
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": crypto_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_market_cap": "true"
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if crypto_id in data:
                return {
                    "success": True,
                    "crypto": crypto,
                    "crypto_id": crypto_id,
                    "price_usd": data[crypto_id].get("usd", 0),
                    "change_24h": data[crypto_id].get("usd_24h_change", 0),
                    "market_cap": data[crypto_id].get("usd_market_cap", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"Cryptocurrency '{crypto}' not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def convert_currency(self, amount, from_currency, to_currency):
        """
        Convert between currencies
        """
        try:
            # Using exchangerate-api.com (free tier available)
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if to_currency.upper() in data["rates"]:
                rate = data["rates"][to_currency.upper()]
                converted = amount * rate
                
                return {
                    "success": True,
                    "amount": amount,
                    "from_currency": from_currency.upper(),
                    "to_currency": to_currency.upper(),
                    "rate": rate,
                    "converted_amount": round(converted, 2)
                }
            else:
                return {
                    "success": False,
                    "error": f"Currency '{to_currency}' not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_random_fact(self):
        """
        Get a random interesting fact
        """
        try:
            url = "https://uselessfacts.jsph.pl/random.json?language=en"
            
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "fact": data.get("text", ""),
                "source": "Useless Facts API"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_joke(self):
        """
        Get a random joke
        """
        try:
            url = "https://official-joke-api.appspot.com/random_joke"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "setup": data.get("setup", ""),
                "punchline": data.get("punchline", ""),
                "type": data.get("type", "general")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def shorten_url(self, long_url):
        """
        Shorten a URL using TinyURL
        """
        try:
            url = f"https://tinyurl.com/api-create.php?url={long_url}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            short_url = response.text.strip()
            
            return {
                "success": True,
                "original_url": long_url,
                "short_url": short_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_github_user(self, username):
        """
        Get GitHub user information
        """
        try:
            url = f"https://api.github.com/users/{username}"
            
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "username": data.get("login", ""),
                "name": data.get("name", "N/A"),
                "bio": data.get("bio", "No bio"),
                "public_repos": data.get("public_repos", 0),
                "followers": data.get("followers", 0),
                "following": data.get("following", 0),
                "location": data.get("location", "N/A"),
                "company": data.get("company", "N/A"),
                "blog": data.get("blog", "N/A"),
                "profile_url": data.get("html_url", "")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }