# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 10: Final Interactive AI with Knowledge Graph - FINAL VERSION
#
# Objective:
# To integrate a more robust parser and an improved response engine, creating
# a more intelligent and conversational AI.
# -----------------------------------------------------------------------------

import os
import spacy
from datetime import datetime
import sqlite3

# --- Component 1: The Upgraded Semantic Parser ---
class SemanticParser:
    """
    Parses natural language with flexible grammatical patterns to identify
    factual statements and questions, now with relationship inference.
    """
    def __init__(self):
        if not hasattr(SemanticParser, 'nlp'):
            try:
                SemanticParser.nlp = spacy.load("en_core_web_sm")
                print("spaCy language model loaded successfully.")
            except OSError:
                print("Error: spaCy model not found. Run: python -m spacy download en_core_web_sm")
                exit()
        self.nlp = SemanticParser.nlp
        # --- **NEW**: Internal knowledge to infer relationships ---
        self.relationship_keywords = {
            'shape': ['round', 'square', 'triangular', 'flat', 'curved'],
            'color': ['red', 'blue', 'green', 'yellow', 'black', 'white']
        }

    def _get_full_subtree(self, token):
        return "".join(t.text_with_ws for t in token.subtree).strip()

    def _infer_relationship(self, fact_text: str) -> str:
        """Infers the relationship type based on the fact's content."""
        for rel, keywords in self.relationship_keywords.items():
            if fact_text.lower() in keywords:
                return rel
        return 'state' # Default if no specific relationship is found

    def parse_sentence(self, sentence: str) -> dict:
        doc = self.nlp(sentence)
        core_thought = {
            "input_sentence": sentence, "mood": "indicative", "learning_fact": None, "query_fact": None,
            "action": None, "agent": None, "object": None, "destination": None, "attribute": None
        }

        root = next((token for token in doc if token.dep_ == "ROOT"), None)
        if not root: return core_thought

        # --- Factual Parsing Logic ---
        if root.lemma_ == "be":
            nsubj = next((t for t in root.children if t.dep_ in ("nsubj", "nsubjpass")), None)
            attr = next((t for t in root.children if t.dep_ == "attr"), None)

            if nsubj:
                # PATTERN 1: "Subject's Relationship is Fact"
                poss_child = next((t for t in nsubj.children if t.dep_ == "poss"), None)
                if poss_child:
                    subject = self._get_full_subtree(poss_child).replace("'s", "")
                    relationship = nsubj.text
                    if attr:
                        if attr.lemma_.lower() == "what":
                            core_thought["query_fact"] = (subject, relationship)
                            core_thought["mood"] = "interrogative_fact"
                        else:
                            core_thought["learning_fact"] = (subject, relationship, self._get_full_subtree(attr))
                            core_thought["mood"] = "declarative_fact"
                        return core_thought

                # PATTERN 2: "The Relationship of Subject is Fact"
                of_child = next((t for t in nsubj.children if t.dep_ == "prep" and t.text.lower() == "of"), None)
                if of_child:
                    pobj = next((t for t in of_child.children if t.dep_ == "pobj"), None)
                    if pobj:
                        subject = self._get_full_subtree(pobj)
                        relationship = nsubj.text.replace("the ", "") # clean up "the capital" -> "capital"
                        if attr:
                            if attr.lemma_.lower() == "what":
                                core_thought["query_fact"] = (subject, relationship)
                                core_thought["mood"] = "interrogative_fact"
                            else:
                                core_thought["learning_fact"] = (subject, relationship, self._get_full_subtree(attr))
                                core_thought["mood"] = "declarative_fact"
                            return core_thought
                
                # --- **FIXED** PATTERN 3: "[A/The] Subject is [Fact/Attribute]"
                if attr:
                    subject_text = self._get_full_subtree(nsubj)
                    subject = subject_text.split(" ", 1)[-1] if subject_text.lower().startswith(('a ', 'the ')) else subject_text
                    fact = self._get_full_subtree(attr)
                    relationship = self._infer_relationship(fact) # Infer the relationship!
                    core_thought["learning_fact"] = (subject, relationship, fact)
                    core_thought["mood"] = "declarative_fact"
                    return core_thought

            # --- **NEW** PATTERN 4: "What [Relationship] is [Subject]?"
            if attr and nsubj and nsubj.lemma_.lower() == "what":
                subject = self._get_full_subtree(attr)
                relationship = nsubj.text.replace("what ", "") # clean up "what shape" -> "shape"
                core_thought["query_fact"] = (subject, relationship)
                core_thought["mood"] = "interrogative_fact"
                return core_thought

        # --- Fallback to original action-based parsing ---
        core_thought["action"] = root.lemma_
        for child in root.children:
            if child.dep_ in ("nsubj", "nsubjpass"): core_thought["agent"] = self._get_full_subtree(child)
            if child.dep_ == "dobj": core_thought["object"] = self._get_full_subtree(child)
            if child.dep_ == "acomp": core_thought["attribute"] = self._get_full_subtree(child)
        
        return core_thought

