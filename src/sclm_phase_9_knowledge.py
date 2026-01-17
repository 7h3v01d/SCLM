# -----------------------------------------------------------------------------
# Project: Semantic Core Language Model (SCLM)
# Phase 10: Knowledge Graph Engine - CORRECTED
#
# Objective:
# To evolve the KnowledgeEngine to support a true knowledge graph by handling
# one-to-many relationships with corrected conflict-detection logic.
# -----------------------------------------------------------------------------

import sqlite3
from datetime import datetime
import os

class KnowledgeGraphEngine:
    """
    Manages the AI's knowledge graph, supporting complex, multi-faceted entities.
    """
    def __init__(self, db_path="sclm_knowledge.db"):
        self.db_path = db_path
        # --- **NEW**: Define which relationships are inherently singular ---
        self.singular_relationships = ['shape', 'capital']
        
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._initialize_database()
        print(f"Knowledge Graph Engine connected to '{self.db_path}'.")

    def _initialize_database(self):
        """
        Creates the knowledge table and populates it with constants.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                subject TEXT NOT NULL, relationship TEXT NOT NULL, fact TEXT NOT NULL,
                is_immutable BOOLEAN DEFAULT FALSE, source TEXT DEFAULT 'unknown', timestamp DATETIME
            )
        """)
        
        if self.cursor.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0] == 0:
            print("Database is empty. Populating with immutable constants...")
            constants = [
                ('ball', 'shape', 'round'),
                ('ball', 'can_be_action', 'thrown'),
                ('ball', 'can_be_action', 'caught'),
                ('car', 'has_part', 'engine'),
                ('car', 'has_part', 'wheel'),
                ('France', 'capital', 'Paris'),
            ]
            for subj, rel, fact in constants:
                # For initialization, we directly add facts without the complex check.
                self.cursor.execute(
                    "INSERT INTO knowledge (subject, relationship, fact, is_immutable, source, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (subj.lower(), rel.lower(), fact, True, 'System_Constant', datetime.now())
                )
            print("Immutable constants have been added.")
        self.connection.commit()

    def query_facts(self, subject: str, relationship: str) -> list:
        """Retrieves a LIST of all facts matching a subject and relationship."""
        print(f"QUERY: Looking for '{relationship}' of '{subject}'...")
        self.cursor.execute(
            "SELECT fact FROM knowledge WHERE subject = ? AND relationship = ?",
            (subject.lower(), relationship.lower())
        )
        return [row[0] for row in self.cursor.fetchall()]

    def learn_fact(self, subject: str, relationship: str, fact: str, source: str = 'user') -> str:
        """
        The corrected critical thinking loop. Distinguishes between singular and plural relationships.
        """
        subj_lower = subject.lower()
        rel_lower = relationship.lower()
        fact_lower = fact.lower()

        # --- 1. Query for existing knowledge on this topic ---
        self.cursor.execute(
            "SELECT fact, is_immutable FROM knowledge WHERE subject = ? AND relationship = ?",
            (subj_lower, rel_lower)
        )
        existing_facts = self.cursor.fetchall()

        # --- 2. Critical Thinking Logic ---
        if existing_facts:
            # Check for conflict with a singular, immutable relationship
            if rel_lower in self.singular_relationships and existing_facts[0][1]: # existing_facts[0][1] is is_immutable
                print(f"CONFLICT: Cannot change the immutable '{rel_lower}' of '{subj_lower}'.")
                return "CONFLICT_WITH_CONSTANT"
            
            # Check if this exact fact is already known (prevents duplicates)
            for existing_fact, _ in existing_facts:
                if fact_lower == existing_fact.lower():
                    print(f"INFO: Fact ({subject}, {relationship}, {fact}) is already known.")
                    return "ALREADY_KNOWN"
        
        # --- 3. Learn the New Fact ---
        print(f"LEARN: Storing fact: ({subject}, {relationship}, {fact})")
        self.cursor.execute(
            "INSERT INTO knowledge (subject, relationship, fact, source, timestamp) VALUES (?, ?, ?, ?, ?)",
            (subj_lower, rel_lower, fact, source, datetime.now())
        )
        self.connection.commit()
        return "LEARNED_SUCCESSFULLY"

    def close(self):
        if self.connection:
            self.connection.close()
            print("Knowledge Graph Engine connection closed.")

# --- Standalone Test Block ---
if __name__ == "__main__":
    if os.path.exists("sclm_knowledge.db"):
        os.remove("sclm_knowledge.db")

    kge = KnowledgeGraphEngine()
    print("-" * 30)
    
    print("--- Test 1: Querying for multiple facts ---")
    car_parts = kge.query_facts("car", "has_part")
    print(f"RESULT: A car has the following parts: {car_parts}\n") # Should be ['engine', 'wheel']

    print("--- Test 2: Learning an additional, valid fact ---")
    kge.learn_fact("car", "has_part", "door")
    car_parts = kge.query_facts("car", "has_part")
    print(f"RESULT: Now, a car has the following parts: {car_parts}\n") # Should include 'door'
    
    print("--- Test 3: Conflict with a singular immutable fact ---")
    result = kge.learn_fact("ball", "shape", "square")
    print(f"RESULT: {result}\n") # Should be CONFLICT_WITH_CONSTANT

    print("--- Test 4: Trying to re-learn an existing fact ---")
    result = kge.learn_fact("car", "has_part", "wheel")
    print(f"RESULT: {result}") # Should be ALREADY_KNOWN

    kge.close()

