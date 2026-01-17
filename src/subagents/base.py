import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class BaseSubAgent:
    """The base architecture for all Omni-Agents."""
    def __init__(self, role_name: str):
        self.role_name = role_name
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def log_thought(self, thought: str):
        print(f"[{self.role_name}] {thought}")