# --- Component 2: The Knowledge Engine (Corrected) ---
class KnowledgeGraphEngine:
    def __init__(self, db_path="sclm_knowledge.db"):
        self.singular_relationships = ['shape', 'capital', 'state']
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._initialize_database()
        print(f"Knowledge Graph Engine connected to '{db_path}'.")

    def _initialize_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS knowledge")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                subject TEXT NOT NULL, relationship TEXT NOT NULL, fact TEXT NOT NULL,
                is_immutable BOOLEAN DEFAULT FALSE, source TEXT, timestamp DATETIME,
                UNIQUE(subject, relationship)
            )
        """)
        if self.cursor.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0] == 0:
            print("Populating with immutable constants...")
            constants = [('ball', 'shape', 'round'), ('France', 'capital', 'Paris')]
            for subj, rel, fact in constants:
                self.cursor.execute(
                    "INSERT INTO knowledge VALUES (?, ?, ?, ?, ?, ?)",
                    (subj.lower(), rel.lower(), fact, True, 'System_Constant', datetime.now())
                )
            self.connection.commit()

    def query_facts(self, subject: str, relationship: str) -> list:
        print(f"QUERY: Looking for '{relationship}' of '{subject}'...")
        self.cursor.execute(
            "SELECT fact FROM knowledge WHERE subject = ? AND relationship = ?",
            (subject.lower(), relationship.lower())
        )
        return [row[0] for row in self.cursor.fetchall()]

    def learn_fact(self, subject: str, relationship: str, fact: str, source: str = 'user') -> str:
        s_lower, r_lower = subject.lower(), relationship.lower()

        self.cursor.execute("SELECT is_immutable FROM knowledge WHERE subject=? AND relationship=?", (s_lower, r_lower))
        immutable_flag = self.cursor.fetchone()
        if immutable_flag and immutable_flag[0]:
             return "CONFLICT_WITH_CONSTANT"
        
        self.cursor.execute("SELECT 1 FROM knowledge WHERE subject=? AND relationship=?", (s_lower, r_lower))
        is_update = self.cursor.fetchone() is not None

        self.cursor.execute("""
            INSERT OR REPLACE INTO knowledge (subject, relationship, fact, is_immutable, source, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (s_lower, r_lower, fact, False, source, datetime.now()))
        self.connection.commit()

        if is_update: return "UPDATED_BELIEF"
        return "LEARNED_SUCCESSFULLY"

    def close(self):
        if self.connection:
            self.connection.close()

# --- Component 3: The Upgraded Response Engine ---
class ResponseEngine:
    def _format_list(self, items: list) -> str:
        if not items: return ""
        if len(items) == 1: return items[0]
        return ", ".join(items[:-1]) + f", and {items[-1]}"

    def generate_response(self, core_thought: dict, kge: KnowledgeGraphEngine) -> str:
        mood = core_thought.get("mood")
        
        if mood == "declarative_fact" and core_thought.get("learning_fact"):
            subject, rel, fact = core_thought["learning_fact"]
            result = kge.learn_fact(subject, rel, fact)
            if result == "LEARNED_SUCCESSFULLY": return f"Okay, I've learned that the {rel} of {subject} is {fact}."
            if result == "UPDATED_BELIEF": return f"Okay, I've updated my belief. I now understand that the {rel} of {subject} is {fact}."
            if result == "CONFLICT_WITH_CONSTANT":
                known_fact = kge.query_facts(subject, rel)
                return f"That's interesting, but my understanding is that the {rel} of {subject} is {self._format_list(known_fact)}."
            
        if mood == "interrogative_fact" and core_thought.get("query_fact"):
            subject, rel = core_thought["query_fact"]
            answers = kge.query_facts(subject, rel)
            if answers:
                verb = "is" if len(answers) == 1 else "are"
                return f"Based on what I know, the {rel} of {subject} {verb}: {self._format_list(answers)}."
            else: return f"I don't have any information about the {rel} of {subject}."

        if core_thought.get("attribute"):
            return f"{core_thought.get('agent', 'It')} certainly seems to be {core_thought.get('attribute')}. That's an interesting observation."
            
        return "I understand. Thank you for telling me."

# --- Component 4: The Dialogue Manager ---
class DialogueManager:
    def __init__(self):
        self.parser = SemanticParser()
        self.kge = KnowledgeGraphEngine()
        self.response_engine = ResponseEngine()
        print("SCLM AI is online.")

    def handle_message(self, message: str) -> str:
        thought = self.parser.parse_sentence(message)
        response = self.response_engine.generate_response(thought, self.kge)
        return response

    def close(self):
        self.kge.close()

# --- Main Interactive Loop ---
if __name__ == "__main__":
    db_file = "sclm_knowledge.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print("Cleared knowledge base.")
        except PermissionError:
            print(f"Warning: Could not clear knowledge base. File '{db_file}' may be in use.")
            exit()

    ai = DialogueManager()
    print("Type 'quit' to exit.")
    print("-" * 30)

    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            
            ai_response = ai.handle_message(user_input)
            print(f"AI: {ai_response}")
    finally:
        ai.close()
        print("AI: Goodbye!")

