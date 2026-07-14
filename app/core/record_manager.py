from pathlib import Path


class RecordManager:

    BASE_DIR = Path(__file__).resolve().parent.parent
    FILE_PATH = BASE_DIR / "data" / "record.txt"

    @classmethod
    def load_record(cls):

        cls.FILE_PATH.parent.mkdir(exist_ok=True)

        if not cls.FILE_PATH.exists():
            cls.FILE_PATH.write_text("0", encoding="utf-8")
            return 0

        try:
            return int(cls.FILE_PATH.read_text(encoding="utf-8"))
        except ValueError:
            cls.FILE_PATH.write_text("0", encoding="utf-8")
            return 0

    @classmethod
    def save_record(cls, score):

        current = cls.load_record()

        if score > current:
            cls.FILE_PATH.write_text(str(score), encoding="utf-8")
            return score

        return current