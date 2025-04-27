import os
import re

# 定义输入和输出文件名
input_file = 'alignments.txt'

# 检查输入文件是否存在
if not os.path.isfile(input_file):
    print(f"未找到文件 {input_file}，请确保该文件存在于当前目录。")
    exit(1)

# 读取alignments.txt文件
with open(input_file, 'r') as file:
    lines = file.readlines()

# 确保文件中有内容
if len(lines) < 2:
    print(f"文件 {input_file} 中没有足够的数据。")
    exit(1)

# 提取标题行
header = lines[0].strip()

# 遍历每一行数据（从第二行开始）
for line in lines[1:]:
    line = line.strip()
    if not line:
        continue  # 跳过空行

    # 使用正则表达式提取Me_N中的N
    match = re.search(r'Me_(\d+)', line)
    if match:
        N = match.group(1)
        output_filename = f"Me_{N}.tsv"

        # 写入TSV文件
        with open(output_filename, 'w') as outfile:
            outfile.write(header + '\n')
            outfile.write(line + '\n')

        print(f"已创建文件 {output_filename}")
    else:
        print(f"无法从以下行中提取编号：\n{line}")
