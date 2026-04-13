from pathlib import Path
import shutil

from core.fragment import FragmentEngine
from core.encrypt import EncryptionEngine
from core.store import StorageEngine
from core.reconstruct import ReconstructionEngine

from app.attack import AttackEngine
from app.verify import VerifyEngine


class XPADIEngine:
    def __init__(self):
        self.fragment_root = "data/fragments"
        self.output_root = "data/output"
        self.workspace_root = Path("data/workspace")
        self.workspace_root.mkdir(parents=True, exist_ok=True)

        self.fragment = FragmentEngine(self.fragment_root)
        self.encrypt = EncryptionEngine()
        self.store = StorageEngine(self.fragment_root)
        self.reconstruct = ReconstructionEngine(self.output_root)

        self.attack = AttackEngine()
        self.verify = VerifyEngine()

        self.metadata = None
        self.original_file = None
        self.working_file = None

    def _prepare_workspace_copy(self, file_path: str) -> str:
        src = Path(file_path)
        if not src.exists():
            raise FileNotFoundError(f"Selected file not found: {src}")

        self.workspace_root.mkdir(parents=True, exist_ok=True)
        dst = self.workspace_root / src.name
        shutil.copy2(src, dst)
        return str(dst)

    def protect(self, file_path: str):
        self.original_file = file_path
        self.working_file = self._prepare_workspace_copy(file_path)

        self.metadata = self.fragment.fragment_file(self.working_file)
        self.metadata = self.encrypt.encrypt_all(self.metadata)
        self.metadata = self.store.distribute_fragments(self.metadata)

    def simulate_attack(self):
        # SAFE MODE: only attempt against workspace copy
        if self.working_file:
            self.attack.delete_original(self.working_file)

        self.attack.delete_fragments(self.metadata, count=0)
        self.attack.corrupt_fragments(self.metadata, count=0)

    def recover(self):
        self.metadata = self.encrypt.decrypt_all(self.metadata)
        return self.reconstruct.reconstruct_file(self.metadata)

    def verify_result(self, recovered_file: str):
        return self.verify.verify(self.metadata, recovered_file)