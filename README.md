# Massive_sub-obj_Judge
批量判断文本主客观水平的脚本 支持两种模式 nlp版/llm版

## How to use
```bash
python -m venv venv
.\venv\Scripts\activate

pip install jieba openpyxl pandas
```
将你想要处理的xlsx文件存储到`input`文件夹中
默认文字存储在`text`列
运行
```bash
python execute.py
```

## NLP part
来自 老刘的 代码 地址: https://github.com/liuhuanyong/ZhuguanDetection

## LLM part 
使用ollama进行模型管理

详见 https://ollama.com/