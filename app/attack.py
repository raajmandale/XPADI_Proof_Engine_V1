from pathlib import Path
import random


class AttackEngine:
    def __init__(self):
        pass

    def delete_original(self, file_path: str):
        # SAFE MODE: never delete any file from user's machine
        print(f"[SAFE MODE] Original file deletion blocked: {file_path}")
        return False

    def corrupt_fragments(self, metadata: dict, count: int = 0):
        # SAFE MODE for now
        return []

    def delete_fragments(self, metadata: dict, count: int = 0):
        # SAFE MODE for now
        return []