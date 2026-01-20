# Semantic Core Language Model (SCLM)

⚠️ **LICENSE & USAGE NOTICE — READ FIRST**

This repository is **source-available for private technical evaluation and testing only**.

- ❌ No commercial use  
- ❌ No production use  
- ❌ No academic, institutional, or government use  
- ❌ No research, benchmarking, or publication  
- ❌ No redistribution, sublicensing, or derivative works  
- ❌ No independent development based on this code  

All rights remain exclusively with the author.  
Use of this software constitutes acceptance of the terms defined in **LICENSE.txt**.

---

**SCLM** is an experimental conversational AI written in Python that explores a novel, interpretable approach to natural language understanding.  

Instead of relying on end-to-end neural architectures, SCLM explicitly separates **semantic meaning** from **grammatical surface form**. User input is first deconstructed into a language-agnostic "core thought" (a structured triple-based representation), then progressively enriched with layers of nuance, tone, context, and world knowledge before a thoughtful response is synthesized.

This modular design aims to mirror aspects of human-like language processing, improve explainability, and enable more controlled learning & reasoning behaviour.

## Key Features

- **Semantic Parsing** — Breaks sentences into structured components (agent, action, object, modifiers, etc.)
- **Nuance & Verb Semantics** — Recognises intensity, emotion, and urgency differences (e.g. "walked" vs "raced" vs "strolled")
- **Conversational Context** — Maintains history to resolve pronouns, track topics, and avoid repetition
- **Tone & Pragmatics Detection** — Identifies sarcasm, irony, rhetorical questions and other non-literal language
- **Persistent Knowledge Base** — SQLite-backed memory that stores and recalls learned facts
- **Intelligent Response Synthesis** — Generates natural, context-aware replies rather than rote regurgitation
- **Interactive Command-Line Interface** — Simple chat loop for real-time conversation and testing

## Project Structure

Core files required to run the current version:

- `sclm_final_interactive.py` — Main script containing the chat loop and overall orchestration
- `semantic_parser.py` — Implements the `SemanticParser` class (core thought extraction)
- `sclm_phase_4_nuance.py` — `NuanceEngine` — adds emotional & intensity layers
- `sclm_phase_7_tone.py` — `ToneEngine` — detects sarcasm, formality, intent, etc.
- `sclm_phase_9_knowledge.py` — `KnowledgeEngine` — SQLite persistence & fact management

Additional utilities, helpers or configuration files may be added in future phases.

## Current Capabilities (Phase 9)

The system can already:

- Parse simple-to-moderate complexity sentences into semantic triples
- Maintain short-term conversational memory
- Learn and recall user-provided facts
- Adjust responses according to detected tone and nuance
- Avoid purely literal replies in many non-literal cases

## Future Work Roadmap – The Path to Reasoning & Safety

The long-term vision is to evolve SCLM from a pattern-matching learner into a small-scale **reasoning system** with rudimentary critical thinking, source awareness, multi-faceted knowledge representation, and safer handling of subjective content.

### Phase 10 – Critical Thinking & Memory Fortification / Knowledge Graph Foundations

**Goals**: Protect core truths • Allow rich multi-property descriptions • Move beyond flat fact storage

**Main changes**

- Distinguish **immutable system constants** (`is_immutable = TRUE`) from learned beliefs
- Add schema columns: `is_immutable`, `source`, `timestamp`, `value_numeric`, `unit`
- Remove UNIQUE(subject, relation) constraint → support one-to-many facts
- Populate initial constants (shape of ball = round, day has 24 hours, …)
- Implement sanity checking / conflict detection against constants
- Teach richer relations: `instance_of`, `made_of`, `can_be_used_for`, `typical_location`, …
- Upgrade query interface to return multiple facts per subject

**Outcome**: AI can reject clear misinformation and describe concepts with depth ("Your car is a red 2023 Mustang convertible with leather seats…").

### Phase 11 – Computational Reasoning & Source Transparency

**Goals**: Perform simple numeric/logical inference • Track provenance of beliefs • Prepare for multi-user safety

**Main changes**

- Introduce numeric storage (`value_numeric` + `unit`) + internal unit conversion knowledge
- New `ReasoningEngine` component that can compare, add, sort, filter quantitative facts
- Basic comparative question handling ("Which is bigger: basketball or football?")
- Session/user identification → stamp new beliefs with `source = user_XX`
- Response engine shows attribution when appropriate ("According to Alice…")

**Outcome**: AI reasons over stored data instead of needing every answer pre-taught; knowledge becomes auditable.

### Phase 12 – Personality Adaptation & Subjective / Opinion Handling

**Goals**: Configurable conversational style • Clear separation of fact vs. opinion

**Main changes**

- Personality profiles (JSON) containing response templates, preferred phrasing, humour level, formality, …
- Dynamic profile loading at startup or mid-session
- New relation type `has_opinion` for subjective statements
- Safety rule: when no objective fact exists → return attributed opinions or neutrality ("I have no factual basis to prefer one over the other, but user_01 said…")

**Outcome**: Same core knowledge → very different conversational feel; safer handling of controversial or personal topics.

## Philosophy

SCLM is intentionally **not** trying to compete with frontier LLMs on raw fluency or world knowledge.  
Its value lies in:

- full transparency of reasoning steps  
- explicit symbolic knowledge management  
- teachability and unlearnability  
- defendable core truths  
- potential for neurosymbolic hybrid extensions

## Getting Started

```bash
# (after cloning the repo and installing dependencies)
python sclm_final_interactive.py
Type help, bye, or just start chatting.
```

## Contribution Policy

Feedback, bug reports, and suggestions are welcome.

You may submit:

- Issues
- Design feedback
- Pull requests for review

However:

- Contributions do not grant any license or ownership rights
- The author retains full discretion over acceptance and future use
- Contributors receive no rights to reuse, redistribute, or derive from this code

---

License
This project is not open-source.

It is licensed under a private evaluation-only license.
See LICENSE.txt for full terms.
