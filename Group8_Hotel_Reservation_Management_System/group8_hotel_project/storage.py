"""JSON persistence helpers with explicit file and data error handling."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class StorageError(Exception):
    """Raised when application data cannot be read or written safely."""


class JsonStorage:
    def __init__(self, data_directory: str | Path) -> None:
        self.data_directory = Path(data_directory)
        try:
            self.data_directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise StorageError(f"Cannot create data directory: {exc}") from exc

    def path_for(self, filename: str) -> Path:
        # Keep filenames inside the configured data directory.
        if Path(filename).name != filename:
            raise StorageError("Invalid data filename.")
        return self.data_directory / filename

    def read_json(self, filename: str, default: Any) -> Any:
        path = self.path_for(filename)
        if not path.exists():
            return default
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise StorageError(f"{filename} contains invalid JSON: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"Could not read {filename}: {exc}") from exc

    def write_json(self, filename: str, data: Any) -> None:
        path = self.path_for(filename)
        temporary_path = None
        try:
            # Write to a temporary file first so a partial write does not
            # overwrite the last valid data file.
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.data_directory,
                delete=False, suffix=".tmp"
            ) as file:
                temporary_path = Path(file.name)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.write("\n")
            os.replace(temporary_path, path)
        except (OSError, TypeError, ValueError) as exc:
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    pass
            raise StorageError(f"Could not save {filename}: {exc}") from exc
