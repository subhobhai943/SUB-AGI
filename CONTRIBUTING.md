# Contributing to SUB-AGI

Thank you for your interest in contributing to SUB-AGI! This project aims to create artificial general intelligence through biologically-inspired, grounded learning. Every contribution, from fixing typos to proposing new cognitive mechanisms, helps advance this ambitious goal.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Research Contributions](#research-contributions)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- **Check existing issues** first to avoid duplicates
- Use the GitHub issue tracker
- Include:
  - Python version and OS
  - Exact steps to reproduce
  - What you expected vs. what happened
  - Relevant logs or error messages

### Suggesting Enhancements

We welcome proposals for:
- New cognitive mechanisms (memory systems, attention, learning rules)
- Improved biological realism
- Better symbol grounding experiments
- Performance optimizations

**Please open an issue first** to discuss major changes before investing time in implementation.

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our coding standards
4. Add tests if applicable
5. Commit with clear messages (`git commit -m 'Add curiosity-driven exploration'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/SUB-AGI.git
cd SUB-AGI

# Run tests (once we add them)
python -m pytest tests/

# Run an experiment
python src/experiments/phase1_grounding.py
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints wherever possible
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation

- Every module should have a docstring explaining its purpose
- Public functions and classes must have docstrings
- Complex algorithms should have inline comments explaining the logic

### Example

```python
from typing import List, Tuple

def ground_symbol(shape_pattern: List[str], label: str) -> SemanticConcept:
    """Associate a visual shape pattern with a symbolic label.
    
    This implements the symbol grounding process where SUB-AGI learns
    to map sensorimotor experiences (shapes) to abstract symbols (letters).
    
    Args:
        shape_pattern: 3x3 visual pattern as list of strings
        label: Symbol to associate (e.g., 'A', 'B')
        
    Returns:
        SemanticConcept storing the grounded association
    """
    # Implementation...
```

## Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
Add curiosity-driven exploration to Phase 2

- Implement boredom metric in AffectState
- Add action selection based on novelty
- Update GridWorld to track visit counts per cell
```

### Pull Request Process

1. Ensure your code follows the style guide
2. Update documentation if you changed APIs
3. Add your changes to the relevant section in `docs/`
4. The PR will be reviewed by maintainers
5. Address any requested changes
6. Once approved, a maintainer will merge

## Research Contributions

### Proposing New Cognitive Mechanisms

If you want to add a new component (e.g., working memory model, attention mechanism):

1. **Open an issue** describing:
   - The cognitive function you're modeling
   - Biological/psychological inspiration
   - How it integrates with existing SUB-AGI architecture
   - Expected behavior and testable predictions

2. **Provide references** to relevant neuroscience or psychology papers

3. **Start simple**: Implement a minimal version first, then iterate

### Running Experiments

Experiments live in `src/experiments/`. Each experiment should:

- Have a clear hypothesis
- Define success/failure criteria
- Log all relevant internal states
- Be reproducible (set random seeds)

### Documenting Results

When sharing experimental results:

- Add a Markdown file in `docs/experiments/`
- Include:
  - Hypothesis
  - Methodology
  - Results (with logs or visualizations)
  - Analysis and interpretation
  - Limitations

## Project Structure

```
SUB-AGI/
├── src/
│   ├── mind_kernel/      # Core cognitive loop
│   ├── environment/      # Simulated worlds
│   ├── experiments/      # Test scenarios
│   └── main.py          # Entry point
├── docs/                # Design documents
├── tests/               # Unit and integration tests (coming soon)
└── .github/workflows/   # CI/CD automation
```

## Questions?

If you have questions about contributing:

- Open a GitHub issue with the "question" label
- Check existing documentation in `docs/`
- Review past issues and PRs

## Attribution

Contributors will be acknowledged in:
- The project README
- Release notes for significant contributions
- Academic papers if the work leads to publications

---

Thank you for helping build AGI that learns like a human mind! 🧠✨
