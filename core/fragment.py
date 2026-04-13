import os
import hashlib
import json
from pathlib import Path
from typing import List, Dict

CHUNK_SIZE = 1024 * 1024  # 1MB


class FragmentEngine:
    def __init__(self, fragment_root: str):
        self.fragment_root = Path(fragment_root)
        self.fragment_root.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # HASH UTIL
    # -----------------------------
    def _hash_file(self, file_path: str) -> str:
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()

    # -----------------------------
    # FRAGMENT
    # -----------------------------
    def fragment_file(self, file_path: str) -> Dict:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = file_path.stat().st_size
        file_hash = self._hash_file(file_path)

        fragments = []
        fragment_index = 0

        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break

                fragment_id = f"{file_hash[:12]}_{fragment_index}"
                fragment_hash = hashlib.sha256(chunk).hexdigest()

                # distribution logic (simple round-robin)
                bucket = ["a", "b", "c"][fragment_index % 3]
                bucket_path = self.fragment_root / bucket
                bucket_path.mkdir(exist_ok=True)

                fragment_file = bucket_path / f"{fragment_id}.frag"

                with open(fragment_file, 'wb') as frag:
                    frag.write(chunk)

                fragments.append({
                    "id": fragment_id,
                    "index": fragment_index,
                    "bucket": bucket,
                    "path": str(fragment_file),
                    "hash": fragment_hash,
                    "size": len(chunk)
                })

                fragment_index += 1

        metadata = {
            "original_file": str(file_path),
            "file_size": file_size,
            "file_hash": file_hash,
            "chunk_size": CHUNK_SIZE,
            "total_fragments": len(fragments),
            "fragments": fragments
        }

        meta_path = self.fragment_root / f"{file_hash}.meta.json"
        with open(meta_path, "w") as m:
            json.dump(metadata, m, indent=2)

        return metadata

    # -----------------------------
    # LOAD METADATA
    # -----------------------------
    def load_metadata(self, meta_file: str) -> Dict:
        with open(meta_file, 'r') as f:
            return json.load(f)

    # -----------------------------
    # VALIDATE FRAGMENTS
    # -----------------------------
    def validate_fragments(self, metadata: Dict) -> List[str]:
        missing = []

        for frag in metadata["fragments"]:
            path = Path(frag["path"])

            if not path.exists():
                missing.append(frag["id"])
                continue

            with open(path, 'rb') as f:
                data = f.read()

            if hashlib.sha256(data).hexdigest() != frag["hash"]:
                missing.append(frag["id"])

        return missing


# -----------------------------
# CLI TEST (FOR INTERNAL USE)
# -----------------------------
if __name__ == "__main__":
    engine = FragmentEngine("data/fragments")

    test_file = "sample_input.txt"

    if not Path(test_file).exists():
        with open(test_file, "w") as f:
            f.write("XPADI TEST DATA " * 100000)

    meta = engine.fragment_file(test_file)

    print("\n[✓] Fragmentation Complete")
    print(f"Total fragments: {meta['total_fragments']}")
    print(f"File hash: {meta['file_hash']}")

    missing = engine.validate_fragments(meta)

    if not missing:
        print("[✓] All fragments valid")
    else:
        print("[!] Missing/Corrupt fragments:", missing)