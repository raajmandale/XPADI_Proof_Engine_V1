import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets


class EncryptionEngine:
    def __init__(self, key: bytes = None):
        # 256-bit key
        self.key = key if key else AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    # -----------------------------
    # ENCRYPT FRAGMENT
    # -----------------------------
    def encrypt_fragment(self, fragment_path: str) -> str:
        fragment_path = Path(fragment_path)

        if not fragment_path.exists():
            raise FileNotFoundError(f"Fragment not found: {fragment_path}")

        with open(fragment_path, "rb") as f:
            data = f.read()

        nonce = secrets.token_bytes(12)  # 96-bit nonce
        encrypted_data = self.aesgcm.encrypt(nonce, data, None)

        encrypted_path = fragment_path.with_suffix(".enc")

        with open(encrypted_path, "wb") as f:
            f.write(nonce + encrypted_data)

        # remove original fragment
        os.remove(fragment_path)

        return str(encrypted_path)

    # -----------------------------
    # DECRYPT FRAGMENT
    # -----------------------------
    def decrypt_fragment(self, encrypted_path: str) -> str:
        encrypted_path = Path(encrypted_path)

        if not encrypted_path.exists():
            raise FileNotFoundError(f"Encrypted fragment not found: {encrypted_path}")

        with open(encrypted_path, "rb") as f:
            content = f.read()

        nonce = content[:12]
        encrypted_data = content[12:]

        decrypted_data = self.aesgcm.decrypt(nonce, encrypted_data, None)

        original_path = encrypted_path.with_suffix(".frag")

        with open(original_path, "wb") as f:
            f.write(decrypted_data)

        return str(original_path)

    # -----------------------------
    # BATCH ENCRYPT
    # -----------------------------
    def encrypt_all(self, metadata: dict) -> dict:
        updated_fragments = []

        for frag in metadata["fragments"]:
            encrypted_path = self.encrypt_fragment(frag["path"])

            frag["path"] = encrypted_path
            frag["encrypted"] = True

            updated_fragments.append(frag)

        metadata["fragments"] = updated_fragments
        metadata["encryption"] = {
            "type": "AES-GCM",
            "mode": "per-fragment"
        }

        return metadata

    # -----------------------------
    # BATCH DECRYPT
    # -----------------------------
    def decrypt_all(self, metadata: dict) -> dict:
        updated_fragments = []

        for frag in metadata["fragments"]:
            decrypted_path = self.decrypt_fragment(frag["path"])

            frag["path"] = decrypted_path
            frag["encrypted"] = False

            updated_fragments.append(frag)

        metadata["fragments"] = updated_fragments

        return metadata


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    from fragment import FragmentEngine

    frag_engine = FragmentEngine("data/fragments")
    enc_engine = EncryptionEngine()

    test_file = "sample_input.txt"

    meta = frag_engine.fragment_file(test_file)

    print("\n[✓] Fragmentation complete")

    meta = enc_engine.encrypt_all(meta)
    print("[✓] Encryption complete")

    meta = enc_engine.decrypt_all(meta)
    print("[✓] Decryption complete")