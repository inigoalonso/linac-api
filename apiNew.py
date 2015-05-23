from flask import Flask, request, render_template, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource

from urllib2 import urlopen

import csv
import json
import xmltodict

##
## Setup the flask api app
##

app = Flask(__name__, static_folder="static")

apiObject = Api(app)

##
## Some converters and parsers
##

def convertCsv2Json(csvFile, fieldNames):
    csv_reader = csv.DictReader(csvFile,fieldNames)
    # Skip the first two rows of the file
    next(csv_reader, None)
    next(csv_reader, None)
    jsonData = json.dumps([row for row in csv_reader])
    return eval(jsonData)

def convert(csvFile, csvFileName, fieldNames):
    csv_reader = csv.DictReader(csvFile,fieldNames)
    json_filename = "static/json/"+csvFileName.split(".")[0]+".json"
    print "Saving JSON to file: ",json_filename
    jsonf = open(json_filename,'w') 
    # Skip the first two rows of the file
    next(csv_reader, None)
    next(csv_reader, None)
    data = json.dumps([r for r in csv_reader])
    jsonf.write(data) 
    jsonf.close()


##
## Global variables
##

# List of API versions
api_versions = ['v1']

linacLegoXmlUrlBase = 'https://f6dea02762c7d72c87ecd77e9ac9c92f0cd2fa43.googledrive.com/host/0B_mauLIA30CDVzY4NWdXODBNU3c/LinacLego/master/xml/'


##
## Retrieve and parse lattice data
##

## From the linaclego output reports
linacLegoOutputUrlBase = linacLegoXmlUrlBase + 'linacLegoOutput/'

linacLegoSectionDataFileName = 'linacLegoSectionData.csv'
linacLegoCellDataFileName = 'linacLegoCellData.csv'
linacLegoCellPartsFileName = 'linacLegoCellParts.csv'
linacLegoSlotDataFileName = 'linacLegoSlotData.csv'
linacLegoSlotPartsFileName = 'linacLegoSlotParts.csv'
linacLegoBleDataFileName = 'linacLegoBleData.csv'
linacLegoBlePartsFileName = 'linacLegoBleParts.csv'
linacLegoMonitorDataFileName = 'linacLegoMonitorData.csv'
linacLegoMonitorPartsFileName = 'linacLegoMonitorParts.csv'
linacLegoLegoSetFileName = 'linacLegoLegoSet.csv'
linacLegoInfoLinksFileName = 'linacLegoInfoLinks.csv'

linacLegoSectionDataFile = urlopen(linacLegoOutputUrlBase + linacLegoSectionDataFileName)
linacLegoCellDataFile = urlopen(linacLegoOutputUrlBase + linacLegoCellDataFileName)
linacLegoCellPartsFile = urlopen(linacLegoOutputUrlBase + linacLegoCellPartsFileName)
linacLegoSlotDataFile = urlopen(linacLegoOutputUrlBase + linacLegoSlotDataFileName)
linacLegoSlotPartsFile = urlopen(linacLegoOutputUrlBase + linacLegoSlotPartsFileName)
linacLegoBleDataFile = urlopen(linacLegoOutputUrlBase + linacLegoBleDataFileName)
linacLegoBlePartsFile = urlopen(linacLegoOutputUrlBase + linacLegoBlePartsFileName)
linacLegoMonitorDataFile = urlopen(linacLegoOutputUrlBase + linacLegoMonitorDataFileName)
linacLegoMonitorPartsFile = urlopen(linacLegoOutputUrlBase + linacLegoMonitorPartsFileName)
linacLegoLegoSetFile = urlopen(linacLegoOutputUrlBase + linacLegoLegoSetFileName)
linacLegoInfoLinksFile = urlopen(linacLegoOutputUrlBase + linacLegoInfoLinksFileName)

