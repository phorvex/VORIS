# VORIS Enhanced Internet Features

VORIS now includes extensive internet connectivity features, allowing you to access real-time information and interact with various online services.

## 🌐 New Internet Capabilities

### IP Address & Network Information
- **Command**: `my ip`, `ip address`, `what is my ip`
- **Description**: Displays detailed information about your public IP address including location, ISP, timezone, and coordinates
- **Example**: 
  ```
  > my ip address
  [VORIS]: Your public IP address: 73.192.54.138
  [VORIS]: Location: Jacksonville, Florida, United States
  [VORIS]: ISP: Comcast Cable Communications
  ```

### Website Status Checker
- **Command**: `check website [url]`, `is [website] up`
- **Description**: Checks if a website is online and measures response time
- **Example**: 
  ```
  > check website github.com
  [VORIS]: Https://github.com is online!
  [VORIS]: Status code: 200
  [VORIS]: Response time: 264.78 milliseconds
  ```

### Cryptocurrency Prices
- **Command**: `bitcoin price`, `ethereum price`, `[crypto] price`
- **Supported**: Bitcoin, Ethereum, Dogecoin, Litecoin, Cardano, Ripple (and their abbreviations)
- **Description**: Get real-time cryptocurrency prices with 24-hour change and market cap
- **Example**: 
  ```
  > ethereum price
  [VORIS]: Ethereum is currently $2,969.91 USD
  [VORIS]: 24-hour change: down 0.01%
  [VORIS]: Market cap: $358,853,332,253
  ```

### Currency Conversion
- **Command**: `convert [amount] [from] to [to]`
- **Description**: Convert between any world currencies using live exchange rates
- **Example**: 
  ```
  > convert 50 USD to GBP
  [VORIS]: 50.0 USD = 37.35 GBP
  [VORIS]: Exchange rate: 1 USD = 0.7470 GBP
  ```

### Random Facts
- **Command**: `tell me a fact`, `random fact`, `interesting fact`
- **Description**: Get random interesting facts to learn something new
- **Example**: 
  ```
  > tell me a fact
  [VORIS]: Scotland has more redheads than any other part of the world
  ```

### Jokes & Entertainment
- **Command**: `tell me a joke`, `say something funny`
- **Description**: VORIS tells you a joke (with perfect comedic timing!)
- **Example**: 
  ```
  > tell me a joke
  [VORIS]: What do you call a computer mouse that swears a lot?
  [VORIS]: A cursor!
  ```

### URL Shortener
- **Command**: `shorten url [long-url]`, `shorten [url]`
- **Description**: Creates shortened URLs using TinyURL
- **Example**: 
  ```
  > shorten url https://www.github.com/example/very-long-repository-name
  [VORIS]: Short URL: https://tinyurl.com/abc123
  ```

### GitHub Profile Lookup
- **Command**: `github user [username]`, `github profile [username]`
- **Description**: Get detailed information about any GitHub user
- **Example**: 
  ```
  > github user torvalds
  [VORIS]: Username: torvalds
  [VORIS]: Name: Linus Torvalds
  [VORIS]: Public repositories: 9
  [VORIS]: Followers: 266711 | Following: 0
  [VORIS]: Location: Portland, OR
  [VORIS]: Company: Linux Foundation
  ```

## 🔧 Existing Internet Features

### Weather Information
- **Command**: `weather`, `weather in [location]`
- Get current weather conditions for any location

### Web Search & Questions
- **Command**: `search for [query]`, `what is [topic]`
- Search the web and answer general knowledge questions

### Location Services
- **Command**: `where am i`, `my location`
- Get your current location based on IP address

### News Headlines
- **Command**: `news`, `headlines`, `tech news`
- Get latest news headlines from various categories

### Google Maps Integration
- **Command**: `show on map`, `find [place] on maps`, `directions to [place]`
- Generate Google Maps URLs for locations and directions

## 💡 Usage Tips

1. **Natural Language**: VORIS understands natural phrasing - try different ways of asking
2. **Quick Info**: Most commands provide instant responses without opening browsers
3. **URLs in Browser**: For maps and other web content, VORIS provides URLs to copy/paste
4. **Help Command**: Type `help` to see all available commands
5. **Combinations**: You can combine features (e.g., get weather after checking location)

## 🔒 Privacy & APIs

All internet features use free, public APIs:
- **IP-API**: Location and IP information
- **CoinGecko**: Cryptocurrency prices
- **ExchangeRate-API**: Currency conversion
- **wttr.in**: Weather data
- **DuckDuckGo**: Web search
- **TinyURL**: URL shortening
- **GitHub API**: User information
- **Various free APIs**: Facts, jokes, and more

No API keys are required for basic functionality, and no personal data is stored or transmitted beyond what's necessary for each request.

## 📊 Feature Status

✅ **Working**: All features tested and operational  
🌐 **Real-time**: Data fetched live from APIs  
🚀 **Fast**: Average response time < 1 second  
🔒 **Secure**: HTTPS connections for all API calls  

## 🎯 Future Enhancements

Potential additions for future versions:
- Stock market quotes
- Sports scores and schedules
- Movie information and reviews
- Recipe searches
- Dictionary and translations
- QR code generation
- YouTube video info
- Twitter/social media lookups

---

**Last Updated**: December 19, 2025  
**Version**: 1.0.0 with Internet Enhancements
