import os
import json
import sqlite3
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
from .utils import execute_sql_query, get_schema

load_dotenv()

# Configuration
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant" # High rate-limit, faster fallback

class OmniAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.current_model = PRIMARY_MODEL
        self.databases = {
            "ShopCore": "DB_ShopCore.db",
            "ShipStream": "DB_ShipStream.db",
            "PayGuard": "DB_PayGuard.db",
            "CareDesk": "DB_CareDesk.db"
        }
        self.schemas = {db: get_schema(path) for db, path in self.databases.items()}
        self.thought_log = []

    def _call_llm(self, messages, temperature=0, json_mode=False):
        """Standard LLM call with built-in rate-limit fallback."""
        kwargs = {
            "messages": messages,
            "model": self.current_model,
            "temperature": temperature,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e) and self.current_model == PRIMARY_MODEL:
                print(f"!!! Rate limit hit on {PRIMARY_MODEL}. Falling back to {FALLBACK_MODEL}...")
                self.current_model = FALLBACK_MODEL # Switch for this session
                kwargs["model"] = FALLBACK_MODEL
                response = self.client.chat.completions.create(**kwargs)
                return response.choices[0].message.content
            else:
                raise e

    def _get_sql_from_llm(self, query: str, db_name: str, context_summary: str = "") -> str:
        """Translates natural language to SQL for a specific database."""
        schema = self.schemas[db_name]
        
        system_prompt = f"""You are a SQLite Expert for the '{db_name}' database.
STRICT SCHEMA:
{schema}

TASK:
Generate a SINGLE SELECT statement for: "{query}"

DOMAINS:
- ShopCore: Find UserID, OrderID, and Name. If user says "I" or "my", find the most RECENT matching order.
- ShipStream: Find StatusUpdate and Warehouse Location using OrderID.
- PayGuard: Find Balance and Transaction details using UserID or OrderID.
- CareDesk: Find Ticket Status, latest Message, and Survey Rating/Comments.

STRICT SCHEMA RULES for "{db_name}":
{schema}
1. ONLY USE TABLES and COLUMNS listed in the schema ABOVE.
2. NO HALLUCINATIONS: Do not guess table or column names (e.g., ShipStream does NOT have tickets or surveys).
3. NO CROSS-DB JOINS: Do not mention other databases.
4. USE SIMPLE JOINS: Join related tables within this DB only.
5. FILTERING: Use these Master IDs: {context_summary}. (e.g., WHERE OrderID = [Value])
6. OUTPUT: Return ONLY the SQL string.
"""
        sql = self._call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User's request: {query}"}
            ]
        )
        sql = sql.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        # Basic SQL safety - ensure it's a SELECT
        if not sql.lower().startswith("select"):
            return "SELECT 'Error: Invalid SQL generated' as Error;"
        return sql

    def run_query(self, user_query: str) -> str:
        """Orchestrates multi-DB query execution without CrewAI."""
        print(f"Analyzing query: {user_query}")
        
        planner_prompt = f"""You are the Omni-Retail Omni-Agent. You handle queries across 4 production platforms:
1. ShopCore: Accounts, Products, Catalog, and initial Order placement. (MANDATORY entry point for "I", "My", or finding Users/Products)
2. ShipStream: Logistics, Shipments, and Tracking. (Depends on OrderID)
3. PayGuard: Balances and Transactions. (Depends on UserID/OrderID)
4. CareDesk: Tickets, Messages, and Surveys. (Depends on UserID/OrderID)

USER QUERY: "{user_query}"

TASK: Identify which platforms need to be queried.
Return your plan as a JSON object with a "plan" key containing a list of database names. 
CRITICAL: If the query is personal ("I", "My") or mentions a product name, you MUST start with "ShopCore" to identify the User/Order.
Example: {{"plan": ["ShopCore", "ShipStream", "PayGuard", "CareDesk"]}}
"""
        plan_content = self._call_llm(
            messages=[{"role": "user", "content": planner_prompt}],
            json_mode=True
        )
        plan_content = plan_content.strip()
        try:
            # Clean possible markdown
            if "```json" in plan_content:
                plan_content = plan_content.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_content:
                plan_content = plan_content.split("```")[1].split("```")[0].strip()
                
            data = json.loads(plan_content)
            
            if isinstance(data, list):
                plan = data
            elif isinstance(data, dict):
                plan = data.get("plan", [])
                if not plan:
                     for v in data.values():
                         if isinstance(v, list):
                             plan = v
                             break
        except Exception as e:
            print(f"Planning error: {e}")
            plan = ["ShopCore", "ShipStream", "PayGuard", "CareDesk"]

        self.thought_log.append(f"Planner decided on: {', '.join(plan)}")
        print(f"Plan: {plan}")
        
        # 2. Sequential Execution with Context Passing
        cumulative_context = {}
        id_hints = {}
        
        for db_name in plan:
            if db_name not in self.databases: continue
            
            # Extract IDs from all results found so far for explicit hints
            context_summary = "No IDs found yet." if not id_hints else json.dumps(id_hints)

            print(f"[{db_name}] Generating SQL...")
            sql = self._get_sql_from_llm(user_query, db_name, context_summary=context_summary)
            print(f"[{db_name}] SQL: {sql}")
            self.thought_log.append(f"Querying {db_name} with SQL: {sql}")
            
            try:
                result_json = execute_sql_query(self.databases[db_name], sql)
                result_data = json.loads(result_json)
                
                # Add to context
                cumulative_context[db_name] = result_data
                
                if isinstance(result_data, list) and len(result_data) > 0:
                    self.thought_log.append(f"Found {len(result_data)} records in {db_name}.")
                    # Update hints from results
                    for record in result_data:
                        for key in ["UserID", "OrderID", "ShipmentID", "ProductID", "TicketID", "WalletID", "TransactionID"]:
                            if key in record and record[key]:
                                id_hints[key] = record[key]
                else:
                    self.thought_log.append(f"No records found in {db_name}.")
            except Exception as e:
                self.thought_log.append(f"Error querying {db_name}: {str(e)}")

        # 3. Final Synthesis
        # 3. Final Synthesis
        # Try to find the user's name from context for a personalized greeting
        user_name = "there"
        for db_res in cumulative_context.values():
            if isinstance(db_res, list) and len(db_res) > 0:
                for record in db_res:
                    # Look for any key that looks like a name
                    for k, v in record.items():
                        if k.lower() in ["name", "username", "customer_name"] and v and isinstance(v, str):
                            user_name = v
                            break
                    if user_name != "there": break
            if user_name != "there": break
        
        synthesis_prompt = f"""You are the Omni-Retail Premium Customer Assistant.
GREETING: Address the customer by their Name found in results.

SEARCH RESULTS FROM DATA NODES:
{json.dumps(cumulative_context, indent=2)}

USER QUERY: "{user_query}"

GOAL: Provide a "Perfect Accuracy" answer in a professional dashboard style.

GUIDELINES:
1. NO FAILURES: Instead of saying "I couldn't find...", describe the status. (e.g., If no shipment info, say "Your order is currently in the processing phase and hasn't been handed to logistics yet.").
2. DATA INTEGRATION: Combine Order details, Tracking status, Wallet balance, and Support ticket history into a single cohesive story.
3. HIGHLIGHTS: Bold (<b>) all IDs, Tracking Numbers, Statuses, and Balances. NEVER use double asterisks **.
4. STRUCTURE: Use a summary paragraph followed by <ul> bits of data.
5. NO TECH-SPEAK: Never mention SQL, JSON, or databases.
6. NO MARKDOWN: Ensure no ** is used in the final response. Use <b> only.
"""
        final_answer = self._call_llm(
            messages=[{"role": "user", "content": synthesis_prompt}]
        )
        
        return final_answer, self.thought_log

def run_omni_query(query: str):
    agent = OmniAgent()
    return agent.run_query(query)
