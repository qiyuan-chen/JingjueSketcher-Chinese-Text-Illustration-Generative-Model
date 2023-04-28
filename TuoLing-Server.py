import json
import torch
from utils import DeviceMap
from flask import Flask, request, jsonify
from transformers import AutoModel, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType

torch.set_default_tensor_type(torch.cuda.HalfTensor)

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)

model = AutoModel.from_pretrained(
    "THUDM/chatglm-6b", trust_remote_code=True, device_map=DeviceMap("ChatGLM").get()
)

# This model is finetuned by Luotuo Team: Li Cheng@Sensetime, Leng Ziang@Sensetime, Chen Qiyuan@CCNU and other 6 members
# Main Github Repo is at https://github.com/LC1332/Luotuo-Chinese-LLM

# https://github.com/LC1332/luotuo-silk-road/blob/main/TuoLing/output/luotuoC.pt
peft_path = "./model/TuoLingC.pt"

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=True,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
)

lora = get_peft_model(model, peft_config)

lora.load_state_dict(torch.load(peft_path), strict=False)

torch.set_default_tensor_type(torch.cuda.FloatTensor)


def format_example(example: dict) -> dict:
    context = f"Instruction: {example['instruction']}\n"
    if example.get("input"):
        context += f"Input: {example['input']}\n"
    context += "Answer: "
    target = example["output"]
    return {"context": context, "target": target}


def evaluate(instruction, input=None):
    with torch.no_grad():
        feature = format_example(
            {
                "instruction": "请帮我为以下内容拟定一个简短的标题:",
                "input": f"{instruction}",
                "output": "",
            }
        )
        input_text = feature["context"]
        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        out = lora.generate(input_ids=input_ids, max_length=2048, temperature=0)
        answer = tokenizer.decode(out[0])
        return answer


app = Flask(__name__)


@app.route("/TuoLingC", methods=["POST"])
def TuoLingC():
    text = request.values.get("text")
    prompt = evaluate(text)
    pos = prompt.find("Answer: ")
    prompt = prompt[pos + len("Answer: ") :]
    return jsonify({"prompt": prompt})


if __name__ == "__main__":
    with open("./config.json", "r") as config:
        conf = json.load(config)
    host = conf["ListenIP"]
    port = conf["TuoLingPort"]
    app.run(host=host, port=port)
