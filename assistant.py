import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, functions

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_tool_calls(tool_calls, messages):
    """Handles tool calls made by the model and returns updated messages."""
    for tool_call in tool_calls:
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        try:
            result = functions[name](**arguments)
        except Exception as e:
            result = json.dumps({"error": str(e)})
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    
    return messages

def email_writer(user_input, tone="formal"):
    """Writes an email based on user description, with optional news research."""
    messages = [
        {
            "role": "system",
            "content": """You are an expert email writer. When given a description of an email needed:
1. If the topic requires current information, use the get_news tool to research first.
2. Write a complete professional email with a subject line.
3. Match the tone requested: formal, friendly, or casual.
4. Format your response as:
Subject: [subject line]

[email body]"""
        },
        {"role": "user", "content": f"Write a {tone} email about: {user_input}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    while response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        messages.append(response.choices[0].message)
        messages = handle_tool_calls(tool_calls, messages)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

    return response.choices[0].message.content

def smart_summarizer(text, length="medium"):
    """Summarizes text and returns analytics."""
    word_count_original = len(text.split())
    
    length_instructions = {
        "short": "1 sentence",
        "medium": "2-3 sentences",
        "long": "4-5 sentences"
    }
    
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert text summarizer. Summarize the given text in {length_instructions.get(length, '2-3 sentences')}.
Return your response in this exact format:
Summary: [your summary here]"""
        },
        {"role": "user", "content": f"Summarize this: {text}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    summary = response.choices[0].message.content
    word_count_summary = len(summary.replace("Summary: ", "").split())
    reduction = round((1 - word_count_summary / word_count_original) * 100, 1)
    
    return f"{summary}\n\n--- Analytics ---\nOriginal word count: {word_count_original}\nSummary word count: {word_count_summary}\nReduction: {reduction}%"

def chat_assistant(user_input, conversation_history):
    """Chat assistant with conversation memory."""
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": """You are a helpful, friendly assistant. You remember everything said 
in the conversation and can answer follow-up questions based on previous exchanges."""
        })
    
    conversation_history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        tools=tools
    )
    
    while response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        conversation_history.append(response.choices[0].message)
        conversation_history = handle_tool_calls(tool_calls, conversation_history)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            tools=tools
        )
    
    assistant_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message, conversation_history

def route_request(user_input, conversation_history):
    """Routes the user input to the correct capability."""
    user_lower = user_input.lower()
    
    # Email writer triggers
    if any(word in user_lower for word in ["write email", "draft email", "compose email", "write an email", "draft an email"]):
        tone = "formal"
        if any(word in user_lower for word in ["friendly", "casual", "informal"]):
            tone = "friendly" if "friendly" in user_lower else "casual"
        print("\n[Email Writer activated]")
        return email_writer(user_input, tone), conversation_history
    
    # Summarizer triggers
    elif any(word in user_lower for word in ["summarize", "summary", "shorten", "tldr", "tl;dr"]):
        length = "medium"
        if "short" in user_lower or "brief" in user_lower:
            length = "short"
        elif "long" in user_lower or "detailed" in user_lower:
            length = "long"
        print("\n[Smart Summarizer activated]")
        text = user_input
        return smart_summarizer(text, length), conversation_history
    
    # Default to chat assistant
    else:
        print("\n[Chat Assistant activated]")
        return chat_assistant(user_input, conversation_history)
    
def main():
    print("=" * 50)
    print("Welcome to your Multi-Capability AI Assistant!")
    print("=" * 50)
    print("\nCapabilities:")
    print("  - Email Writer: 'write an email about...'")
    print("  - Summarizer:   'summarize: [your text]'")
    print("  - Chat:          anything else!")
    print("\nTools available: Calculator, Web Search, Data Analyzer, News Fetcher")
    print("\nType 'help' for this menu again or 'quit' to exit.\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                print("Please enter something!\n")
                continue
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("\nCapabilities:")
                print("  - Email Writer: 'write an email about...'")
                print("  - Summarizer:   'summarize: [your text]'")
                print("  - Chat:          anything else!")
                print("\nTools: Calculator, Web Search, Data Analyzer, News Fetcher\n")
                continue
            
            response, conversation_history = route_request(user_input, conversation_history)
            print(f"\nAssistant: {response}\n")
        
        except Exception as e:
            print(f"Error: {e}\n")
            conversation_history = []

if __name__ == "__main__":
    main()