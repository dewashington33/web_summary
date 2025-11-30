"""
Website summarizer using Ollama instead of OpenAI.
"""

import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from scraper import fetch_website_contents

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
LLM_MODEL = os.getenv("LLM_MODEL")  # optional for OpenAI/Gemini

system_prompt = """
You are a helpful and knowledgeable assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""


def messages_for(website):
    """Create message list for the LLM."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]


def summarize(url):
    """Fetch and summarize a website using selected LLM provider."""
    website = fetch_website_contents(url)

    if LLM_PROVIDER == "openai":
        # Uses the OpenAI API (requires OPENAI_API_KEY)
        model = LLM_MODEL or "gpt-5-nano"
        client = OpenAI()  # reads OPENAI_API_KEY from env
        resp = client.chat.completions.create(
            model=model,
            messages=messages_for(website),
            temperature=0.3,
        )
        return resp.choices[0].message.content

    if LLM_PROVIDER == "gemini":
        # Uses Google Gemini (requires GEMINI_API_KEY)
        # Import dynamically to avoid a hard import at module load time (prevents static import errors
        # in environments that don't have the package installed).
        try:
            import importlib
            genai = importlib.import_module("google.generativeai")
        except ModuleNotFoundError:
            raise RuntimeError(
                "google.generativeai is not installed; install it with 'pip install google-generative-ai' "
                "to use the GEMINI provider"
            )
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)
        model = LLM_MODEL or "gemini-2.5-pro"
        gm = genai.GenerativeModel(model)
        full_prompt = f"{system_prompt}\n\n{user_prompt_prefix}{website}"
        resp = gm.generate_content(full_prompt)
        return getattr(resp, "text", "").strip()

    # Default: Ollama via OpenAI-compatible endpoint
    ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
    response = ollama.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages_for(website)
    )
    return response.choices[0].message.content


def main():
    """Main entry point for testing."""
    url = input("Enter a URL to summarize: ")
    print("\nFetching and summarizing...\n")
    summary = summarize(url)
    print(summary)


if __name__ == "__main__":
    main()
