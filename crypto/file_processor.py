import base64
from pathlib import Path


class FileProcessor:
    def read_file(self, filepath: Path) -> bytes:
        """Read file content, handling both binary and base64 encoded files"""
        # Try reading as base64 first
        try:
            with open(filepath, "r") as f:
                content = f.read().strip()
                try:
                    return base64.b64decode(content)
                except:
                    pass
        except:
            pass

        # Fall back to binary reading
        with open(filepath, "rb") as f:
            return f.read()

    def write_file(self, filepath: Path, data: bytes, use_base64: bool = False) -> None:
        """Write file content, optionally using base64 encoding"""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if use_base64:
            encoded_data = base64.b64encode(data).decode("utf-8")
            with open(filepath, "w") as f:
                f.write(encoded_data)
        else:
            with open(filepath, "wb") as f:
                f.write(data)
