from ..orchestrator_groq import OmniAgent

class FinTechAgent:
    """The modern PayGuard Agent. Part of the Unified Omni-Brain."""
    def __init__(self):
        self.brain = OmniAgent()

    def query(self, user_query):
        ans, thoughts = self.brain.run_query(user_query)
        return ans
