# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 8: The Interactive Loop - CORRECTED
#
# Objective:
# To create a simple command-line interface that allows a user to have a
# live, interactive conversation with the fully-built SCLM AI.
#
# How to Run:
# 1. Ensure all other SCLM files (parser, fluency, nuance, tone) are present.
# 2. Run this script: python sclm_interactive_chat.py
# 3. Type sentences and press Enter.
# 4. To end the conversation, type "quit".
# -----------------------------------------------------------------------------

# Import all the necessary components of our AI
from semantic_parser import SemanticParser
from sclm_phase_4_nuance import NuanceEngine
from sclm_phase_7_tone import ToneEngine

# --- **FIX**: The complete, final ResponseEngine is now inside this script ---
class ResponseEngine:
    """
    The creative "frontal lobe" of the AI. It decides what to say next.
    This version includes all rules for sarcasm, questions, and observations.
    """
    def generate_response(self, final_thought: dict) -> str:
        mood = final_thought.get("mood")
        attribute = final_thought.get("attribute")
        tone = final_thought.get("tone")

        # Rule 0: Handle Sarcasm First
        if tone == "sarcastic":
            return "Oh no, that sounds frustrating. I hope everything is okay!"

        # Rule 1: Handle Questions
        if mood == "interrogative":
            return "That's a good question. I'm not sure what the answer is."

        # Rule 2: Respond to Observations (e.g., "The cat is fast")
        if attribute:
            agent = final_thought.get("agent", "That")
            return f"{agent} certainly seems to be {attribute}. It's an interesting observation."

        # Rule 3: Default Acknowledgment for simple statements
        return "I understand. Thank you for telling me."

class DialogueManager:
    """
    The final, complete version of our AI's central brain.
    """
    def __init__(self):
        # Initialize all the component engines
        self.parser = SemanticParser()
        self.nuance_engine = NuanceEngine()
        self.tone_engine = ToneEngine()
        self.response_engine = ResponseEngine() # Uses the class defined above
        self.conversation_history = []
        print("SCLM AI is online. Type 'quit' to exit.")

    def _resolve_context(self, current_thought: dict) -> dict:
        """ Resolves pronouns like 'it' using conversation history. """
        agent = current_thought.get("agent")
        if isinstance(agent, str) and agent.lower() == "it":
            if self.conversation_history:
                last_thought = self.conversation_history[-1]
                antecedent = last_thought.get("object") or last_thought.get("agent")
                if antecedent:
                    print(f"--- (Context Resolved: 'it' -> '{antecedent}') ---")
                    current_thought["agent"] = antecedent
        return current_thought

    def get_response(self, message: str) -> str:
        """
        Processes a single user message through the full AI pipeline and
        returns the final, generated response.
        """
        # --- The Full Thought Cycle ---
        parsed_thought = self.parser.parse_sentence(message)
        contextual_thought = self._resolve_context(parsed_thought)
        nuanced_thought = self.nuance_engine.analyze_thought(contextual_thought)
        final_thought = self.tone_engine.analyze_thought(nuanced_thought)
        
        self.conversation_history.append(final_thought)
        ai_response = self.response_engine.generate_response(final_thought)
        
        return ai_response

# --- Main Interactive Loop ---
if __name__ == "__main__":
    ai = DialogueManager()
    print("-" * 30)

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("AI: Goodbye!")
            break
        
        ai_response = ai.get_response(user_input)
        print(f"AI: {ai_response}")

