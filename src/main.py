"""Command-line entrypoint for interacting with SUB-AGI.

This is a very small REPL (read–eval–print loop) that lets you
experience the evolving MindKernel in a terminal.

Run with:

    python -m src.main

or, depending on your setup, from the project root:

    python -m src.main
"""

from __future__ import annotations

from mind_kernel.core import MindKernel


def main() -> None:
    kernel = MindKernel()
    print("SUB-AGI initialized. Say something (Ctrl+C to exit).")

    try:
        while True:
            user_text = input("You: ")
            reply, state = kernel.step(user_text)
            print("SUB-AGI:", reply)
    except KeyboardInterrupt:
        print("\nExiting SUB-AGI session.")


if __name__ == "__main__":
    main()
