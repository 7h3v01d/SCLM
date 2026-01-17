# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 10: Advanced Parser for Knowledge Graph Interaction
#
# Objective:
# To upgrade the parser to understand questions that expect a list of facts
# as an answer (e.g., "What are the parts of a car?").
# -----------------------------------------------------------------------------

import spacy

class SemanticParser:
    """
    Parses natural language into a structured "core thought", now with the
    ability to identify multiple factual sentence structures for the KnowledgeEngine.
    """

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("spaCy language model loaded successfully.")
        except OSError:
            print(
                "Error: spaCy model 'en_core_web_sm' not found.\n"
                "Please run: python -m spacy download en_core_web_sm"
            )
            exit()

    def _get_full_subtree(self, token):
        """Helper function to get the full text of a token's subtree."""
        return "".join(t.text_with_ws for t in token.subtree).strip()

    def parse_sentence(self, sentence: str) -> dict:
        doc = self.nlp(sentence)

        core_thought = {
            "input_sentence": sentence,
            "action": None, "agent": None, "object": None, "destination": None,
            "tense": None, "mood": "indicative", "attribute": None,
            "urgency": "neutral", "mood_connotation": "neutral", "tone": "neutral",
            "entities": [], "preposition": None, "tense_aspect": None,
            "learning_fact": None,
            "query_fact": None
        }

        root = next((token for token in doc if token.dep_ == "ROOT"), None)
        
        if not root:
            return core_thought

        # --- Factual statement/question parsing logic ---
        if root.lemma_ == "be":
            subject_token = next((child for child in root.children if child.dep_ in ("nsubj", "nsubjpass")), None)
            attr_token = next((child for child in root.children if child.dep_ == "attr"), None)
            
            if subject_token:
                # PATTERN 1: "Subject's Relationship is Fact"
                possessive_child = next((child for child in subject_token.children if child.dep_ == "poss"), None)
                if possessive_child:
                    subject_text = self._get_full_subtree(possessive_child)
                    subject = subject_text[:-2] if subject_text.endswith("'s") else subject_text
                    relationship = subject_token.text
                    if attr_token:
                        if attr_token.lemma_.lower() == "what": core_thought["query_fact"] = (subject, relationship); core_thought["mood"] = "interrogative_fact"
                        else: core_thought["learning_fact"] = (subject, relationship, self._get_full_subtree(attr_token)); core_thought["mood"] = "declarative_fact"
                        return core_thought

                # PATTERN 2: "The Relationship of Subject is Fact"
                of_child = next((child for child in subject_token.children if child.dep_ == "prep" and child.text.lower() == "of"), None)
                if of_child:
                    pobj_child = next((child for child in of_child.children if child.dep_ == "pobj"), None)
                    if pobj_child:
                        subject = self._get_full_subtree(pobj_child)
                        relationship = subject_token.text
                        if attr_token:
                            if attr_token.lemma_.lower() == "what": core_thought["query_fact"] = (subject, relationship); core_thought["mood"] = "interrogative_fact"
                            else: core_thought["learning_fact"] = (subject, relationship, self._get_full_subtree(attr_token)); core_thought["mood"] = "declarative_fact"
                            return core_thought
                
                # --- **NEW** PATTERN 3: "What are the [Relationship] of [Subject]?" ---
                if subject_token.lemma_.lower() == "what" and attr_token:
                    relationship = attr_token.text
                    of_child = next((child for child in attr_token.children if child.dep_ == "prep" and child.text.lower() == "of"), None)
                    if of_child:
                        pobj_child = next((child for child in of_child.children if child.dep_ == "pobj"), None)
                        if pobj_child:
                            subject = self._get_full_subtree(pobj_child)
                            core_thought["query_fact"] = (subject, relationship)
                            core_thought["mood"] = "interrogative_fact"
                            return core_thought

        # --- Fallback to original parsing logic ---
        # (The rest of the logic remains the same)
        main_verb, aux_verb = root, None
        if root.pos_ == "AUX":
            aux_verb = root
            main_verb = next((child for child in root.children if child.dep_ in ("xcomp", "acomp", "advcl") and child.pos_ == "VERB"), root)
        
        core_thought["action"] = main_verb.lemma_
        
        tense_verb = aux_verb if aux_verb else root
        if "Tense=Past" in tense_verb.morph: core_thought["tense"] = "past"
        if "Tense=Pres" in tense_verb.morph: core_thought["tense"] = "present"
        if any(t.text.lower() == "did" for t in doc): core_thought["tense"] = "past"
        if "VerbForm=Inf" in tense_verb.morph and any(c.lemma_ == 'will' for c in tense_verb.children): core_thought["tense"] = "future"
        if "Aspect=Prog" in main_verb.morph: core_thought["tense_aspect"] = "progressive"
        if root.pos_ == "AUX" and (doc[0].pos_ == "AUX" or doc[0].tag_ in ("WDT", "WP", "WRB")): core_thought["mood"] = "interrogative"

        for child in root.children:
            if child.dep_ in ("nsubj", "nsubjpass"): core_thought["agent"] = self._get_full_subtree(child)
            if child.dep_ == "dobj": core_thought["object"] = self._get_full_subtree(child)
            if child.dep_ == "acomp": core_thought["attribute"] = self._get_full_subtree(child)
            if child.dep_ == "prep":
                core_thought["preposition"] = child.text
                pobj = next((p_child for p_child in child.children if p_child.dep_ == "pobj"), None)
                if pobj: core_thought["destination"] = self._get_full_subtree(pobj)

        for ent in doc.ents:
            core_thought["entities"].append({"text": ent.text, "type": ent.label_})
            
        return core_thought

