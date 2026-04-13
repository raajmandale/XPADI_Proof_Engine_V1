import hashlib
from pathlib import Path
from typing import Dict


class ReconstructionEngine:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _read_fragment(self, path: str) -> bytes:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Fragment missing: {p}")

        with open(p, "rb") as f:
            return f.read()

    def reconstruct_file(self, metadata: Dict) -> str:
        fragments = metadata.get("fragments", [])
        if not fragments:
            raise ValueError("No fragments found in metadata")

        fragments_sorted = sorted(fragments, key=lambda x: x["index"])

        reconstructed_data = bytearray()

        for frag in fragments_sorted:
            data = self._read_fragment(frag["path"])

            current_hash = hashlib.sha256(data).hexdigest()
            if current_hash != frag["hash"]:
                raise ValueError(
                    f"Fragment integrity mismatch: {frag['id']}"
                )

            reconstructed_data.extend(data)

        original_name = Path(metadata["original_file"]).name
        output_file = self.output_dir / f"recovered_{original_name}"

        with open(output_file, "wb") as f:
            f.write(reconstructed_data)

        return str(output_file)