# search onine for information
import requests
from bs4 import BeautifulSoup

class SearchOnlineService:
    def fetch_web_page(self, url: str) -> str:
        """
        Fetches and returns the content of a web page.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            str: The content of the web page.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
        """
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.text

    def search_google(self, query: str) -> str:
        """
        Simulate a simple Google search and return the first result URL.

        Args:
            query (str): The search query to be sent to Google.

        Returns:
            str: The URL of the first search result.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
        """
        params = {'q': query}
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://www.google.com/search', params=params, headers=headers)
        response.raise_for_status()
        
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract and return the first result link
        link = soup.find('a', href=True)
        return link['href']
