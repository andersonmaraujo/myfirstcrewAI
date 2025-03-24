# 🧪 Research Copilot Swarm

Multi-agent LLM system for collaborative literature review and synthesis using [Autogen](https://github.com/microsoft/autogen).

## 🚀 Overview

This PoC tests whether a swarm of LLM agents can break down and answer a complex research query more effectively than a single prompt.

It orchestrates agents to:
1. Retrieve relevant papers.
2. Summarize each one.
3. Compare findings.
4. Output a concise synthesis.

## 🎯 Example Research Prompt

> "What are the latest methods in Retrieval-Augmented Generation (RAG)?"

## 🤖 Agents & Roles

| Agent | Description |
|-------|-------------|
| **Planner** | Breaks down the user query into subtasks. *(Optional in V0)* |
| **Retriever** | Uses Semantic Scholar API to find 3–5 recent papers. |
| **Summarizer** | Extracts key insights from each paper. |
| **Synthesizer** | Compares and synthesizes findings into a final report. |

## 🛠️ Minimal Setup (PoC)

- Hardcoded prompt.
- Static agent configuration (no dynamic planning yet).
- Output is a markdown report.
- No human-in-the-loop required.

## 📦 Tech Stack

- [Autogen](https://github.com/microsoft/autogen)
- OpenAI GPT-4 (or compatible LLM)
- Semantic Scholar API (REST)
- Python

## ✅ Success Criteria

- Agents can coordinate end-to-end with no human help.
- Final report compares at least 3 papers on core methods and tradeoffs.
- Reproducible run with a single config or script.

## 🔧 Getting Started

1. Clone this repo
2. Install requirements:
   ```bash
   pip install autogen openai requests
3. Get an OpenAI API key and Semantic Scholar API key (optional for higher rate limits).
4. Run the script:
   python main.py

## 🧪 Stretch Goals

- Add Planner Agent for dynamic task breakdown
- Let users input arbitrary queries
- PDF ingestion for richer source material
- Human critique / scoring loop
- Compare vs single-prompt baseline

## 📚 Outputs

The final report will look like:

### 🔍 Research Summary: Retrieval-Augmented Generation (RAG)

**Paper 1:** "Title"  
- **Problem:**  
- **Method:**  
- **Results:**  
- **Novelty:**  

**Paper 2:** "Title"  
...

**🧠 Synthesis:**  
- Most common techniques: …
- Notable innovations: …
- Open challenges: …

## 🧠 Why This Matters

Exploring whether LLM-agent collaboration can actually improve scientific research workflows—especially for deep dives into fast-moving fields like AI/ML.
