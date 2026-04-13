import json
import shutil
from pathlib import Path
from typing import Dict, List


class StorageEngine:
    """
    XPADI Proof Engine V1
    Storage/distribution layer for encrypted fragments.

    Responsibilities:
    - Ensure survivability bucket structure exists
    - Place fragments into deterministic buckets
    - Persist updated metadata manifest
    - Support relocation scenarios for testing
    - Provide inventory checks before recovery
    """

    BUCKETS = ("a", "b", "c")

    def __init__(self, fragment_root: str):
        self.fragment_root = Path(fragment_root)
        self.fragment_root.mkdir(parents=True, exist_ok=True)
        self._ensure_buckets()

    # --------------------------------------------------
    # INTERNAL
    # --------------------------------------------------
    def _ensure_buckets(self) -> None:
        for bucket in self.BUCKETS:
            (self.fragment_root / bucket).mkdir(parents=True, exist_ok=True)

    def _bucket_path(self, bucket: str) -> Path:
        if bucket not in self.BUCKETS:
            raise ValueError(f"Invalid bucket: {bucket}")
        return self.fragment_root / bucket

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------
    def save_metadata(self, metadata: Dict) -> str:
        file_hash = metadata.get("file_hash")
        if not file_hash:
            raise ValueError("Metadata missing file_hash")

        meta_path = self.fragment_root / f"{file_hash}.meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return str(meta_path)

    def load_metadata(self, meta_path: str) -> Dict:
        meta_file = Path(meta_path)
        if not meta_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {meta_file}")

        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # --------------------------------------------------
    # DISTRIBUTION
    # --------------------------------------------------
    def distribute_fragments(self, metadata: Dict) -> Dict:
        """
        Ensures all fragment paths are correctly placed under their assigned buckets.
        Useful after encryption or when normalizing runtime state.
        """
        updated_fragments: List[Dict] = []

        for frag in metadata.get("fragments", []):
            source = Path(frag["path"])
            if not source.exists():
                raise FileNotFoundError(f"Fragment missing during distribution: {source}")

            bucket = frag["bucket"]
            target_dir = self._bucket_path(bucket)
            target = target_dir / source.name

            if source.resolve() != target.resolve():
                shutil.move(str(source), str(target))

            frag["path"] = str(target)
            updated_fragments.append(frag)

        metadata["fragments"] = updated_fragments
        metadata["storage"] = {
            "mode": "bucketed_distribution",
            "buckets": list(self.BUCKETS),
            "root": str(self.fragment_root)
        }
        return metadata

    # --------------------------------------------------
    # INVENTORY / HEALTH
    # --------------------------------------------------
    def inventory(self, metadata: Dict) -> Dict:
        """
        Returns current storage visibility and missing paths.
        """
        result = {
            "total_fragments": len(metadata.get("fragments", [])),
            "present": 0,
            "missing": 0,
            "missing_ids": [],
            "bucket_counts": {b: 0 for b in self.BUCKETS}
        }

        for frag in metadata.get("fragments", []):
            path = Path(frag["path"])
            bucket = frag["bucket"]

            if path.exists():
                result["present"] += 1
                if bucket in result["bucket_counts"]:
                    result["bucket_counts"][bucket] += 1
            else:
                result["missing"] += 1
                result["missing_ids"].append(frag["id"])

        return result

    # --------------------------------------------------
    # RELOCATION SUPPORT
    # --------------------------------------------------
    def relocate_bucket(self, bucket: str, new_root: str, metadata: Dict) -> Dict:
        """
        Moves an entire bucket to another root folder.
        This is useful for simulating device/path movement while preserving survivability.
        """
        if bucket not in self.BUCKETS:
            raise ValueError(f"Invalid bucket: {bucket}")

        source_dir = self._bucket_path(bucket)
        new_root_path = Path(new_root)
        new_root_path.mkdir(parents=True, exist_ok=True)

        target_dir = new_root_path / bucket
        if target_dir.exists():
            shutil.rmtree(target_dir)

        shutil.move(str(source_dir), str(target_dir))

        # Recreate empty original bucket to preserve expected structure
        source_dir.mkdir(parents=True, exist_ok=True)

        updated_fragments: List[Dict] = []
        for frag in metadata.get("fragments", []):
            if frag["bucket"] == bucket:
                old_name = Path(frag["path"]).name
                frag["path"] = str(target_dir / old_name)
            updated_fragments.append(frag)

        metadata["fragments"] = updated_fragments
        metadata.setdefault("relocations", []).append({
            "bucket": bucket,
            "new_root": str(new_root_path),
            "target_dir": str(target_dir)
        })

        return metadata

    # --------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------
    def normalize_paths(self, metadata: Dict) -> Dict:
        """
        Rebuilds fragment paths based on current bucket + filename assumptions.
        Useful if manifest was loaded on another machine/path.
        """
        updated_fragments: List[Dict] = []

        for frag in metadata.get("fragments", []):
            current_name = Path(frag["path"]).name
            bucket_dir = self._bucket_path(frag["bucket"])
            frag["path"] = str(bucket_dir / current_name)
            updated_fragments.append(frag)

        metadata["fragments"] = updated_fragments
        return metadata


# ------------------------------------------------------
# TEST
# ------------------------------------------------------
if __name__ == "__main__":
    from core.fragment import FragmentEngine
    from core.encrypt import EncryptionEngine

    test_file = "sample_input.txt"
    fragment_root = "data/fragments"

    frag_engine = FragmentEngine(fragment_root)
    enc_engine = EncryptionEngine()
    store_engine = StorageEngine(fragment_root)

    # Create sample file if missing
    sample = Path(test_file)
    if not sample.exists():
        sample.write_text("XPADI PROOF ENGINE TEST DATA\n" * 50000, encoding="utf-8")

    metadata = frag_engine.fragment_file(str(sample))
    metadata = enc_engine.encrypt_all(metadata)
    metadata = store_engine.distribute_fragments(metadata)
    meta_path = store_engine.save_metadata(metadata)

    print("\n[✓] Distribution complete")
    print(f"[✓] Metadata saved: {meta_path}")
    print("[✓] Inventory:", store_engine.inventory(metadata))

    metadata = store_engine.relocate_bucket("b", "data/relocated", metadata)
    store_engine.save_metadata(metadata)

    print("[✓] Bucket 'b' relocated successfully")
    print("[✓] Inventory after relocation:", store_engine.inventory(metadata))