import requests
import beautifulsoup4

r = requests.get("http://example.webscraping.com/")

print(r.status)
