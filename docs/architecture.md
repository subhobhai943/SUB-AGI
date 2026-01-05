# SUB-AGI Architecture

This document captures the very first high-level architecture ideas for SUB-AGI, an open-source artificial general intelligence project aiming to grow from "newborn" to the cognitive level of a 3-year-old human child.

## Core Principles
- **Human-like thinking, not math tricks**: Focus on processes that resemble biological cognition (attention, memory, perception, emotion-like signals), not just large-scale statistical prediction.
- **Developmental approach**: SUB-AGI should *grow* through stages (infant → toddler), learning from experience rather than being pre-programmed with all knowledge.
- **Grounded understanding**: Symbols (like words or letters) must connect to internal experiences and sensorimotor patterns, not just text statistics.
- **Transparency**: The system must expose internal states so researchers can inspect what it "thinks" and "feels".

## Top-Level System Layout

1. **Embodied Core ("Mind Kernel")**
   - Persistent process that maintains SUB-AGI's internal state across time.
   - Owns:
     - Working memory (short-term thoughts)
     - Long-term memory store (episodes, concepts, skills)
     - Motivational system (curiosity, comfort, novelty signals)
   - Communicates via a well-defined API with input/output modules.

2. **Perception Layer**
   - Text input initially (console / API), later extendable to vision and audio.
   - Converts raw streams (characters, tokens) into internal representations.
   - Handles:
     - Alphabet perception (A–Z recognition)
     - Basic pattern detection ("this looks like what I saw before").

3. **Action / Expression Layer**
   - Produces outputs: text replies, questions, or internal actions ("think more before answering").
   - Must be able to say "I don't know" or "I am confused" rather than guess.

4. **Memory System**
   - **Episodic memory**: "What happened to me?" (chronological timeline of interactions).
   - **Semantic memory**: "What is true about the world?" (facts, concepts, relationships).
   - **Procedural memory**: "What can I do?" (skills, routines for tasks).

5. **Learning Engine**
   - Central mechanism that updates memories and internal models from experience.
   - Should support:
     - Continual learning without catastrophic forgetting.
     - Play-based and curriculum-based training.

6. **Safety and Introspection Module**
   - Monitors thoughts and actions for unsafe patterns.
   - Provides self-report: "What are you thinking about right now?" and "Why did you answer this way?".

## First Milestone: 3-Year-Old Equivalent (Text-Only)

Target abilities:
- Understand and use simple English sentences.
- Recognize and use all letters A–Z.
- Answer basic questions about itself and previous interactions.
- Show simple preferences (likes, dislikes, curiosity).
- Learn new words and concepts from very few examples.

## Initial Implementation Plan

- Start with a **simple, inspectable prototype** in Python.
- Use a modular design so we can later replace components (e.g., swap a simple memory with a more advanced one).
- Begin with text I/O only and build a sandbox environment to train SUB-AGI, similar to a safe "nursery".

This file will evolve as design discussions progress and experiments teach us what works and what fails.