# Instructions

## Prepare data

1. Export your data from ChatGPT.
2. Clone the repository containing the processing script:

```bash
$ git clone https://github.com/duarteocarmo/mistral-doc.git
$ cd mistral-doc
```

3. Install the necessary requirements:

```bash
pip install -r requirements.txt
```

4. Load your exported data into Hugging Face (to a private repo), using the following command:

```bash
$ python process_gpt_export.py --export_file_name datasets/conversations_old.json \
                             --hf_dataset_name duarteocarmo/chatgpt-v2 \ # this is an example
                             --hf_token <your_hf_token>
```

Replace `<your_hf_token>` with your actual Hugging Face token.

## Train model

1. Create your config. My example is in `configs/mistral-doc-instruct.yml` (especially wandb and hf sections)
2. Get a runpod machine with a GPU with at least 40 GB of VRAM and the axolotl jupyter lab template - [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl?tab=readme-ov-file) should already be installed in there
3. SSH into the machine 
4. Run the following 
```bash
# move to the right directory
$ cd /workspace/axolotl/

# set creds
$ huggingface-cli login --token <your_hf_token>
$ wandb login <your_wandb_api_key>

# create config file
$ vi config.yaml
# run ':set paste' and then paste your config file

# launch training
$ accelerate launch -m axolotl.cli.train config.yml
```

You should be able to see the model training in wandb and it should be uploaded to hf in the end of training.

## Merge model to base



