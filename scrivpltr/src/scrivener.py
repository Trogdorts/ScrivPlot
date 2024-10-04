import logging
import os
import xml.etree.ElementTree as ET
from scrivplot.src.exceptions import ScrivenerError, FileNotFoundError, InvalidFileTypeError, InvalidScrivenerVersionError, \
    NotAFileError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Scrivener:
    def __init__(self):
        self._scrivener_file = ''
        self._scrivener_folder = ''
        self.scrivener_xml = ''

    def load(self, scrivener_file):
        # Step 1: Validate the scrivener file
        self._scrivener_file = self._validate_scrivener_file(scrivener_file)

        # Step 2: Get and validate the scrivener folder
        self._scrivener_folder = self._validate_scrivener_folder(scrivener_file)

        self.scrivener_xml = self.load_xml(self._scrivener_file, self._scrivener_folder)

        self._validate_xml_version(self.scrivener_xml)

    def load_xml(self, scrivener_file: str, scrivener_folder: str):
        """
        Loads and parses the XML from the provided Scrivener file.

        :param scrivener_file: Path to the .scrivx Scrivener file.
        :param scrivener_folder: Path to the Scrivener folder.
        :return: Parsed XML root element.
        :raises ScrivenerError: If there is any issue with loading or parsing the XML.
        """
        try:
            # Log the start of the operation
            logging.info(f"Attempting to load Scrivener XML file: {scrivener_file}")

            # Step 1: Open the file and read the contents
            with open(scrivener_file, 'r', encoding='utf-8') as file:
                scrivener_xml_string = file.read()

            # Step 2: Parse the XML string into an ElementTree element
            scrivener_xml = ET.fromstring(scrivener_xml_string)

            # Log successful parsing
            logging.info(f"Successfully parsed XML from file: {scrivener_file}")

            return scrivener_xml

        except FileNotFoundError:
            logging.error(f"File not found: {scrivener_file}")
            raise ScrivenerError(f"File not found: {scrivener_file}")

        except ET.ParseError as e:
            logging.error(f"Failed to parse XML in file {scrivener_file}: {e}")
            raise ScrivenerError(f"Failed to parse XML: {e}")

        except Exception as e:
            logging.error(f"An unexpected error occurred while loading the file {scrivener_file}: {e}")
            raise ScrivenerError(f"An unexpected error occurred: {e}")

    def _validate_scrivener_file(self, file_path: str) -> str:
        """
        Validates if the provided file is a valid .scrivx Scrivener file.

        :param file_path: Path to the Scrivener file.
        :return: The validated file path.
        :raises ScrivenerError: If the file is invalid.
        """
        # Check if the provided path exists
        if not os.path.exists(file_path):
            logging.error(f"The provided file path does not exist: {file_path}")
            raise FileNotFoundError(file_path)

        # Check if the provided path is a file and if it ends with .scrivx
        if os.path.isfile(file_path):
            if file_path.endswith('.scrivx'):
                logging.info(f"Valid Scrivener file: {file_path}")
                return file_path
            else:
                logging.error("The provided file is not a .scrivx file.")
                raise InvalidFileTypeError(file_path)
        else:
            logging.error(f"The provided path is not a valid file: {file_path}")
            raise NotAFileError(file_path)

    def _validate_xml_version(self, scrivener_xml: ET.Element) -> None:
        """
        Validates the XML version for a Scrivener file. Scrivener 3 files should have Version 2.0.

        :param scrivener_xml: Parsed XML element of the Scrivener file.
        :raises InvalidScrivenerVersionError: If the Scrivener XML version is not 2.0.
        """
        try:
            # Log the start of the validation process
            logging.info("Validating Scrivener XML version.")

            # Final sanity check: verify the Scrivener version (should be 2.0 for Scrivener 3 files)
            version = scrivener_xml.attrib.get('Version')

            if version != '2.0':
                logging.error(f"Invalid Scrivener version: {version}. Expected version 2.0.")
                raise InvalidScrivenerVersionError(version)

            # Log success if version is valid
            logging.info("Scrivener XML version is valid (2.0).")

        except KeyError:
            logging.error("Version attribute missing from Scrivener XML.")
            raise InvalidScrivenerVersionError("Version attribute missing.")

        except Exception as e:
            logging.error(f"An unexpected error occurred during version validation: {e}")
            raise e
    def _validate_scrivener_folder(self, file_path: str) -> str:
        """
        Validates and returns the folder containing the Scrivener file.

        :param file_path: Path to the Scrivener file.
        :return: The folder path containing the Scrivener project.
        """
        project_folder = os.path.dirname(file_path)
        project_file = os.path.basename(file_path)

        # Additional validation for the folder (if needed) can go here
        logging.info(f"Scrivener project folder: {project_folder}")
        logging.info(f"Scrivener project file: {project_file}")

        return project_folder
