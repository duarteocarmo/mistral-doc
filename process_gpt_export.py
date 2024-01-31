import json
import pandas
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
import subprocess
import typing as t
import fire
import os


def login_to_huggingface(token):
    subprocess.run(["huggingface-cli", "login", "--token", token], check=True)


# stolen from langchain
def concatenate_rows(message: dict, title: str) -> t.Optional[dict]:
    if not message:
        return None

    sender = message["author"]["role"] if message["author"] else "unknown"

    if "parts" not in message["content"]:
        return None

    metadata = message.get("metadata", {})
    is_user_system_message = metadata.get("is_user_system_message", False)

    if is_user_system_message is True:
        user_about_message = metadata["user_context_message_data"]["about_user_message"]
        about_model_message = metadata["user_context_message_data"][
            "about_model_message"
        ]
        total_system_message = f"ABOUT YOU:\n{about_model_message}\n\nABOUT YOUR USER:\n{user_about_message}\n\nFIRST MESSAGE FROM THE USER:\n\n"
        return {"sender": "system", "text": total_system_message}

    text = message["content"]["parts"][0]

    if text == "":
        return None

    return {"sender": sender, "text": text}


def load_documents(data: dict) -> list[list[dict]]:
    documents = []
    for d in data:
        title = d["title"]
        messages = d["mapping"]
        conversation = [
            concatenate_rows(messages[key]["message"], title)
            for _, key in enumerate(messages)
        ]
        conversation = [x for x in conversation if x]
        documents.append(conversation)

    return documents


def format_conversation(conversation: list[dict]) -> str:
    bos_token = "<s>"
    eos_token = "</s>"
    instruction_token = "[INST]"
    instruction_end_token = "[/INST]"

    prompt = f"{bos_token}{instruction_token} "

    first_message = conversation[0]
    if first_message["sender"] == "system":
        system_prompt = [m["text"] for m in conversation if m["sender"] == "system"][-1]
        prompt += system_prompt

    else:
        assert first_message["sender"] == "user"

    for message in conversation:
        if message["sender"] == "system":
            continue
        elif message["sender"] == "user":
            prompt += f" {message['text']} {instruction_end_token}"

        elif message["sender"] == "assistant":
            prompt += f" {message['text']} {eos_token} {instruction_end_token}"

    return prompt


def format_and_push(
    documents: list[list[dict]],
    hf_dataset_name: str,
) -> None:
    dataset_file_name = "dataset.jsonl"
    dataset = [{"text": format_conversation(c)} for c in documents]
    print(f"Formatted {len(dataset)} conversations")

    # random.seed(42)
    # to_preview = random.sample(dataset, 1)
    # for d in to_preview:
    #     print(d["text"])
    #     print("-" * 50)

    # save to jsonl
    with open(dataset_file_name, "w") as f:
        for d in dataset:
            f.write(json.dumps(d) + "\n")

    print(f"Saved dataset to {dataset_file_name}")

    # read and split
    df = pandas.read_json(dataset_file_name, lines=True)
    train_df, test_df = train_test_split(
        df, test_size=0.10, random_state=42, shuffle=True
    )

    assert isinstance(train_df, pandas.DataFrame)
    assert isinstance(test_df, pandas.DataFrame)

    # push to hub
    train_tiger = Dataset.from_pandas(train_df)
    test_tiger = Dataset.from_pandas(test_df)

    ds = DatasetDict()
    ds["train"] = train_tiger
    ds["test"] = test_tiger

    ds.push_to_hub(hf_dataset_name, revision="main", private=True)

    os.remove(dataset_file_name)


# format: <s>[INST] System Prompt + Instruction [/INST] Model answer</s>[INST] Follow-up instruction [/INST]


def main(export_file_name: str, hf_dataset_name: str, hf_token: str):
    data = json.load(open(export_file_name))
    print(f"Loaded {len(data)} conversations from your export.")

    login_to_huggingface(hf_token)
    print("Logged in to HuggingFace")

    documents = load_documents(data)
    print(f"Loaded {len(documents)} documents")

    format_and_push(
        documents=documents,
        hf_dataset_name=hf_dataset_name,
    )
    print(f"Pushed dataset to https://huggingface.co/datasets/{hf_dataset_name}")


# lol, if you end up here email me: me at duarteocarmo.com :)
if __name__ == "__main__":
    fire.Fire(main)
