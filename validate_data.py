import json
from pathlib import Path

REQUIRED_TAGS = [
    "<start_of_turn>user",
    "<end_of_turn>",
    "<start_of_turn>model",
    "<end_of_turn>",
]


def load_jsonl(path: Path):
    items = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at {path}:{i}: {e}")
            if "text" not in obj or not isinstance(obj["text"], str):
                raise ValueError(f"Missing 'text' string at {path}:{i}")
            items.append(obj["text"])
    return items


def has_required_tags(text: str) -> bool:
    # Must contain both user and model turns with end tags
    return (
        "<start_of_turn>user" in text
        and "<start_of_turn>model" in text
        and text.count("<end_of_turn>") >= 2
    )


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate Gemma JSONL datasets")
    parser.add_argument(
        "--train-file",
        type=str,
        default=str((Path(__file__).resolve().parent / "data" / "train.jsonl")),
    )
    parser.add_argument(
        "--valid-file",
        type=str,
        default=str((Path(__file__).resolve().parent / "data" / "valid.jsonl")),
    )
    args = parser.parse_args()

    train_p = Path(args.train_file)
    valid_p = Path(args.valid_file)

    train = load_jsonl(train_p)
    valid = load_jsonl(valid_p)

    # Basic stats
    print(f"Train count: {len(train)}")
    print(f"Valid count: {len(valid)}")

    # Tag checks
    for i, t in enumerate(train, start=1):
        if not has_required_tags(t):
            raise AssertionError(f"Missing tags in train sample #{i}")
    for i, v in enumerate(valid, start=1):
        if not has_required_tags(v):
            raise AssertionError(f"Missing tags in valid sample #{i}")

    # Uniqueness & split integrity
    set_train = set(train)
    set_valid = set(valid)
    if len(set_train) != len(train):
        raise AssertionError("Train set contains duplicate text entries")
    if len(set_valid) != len(valid):
        raise AssertionError("Valid set contains duplicate text entries")
    overlap = set_train.intersection(set_valid)
    if overlap:
        raise AssertionError(f"Train/valid overlap detected: {len(overlap)} entries")

    print("Validation passed: format, tags, uniqueness, split.")


if __name__ == "__main__":
    main()
