from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

#import numpy as np
#from lxml import etree
from urllib2 import urlopen

import json
import xmltodict

app = Flask(__name__,
            static_folder="../pydynac/static",
            static_url_path="/static")

apiObject = Api(app)

apiVersions = ['v1']

# Open the linacLego xml file
xmlfile = open('linacLegoParsed.xml')
#xmlfile2 = open('hebtLego.xml')

#parser = etree.XMLParser(remove_comments=True)
#tree = etree.parse(xmlfile, parser=parser)
#header = tree.getroot()[0]
#linac = tree.getroot()[1]
#linacData = linac[0]
#section = linac[1]

# Convert the xml file into a dict
# More exactly, the linacLego tag
linacLego_dict = xmltodict.parse(xmlfile)['linacLego']

# Store the "header" tag in a separate variable
header = linacLego_dict.get('header')
#for slotModel in header['slotModels']:
#    print slotModel['@id']
#for cellModel in header['cellModels']:
#    print cellModel['@id']
#for legoSet in header['legoSets']:
#    print legoSet['@id']
#for legoMonitor in header['legoMonitors']:
#    print legoMonitor['@id']

# Store the "linac" tag in a separate variable
linac = linacLego_dict.get('linac')

# Store the "section" tags in a separate variable
sections = linac.get('section')
#for section in sections:
#    print section['@id']
section_ids = [section['@id'] for section in sections]

# Store the "linacData" tag in a separate variable
linacData = linac.get('linacData')
ds = linacData.get('d')
#for data in ds:
#    print data['@id']
linacData_d_ids = [d['@id'] for d in ds]

#for i in range(0,7):
#    print len(sections[i]['cell'])

def abort_if_version_doesnt_exist(version):
    """Check if the API version exists, otherwise return a 404 error."""
    if version not in apiVersions:
        abort(404)

def abort_if_cell_doesnt_exist(section_id, cell_id):
    """Check if the cell exists in the section, otherwise return a 404 error."""
    abort_if_section_doesnt_exist(section_id)
    cells_ids = []
    for section in sections:
        if section['@id'] == section_id:
            cells = section.get('cell')
            if len(cells) > 2:
                cell_ids = [cell['@id'] for cell in cells]
            else:
                cells_ids = cells['@id']
    if cell_id not in cell_ids:
        abort(404, message='Cell {} doesn\'t exist in this section'.format(cell_id))

def abort_if_section_doesnt_exist(section_id):
    """Check if the section exists in the linac, otherwise return a 404 error."""
    if section_id not in section_ids:
        abort(404, message='Section {} doesn\'t exist'.format(section_id))


def abort_if_linacData_d_attrib_doesnt_exist(d_id, attrib_id):
    """Check if the data attribute exists in the linacData, otherwise return a 404 error."""
    abort_if_linacData_d_doesnt_exist(d_id)
    for d in ds:
        if d['@id'] == d_id:
            attrib_ids = d.keys()
    if '@' +attrib_id not in attrib_ids:
        abort(404, message='Attribute {} doesn\'t exist in this parameter'.format(attrib_id))


