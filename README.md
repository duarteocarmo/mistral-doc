# Instructions

1. Export your data from ChatGPT.
2. Clone the repository containing the processing script:

```bash
git clone https://github.com/duarteocarmo/mistral-doc.git
cd mistral-doc
```

3. Install the necessary requirements:

```bash
pip install -r requirements.txt
```

4. Load your exported data into Hugging Face (to a private repo), using the following command:

```bash
python process_gpt_export.py --export_file_name datasets/conversations_old.json \
                             --hf_dataset_name duarteocarmo/chatgpt-v2 \ # this is an example
                             --hf_token <your_hf_token>
```

Replace `<your_hf_token>` with your actual Hugging Face token.

5. Create your config. My example is in `configs/mistral-doc-instruct.yml` (especially wandb and hf sections)
6. Get a runpod machine with a GPU using [this](https://runpod.io/gsc?template=v2ickqhz9s&ref=6i7fkpdz) link (get a machine with at least 40 GB of VRAM) - if you use the link, [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl?tab=readme-ov-file) should already be installed

