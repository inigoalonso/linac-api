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

def convertDataCsv2Json(csvFile, fieldNames):
    csv_reader = csv.DictReader(csvFile,fieldNames)
    # Skip the first two rows of the file
    next(csv_reader, None)
    next(csv_reader, None)
    jsonData = json.dumps([row for row in csv_reader])
    return eval(jsonData)

def convertCsv2Json(csvFile, fieldNames):
    csv_reader = csv.DictReader(csvFile,fieldNames)
    # Skip the first two rows of the file
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

def global_variables():
    global api_versions
    api_versions = ['v1']
    global linacLegoXmlUrlBase
    linacLegoXmlUrlBase = 'https://f6dea02762c7d72c87ecd77e9ac9c92f0cd2fa43.googledrive.com/host/0B_mauLIA30CDVzY4NWdXODBNU3c/LinacLego/master/xml/'

global_variables()

##
## Retrieve and parse lattice data
##

## From the linaclego output reports
linacLegoOutputUrlBase = linacLegoXmlUrlBase + 'linacLegoOutput/'

linacLegoSectionDataFileName = 'linacLegoSectionData.csv'
linacLegoCellDataFileName = 'linacLegoCellData.csv'
linacLegoSlotDataFileName = 'linacLegoSlotData.csv'
linacLegoBleDataFileName = 'linacLegoBleData.csv'
linacLegoMonitorDataFileName = 'linacLegoMonitorData.csv'

linacLegoCellPartsFileName = 'linacLegoCellParts.csv'
linacLegoSlotPartsFileName = 'linacLegoSlotParts.csv'
linacLegoBlePartsFileName = 'linacLegoBleParts.csv'
linacLegoMonitorPartsFileName = 'linacLegoMonitorParts.csv'

linacLegoLegoSetFileName = 'linacLegoLegoSet.csv'
linacLegoInfoLinksFileName = 'linacLegoInfoLinks.csv'

linacLegoSectionDataFile = urlopen(linacLegoOutputUrlBase + linacLegoSectionDataFileName)
linacLegoCellDataFile = urlopen(linacLegoOutputUrlBase + linacLegoCellDataFileName)
linacLegoSlotDataFile = urlopen(linacLegoOutputUrlBase + linacLegoSlotDataFileName)
linacLegoBleDataFile = urlopen(linacLegoOutputUrlBase + linacLegoBleDataFileName)
linacLegoMonitorDataFile = urlopen(linacLegoOutputUrlBase + linacLegoMonitorDataFileName)

linacLegoCellPartsFile = urlopen(linacLegoOutputUrlBase + linacLegoCellPartsFileName)
linacLegoSlotPartsFile = urlopen(linacLegoOutputUrlBase + linacLegoSlotPartsFileName)
linacLegoBlePartsFile = urlopen(linacLegoOutputUrlBase + linacLegoBlePartsFileName)
linacLegoMonitorPartsFile = urlopen(linacLegoOutputUrlBase + linacLegoMonitorPartsFileName)

linacLegoLegoSetFile = urlopen(linacLegoOutputUrlBase + linacLegoLegoSetFileName)
linacLegoInfoLinksFile = urlopen(linacLegoOutputUrlBase + linacLegoInfoLinksFileName)

