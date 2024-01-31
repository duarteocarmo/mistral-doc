# Instructions

1. Export your data from ChatGPT.
2. Load it into Hugging Face (to a private repo), using the following command:

```bash
python process_gpt_export.py --export_file_name datasets/conversations_old.json \
                             --hf_dataset_name duarteocarmo/chatgpt-v2 \ # this is an example
                             --hf_token <your_hf_token>
```

Replace `<your_hf_token>` with your actual Hugging Face token.

