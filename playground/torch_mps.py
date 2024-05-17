import torch
from time import process_time
import time

# Check that MPS is available
if not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print(
            "MPS not available because the current PyTorch install was not "
            "built with MPS enabled."
        )
    else:
        print(
            "MPS not available because the current MacOS version is not 12.3+ "
            "and/or you do not have an MPS-enabled device on this machine."
        )

else:
    t0 = process_time()
    mps_device = torch.device("mps")
    # mps_device = None

    # # Create a Tensor directly on the mps device
    # x = torch.ones(1000, device=mps_device)

    # print(x)
    # # Any operation happens on the GPU
    # y = x * 2
    # print(y)

# Element Wise operations (multiplication,addition,subtraction)
dim = 10000

x = torch.randn(dim, dim)
y = torch.randn(dim, dim)
start_time = time.time()
a = x * y
b = x + y
c = x - y
elapsed_time = time.time() - start_time
print("CPU_time = ", elapsed_time)


x = torch.randn(dim, dim, device=mps_device)
y = torch.randn(dim, dim, device=mps_device)
start_time = time.time()
a = x * y
b = x + y
c = x - y
elapsed_time = time.time() - start_time
print("GPU_time = ", elapsed_time)
