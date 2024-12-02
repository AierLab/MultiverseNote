# search online for information
import requests

def fetch_web_page(url):
    """Fetches and returns the content of a web page."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return "Failed to access: " + str(e)

def search_duckduckgo(query):
    """Use the DuckDuckGo Instant Answer API to search for a query and format the response in JSON."""
    url = "https://api.duckduckgo.com/"
    params = {
        'q': query,      # query text
        'format': 'json', # response format
        'no_html': 1,     # Remove HTML from text responses
        'skip_disambig': 1 # Skip disambiguation pages
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract and structure the data into a JSON format
        structured_response = {
            "Heading": data.get("Heading"),
            "Abstract": data.get("Abstract"),
            "AbstractURL": data.get("AbstractURL"),
            "Image": data.get("Image"),
            "RelatedTopics": [],
            "Results": []
        }
        
        # Process RelatedTopics if available
        for topic in data.get("RelatedTopics", []):
            if "Topics" in topic:  # Handle nested topics
                for subtopic in topic["Topics"]:
                    structured_response["RelatedTopics"].append({
                        "Text": subtopic.get("Text"),
                        "FirstURL": subtopic.get("FirstURL")
                    })
            else:
                structured_response["RelatedTopics"].append({
                    "Text": topic.get("Text"),
                    "FirstURL": topic.get("FirstURL")
                })
        
        # Process Results if available
        for result in data.get("Results", []):
            structured_response["Results"].append({
                "Text": result.get("Text"),
                "FirstURL": result.get("FirstURL")
            })

        return structured_response
    except requests.RequestException as e:
        return {"error": str(e)}


FUNCTION_MAPPING = {
    "fetch_web_page": fetch_web_page,
    "search_duckduckgo": search_duckduckgo,
}

TOOLS_DEFINE = [
    {
        "type": "function",
        "function": {
            "name": "fetch_web_page",
            "description": "Fetches and returns the content of a web page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the web page to fetch."
                    }
                },
                "required": [
                    "url"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_duckduckgo",
            "description": "Simulates a simple DuckDuck Go search and returns the first result URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on Duck Duck Go."
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    }
]