sectionsFieldNames=["Section", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur"]
cellsFieldNames=["Section", "Cell", "Model", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur"]
slotsFieldNames=["Section", "Cell", "Slot", "Model", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur"]
blesFieldNames=["Section", "Cell", "Slot", "BLE", "Type", "Model", "Disc", "Name", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur", "VT", "PhiS", "G", "Theta"]
monitorsFieldNames=["Section", "Cell", "Slot", "BLE", "MON", "Type", "Model", "Disc", "Name", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur"]

def convertData():
    """Loads the data from the source"""

    global sectionDataJson
    global cellDataJson
    global slotDataJson
    global bleDataJson
    global monitorDataJson
    sectionDataJson = convertCsv2Json(linacLegoSectionDataFile, sectionsFieldNames)
    cellDataJson = convertCsv2Json(linacLegoCellDataFile, cellsFieldNames)
    slotDataJson = convertCsv2Json(linacLegoSlotDataFile, slotsFieldNames)
    bleDataJson = convertCsv2Json(linacLegoBleDataFile, blesFieldNames)
    monitorDataJson = convertCsv2Json(linacLegoMonitorDataFile, monitorsFieldNames)

    #sectionData2JsonFile = convert(linacLegoSectionDataFile, linacLegoSectionDataFileName, sectionsFieldNames)
    #cellData2JsonFile = convert(linacLegoCellDataFile, linacLegoCellDataFileName, cellsFieldNames)
    #slotData2JsonFile = convert(linacLegoSlotDataFile, linacLegoSlotDataFileName, slotsFieldNames)
    #bleData2JsonFile = convert(linacLegoBleDataFile, linacLegoBleDataFileName, blesFieldNames)
    #monitorData2JsonFile = convert(linacLegoMonitorDataFile, linacLegoMonitorDataFileName, monitorsFieldNames)

convertData()

## From a LinacLego parsed xml file

# Open the linacLego xml file
#xmlfile = open('linacLegoParsed.xml')
xmlfile = urlopen(linacLegoXmlUrlBase+'linacLegoParsed.xml')

# Convert the xml file into a dict
# More exactly, the linacLego tag
linacLego_dict = xmltodict.parse(xmlfile)['linacLego']

# Store the "header" and "linac" tags in a separate variables
header = linacLego_dict.get('header')
linac = linacLego_dict.get('linac')

# Store the "section" tags in a separate variable
sectionList = linac.get('section')
section_ids = [section['@id'] for section in sectionList]

# Store the "linacData" tag in a separate variable
linacData = linac.get('linacData')
ds = linacData.get('d')
linacData_d_ids = [d['@id'] for d in ds]

# Lists of the hierarchical ids
lattice_ids = ['latest']
#section_ids = None
cell_ids = None
slot_ids = None
ble_ids = None
monitor_ids = None

##
## Abort classes
##

def abort_if_version_doesnt_exist(api_version_id):
    """Check if the API version exists, otherwise return a 404 error."""
    if api_version_id not in api_versions:
        abort(404, message='API {} doesn\'t exist'.format(api_version_id))

def abort_if_lattice_doesnt_exist(lattice_id):
    """Check if the lattice exists, otherwise return a 404 error."""
    if lattice_id not in lattice_ids:
        abort(404, message='Lattice {} doesn\'t exist'.format(lattice_id))

def abort_if_section_doesnt_exist(lattice_id, section_id):
    """Check if the section exists, otherwise return a 404 error."""
    abort_if_lattice_doesnt_exist(lattice_id)
    if section_id not in section_ids:
        abort(404, message='Section {} doesn\'t exist'.format(section_id))

def abort_if_cell_doesnt_exist(lattice_id, section_id, cell_id):
    """Check if the cell exists, otherwise return a 404 error."""
    abort_if_section_doesnt_exist(lattice_id, section_id)
    cells_ids = []
    for section in sectionList:
        if section['@id'] == section_id:
            cells = section.get('cell')
            if len(cells) > 2:
                cell_ids = [cell['@id'] for cell in cells]
            else:
                cells_ids = cells['@id']
    if cell_id not in cell_ids:
        abort(404, message='Cell {} doesn\'t exist in this section'.format(cell_id))

def abort_if_slot_doesnt_exist(lattice_id, section_id, cell_id, slot_id):
    abort_if_cell_doesnt_exist(lattice_id, section_id, cell_id)
    """Check if the section exists, otherwise return a 404 error."""
    if slot_id not in slot_ids:
        abort(404, message='Slot {} doesn\'t exist'.format(slot_id))

def abort_if_ble_doesnt_exist(lattice_id, section_id, cell_id, slot_id, ble_id):
    """Check if the ble exists, otherwise return a 404 error."""
    abort_if_slot_doesnt_exist(lattice_id, section_id, cell_id, slot_id)
    if ble_id not in ble_ids:
        abort(404, message='BLE {} doesn\'t exist'.format(ble_id))

def abort_if_monitor_doesnt_exist(lattice_id, section_id, cell_id, slot_id, ble_id, monitor_id):
    """Check if the monitor exists, otherwise return a 404 error."""
    abort_if_ble_doesnt_exist(lattice_id, section_id, cell_id, slot_id, ble_id)
    if monitor_id not in monitor_ids:
        abort(404, message='Monitor {} doesn\'t exist'.format(monitor_id))

##
## API classes
##

# api
#   shows the API versions and documentation (TODO)
class api(Resource):
    def get(self):
        versions = ''
        for version_id in api_versions:
            versions = versions+' '+version_id
        return 'Currently available API versions:'+versions

# v1
#   shows API version 1
class version(Resource):
    def get(self, api_version_id):
        abort_if_version_doesnt_exist(api_version_id)
        return 'Welcome to the linacLego API version ' + api_version_id

##
## List classes
##

# lattices
#   show a list of lattices
class lattices(Resource):
    def get(self):
        latticeList = [{'this is a':'list of lattices'}]
        return latticeList

# sections
#   show a list of sections
class sections(Resource):
    def get(self, lattice_id='latest'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return sectionDataJson

# cells
#   show a list of cells
class cells(Resource):
    def get(self, lattice_id='latest', section_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        return cellDataJson

# slots
#   show a list of slots
class slots(Resource):
    def get(self, lattice_id='latest', section_id=None, cell_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        return slotDataJson

# bles
#   show a list of bles
class bles(Resource):
    def get(self, lattice_id='latest', section_id=None, cell_id=None, slot_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        return bleDataJson

# monitors
#   show a list of monitors
class monitors(Resource):
    def get(self, lattice_id='latest', section_id=None, cell_id=None, slot_id=None, ble_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        return monitorDataJson

##
## Instance classes
##

# lattice
#   show a single lattice
class lattice(Resource):
    def get(self, lattice_id):
        abort_if_lattice_doesnt_exist(lattice_id)
        lattice = {'name':lattice_id,'version':'version','description':'This is the description of the lattice.'}
        return lattice

# section
#   show a single section
class section(Resource):
    def get(self, lattice_id, section_id):
        abort_if_section_doesnt_exist(lattice_id, section_id)
        for section in sectionList:
            if section['@id'] == section_id:
                return section

# cell
#   show a single cell
class cell(Resource):
    def get(self, lattice_id, section_id, cell_id):
        abort_if_cell_doesnt_exist(lattice_id, section_id, cell_id)
        for section in sectionList:
            if section['@id'] == section_id:
                cells = section.get('cell')
                cell_ids = [cell['@id'] for cell in cells]
        for cell in cells:
            if cell['@id'] == cell_id:
                return cell

# slot
#   show a single slot
class slot(Resource):
    def get(self, lattice_id, section_id, cell_id, slot_id):
        abort_if_slot_doesnt_exist(lattice_id, section_id, cell_id, slot_id)
        slot = 'Looking for the ' + slot_id + ' slot?'
        return slot

# ble
#   show a single ble (Beam Line Element)
class ble(Resource):
    def get(self, lattice_id, section_id, cell_id, slot_id, ble_id):
        abort_if_ble_doesnt_exist(lattice_id, section_id, cell_id, slot_id, ble_id)
        ble = 'Looking for the ' + ble_id + ' Beam Line Element in the ' + slot_id + ' slot?'
        return ble

# monitor
#   show a single monitor
class monitor(Resource):
    def get(self, lattice_id, section_id, cell_id, slot_id, ble_id, monitor_id):
        abort_if_monitor_doesnt_exist(lattice_id, section_id, cell_id, slot_id, ble_id, monitor_id)
        monitor = {}
        return monitor


##
## Actually setup the Api resource routing here
##

apiObject.add_resource(api, 
    '/api')
apiObject.add_resource(version, 
    '/api/<api_version_id>')
    
# List resources
    
apiObject.add_resource(lattices, 
    '/api/v1/lattices')
apiObject.add_resource(sections, 
    '/api/v1/lattices/<lattice_id>/sections')
apiObject.add_resource(cells, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells',
    '/api/v1/lattices/<lattice_id>/cells')
apiObject.add_resource(slots, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots',
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>/slots',
    '/api/v1/lattices/<lattice_id>/slots')
apiObject.add_resource(bles, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/bles', 
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>/slots/<slot_id>/bles', 
    '/api/v1/lattices/<lattice_id>/slots/<slot_id>/bles', 
    '/api/v1/lattices/<lattice_id>/bles')
apiObject.add_resource(monitors, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/slots/<slot_id>/bles/<ble_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/bles/<ble_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/monitors')
    
# Instance resources
    
apiObject.add_resource(lattice, 
    '/api/v1/lattices/<lattice_id>')
apiObject.add_resource(section, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>')
apiObject.add_resource(cell, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>',
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>')
apiObject.add_resource(slot, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>',
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>/slots/<slot_id>',
    '/api/v1/lattices/<lattice_id>/slots/<slot_id>')
apiObject.add_resource(ble, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>', 
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>', 
    '/api/v1/lattices/<lattice_id>/slots/<slot_id>/bles/<ble_id>', 
    '/api/v1/lattices/<lattice_id>/bles/<ble_id>')
apiObject.add_resource(monitor, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>/monitors/<monitor_id>', 
    '/api/v1/lattices/<lattice_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>/monitors/<monitor_id>', 
    '/api/v1/lattices/<lattice_id>/slots/<slot_id>/bles/<ble_id>/monitors/<monitor_id>', 
    '/api/v1/lattices/<lattice_id>/bles/<ble_id>/monitors/<monitor_id>', 
    '/api/v1/lattices/<lattice_id>/monitors/<monitor_id>')

##
## The web pages
##

# The root page
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)