sectionsFieldNames=["Section", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur"]
cellsFieldNames=["Section", "Cell", "Model", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur"]
slotsFieldNames=["Section", "Cell", "Slot", "Model", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur"]
blesFieldNames=["Section", "Cell", "Slot", "BLE", "Type", "Model", "Disc", "Name", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur", "Zsur", "VT", "PhiS", "G", "Theta"]
monitorsFieldNames=["Section", "Cell", "Slot", "BLE", "MON", "Type", "Model", "Disc", "Name", "eVout", "v/c", "Length", "Xend", "Yend", "Zend", "Xsur", "Ysur"]

cellPartsFieldNames = ["type", "model", "FE", "MEBT", "DTL", "SPK", "MBL", "HBL", "HEBT", "A2T", "Total"]
slotPartsFieldNames = ["type", "model", "FE", "MEBT", "DTL", "SPK", "MBL", "HBL", "HEBT", "A2T", "Total"]
blePartsFieldNames = ["type", "model", "FE", "MEBT", "DTL", "SPK", "MBL", "HBL", "HEBT", "A2T", "Total", "minValue", "avgValue", "maxValue", "Unit"]
monitorPartsFieldNames = ["type", "model", "FE", "MEBT", "DTL", "SPK", "MBL", "HBL", "HEBT", "A2T", "Total"]

infoLinksFieldNames = ["Type", "Id", "Link"]
legoSetFieldNames = ["BLE devName", "BLE data", "BLE value", "BLE unit", "LinacSet devName", "LinacSet Value", "LinacSet Unit", "TF 0", "TF 1", "TF 2", "TF 3", "TF 4"]

def convertData():
    """Loads the data from the source"""

    global sectionDataJson
    global cellDataJson
    global slotDataJson
    global bleDataJson
    global monitorDataJson
    sectionDataJson = convertDataCsv2Json(linacLegoSectionDataFile, sectionsFieldNames)
    cellDataJson = convertDataCsv2Json(linacLegoCellDataFile, cellsFieldNames)
    slotDataJson = convertDataCsv2Json(linacLegoSlotDataFile, slotsFieldNames)
    bleDataJson = convertDataCsv2Json(linacLegoBleDataFile, blesFieldNames)
    monitorDataJson = convertDataCsv2Json(linacLegoMonitorDataFile, monitorsFieldNames)
    
    global cellPartsJson
    global slotPartsJson
    global blePartsJson
    global monitorPartsJson
    cellPartsJson = convertCsv2Json(linacLegoCellPartsFile, cellPartsFieldNames)
    slotPartsJson = convertCsv2Json(linacLegoSlotPartsFile, slotPartsFieldNames)
    blePartsJson = convertCsv2Json(linacLegoBlePartsFile, blePartsFieldNames)
    monitorPartsJson = convertCsv2Json(linacLegoMonitorPartsFile, monitorPartsFieldNames)
    
    global infoLinksDataJson
    global legoSetsDataJson
    infoLinksDataJson = convertCsv2Json(linacLegoInfoLinksFile, infoLinksFieldNames)
    legoSetsDataJson = convertCsv2Json(linacLegoLegoSetFile, legoSetFieldNames)
    
    global emittancesDataJson
    with open("emittances.csv") as emittancesFile:
        emittancesFieldNames = ["Entrance of", "Energy min (MeV)", "Energy nom (MeV)", "Energy max (MeV)", "Current (mA)", "RMS emittance horizontal (mm mrad)", "Twiss alpha horizontal", "Twiss beta horizontal (m)", "RMS emittance vertical (mm mrad)", "Twiss alpha vertical", "Twiss beta vertical", "RMS emittance longitudinal (mm MeV)", "Twiss alpha longitudinal", "Twiss beta longitudinal", "Location (m)"]
        emittancesDataJson = convertCsv2Json(emittancesFile, emittancesFieldNames)

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
lattice_ids = ['master', 'development']
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
## Data selection
##

def cellsBySection(section_id):
    """Returns a list of the cells in the section"""
    cells = [item for item in cellDataJson 
        if item["Section"] == section_id]
    return cells

def slotsBySection(section_id):
    """Returns a list of the slots in the section"""
    slots = [item for item in slotDataJson 
        if item["Section"] == section_id]
    return slots

def blesBySection(section_id):
    """Returns a list of the slots in the section"""
    bles = [item for item in bleDataJson 
        if item["Section"] == section_id]
    return bles

def monitorsBySection(section_id):
    """Returns a list of the slots in the section"""
    monitors = [item for item in monitorDataJson 
        if item["Section"] == section_id]
    return monitors


def slotsByCell(section_id, cell_id):
    """Returns a list of the slots in the cell"""
    slots = [item for item in slotDataJson 
        if item["Section"] == section_id and item["Cell"] == cell_id]
    return slots

def blesByCell(section_id, cell_id):
    """Returns a list of the slots in the cell"""
    bles = [item for item in bleDataJson 
        if item["Section"] == section_id and item["Cell"] == cell_id]
    return bles

def monitorsByCell(section_id, cell_id):
    """Returns a list of the slots in the cell"""
    monitors = [item for item in monitorDataJson 
        if item["Section"] == section_id and item["Cell"] == cell_id]
    return monitors

def blesBySlot(section_id, cell_id, slot_id):
    """Returns a list of the bles in the slot"""
    bles = [item for item in bleDataJson 
        if item["Section"] == section_id and item["Cell"] == cell_id and item["Slot"] == slot_id]
    return bles

def monitorsBySlot(section_id, cell_id, slot_id):
    """Returns a list of the monitors in the slot"""
    monitors = [item for item in monitorDataJson 
        if item["Section"] == section_id and item["Cell"] == cell_id and item["Slot"] == slot_id]
    return monitors

def monitorsByBle(section_id, cell_id, slot_id, ble_id):
    """Returns a list of the monitors in the ble"""
    monitors = [item for item in monitorDataJson 
        if item["Section"] == section_id and item["Cell"] == cell_id and item["Slot"] == slot_id and item["BLE"] == ble_id]
    return monitors

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
        latticeList = []
        for lattice in lattice_ids:
            latticeList.append({'name':lattice})
        return latticeList

# sections
#   show a list of sections
class sections(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return sectionDataJson

# cells
#   show a list of cells
class cells(Resource):
    def get(self, lattice_id='master', section_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        if section_id == None:
            return cellDataJson
        else:
            abort_if_section_doesnt_exist(lattice_id, section_id)
            return cellsBySection(section_id)

# slots
#   show a list of slots
class slots(Resource):
    def get(self, lattice_id='master', section_id=None, cell_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        if section_id == None:
            return slotDataJson
        elif cell_id == None:
            abort_if_section_doesnt_exist(lattice_id, section_id)
            return slotsBySection(section_id)
        else:
            abort_if_cell_doesnt_exist(lattice_id, section_id, cell_id)
            return slotsByCell(section_id, cell_id)

# bles
#   show a list of bles
class bles(Resource):
    def get(self, lattice_id='master', section_id=None, cell_id=None, slot_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        if section_id == None:
            return bleDataJson
        elif cell_id == None:
            abort_if_section_doesnt_exist(lattice_id, section_id)
            return blesBySection(section_id)
        elif slot_id == None:
            abort_if_cell_doesnt_exist(lattice_id, section_id, cell_id)
            return blesByCell(section_id, cell_id)
        else:
            abort_if_slot_doesnt_exist(lattice_id, section_id, cell_id, slot_id)
            return blesBySlot(section_id, cell_id, slot_id)

# monitors
#   show a list of monitors
class monitors(Resource):
    def get(self, lattice_id='master', section_id=None, cell_id=None, slot_id=None, ble_id=None):
        abort_if_lattice_doesnt_exist(lattice_id)
        if section_id == None:
            return monitorDataJson
        elif cell_id == None:
            abort_if_section_doesnt_exist(lattice_id, section_id)
            return monitorsBySection(section_id)
        elif slot_id == None:
            abort_if_cell_doesnt_exist(lattice_id, section_id, cell_id)
            return monitorsByCell(section_id, cell_id)
        elif ble_id == None:
            abort_if_slot_doesnt_exist(lattice_id, section_id, cell_id, slot_id)
            return monitorsBySlot(section_id, cell_id, slot_id)
        else:
            abort_if_ble_doesnt_exist(lattice_id, section_id, cell_id, slot_id, ble_id)
            return monitorsByBle(section_id, cell_id, slot_id, ble_id)

# infoLinks
#   show a list of infoLinks
class infoLinks(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return infoLinksDataJson

# legoSet
#   show a list of lego sets
class legoSets(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return legoSetsDataJson

# emittances
#   show the emittances_table.ods data
class emittances(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return emittancesDataJson
        
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
## Parts
##

# cellParts
class cellParts(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return cellPartsJson

# slotParts
class slotParts(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return slotPartsJson

# bleParts
class bleParts(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return blePartsJson

# monitorParts
class monitorParts(Resource):
    def get(self, lattice_id='master'):
        abort_if_lattice_doesnt_exist(lattice_id)
        return monitorPartsJson


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
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/slots',
    '/api/v1/lattices/<lattice_id>/slots')
apiObject.add_resource(bles, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/bles', 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/bles', 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/bles', 
    '/api/v1/lattices/<lattice_id>/bles')
apiObject.add_resource(monitors, 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/bles/<ble_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/slots/<slot_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/cells/<cell_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/sections/<section_id>/monitors', 
    '/api/v1/lattices/<lattice_id>/monitors')
apiObject.add_resource(infoLinks, 
    '/api/v1/lattices/<lattice_id>/infoLinks')
apiObject.add_resource(legoSets, 
    '/api/v1/lattices/<lattice_id>/legoSets')
apiObject.add_resource(emittances, 
    '/api/v1/lattices/<lattice_id>/emittances')
apiObject.add_resource(cellParts, 
    '/api/v1/lattices/<lattice_id>/cellParts')
apiObject.add_resource(slotParts, 
    '/api/v1/lattices/<lattice_id>/slotParts')
apiObject.add_resource(bleParts, 
    '/api/v1/lattices/<lattice_id>/bleParts')
apiObject.add_resource(monitorParts, 
    '/api/v1/lattices/<lattice_id>/monitorParts')
    
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
    lattice = request.args.get('lattice')
    if lattice == None:
        lattice = "master"
    return render_template('template.html', lattice=lattice, links=infoLinksDataJson)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')