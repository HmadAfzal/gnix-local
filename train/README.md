# Training
This folder contains the notebooks used to build the dataset pipeline and fine-tuning setup for Gnix.

## Initial Plan
The original plan for Genix was to fine-tune a small language model specifically on natural language to shell command pairs, so the tool could run completely locally without depending on a general purpose pretrained model.

The planned pipeline was:

1. Download and combine multiple NL to bash datasets from HuggingFace
2. Clean and normalize everything into a single training file
3. Fine-tune `microsoft/Phi-3.5-mini-instruct` using LoRA and 4-bit quantization on a free GPU
4. Quantize the final model to GGUF format for fast local CPU inference
5. Ship the fine-tuned model inside the Gnix CLI

## What Was Built

**dataset.ipynb** — fully working dataset pipeline that:
- Downloads 3 datasets from HuggingFace totalling ~36,500 raw examples
- Normalizes field names, cleans bad rows, removes duplicates
- Combines everything into a single dataset of ~19,800 examples
- Splits into train (17,820 rows) and test (1,981 rows)
- Published dataset: [llhax/nlbash-cleaned](https://huggingface.co/datasets/llhax/nlbash-cleaned)

**train.ipynb** — LoRA fine-tuning setup for Phi-3.5-mini-instruct that:
- Loads the model in 4-bit quantized form using bitsandbytes
- Applies LoRA adapters on attention layers (q, k, v, o projections)
- Uses SFTTrainer
- Saves checkpoints to Google Drive and HuggingFace

## Why Fine-tuning Was Dropped

Fine-tuning was attempted across multiple sessions on both Kaggle and Google Colab free tiers. The process kept getting interrupted due to:

- **GPU time limits** — Kaggle gives 30 hours per week, Colab disconnects randomly
- **Storage limits** — free tier storage fills up quickly with model checkpoints
- **Out of memory errors** — 4-bit quantized Phi-3.5-mini pushed T4 VRAM to its limits
- **Training time** — 3 epochs on 17,820 examples took 7-8 hours total, too long for any free tier session in one shot

After several days of attempts, the decision was made to ship Gnix v1 using a pretrained model with a strong system prompt. This is a pragmatic and valid approach, the pretrained model already has strong knowledge of shell commands and performs well on the task.

Fine-tuning remains the goal for a future version once proper GPU access is available.

## Dataset

The cleaned dataset is publicly available on HuggingFace and can be used by anyone who wants to fine-tune their own model for this task:

[llhax/nlbash-cleaned](https://huggingface.co/datasets/llhax/nlbash-cleaned)