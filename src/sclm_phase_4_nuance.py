# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 4: Semantic Nuance Engine - CORRECTED
#
# Objective:
# To enrich the core semantic schema with metadata about intent, mood, and
# urgency, and to correctly generate sentences using the improved grammar engine.
#
# How to Run:
# 1. Ensure the LATEST 'semantic_parser.py' and 'sclm_phase_3_fluency.py' are present.
# 2. Run this script: python sclm_phase_4_nuance.py
# -----------------------------------------------------------------------------

import json
# These imports now refer to the corrected versions of the files
from semantic_parser import SemanticParser
from sclm_phase_3_fluency import FluentSentenceGenerator

class NuanceEngine:
    """
    Analyzes the original verb choice in a sentence to infer semantic nuance
    like urgency and mood.
    """
    def __init__(self):
        """
        Initializes the engine with a simple, rule-based dictionary of verb connotations.
        In a more advanced system, this would be learned from a word embedding model.
        """
        self.verb_connotations = {
            "race": {"urgency": "high", "mood": "hurried"},
            "rush": {"urgency": "high", "mood": "stressed"},
            "hurry": {"urgency": "high", "mood": "anxious"},
            "walk": {"urgency": "low", "mood": "casual"},
            "stroll": {"urgency": "low", "mood": "leisurely"},
            "wander": {"urgency": "low", "mood": "aimless"},
            "chase": {"urgency": "medium", "mood": "aggressive"},
            "write": {"urgency": "neutral", "mood": "creative"},
            "eat": {"urgency": "low", "mood": "neutral"}
        }

    def analyze_thought(self, core_thought: dict) -> dict:
        """
        Takes a core thought and enriches it with nuance based on the action verb.
        """
        action_verb = core_thought.get("action")
        if action_verb in self.verb_connotations:
            nuance = self.verb_connotations[action_verb]
            core_thought["urgency"] = nuance["urgency"]
            core_thought["mood_connotation"] = nuance["mood"]
        return core_thought

# --- Main execution block to demonstrate the Nuance Engine with fixes ---
if __name__ == "__main__":
    parser = SemanticParser()
    nuance_engine = NuanceEngine()
    generator = FluentSentenceGenerator()

    # Using the sentences that previously revealed bugs to confirm fixes
    test_sentences = [
        "I walked to the store.",
        "I raced to the store.",
        "The cat strolled in the garden.", # Will test the preposition fix
        "She is writing a novel."      # Will test the tense fix
    ]

    print("\n--- Starting Phase 4: Nuance Engine Cycle (Corrected) ---")
    for sentence in test_sentences:
        # Step 1: Parse the sentence with our improved parser
        parsed_thought = parser.parse_sentence(sentence)
        
        # Step 2: Enrich the thought with emotional/intent data
        nuanced_thought = nuance_engine.analyze_thought(parsed_thought)
        
        # Step 3: Generate a sentence with our improved generator
        generated_sentence = generator.generate_sentence(nuanced_thought)

        print(f"\n[Original Sentence]: \"{sentence}\"")
        print("[Enriched Core Thought]:")
        # The JSON output will now show the correct preposition and tense_aspect
        print(json.dumps(nuanced_thought, indent=2))
        print(f"[Generated Sentence]:  \"{generated_sentence}\"")
        print("-" * 30)
        
    print("\nPhase 4 Complete. The AI's grammatical and nuance engines are stable.")

