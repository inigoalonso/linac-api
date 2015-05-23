linac REST API documentation
============================
This document describes the REST API and resources provided by linac. The REST APIs are for developers who want to integrate linac into their application and for administrators who want to script interactions with the linac server.

linac's REST APIs provide access to resources (data entities) via URI paths. To use a REST API, your application will make an HTTP request and parse the response. The response format is JSON. Your methods will be the standard HTTP methods like GET, PUT, POST and DELETE.

Because the REST API is based on open standards, you can use any web development language to access the API.

Structure of the REST URIs
--------------------------
URIs for the linac API resource have the following structure:

http://example.com:5000/linac/section/cell/slot/ble

Index
-----
This documents the current REST API provided by linac.

* Resources
    * `/linac`
    * `/linac/linacData`
    * `/linac/linacData/<d_id>`
    * `/linac/linacData/<d_id>/value`
    * `/linac/linacData/<d_id>/<attrib_id>`
    * `/linac/<section_id>`
    * `/linac/<section_id>/<cell_id>`
    * `/linac/<section_id>/<cell_id>/<slot_id>`
    * `/linac/<section_id>/<cell_id>/<slot_id>/<ble_id>`

Resources
---------
`linac`
