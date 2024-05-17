from time import process_time
import torch


def testgpu():
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
    t0 = process_time()
    x = torch.ones(n1, device=mps_device)
    x = x + torch.rand(n1, device=mps_device)
    t1 = process_time()
    print(f"Total time with gpu ({n1}): {t1-t0}")
    t0 = process_time()
    x = torch.ones(n2, device=mps_device)
    x = x + torch.rand(n2, device=mps_device)
    t1 = process_time()
    print(f"Total time with gpu ({n2}): {t1-t0}")


def testcpu():
    t0 = process_time()
    x = torch.ones(n1)
    x = x + torch.rand(n1)
    t1 = process_time()
    print(f"Total time with cpu ({n1}): {t1-t0}")
    t0 = process_time()
    x = torch.ones(n2)
    x = x + torch.rand(n2)
    t1 = process_time()
    print(f"Total time with cpu ({n2}): {t1-t0}")


if __name__ == "__main__":
    n1 = 1000
    n2 = 10000000
    testcpu()
    testgpu()
