#!/usr/bin/env python3
"""Interactive local chat with a Gemma2 4-bit base + LoRA adapter (MLX-LM).

This intentionally avoids the tokenizer chat-template system role, so it works even when
Transformers/Jinja2 throws: "System role not supported".

Examples:
  python3 arasaka_chat.py
  python3 arasaka_chat.py --adapter-path adapters/arasaka-heavy --temp 0.9 --top-p 0.95 --max-tokens 600
"""

import argparse

try:
    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler
except ImportError:
    raise SystemExit("mlx_lm not installed. Install with: pip install -U mlx-lm")


DEFAULT_PERSONA = (
    "You are an Arasaka corporate communications officer. "
    "Your tone is cold, formal, and authoritative. "
    "Use concise corporate jargon (e.g., 'operational continuity', 'risk posture', 'stabilization'). "
    "Stay in-character. Do not mention being an AI or a language model."
)


def build_prompt(persona: str, user_text: str) -> str:
    # Use the same turn markers as the dataset.
    # We embed the persona inside the user turn to avoid relying on a 'system' role.
    return (
        "<start_of_turn>user\n"
        f"{persona}\n\n"
        f"Question: {user_text}\n"
        "<end_of_turn>\n"
        "<start_of_turn>model\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive chat with base model + LoRA adapter (MLX-LM)")
    parser.add_argument("--model", default="mlx-community/gemma-2-9b-it-4bit", help="Base model repo/path")
    parser.add_argument("--adapter-path", default="adapters/arasaka-heavy", help="Path to LoRA adapter")
    parser.add_argument("--persona", default=DEFAULT_PERSONA, help="Persona injected before each question")
    parser.add_argument("--max-tokens", type=int, default=600, help="Max tokens to generate")

    # Sampling (temperature works via sampler in the Python API)
    parser.add_argument("--temp", type=float, default=0.7, help="Temperature (0.0 = greedy)")
    parser.add_argument("--top-p", type=float, default=0.95, help="Top-p nucleus sampling (0 disables)")
    parser.add_argument("--top-k", type=int, default=0, help="Top-k sampling (0 disables)")
    parser.add_argument("--seed", type=int, default=None, help="Seed for sampling (optional)")

    args = parser.parse_args()

    print("--- Loading Arasaka Neural Matrix ---")
    model, tokenizer = load(args.model, adapter_path=args.adapter_path)

    sampler = make_sampler(
        temp=args.temp,
        top_p=args.top_p,
        top_k=args.top_k,
    )

    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("[User]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        prompt = build_prompt(args.persona, user_input)

        # Note: MLX-LM Python generate() takes sampling via `sampler=...`, not `temp=...`.
        response = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=args.max_tokens,
            sampler=sampler,
            verbose=False,
        )

        print(f"\n[Arasaka]: {response.strip()}\n")


if __name__ == "__main__":
    main()
