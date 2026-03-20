import requests

def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url).json()

        result = response.get("AbstractText")

        if result:
            return result
        else:
            return "No useful result found"

    except Exception as e:
        return f"Web search error: {str(e)}"