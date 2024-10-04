import os
import json
import logging

class Mappings:
    def __init__(self):
        self.mappings = []

    def load(self, mappings_file: str) -> list:
        """
        Loads the mappings from a JSON file. If the file doesn't exist, default mappings are used
        and the file is saved with those default mappings.

        :param mappings_file: Path to the mappings config file.
        :return: The mappings as a list of dictionaries.
        """
        if not self._check_file_exists(mappings_file):
            logging.warning(f"Mappings file does not exist, using default mappings and saving new file.")
            self.mappings = self.default_mappings()
            self.save(mappings_file)  # Save default mappings to file
            return self.mappings

        try:
            with open(mappings_file, 'r') as file:
                self.mappings = json.load(file)
                logging.info(f"Loaded mappings from {mappings_file}")
                return self.mappings
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading mappings from {mappings_file}: {e}")
            logging.info("Using default mappings due to an error.")
            self.mappings = self.default_mappings()
            self.save(mappings_file)  # Save default mappings to file if there was an error
            return self.mappings

    def save(self, mappings_file: str) -> None:
        """
        Saves the current mappings to a JSON file.

        :param mappings_file: Path to the mappings config file.
        """
        try:
            with open(mappings_file, 'w') as file:
                json.dump(self.mappings, file, indent=4)
                logging.info(f"Saved mappings to {mappings_file}")
        except IOError as e:
            logging.error(f"Error saving mappings file {mappings_file}: {e}")

    def _check_file_exists(self, file_path: str) -> bool:
        """
        Checks if a given file path exists.
        Logs an error if the file doesn't exist.

        :param file_path: The path to the file to check.
        :return: True if the file exists, False otherwise.
        """
        if not os.path.exists(file_path):
            return False
        return True

    def default_mappings(self) -> list:
        """
        Returns default mappings with fields: plottr, scrivener, description, and use.

        :return: A list of default mappings as dictionaries.
        """
        return [
            {
                "plottr": "PlottrScene",
                "scrivener": "ScrivenerScene",
                "description": "Maps a Plottr scene to a Scrivener scene.",
                "use": True
            },
            {
                "plottr": "PlottrChapter",
                "scrivener": "ScrivenerChapter",
                "description": "Maps a Plottr chapter to a Scrivener chapter.",
                "use": True
            }
        ]

    def enable_mapping(self, index: int):
        """
        Enables the mapping at the given index by setting the 'use' field to True.

        :param index: The index of the mapping to enable.
        """
        if 0 <= index < len(self.mappings):
            self.mappings[index]['use'] = True
            logging.info(f"Enabled mapping at index {index}.")
        else:
            logging.warning(f"Mapping at index {index} not found.")

    def disable_mapping(self, index: int):
        """
        Disables the mapping at the given index by setting the 'use' field to False.

        :param index: The index of the mapping to disable.
        """
        if 0 <= index < len(self.mappings):
            self.mappings[index]['use'] = False
            logging.info(f"Disabled mapping at index {index}.")
        else:
            logging.warning(f"Mapping at index {index} not found.")

    def update_description(self, index: int, description: str):
        """
        Updates the description of a mapping at the given index.

        :param index: The index of the mapping to update.
        :param description: The new description to set.
        """
        if 0 <= index < len(self.mappings):
            self.mappings[index]['description'] = description
            logging.info(f"Updated description for mapping at index {index}.")
        else:
            logging.warning(f"Mapping at index {index} not found.")
