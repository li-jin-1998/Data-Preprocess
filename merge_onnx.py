import onnx
from onnx import helper, numpy_helper
import numpy as np
import onnxruntime as ort


def load_model(path):
    return onnx.load(path)


def get_initializer_dict(graph):
    return {init.name: numpy_helper.to_array(init) for init in graph.initializer}


def merge_models(model1, model2):
    # 获取两个模型的图结构
    graph1 = model1.graph
    graph2 = model2.graph

    # 假设两个模型的输入相同，使用 graph1 的输入
    input_tensor = graph1.input[0]

    # 合并初始化器
    initializers = list(graph1.initializer) + list(graph2.initializer)

    # 创建新的节点列表
    nodes = []

    # 处理 graph1 的节点
    for node in graph1.node:
        new_node = helper.make_node(node.op_type, node.input,
                                    [f"{output}_model1" for output in node.output],
                                    name=node.name + "_model1")
        nodes.append(new_node)

    # 处理 graph2 的节点，修改输入名称为 graph1 的输入
    for node in graph2.node:
        new_inputs = [input_name if input_name != graph2.input[0].name else input_tensor.name for input_name in
                      node.input]
        new_node = helper.make_node(node.op_type, new_inputs,
                                    [f"{output}_model2" for output in node.output],
                                    name=node.name + "_model2")
        nodes.append(new_node)

    # 创建新的输出
    output1 = graph1.output[0]
    output2 = graph2.output[0]

    new_output1 = helper.make_tensor_value_info(f"{output1.name}_model1",
                                                output1.type.tensor_type.elem_type,
                                                [dim.dim_value for dim in output1.type.tensor_type.shape.dim])

    new_output2 = helper.make_tensor_value_info(f"{output2.name}_model2",
                                                output2.type.tensor_type.elem_type,
                                                [dim.dim_value for dim in output2.type.tensor_type.shape.dim])

    # 创建新的图
    combined_graph = helper.make_graph(
        nodes,
        "combined_model",
        [input_tensor],
        [new_output1, new_output2],
        initializers
    )

    # 创建新的模型
    combined_model = helper.make_model(combined_graph)

    return combined_model


# 加载两个模型
model1 = load_model("edentulous.onnx")
model2 = load_model("edentulous.onnx")

# 合并模型
combined_model = merge_models(model1, model2)

# 保存合并后的模型
onnx.save(combined_model, "combined_model.onnx")
print("模型合并成功并保存为 combined_model.onnx")


# 使用 ONNX Runtime 进行推理
def run_inference(model_path, input_data):
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_names = [output.name for output in session.get_outputs()]
    outputs = session.run(output_names, {input_name: input_data})
    return outputs


# 创建一个示例输入数据
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)

# 进行推理
outputs = run_inference("combined_model.onnx", input_data)
output1, output2 = outputs
print("Output from model 1:", output1)
print("Output from model 2:", output2)
