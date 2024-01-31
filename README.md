# Mistral-doc (fine tune Mistral 7B on your own GPT data)

> [!IMPORTANT]  
> This is very ilegal according to OpenAI so it's not like you should do it or anything
> this is all a joke and I obviously did not do it, because rainbows are great and unicorns are marvelous


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

We got a model, but it's not the whole model, it's a LORA. Let's get the whole model. 

1. Merge the model to base

```bash
$ python3 -m axolotl.cli.merge_lora config.yml 
# You should get a whole model in `{lora_model_dir}/merged`
```
2. Let's upload the merged model to hf
```bash
$ cd <merged_path>
$ git lfs install
$ huggingface-cli repo create <your_merged_repo_name>
$ huggingface-cli upload <your_merged_repo_name> .
```

Cool, verify the repo with the merged model exists, and then TURN OFF YOUR RUNPOD MACHINE.

