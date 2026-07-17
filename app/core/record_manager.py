"""
Record Manager Module

This module handles the persistent storage and retrieval of the player's
highest score (record) in the Space Shooter game.

The record is stored in a text file (record.txt) in the data directory.
"""

from pathlib import Path


class RecordManager:
    """
    Manager for handling high score persistence.
    
    Provides methods to load and save the player's highest score to a file.
    Automatically creates the data directory and record file if they don't exist.
    Handles file I/O errors by resetting to 0 if the file is corrupted.
    """
    # Base directory where this module is located (app/ folder)
    BASE_DIR = Path(__file__).resolve().parent.parent
    # Path to the record file containing the high score
    FILE_PATH = BASE_DIR / "data" / "record.txt"

    @classmethod
    def load_record(cls):
        """
        Load the current high score from the record file.
        Returns:
            int: The current high score, or 0 if the file doesn't exist or is corrupted.
        """
        # Ensure the data directory exists
        cls.FILE_PATH.parent.mkdir(exist_ok=True)

        # Initialize with 0 if file doesn't exist
        if not cls.FILE_PATH.exists():
            cls.FILE_PATH.write_text("0", encoding="utf-8")
            return 0

        try:
            # Read and parse the score from file
            return int(cls.FILE_PATH.read_text(encoding="utf-8"))
        except ValueError:
            # File contains invalid data, reset to 0
            cls.FILE_PATH.write_text("0", encoding="utf-8")
            return 0

    @classmethod
    def save_record(cls, score):
        """
        Save a score if it's higher than the current record.
        
        Only updates the record file if the provided score is greater than
        the current record. Returns the highest score between the provided
        score and the existing record.
        Args:
            score (int): The score to potentially save as the new record.
        Returns:
            int: The highest score between the provided score and the existing record.
        """
        # Get the current record
        current = cls.load_record()

        # Only save if the new score is better
        if score > current:
            cls.FILE_PATH.write_text(str(score), encoding="utf-8")
            return score

        return current