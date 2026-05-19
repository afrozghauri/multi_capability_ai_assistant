import json
import math
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def calculate(expression):
    """Performs mathematical calculations."""
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})
    
def web_search(query):
    """Performs a real web search using DuckDuckGo."""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))
        return json.dumps({"query": query, "results": results})
    except Exception as e:
        return json.dumps({"error": str(e)})

def analyze_data(numbers):
    """Analyzes a list of numbers and returns statistics."""
    try:
        nums = [float(x) for x in numbers]
        result = {
            "count": len(nums),
            "sum": sum(nums),
            "average": sum(nums) / len(nums),
            "min": min(nums),
            "max": max(nums)
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_news(topic):
    """Fetches real news headlines from NewsAPI."""
    try:
        api_key = os.getenv("NEWSAPI_KEY")
        url = "https://newsapi.org/v2/everything"
        parameters = {
            "q": topic,
            "apiKey": api_key,
            "pageSize": 1,
            "sortBy": "publishedAt",
            "language": "en"
        }
        response = requests.get(url, params=parameters)
        data = response.json()

        if data["status"] != "ok":
            return json.dumps({"error": data.get("message", "Unknown error")})
        
        articles = [
            {
                "title": a["title"],
                "source": a["source"]["name"],
                "description": a["description"],
                "url": a["url"]
            }
            for a in data["articles"]
        ]
        return json.dumps({"topic": topic, "articles": articles})
    except Exception as e:
        return json.dumps({"error": str(e)})
    
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Performs mathematical calculations. Use for any math question.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The mathematical expression to evaluate, e.g. '2 + 2' or 'sqrt(16)'"}
            },
            "required": ["expression"]
        }
    }
}

web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Searches the web for information on any topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    }
}

data_analyzer_tool = {
    "type": "function",
    "function": {
        "name": "analyze_data",
        "description": "Analyzes a list of numbers and returns statistics like sum, average, min and max.",
        "parameters": {
            "type": "object",
            "properties": {
                "numbers": {"type": "array", "items": {"type": "number"}, "description": "List of numbers to analyze"}
            },
            "required": ["numbers"]
        }
    }
}

news_tool = {
    "type": "function",
    "function": {
        "name": "get_news",
        "description": "Fetches the latest news headlines for a given topic. Use when user asks about news or when researching before writing an email.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The topic to search news for"}
            },
            "required": ["topic"]
        }
    }
}

tools = [calculator_tool, web_search_tool, data_analyzer_tool, news_tool]

functions = {
    "calculate": calculate,
    "web_search": web_search,
    "analyze_data": analyze_data,
    "get_news": get_news
}
