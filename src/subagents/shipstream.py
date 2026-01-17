from ..orchestrator_groq import OmniAgent

class LogisticsAgent:
    """The modern ShipStream Agent. Part of the Unified Omni-Brain."""
    def __init__(self):
        self.brain = OmniAgent()

    def query(self, user_query):
        ans, thoughts = self.brain.run_query(user_query)
        return ans
