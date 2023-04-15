# 精绝绘影：中文文本插图生成模型
精绝绘影是由 熊吉祥，黄泓森，陈启源 @ 华中师范大学 发起的中文文本插图生成项目，[杨海彤](http://cs.ccnu.edu.cn/info/1158/2237.htm)副教授是本项目的指导老师。同时它也是基于[骆驼](https://github.com/LC1332/Luotuo-Chinese-LLM)语言模型的工作。

我们将模型取名为精绝绘影，是因为我们的项目属于[丝绸之路](https://github.com/LC1332/luotuo-silk-road)项目，精绝国也是丝绸之路上的要地。


## 参考
[StableDiffusion](https://github.com/CompVis/stable-diffusion) 是一种优秀的文生图模型。我们的项目使用Stable Diffusion作为图像生成的模型。

[CamelBell](https://github.com/LC1332/CamelBell-Chinese-LoRA)和[Luotuo](https://github.com/LC1332/Luotuo-Chinese-LLM) 是一个基于LoRA技术分别在中文语料上微调ChatGLM和LLaMa的项目。我们的项目使用了CamelBell-C作为摘要模型，并在此基础上进一步作了指令微调。


## 引用

如果这个项目对你有帮助，你可以以如下格式引用：

```
@misc{jingjue,
  author={Jixiang Xiong, Hongsen Huang, Qiyuan Chen, Haitong Yang},
  title = {JingjueSketcher: An Open-Source Chinese Text Illustration Generative Model},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/qiyuan-chen/JingjueSketcher-Chinese-Text-Illustration-Generative-Model}},
}
```


