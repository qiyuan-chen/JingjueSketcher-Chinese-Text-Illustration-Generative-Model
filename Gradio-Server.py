import json
import http
import gradio
import random
import urllib
import hashlib
import requests
import numpy as npy


def translate(translate_text):
    appid = ""
    secretKey = ""
    httpClient = None

    text = urllib.parse.quote(translate_text)

    salt = random.randint(3276, 65536)

    sign = appid + translate_text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()

    url = f"/api/trans/vip/translate?appid={appid}&q={text}&from=auto&to=en&salt={salt}&sign={sign}"

    try:
        httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
        httpClient.request("GET", url)
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        return result["trans_result"][0]["dst"]

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


tuol_url: str = ""
diff_url: str = ""

styles = {
    "无风格": "",
    "油画": "Oil painting",
    "水彩画": "Watercolor painting",
    "素描": "Sketch",
    "中国画": "Chinese painting",
    "印象派": "Impressionism",
    "表现主义": "Expressionism",
    "抽象派": "Abstract art",
    "极简主义": "Minimalism",
}

colors = {"黑白": "black and white", "彩色": "colored"}


def text2img(text, color, style):
    prompt_zh = requests.post(url=tuol_url, data={"text": text}).json()['prompt']
    prompt_en = translate(prompt_zh)
    diff_res = requests.post(
        url=diff_url,
        data={"prompt": prompt_en, "color": colors[color], "style": styles[style]},
    ).json()
    image = npy.array(diff_res['image'])
    return image


interface = gradio.Interface(
    fn=text2img,
    inputs=[
        gradio.Textbox(label="课文"),
        gradio.components.Dropdown(label="色彩", choices=list(colors.keys())),
        gradio.components.Dropdown(label="绘画风格", choices=list(styles.keys())),
    ],
    outputs=[gradio.Image(label="插图")],
)


if __name__ == "__main__":
    with open("./config.json", "r") as config:
        conf = json.load(config)

    host = conf["ListenIP"]
    port = conf["GradioPort"]
    tport = conf["TuoLingPort"]
    dport = conf["DiffusionPort"]
    tuol_url = f"http://{host}:{tport}/TuoLingC"
    diff_url = f"http://{host}:{dport}/diffusion"

    interface.launch(server_port=int(port), share=True)
