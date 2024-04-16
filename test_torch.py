import torch

def check_pytorch_installation():
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
    except ImportError:
        print("PyTorch is not installed.")

def check_cuda_availability():
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU.")
    else:
        print("CUDA is not available. Using CPU.")

if __name__ == "__main__":
    check_pytorch_installation()
    check_cuda_availability()
