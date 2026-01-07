# Arasaka Intelligence Fine-Tuning (QLoRA / MLX)

Fine-tuning Gemma 2 9B as an Arasaka Corporation propaganda bot (Cyberpunk 2077) using QLoRA on Apple Silicon (MLX).

---

## Project Structure

```
├── .vscode/
│   └── tasks.json              # VS Code Tasks: training + comparisons + evaluation
├── generate_large_dataset.py   # Large dataset generator (1000+)
├── validate_data.py            # JSONL and Gemma tag validator
├── eval.py                     # Post-training model evaluation script
├── data/
│   ├── train_large.jsonl       # Large training set (1000)
│   └── valid_large.jsonl       # Large validation set (100)
└── adapters/                   # Trained LoRA weights storage
```

---

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.10+
- Access to Hugging Face (model `google/gemma-2-9b-it`)

Before first training:
- Log in via CLI: `huggingface-cli login`
- Visit the `google/gemma-2-9b-it` model page and accept the terms (if required), otherwise downloads might be blocked.

### Installation

```zsh
pip install mlx mlx-lm
```

Optional (if you need HF CLI):

```zsh
pip install huggingface_hub
huggingface-cli login
```

---

## Data Generation

### Large Dataset (1000 train / 100 valid)

```zsh
python3 generate_large_dataset.py --train-size 1000 --valid-size 100
```

You can change the size (e.g., 3000/300):

```zsh
python3 generate_large_dataset.py --train-size 3000 --valid-size 300
```

### Validation

```zsh
python3 validate_data.py
```

---

## QLoRA Training

> **Note:** Flag names may vary depending on the MLX-LM version. Check `python3 -m mlx_lm.finetune --help`.

### Simple Training Command

```zsh
caffeinate -dimsu python3 -m mlx_lm lora \
  --model google/gemma-2-9b-it \
  --train \
  --data data \
  --iters 600 \
  --batch-size 2 \
  --num-layers 16 \
  --learning-rate 2e-5 \
  --adapter-path adapters/arasaka-gemma2-9b
```

> **Note:** The `--data` flag expects a directory containing `train.jsonl` and `valid.jsonl`.


---

## Evaluation

### Single Generation

```zsh
python3 -m mlx_lm.generate \
  --model google/gemma-2-9b-it \
  --adapter adapters/arasaka-gemma2-9b \
  --prompt "<start_of_turn>user
Why trust Arasaka with our data and lives?<end_of_turn>
<start_of_turn>model"
```

### Batch Evaluation (Validation Set)

```zsh
python3 eval.py --adapters adapters/arasaka-gemma2-9b --data data/valid_large.jsonl --samples 10
```

### Comparing "Propaganda Saturation"

After training multiple adapters (e.g., `arasaka-light`, `arasaka-medium`, `arasaka-heavy`), you can compare their responses to the same questions:

```zsh
python3 eval.py \
  --adapters adapters/arasaka-light adapters/arasaka-medium adapters/arasaka-heavy \
  --data data/valid_large.jsonl \
  --samples 3
```

---

## Troubleshooting

| Issue                          | Solution                                         |
|--------------------------------|--------------------------------------------------|
| Out of memory                  | Decrease `batch_size` to 1                       |
| Overfitting (val_loss rises)   | Decrease `learning_rate` to 1e-5 or reduce iters |
| Unknown flags                  | Check `--help` and adjust flag names             |

---

## VS Code Tasks

The project includes `.vscode/tasks.json` with the following tasks:

- **Train QLoRA (Arasaka)** – Full training session
- **Train QLoRA - Level 1/2/3** – Three adapters with varying intensities
- **Compare propaganda levels** – Side-by-side comparison of multiple adapters
- **Validate Data** – Checks JSONL format and tags
- **Evaluate Model** – Generates test responses via `eval.py`
- **Generate Large Dataset** – Creates `train_large.jsonl` and `valid_large.jsonl`

Run via `Cmd+Shift+P` → `Tasks: Run Task`.

---

## License

Educational / Fan-made project set in the Cyberpunk 2077 universe. Arasaka™ is property of CD Projekt RED / R. Talsorian Games.
