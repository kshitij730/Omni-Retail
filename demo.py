import os
import sys
from dotenv import load_dotenv

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.orchestrator_groq import run_omni_query

# Load env if present
load_dotenv()

def main():
    print("Initializing Omni-Retail Multi-Agent System (Pure Groq)...")
    
    if not os.environ.get("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY not found in environment variables.")
        return

    # Scenario 1: The Missing Package & Ticket
    query1 = (
        "I am Alice Johnson. I ordered a 'Gaming Monitor' recently, but it hasn't arrived. "
        "I opened a ticket about this. Can you tell me where the package is right now "
        "and the status of my ticket?"
    )
    
    # Scenario 2: Refund Verification
    query2 = (
        "I am Alice Johnson. I returned a 'Wireless Mouse'. "
        "Can you check if a refund transaction appears in my wallet for that order, "
        "and if the support ticket is marked as resolved?"
    )
    
    # Scenario 3: Cross-Domain Logistics
    query3 = (
        "Check on Bob Smith. Does he have any orders currently processing? "
        "Also, based on his payment history, what is his current wallet balance?"
    )

    queries = [query1, query2, query3]
    
    print("\n" + "="*50)
    print("STARTING DEMONSTRATION")
    print("="*50)

    for i, q in enumerate(queries, 1):
        print(f"\n\n### DEMO SCENARIO {i} ###")
        try:
            print(f"User Query: {q}")
            result = run_omni_query(q)
            print(f"\nResult:\n{result}")
        except Exception as e:
            print(f"Error processing query: {e}")
            
    print("\n" + "="*50)
    print("DEMONSTRATION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()
