import streamlit as st
import requests
from anthropic import Anthropic

ANTHROPIC_API_KEY = "your_anthropic_api_key"
TAVILY_API_KEY = "your_tavily_api_key"

claude = Anthropic(api_key=ANTHROPIC_API_KEY)

def get_llm_response(query):
    try:
        response = claude.completions.create(
            model="claude-v1",
            prompt=f"\n\nHuman: {query}\n\nAssistant:",
            max_tokens=300
        )
        if response and 'completion' in response:
            return response['completion']
        else:
            return "No response from LLM."
    except Exception as e:
        return f"Error in getting LLM response: {str(e)}"

def get_tavily_results(query):
    try:
        response = requests.get(
            f"https://api.tavily.com/v1/search?query={query}",
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"TAVILY API error: {response.status_code} {response.text}"}
    except Exception as e:
        return {"error": f"Error with TAVILY API: {str(e)}"}

def generate_response_and_search(query):
    try:
        llm_response = get_llm_response(query)
        search_results = get_tavily_results(llm_response)
        final_response = f"### LLM Response ###\n{llm_response}\n\n### Search Results from TAVILY ###\n"
        if "items" in search_results:
            for i, result in enumerate(search_results.get("items", [])):
                final_response += f"{i + 1}. {result.get('title', 'No Title')} - {result.get('url', 'No URL')}\n"
        elif "error" in search_results:
            final_response += f"TAVILY API Error: {search_results['error']}\n"
        else:
            final_response += "No search results found.\n"
        return final_response
    except Exception as e:
        return f"Error in generating response: {str(e)}"

def main():
    st.title("LLM Query and Tavily Search")
    query = st.text_input("Enter your query:", "")
    if st.button("Submit"):
        if query:
            with st.spinner("Processing..."):
                response = generate_response_and_search(query)
                st.subheader("Response and Search Results")
                st.text(response)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
