import logging

from scrivplot.src.scrivener import Scrivener
from scrivplot.src.plottr import Plottr
from scrivplot.src.mappings import Mappings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# How do I handle if the files don't exist?
# Will be a box that lets you pick a .scrivx file
scrivener_file = r"C:\Users\criss\writing\new_auto.scriv\new_auto.scrivx"

# How do I handle if the files don't exist?
# Will be a box that lets you pick a .pltr file
plottr_file = r"C:\Users\criss\writing\new_auto.pltr"

# Path to the mappings config file (to be used for saving and loading mappings)
mappings_file = 'config/mappings_config.json'

# Initialize the Mappings class
mappings = Mappings()

# Load existing mappings or create new ones if the file doesn't exist
loaded_mappings = mappings.load(mappings_file)

# Buttons and options (These will be part of the GUI later)
to_plottr = True
to_scrivener = False
load_mappings = True


# Run if "Convert to Plottr" button is pushed
if to_plottr:
    logging.info('Converting Scrivener to Plottr')
    scrivener = Scrivener()
    scrivener.load(scrivener_file)

# Run if "Convert to Scrivener" button is pushed
if to_scrivener:
    logging.info('Converting Plottr to Scrivener')
    plottr = Plottr()
    plottr.load(plottr_file)



