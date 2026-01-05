# SUB-AGI: The Path to Biological Intelligence

![License](https://img.shields.io/github/license/subhobhai943/SUB-AGI)
![Build Status](https://github.com/subhobhai943/SUB-AGI/actions/workflows/sub-agi-runner.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-Phase%201%3A%20Symbol%20Grounding-orange)

> "We will create the AGI that will think like a real human... It will be an alive mind."

**SUB-AGI** is an ambitious open-source project aiming to build Artificial General Intelligence not through massive statistical prediction (like LLMs), but through biologically-inspired cognitive architecture. Our goal is to create a system that develops from "newborn" to the cognitive equivalence of a 3-year-old human child.

## 🧠 Core Philosophy

Current AI models (LLMs) are statistical engines that predict the next token. They do not "understand" in the human sense.

**SUB-AGI is different.**
*   **Biological Realism**: We model working memory, episodic memory, and drives (curiosity, hunger for knowledge).
*   **Symbol Grounding**: Concepts are learned through sensorimotor experience in a simulated world, not just text ingestion.
*   **Transparent Thought**: The internal state (`MindState`) is fully inspectable. We can see *why* it thinks what it thinks.
*   **Developmental**: It starts knowing nothing and learns A-Z through interaction, just like a child.

## 🚀 Key Features (Phase 1)

*   **Mind Kernel**: An "alive" loop that maintains state, emotion, and memory across time steps.
*   **GridWorld Environment**: A simulated 2D space for embodied learning.
*   **Visual Perception**: Ability to recognize shapes and objects in the environment.
*   **Symbol Grounding**: Learning that a specific visual pattern is "A" or "B" through interaction.
*   **Memory Systems**:
    *   *Episodic*: "I saw a square shape at tick 42."
    *   *Semantic*: "The square shape is called 'A'."
    *   *Working*: Current focus of attention.

## 🛠️ Installation & Usage

### Prerequisites
*   Python 3.11 or higher

### Getting Started

1.  **Clone the repository**
    ```bash
    git clone https://github.com/subhobhai943/SUB-AGI.git
    cd SUB-AGI
    ```

2.  **Talk to SUB-AGI (Interactive Mode)**
    Experience the Mind Kernel directly in your terminal.
    ```bash
    python -m src.main
    ```

3.  **Run the Symbol Grounding Experiment**
    Watch SUB-AGI learn to recognize letters from visual shapes.
    ```bash
    python src/experiments/phase1_grounding.py
    ```

## 📂 Project Structure

*   `src/mind_kernel/`: The core cognitive architecture (MindState, Memory, Affect).
*   `src/environment/`: Simulated worlds (GridWorld) for embodied experience.
*   `src/experiments/`: Scientific scenarios to validate cognitive growth.
*   `docs/`: Design documents, roadmaps, and research notes.
*   `.github/workflows/`: Automated testing and experiments.

## 🗺️ Roadmap

*   **Phase 0**: Foundation & Architecture ✅
*   **Phase 1**: Symbol Grounding (Visual Shapes) ✅ *(Current)*
*   **Phase 2**: Curiosity-Driven Exploration 🚧 *(Next)*
*   **Phase 3**: Toddler-Level Dialogue & Self-Reference
*   **Phase 4**: Multi-modal Integration

See [docs/roadmap.md](docs/roadmap.md) for details.

## 🤝 Contributing

We welcome researchers, developers, and visionaries.
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and our process for submitting pull requests.

## 🛡️ Governance

*   [Code of Conduct](CODE_OF_CONDUCT.md)
*   [Security Policy](SECURITY.md)

## 📄 License

This project is licensed under the **GNU General Public License v2.0**. See the [LICENSE](LICENSE) file for details.
