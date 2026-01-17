Semantic Core Language Model (SCLM)
Introduction
The Semantic Core Language Model (SCLM) is a conversational AI built in Python that explores a unique architectural approach to Natural Language Processing (NLP). The core concept of this project is the separation of semantic meaning from grammatical expression.

Instead of treating language as a simple string of words, the SCLM first deconstructs a user's sentence into a structured, language-agnostic "core thought." This core thought is then enriched with layers of understanding—such as emotional nuance, tone, and conversational context—before a final, intelligent response is generated.

This modular, interpretable design allows the AI to develop a sophisticated understanding of language that mirrors human learning processes.

Key Features
Semantic Parsing: The AI can break down sentences into their fundamental components (agent, action, object, etc.).

Nuance Detection: Understands the subtle differences in mood and urgency conveyed by verb choice (e.g., "walked" vs. "raced").

Contextual Awareness: Maintains a conversation history to remember previous statements and correctly resolve pronouns.

Tone Detection: Capable of identifying non-literal tones like sarcasm to avoid literal-minded responses.

Knowledge Base: Features a persistent memory (SQLite database) allowing it to learn, store, and recall factual information.

Intelligent Response Generation: Crafts its own context-aware replies instead of simply echoing its understanding.

Interactive Chat: A simple and intuitive command-line interface for live conversation.

Project Files
The final, functional AI requires the following core files:

sclm_final_interactive.py: The main, executable script that runs the interactive chat loop.

semantic_parser.py: The module containing the SemanticParser class.

sclm_phase_4_nuance.py: The module containing the NuanceEngine.

sclm_phase_7_tone.py: The module containing the ToneEngine.

sclm_phase_9_knowledge.py: The module containing the KnowledgeEngine for database interaction.

Future Work Roadmap: The Evolution to a Reasoning AI
This new roadmap outlines the next major evolution of the SCLM project. The goal is to transform the AI from a system that stores facts into a system that understands and reasons with a multi-faceted knowledge graph.

Phase 10: Building a True Knowledge Graph
Objective: To move beyond a "flat" fact-book and enable the AI to understand that concepts have multiple, rich characteristics, actions, and properties.

Key Activities:

Embrace One-to-Many Relationships:

Modify the knowledge database schema to remove the UNIQUE(subject, relationship) constraint. This is the key change that allows for depth.

Upgrade the KnowledgeEngine's query_fact() method to query_facts() (plural), which will return a list of all relevant facts.

Distinguish Classes from Instances:

Enhance the SemanticParser to differentiate between a general class (e.g., "car") and a specific instance (e.g., "my car," which becomes car_01).

This will be managed via a new relationship type: (car_01, instance_of, car).

Expand the Relationship Vocabulary:

Teach the SemanticParser to recognize a richer set of relationships beyond simple properties, including:

Actions: (ball, can_be_action, thrown)

Materials: (tyre, made_of, rubber)

Classifications: (mustang, is_a, car_model)

Upgrade the Response Engine for Synthesis:

Enhance the ResponseEngine to query for multiple facts about a subject and synthesize them into a coherent, descriptive paragraph that can "paint a picture" for the user.

Expected Outcome: The AI will be able to describe a concept with multiple characteristics (e.g., "Tell me about your car" -> "Your car is a red 2023 Ford Mustang."). It will no longer make incorrect generalizations based on specific instances.

Phase 11: The Computational Reasoning Engine
Objective: To give the AI the ability to infer new knowledge and answer comparative questions by performing logical operations on computable data.

Key Activities:

Evolve the Database for Computable Data:

Modify the knowledge schema to include new columns: value_numeric (REAL) and unit (TEXT). This allows the storage of quantitative facts (e.g., (baseball, diameter, 7.5, 'cm')).

Develop the ReasoningEngine:

Create a new, dedicated ReasoningEngine component. This engine's job is not to store data, but to perform computations on it.

It will contain its own internal knowledge of unit conversions (e.g., meters to centimeters).

Implement the compare() Method:

The ReasoningEngine's core function will query the KnowledgeEngine for the raw numerical data of two subjects, standardize the units, perform the mathematical comparison, and return a logical conclusion.

Integrate into the AI's Brain:

Upgrade the ResponseEngine to act as a delegator. When it identifies a comparative question, it will call the ReasoningEngine to get a logical answer before translating it into natural language.

Expected Outcome: The AI will be able to answer questions it was never explicitly told the answer to, such as "Which is bigger, a basketball or a bus?", by reasoning with the underlying data.

Phase 12: Handling Subjectivity & Opinions
Objective: To make the AI safer and more transparent by teaching it to distinguish between objective facts and subjective user opinions, always attributing the source of the opinion.

Key Activities:

Implement User Identification:

Introduce a basic user system (e.g., a session-based user_id).

Create the has_opinion Relationship:

When a user states a subjective preference (e.g., "I like dogs better than cats"), the KnowledgeEngine will store this using the new relationship type: (user_01, has_opinion, "dogs are better than cats").

Develop a Safety-Oriented Response Rule:

Upgrade the ResponseEngine with a crucial new protocol: when asked a subjective question, it must first search for objective facts. Finding none, it may then search for opinions but must attribute the source in its response.

Expected Outcome: The AI will not adopt user opinions as its own. It will respond to subjective questions safely and truthfully, for example: "I don't have an objective answer