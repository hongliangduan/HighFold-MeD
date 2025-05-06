import os
import pandas as pd
import subprocess

# 定义路径
base_path = "./targets"
input_file = os.path.join(base_path, "targets.tsv")
output_prefix = "./outputs/"
model_params = "./finetune_params/alphafold_cyclic_params_17500.pkl"

# 读取 targets.tsv 文件
df = pd.read_csv(input_file, sep="\t")

# 遍历每一行
for _, row in df.iterrows():
    # 构造文件名
    target_chainseq = row["target_chainseq"]
    output_file = os.path.join(base_path, f"target999{target_chainseq}999.tsv")

    # 写入新的 TSV 文件
    with open(output_file, "w") as f:
        f.write("peptide\ttargetid\ttarget_chainseq\ttemplates_alignfile\n")
        f.write("\t".join(map(str, row.values)) + "\n")

    # 构造命令
    command = [
        "python", "run_prediction.py",
        "--targets", output_file,
        "--outfile_prefix", output_prefix,
        "--model_names", "model_2_ptm_ft",
        "--model_params_files", model_params,
        "--ignore_identities"
    ]

    # 执行命令
    subprocess.run(command)

print("任务完成！")
