# search onine for information

import requests


class SearchOnlineService:
    def fetch_web_page(self, url):
        """Fetches and returns the content of a web page."""
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.text

    def search_google(self, query):
        """Simulate a simple Google search and return the first result URL."""
        params = {'q': query}
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://www.google.com/search', params=params, headers=headers)
        response.raise_for_status()
        # Example: Extract and return the first result link
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('a', href=True)
        return link['href']
