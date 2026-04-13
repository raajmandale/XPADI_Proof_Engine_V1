import hashlib


class VerifyEngine:

    @staticmethod
    def hash_file(file_path: str) -> str:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()

    @staticmethod
    def verify(metadata: dict, recovered_file: str) -> bool:
        expected = metadata["file_hash"]
        actual = VerifyEngine.hash_file(recovered_file)

        print("\n===== VERIFICATION =====")
        print(f"Expected:  {expected}")
        print(f"Recovered: {actual}")

        if expected == actual:
            print("\n🔥 SUCCESS: DATA MATCHED")
            return True
        else:
            print("\n❌ FAILURE: DATA MISMATCH")
            return False