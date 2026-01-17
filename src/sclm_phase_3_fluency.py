# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 3: Pattern Recognition & Fluency Layer - UPDATED
#
# Objective:
# To use a library of linguistic patterns to generate natural language.
# -----------------------------------------------------------------------------

import json
from semantic_parser import SemanticParser

class FluentSentenceGenerator:
    """
    Upgraded generator using a pattern library and improved conjugation.
    """
    def __init__(self):
        self.pattern_library = [
            {"structure": ("agent", "action", "object"), "template": "{agent} {action} {object}."},
            {"structure": ("agent", "action", "destination"), "template": "{agent} {action} {preposition} {destination}."},
            {"structure": ("agent", "action", "object", "destination"), "template": "{agent} {action} {object} {preposition} {destination}."},
            # --- **NEW**: A pattern for states of being (Subject-Verb-Attribute) ---
            {"structure": ("agent", "action", "attribute"), "template": "{agent} {action} {attribute}."}
        ]

    def _conjugate_verb(self, verb: str, tense: str, aspect: str, agent: str) -> str:
        if not verb: return ""

        # --- **FIX**: Greatly improved conjugation for the verb 'be' ---
        if verb == "be":
            if tense == "present":
                if agent.lower() == 'i': return "am"
                if agent.lower().endswith('s') or agent.lower() in ['you', 'we', 'they']: return "are"
                return "is"
            if tense == "past":
                if agent.lower().endswith('s') or agent.lower() in ['you', 'we', 'they']: return "were"
                return "was"
            return "be" # Default for future, etc.

        if aspect == "progressive":
            verb_ing = verb + "ing" if not verb.endswith('e') else verb[:-1] + "ing"
            if tense == "present":
                if agent.lower() == 'i': return f"am {verb_ing}"
                if agent.lower().endswith('s') or agent.lower() in ['you', 'we', 'they']: return f"are {verb_ing}"
                return f"is {verb_ing}"
            if tense == "past":
                if agent.lower().endswith('s') or agent.lower() in ['you', 'we', 'they']: return f"were {verb_ing}"
                return f"was {verb_ing}"

        if tense == "past":
            irregular_past = {"write": "wrote", "eat": "ate", "win": "won", "go": "went"}
            if verb in irregular_past: return irregular_past[verb]
            if verb.endswith("e"): return verb + "d"
            if verb.endswith("y") and len(verb) > 1 and verb[-2] not in "aeiou": return verb[:-1] + "ied"
            return verb + "ed"
        
        if tense == "future": return "will " + verb
        
        if tense == "present":
            if agent.lower() not in ["i", "you", "we", "they"] and not agent.lower().endswith('s'):
                if verb.endswith(("s", "sh", "ch", "x", "z")): return verb + "es"
                if verb.endswith("y") and len(verb) > 1 and verb[-2] not in "aeiou": return verb[:-1] + "ies"
                return verb + "s"
        
        return verb

    def generate_sentence(self, core_thought: dict) -> str:
        # Now checks for 'attribute' as a possible component
        thought_structure = tuple(key for key in ["agent", "action", "object", "destination", "attribute"] if core_thought.get(key))

        matching_pattern = None
        for pattern in self.pattern_library:
            if tuple(pattern["structure"]) == thought_structure:
                matching_pattern = pattern
                break
        
        if not matching_pattern:
            # Fallback for simple agent-action sentences
            if "agent" in core_thought and "action" in core_thought:
                 matching_pattern = {"template": "{agent} {action}."}
            else:
                return "I have a thought, but no pattern to express it yet."

        agent = core_thought.get("agent", "")
        action = core_thought.get("action", "")
        tense = core_thought.get("tense")
        aspect = core_thought.get("tense_aspect")
        
        conjugated_action = self._conjugate_verb(action, tense, aspect, agent)
        
        thought_for_template = core_thought.copy()
        thought_for_template['action'] = conjugated_action
        thought_for_template['preposition'] = core_thought.get("preposition", "to")
        
        final_sentence = matching_pattern["template"].format(**thought_for_template)
        
        return final_sentence.capitalize()

