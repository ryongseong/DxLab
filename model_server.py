from fastapi import FastAPI
import torch

app = FastAPI()

@app.get("/available-gpu")
async def available_gpu():
    cuda_available = torch.cuda.is_available()

    mps_available = torch.backends.mps.is_available()

    if cuda_available:
        gpu_count = torch.cuda.device_count()
        gpu_names = [torch.cuda.get_device_name(i) for i in range(gpu_count)]
        return {"available": True, "gpu_type": "CUDA", "gpu_count": gpu_count, "gpu_names": gpu_names}
    elif mps_available:
        return {"available": True, "gpu_type": "MPS", "gpu_names": ["Apple GPU"]}
    else:
        return {"available": False, "gpu_count": 0, "gpu_names": []}