import platform
import psutil
import subprocess
import json

def get_system_info():
    # CPU
    cpu_name = platform.processor() or platform.machine()
    
    # RAM (GB)
    ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    
    # GPU & VRAM via nvidia-smi
    gpu_name = "Unknown"
    vram_gb = 0
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(',')
            if len(parts) >= 2:
                gpu_name = parts[0].strip()
                vram_mb = float(parts[1].strip())
                vram_gb = round(vram_mb / 1024, 1)
    except:
        pass

    # Fallback cho CPU (nếu chạy trên môi trường không có Nvidia)
    if gpu_name == "Unknown":
        gpu_name = platform.uname().processor or "CPU-only"

    return {
        "cpu": cpu_name,
        "ram_gb": ram_gb,
        "gpu": gpu_name,
        "vram_gb": vram_gb,
        "os": platform.platform()
    }

if __name__ == "__main__":
    info = get_system_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
    # Lưu vào file temp để Agent đọc
    with open("system_specs.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
