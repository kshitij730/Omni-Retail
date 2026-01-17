import json
from ..orchestrator_groq import OmniAgent

class SupportAgent:
    """The modern CareDesk Agent. Part of the Unified Omni-Brain."""
    def __init__(self):
        self.brain = OmniAgent()

    def query(self, user_query):
        # This agent now uses the consolidated high-performance engine
        ans, thoughts = self.brain.run_query(user_query)
        return ans

# ... existing schema logic for visibility ...
SCHEMA = {
    "Tickets": ["TicketID", "UserID", "ReferenceID", "IssueType", "Status"],
    "TicketMessages": ["MessageID", "TicketID", "Sender", "Content", "Timestamp"]
}
