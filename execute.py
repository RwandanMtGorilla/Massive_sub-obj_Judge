import pandas as pd
import ollama.client as client
import re
from zhuguan import *

import pandas as pd
import os
from tqdm import tqdm

handler = ZhuguanDetect()




# 假设函数定义保持不变
def process_response(question, response):
    status_match = re.search(r'status:\s*(\d+)', response)
    text_match = re.search(r'text:\s*(.+)', response, re.DOTALL)
    if status_match and text_match:
        status = status_match.group(1)
        text = text_match.group(1).strip()
        return status, text
    else:
        raise ValueError(f"Invalid response format:\n{response}")

def query_response(query):
    sys_prompt = (
        "您是一位语言学家，擅长判断评论文字的主客观状况\n"
        "您的回答应当是格式化的，且不会有任何多余的文字，示例如下:\n"
        "\tstatus: 1或0 (1代表文本为主观 0则代表文本为客观)\n"
        "\ttext: 在这里书写你判断文字为主观/客观 的理由"
    )
    prompt = f"现在，请进行判断。以下是评论文字:<{query}>\n\n您的回答:"

    response, _ = client.generate(
        model_name="qwen:14b", 
        system=sys_prompt, 
        prompt=prompt
    )
    return process_response(query, response)


files = [file for file in os.listdir('input') if file.endswith('.xlsx')]
# 确保输出目录存在
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
# 逐个文件进行处理
for file in tqdm(files, desc='Processing files'):

    input_path = os.path.join('input', file)
    output_path = os.path.join(output_dir, f"output_{file}")
    # 读取或初始化DataFrame
    if os.path.exists(output_path):
        df = pd.read_excel(output_path)
        # 检查是否有新行需要添加（如果输入文件有更新）
        df_input = pd.read_excel(input_path)
        if len(df_input) > len(df):
            additional_rows = df_input.iloc[len(df):]
            df = pd.concat([df, additional_rows], ignore_index=True)
    else:
        df = pd.read_excel(input_path)
        # 初始化两个新列用于存储结果
        df['nlp_score'] = None
        df['status'] = None
        df['explanation'] = None

    # 对status为空的行进行处理
    for index, row in tqdm(df.iterrows()):
        if pd.isnull(row['status']):
            try:
                sent = row['text']
                score = handler.detect(sent)
                df.at[index, 'nlp_score'] = score
            
                # status, explanation = query_response(row['text'])
                # df.at[index, 'status'] = status
                # df.at[index, 'explanation'] = explanation

            except ValueError as e:
                print(f"Error processing row {index} in {file}: {e}")
    # 保存到输出文件
    df.to_excel(output_path, index=False)

