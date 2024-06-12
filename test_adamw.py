import torch
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 定义数据集和数据加载器
data = torch.randn(1000, 10)  # 假设有1000个样本，每个样本有10个特征
labels = torch.randint(0, 2, (1000,))  # 假设二分类任务
dataset = TensorDataset(data, labels)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# 定义模型
model = torch.nn.Linear(10, 2)
criterion = torch.nn.CrossEntropyLoss()

# 创建AdamW优化器
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# 训练循环
num_epochs = 100
for epoch in range(num_epochs):
    for batch_data, batch_labels in data_loader:
        optimizer.zero_grad()
        outputs = model(batch_data)
        loss = criterion(outputs, batch_labels)
        loss.backward()
        optimizer.step()

    # 打印每个epoch的损失
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')
