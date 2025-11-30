# Smart Study & Exam Planner Agent

This is the ADK-based implementation of my capstone project for the Google x Kaggle Agents Intensive Program.

## Features
- Generates daily/weekly study plans
- Tracks progress
- Stores memory across sessions
- Creates revision quiz prompts
- Multi-agent design (planner, tracker, tutor)
- Uses Google ADK and Gemini

## Files
- `agent.py` – contains the ADK agent and tools
- `data/progress.json` – automatically saved memory file

## How to run (local)
1. Install ADK:
   ```bash
   pip install google-adk
