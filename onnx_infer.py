import numpy as np
import onnxruntime as ort

# 加载合并后的模型
model_path = "combined_model.onnx"
session = ort.InferenceSession(model_path)

# 获取模型的输入和输出名称
input_name = session.get_inputs()[0].name
output_names = [output.name for output in session.get_outputs()]

# 创建一个示例输入数据
# 假设输入形状为 (batch_size, channels, height, width)
input_data = np.random.randn(1, 224, 224, 3).astype(np.float32)

# 进行推理
outputs = session.run(output_names, {input_name: input_data})

# 输出结果
output1, output2 = outputs
print("Output from model 1:", output1)
print("Output from model 2:", output2)
