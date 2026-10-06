# CyberGuard AI

A responsive cybersecurity awareness dashboard built with HTML, CSS, and vanilla JavaScript, hosted in Streamlit. The dashboard's quiz results, safety score, preferences, and chat history are stored in the browser. Chat replies use a local Ollama model.

## Run locally

Install the Python dependencies, install [Ollama](https://ollama.com/), and download the configured model:

```powershell
pip install -r requirements.txt
ollama pull llama3.2:3b
streamlit run Bot.py
```

Open the Streamlit URL shown in the terminal. Ollama must be running locally for AI chat replies; the rest of the dashboard works without it.

## Demo notes

- The phishing detector uses transparent pattern matching and is not a live threat-intelligence service.
- In Streamlit, chat questions are passed from the JavaScript dashboard to `AI.py`, which calls the local Ollama model. Opening `index.html` directly runs the browser-only mock chat.
- Google Fonts and Lucide icons load from their CDNs; the dashboard remains usable if those resources are unavailable.
