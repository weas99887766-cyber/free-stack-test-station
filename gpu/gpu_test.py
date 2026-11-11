"""Kaggle / Colab shared GPU probe. Reports cpu_only honestly when no GPU."""
import json
import platform
import time
from datetime import datetime, timezone


def main():
    info = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "gpu": [],
        "status": "cpu_only",
        "matmul_ms": None,
    }
    try:
        import torch

        info["torch"] = torch.__version__
        if torch.cuda.is_available():
            info["gpu"] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
            a = torch.randn(2048, 2048, device="cuda")
            b = torch.randn(2048, 2048, device="cuda")
            torch.cuda.synchronize()
            t0 = time.time()
            _ = a @ b
            torch.cuda.synchronize()
            info["matmul_ms"] = round((time.time() - t0) * 1000, 1)
            info["status"] = "gpu_ok"
    except Exception as e:
        info["error"] = str(e)
    with open("result.json", "w") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
