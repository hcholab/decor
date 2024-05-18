import torch

x = torch.arange(12, dtype=torch.float32)
print(x)
print(x.numel())
print(x.shape)

X = x.reshape(3, 4)
print(X)

print(torch.zeros((2, 3, 4)))

print(torch.randn(3, 4))

a, b = 3, 4  # dimension of the pytorch tensor to be generated
low, high = 0, 1  # range of uniform distribution
x = torch.distributions.uniform.Uniform(low, high).sample([a, b])
print(x)

x = torch.tensor([[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
print(x)

print()


def f(x, y):
    return x + y


x = torch.tensor([1, 2, 4, 8])
y = torch.tensor([2, 2, 2, 2])
print(f"x = {x}, y = {y}")
print(x + y, f(x, y), x - y, x * y, x / y, x**y)
# concatanate tensors columnwise  x + y, f(x, y), x - y, x * y, x / y, x**y
# z = torch.cat((x, y), dim=1)
