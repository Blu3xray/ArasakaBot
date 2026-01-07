# Data

This repository does **not** commit the generated JSONL datasets (they can be large and are fully reproducible).

## Generate datasets

```zsh
python3 generate_large_dataset.py --train-size 1000 --valid-size 100
```

This produces:
- `data/train_large.jsonl`
- `data/valid_large.jsonl`

## Validate datasets

```zsh
python3 validate_data.py --train-file data/train_large.jsonl --valid-file data/valid_large.jsonl
```
