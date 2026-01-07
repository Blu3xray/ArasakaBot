# Arasaka Intelligence Fine-Tuning (QLoRA / MLX)

Fine-tuning Gemma 2 9B jako bota propagandowego korporacji Arasaka (Cyberpunk 2077) metodą QLoRA na Apple Silicon (MLX).

---

## Struktura projektu

```
├── .vscode/
│   └── tasks.json              # Taski: trening + porównania + ewaluacja
├── generate_large_dataset.py   # Generator dużego datasetu (1000+)
├── validate_data.py            # Walidator JSONL i tagów Gemmy
├── eval.py                     # Ewaluacja modelu po treningu
├── data/
│   ├── train_large.jsonl       # Duży zbiór treningowy (1000)
│   └── valid_large.jsonl       # Duży zbiór walidacyjny (100)
└── adapters/                   # Tutaj zapiszą się wagi LoRA
```

---

## Wymagania

- macOS z Apple Silicon (M1/M2/M3/M4)
- Python 3.10+
- Dostęp do Hugging Face (model `google/gemma-2-9b-it`)

Przed pierwszym treningiem:
- Zaloguj się w CLI: `huggingface-cli login`
- Wejdź na stronę modelu `google/gemma-2-9b-it` i zaakceptuj warunki (jeśli wymagane), inaczej pobieranie może zostać zablokowane.

### Instalacja zależności

```zsh
pip install mlx mlx-lm
```

Opcjonalnie (jeśli potrzebujesz HF CLI):

```zsh
pip install huggingface_hub
huggingface-cli login
```

---

## Generowanie danych

### Duży zbiór (1000 train / 100 valid)

```zsh
python3 generate_large_dataset.py --train-size 1000 --valid-size 100
```

Możesz zmienić rozmiar (np. 3000/300):

```zsh
python3 generate_large_dataset.py --train-size 3000 --valid-size 300
```

### Walidacja

```zsh
python3 validate_data.py
```

---

## Trening QLoRA

> **Uwaga:** Nazwy flag mogą się różnić w zależności od wersji MLX-LM. Sprawdź `python3 -m mlx_lm.finetune --help`.

### Wariant A (typowe flagi)

```zsh
caffeinate -dimsu python3 -m mlx_lm.finetune \
  --model google/gemma-2-9b-it \
  --train-file data/train_large.jsonl \
  --val-file data/valid_large.jsonl \
  --iters 600 \
  --batch-size 2 \
  --lora-layers 16 \
  --learning-rate 2e-5 \
  --save-adapter adapters/arasaka-gemma2-9b \
  --quantize 4
```

### Wariant B (alternatywne nazwy)

```zsh
caffeinate -dimsu python3 -m mlx_lm.finetune \
  --model google/gemma-2-9b-it \
  --train data/train_large.jsonl \
  --valid data/valid_large.jsonl \
  --out_dir adapters/arasaka-gemma2-9b \
  --iters 600 \
  --batch_size 2 \
  --lora_layers 16 \
  --learning_rate 2e-5 \
  --bits 4
```

---

## Ewaluacja

### Pojedyncza generacja

```zsh
python3 -m mlx_lm.generate \
  --model google/gemma-2-9b-it \
  --adapter adapters/arasaka-gemma2-9b \
  --prompt "<start_of_turn>user
Dlaczego powierzyć dane i życie Arasace?<end_of_turn>
<start_of_turn>model"
```

### Batch evaluation na zbiorze walidacyjnym

```zsh
python3 eval.py --adapters adapters/arasaka-gemma2-9b --data data/valid_large.jsonl --samples 10
```

### Porównywanie "poziomów nasiąknięcia"

Po wytrenowaniu kilku adapterów (np. `arasaka-light`, `arasaka-medium`, `arasaka-heavy`) możesz porównać odpowiedzi na te same pytania:

```zsh
python3 eval.py \
  --adapters adapters/arasaka-light adapters/arasaka-medium adapters/arasaka-heavy \
  --data data/valid_large.jsonl \
  --samples 3
```

---

## Rozwiązywanie problemów

| Problem                        | Rozwiązanie                                      |
|--------------------------------|--------------------------------------------------|
| Out of memory                  | Zmniejsz `batch_size` do 1                       |
| Overfitting (val_loss rośnie)  | Zmniejsz `learning_rate` do 1e-5 lub skróć iters |
| Nieznane flagi                 | Sprawdź `--help` i dopasuj nazwy                 |

---

## VS Code Tasks

Projekt zawiera `.vscode/tasks.json` z zadaniami:

- **Train QLoRA (Arasaka)** – pełny trening i zapis adaptera
- **Train QLoRA - Level 1/2/3** – trzy adaptery o różnym stopniu „nasiąknięcia”
- **Compare propaganda levels** – porównuje odpowiedzi wielu adapterów (korzysta z `eval.py`)
- **Validate Data** – sprawdza poprawność JSONL
- **Evaluate Model** – generuje odpowiedzi testowe
- **Generate Large Dataset** – generuje `train_large.jsonl` i `valid_large.jsonl`

Uruchom przez `Cmd+Shift+P` → `Tasks: Run Task`.

---

## Licencja

Projekt edukacyjny / fan-made w uniwersum Cyberpunk 2077. Arasaka™ jest własnością CD Projekt RED / R. Talsorian Games.
