import torch
import subprocess


# Check if CUDA is available
if torch.cuda.is_available():
    # Get the number of available CUDA devices
    num_cuda_devices = torch.cuda.device_count()
    print(f"Found {num_cuda_devices} CUDA device(s) available.")
    
    # Iterate over each CUDA device and print its properties
    for i in range(num_cuda_devices):
        print(f"CUDA device {i}: {torch.cuda.get_device_name(i)}")
else:
    print("CUDA is not available. Make sure CUDA drivers are properly installed.")


for fold in range(0,5):
    command = f"nnUNetv2_train 001 2d {fold} --npz -device cuda"
    # Execute the command
    subprocess.run(command, shell=True)