def abort_if_linacData_d_doesnt_exist(d_id):
    """Check if the data exists in the linacData, otherwise return a 404 error."""
    if d_id not in linacData_d_ids:
        abort(404, message='Parameter {} doesn\'t exist'.format(d_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# root
#   shows all linac data and sections
class root(Resource):
    def get(self):
        return 'Currently available services: api'

# api
#   shows the API versions and documentation
class api(Resource):
    def get(self):
        versions = ''
        for version in apiVersions:
            versions = versions+' '+version
        return 'Currently available API versions:'+versions

# v1
#   shows API verison 1
class version(Resource):
    def get(self, version):
        abort_if_version_doesnt_exist(version)
        return 'Welcome to the linacLego API version ' + version

# linac
#   shows all linac data and sections
class linac(Resource):
    def get(self):
        return linacLego_dict.get('linac')


# linacData
#   shows a list of all the linac parameters
class linacData(Resource):
    def get(self):
        return ds


# linacData d value
#   shows a linac parameter value
class linacData_d_value(Resource):
    def get(self, d_id):
        abort_if_linacData_d_doesnt_exist(d_id)
        for d in ds:
            if d['@id'] == d_id:
                return d['#text']

# linacData d attrib
#   shows a linac parameter attribute
class linacData_d_attrib(Resource):
    def get(self, d_id, attrib_id):
        abort_if_linacData_d_attrib_doesnt_exist(d_id, attrib_id)
        for d in ds:
            if d['@id'] == d_id:
                return d['@' +attrib_id]

# linacData d
#   shows a linac parameter
class linacData_d(Resource):
    def get(self, d_id):
        abort_if_linacData_d_doesnt_exist(d_id)
        for d in ds:
            if d['@id'] == d_id:
                return d

# section
#   show a single section
class section(Resource):
    def get(self, section_id):
        abort_if_section_doesnt_exist(section_id)
        for section in sections:
            if section['@id'] == section_id:
                return section

# cell
#   show a single cell
class cell(Resource):
    def get(self, section_id, cell_id):
        abort_if_cell_doesnt_exist(section_id, cell_id)
        for section in sections:
            if section['@id'] == section_id:
                cells = section.get('cell')
                cell_ids = [cell['@id'] for cell in cells]
        for cell in cells:
            if cell['@id'] == cell_id:
                return cell

# slot
#   show a single slot
class slot(Resource):
    def get(self, section_id, cell_id, slot_id):
        abort_if_section_doesnt_exist(section_id)
        abort_if_cell_doesnt_exist(section_id, cell_id)
        #abort_if_slot_doesnt_exist(section_id, cell_id)
        slot = 'Looking for the ' + slot_id + ' slot?'
        return slot

# ble
#   show a single ble (Beam Line Element)
class ble(Resource):
    def get(self, section_id, cell_id, slot_id, ble_id):
        abort_if_section_doesnt_exist(section_id)
        abort_if_cell_doesnt_exist(section_id, cell_id)
        #abort_if_slot_doesnt_exist(section_id, cell_id)
        #abort_if_ble_doesnt_exist(section_id, cell_id)
        ble = 'Looking for the ' + ble_id + ' Beam Line Element in the ' + slot_id + ' slot?'
        return ble


# getSections
#   Returns a list of the available Sections in the linac.
class getSections(Resource):
    def get(self):
        listSections = []
        for section in sections:
            listSections.append(section['@id'])
        dictSections = {"Sections":listSections}
        return dictSections

# getCells
#   Returns a list of the available Cells in the section.
class getCells(Resource):
    def get(self, section_id):
        abort_if_section_doesnt_exist(section_id)
        for section in sections:
            if section['@id'] == section_id:
                cells = section.get('cell')
        #cell_ids = [cell['@id'] for cell in cells]
        listCells = []
        if len(cells) == 2:
            listCells = [cells['@id']]
        else:
            for cell in cells:
                listCells.append(cell['@id'])
        dictCells = {"Cells":listCells}
        return dictCells

# getAllCells
#   Returns a list of all the Cells in the linac.
class getAllCells(Resource):
    def get(self):
        listCells = []
        for section in sections:
            cells = section.get('cell')
            if len(cells) == 2:
                listCells = [cells['@id']]
            else:
                for cell in cells:
                    listCells.append(cell['@id'])
        dictCells = {"Cells":listCells}
        return dictCells

##
## Actually setup the Api resource routing here
##
apiObject.add_resource(root, '/')
apiObject.add_resource(api, '/api')
apiObject.add_resource(version, '/api/<version>')
apiObject.add_resource(linac, '/api/v1/linac')
apiObject.add_resource(linacData, '/api/v1/linac/linacData')
apiObject.add_resource(linacData_d, '/api/v1/linac/linacData/<d_id>')
apiObject.add_resource(linacData_d_value, '/api/v1/linac/linacData/<d_id>/value')
apiObject.add_resource(linacData_d_attrib, '/api/v1/linac/linacData/<d_id>/<attrib_id>')
apiObject.add_resource(section, '/api/v1/linac/<section_id>')
apiObject.add_resource(cell, '/api/v1/linac/<section_id>/<cell_id>')
apiObject.add_resource(slot, '/api/v1/linac/<section_id>/<cell_id>/<slot_id>')
apiObject.add_resource(ble, '/api/v1/linac/<section_id>/<cell_id>/<slot_id>/<ble_id>')
apiObject.add_resource(getSections, '/api/v1/linac/getSections')
apiObject.add_resource(getCells, '/api/v1/linac/<section_id>/getCells')
apiObject.add_resource(getAllCells, '/api/v1/linac/getCells')


if __name__ == '__main__':
    app.run(debug=True)