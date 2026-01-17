# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 9: Final Interactive AI with Knowledge Base
#
# Objective:
# To create a fully interactive AI that integrates all components: parsing,
# nuance, tone, context, and a persistent knowledge base for learning and recall.
# -----------------------------------------------------------------------------

import json
import os

# Import all our custom-built engine components
from semantic_parser import SemanticParser
from sclm_phase_4_nuance import NuanceEngine
from sclm_phase_7_tone import ToneEngine
from sclm_phase_9_knowledge import KnowledgeEngine

class ResponseEngine:
    """
    Decides on the AI's response based on the final, enriched core thought.
    Now includes logic for responding to factual statements and questions.
    """
    def generate_response(self, core_thought: dict, knowledge_engine: KnowledgeEngine) -> str:
        mood = core_thought.get("mood")
        
        # --- 1. Handle Factual Learning ---
        if mood == "declarative_fact" and core_thought.get("learning_fact"):
            subject, relationship, fact = core_thought["learning_fact"]
            success = knowledge_engine.learn_fact(subject, relationship, fact)
            if success:
                return f"Okay, I've learned that the {relationship} of {subject} is {fact}."
            else:
                return "I had trouble remembering that. Could you try phrasing it differently?"

        # --- 2. Handle Factual Questions ---
        if mood == "interrogative_fact" and core_thought.get("query_fact"):
            subject, relationship = core_thought["query_fact"]
            answer = knowledge_engine.query_fact(subject, relationship)
            if answer:
                return f"Based on what I know, the {relationship} of {subject} is {answer}."
            else:
                return f"I'm sorry, I don't have any information about the {relationship} of {subject}."

        # --- 3. Handle Sarcasm ---
        if core_thought.get("tone") == "sarcastic":
            return "Oh no, that sounds frustrating. I hope everything is okay!"

        # --- 4. Handle Standard Questions ---
        if mood == "interrogative":
            return "That's a good question. I'm not sure what the answer is."

        # --- 5. Handle Observations (Statements with attributes) ---
        if core_thought.get("attribute"):
            agent = core_thought.get("agent", "It")
            attribute = core_thought.get("attribute")
            return f"{agent} certainly seems to be {attribute}. That's an interesting observation."

        # --- 6. Default Fallback ---
        return "I understand. Thank you for telling me."


class DialogueManager:
    """The central brain, orchestrating all AI components."""
    def __init__(self):
        # Initialize all engines
        self.parser = SemanticParser()
        self.nuance_engine = NuanceEngine()
        self.tone_engine = ToneEngine()
        self.knowledge_engine = KnowledgeEngine()
        self.response_engine = ResponseEngine()
        
        self.conversation_history = []
        print("SCLM AI with Knowledge Base is online.")

    def _resolve_context(self, current_thought: dict) -> dict:
        agent = current_thought.get("agent")
        obj = current_thought.get("object")
        is_agent_it = isinstance(agent, str) and agent.lower() == "it"
        
        if is_agent_it:
            if self.conversation_history:
                last_thought = self.conversation_history[-1]
                antecedent = last_thought.get("object") or last_thought.get("agent")
                if antecedent:
                    print(f"--- Context Resolved: 'it' -> '{antecedent}' ---")
                    current_thought["agent"] = antecedent
        return current_thought

    def handle_message(self, message: str) -> str:
        # The full SCLM pipeline
        parsed_thought = self.parser.parse_sentence(message)
        contextual_thought = self._resolve_context(parsed_thought)
        nuanced_thought = self.nuance_engine.analyze_thought(contextual_thought)
        final_thought = self.tone_engine.analyze_thought(nuanced_thought)
        
        self.conversation_history.append(final_thought)
        
        # Generate a response using the new, intelligent ResponseEngine
        response = self.response_engine.generate_response(final_thought, self.knowledge_engine)
        
        return response

    def close(self):
        """Gracefully shuts down the AI and its components."""
        self.knowledge_engine.close()


# --- The Main Interactive Chat Loop ---
if __name__ == "__main__":
    # For a consistent experience, we can remove the database file on start.
    # Comment this out if you want the AI to remember facts between sessions.
    if os.path.exists("sclm_knowledge.db"):
        os.remove("sclm_knowledge.db")
        print("Cleared knowledge base for a fresh session.")
        
    ai = DialogueManager()
    print("Type 'quit' to exit.")
    print("-" * 30)

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            ai.close()
            print("AI: Goodbye!")
            break
        
        ai_response = ai.handle_message(user_input)
        print(f"AI: {ai_response}")
