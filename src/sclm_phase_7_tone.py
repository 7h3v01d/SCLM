# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 7: Sarcasm & Tone Detection
#
# Objective:
# To create a component that can detect non-literal tones like sarcasm
# by looking for contextual clues and linguistic patterns.
# -----------------------------------------------------------------------------

class ToneEngine:
    """
    Analyzes a sentence to detect non-literal tones like sarcasm.
    """
    def __init__(self):
        """
        Initializes the engine with simple lists of words that can indicate
        sarcasm when used in a negative context.
        """
        self.sarcastic_positives = ["great", "perfect", "fantastic", "wonderful", "lovely"]
        self.negative_context_verbs = ["spill", "break", "lose", "forget", "drop"]

    def analyze_thought(self, core_thought: dict) -> dict:
        """
        Analyzes the core thought for signs of sarcasm and enriches it.
        """
        # Add a 'tone' field to the thought, defaulting to neutral.
        core_thought["tone"] = "neutral"
        
        sentence = core_thought.get("input_sentence", "").lower()
        action = core_thought.get("action", "")

        # A simple rule for sarcasm:
        # Does the sentence contain a highly positive word AND a negative action?
        has_positive_word = any(word in sentence for word in self.sarcastic_positives)
        has_negative_context = action in self.negative_context_verbs

        if has_positive_word and has_negative_context:
            core_thought["tone"] = "sarcastic"
            
        return core_thought
