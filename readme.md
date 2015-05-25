linac REST API documentation
============================
This document describes the REST API and resources provided by linac. The REST APIs are for developers who want to integrate linac lattice data into their application and for administrators who want to script interactions with the linac server.

linac's REST APIs provide access to resources (data entities) via URI paths. To use a REST API, your application will make an HTTP request and parse the response. The response format is JSON. Your methods will be the standard HTTP methods like GET, PUT, POST and DELETE (for now only GET :D ).

Because the REST API is based on open standards, you can use any web development language to access the API.

Structure of the REST URIs
--------------------------
URIs for the linac API resources have the following structure:

http://example.com:5000/api/v1/lattices/latest/sections/<sectionId>/cells/<cellId>/slots/<slotId>/bles/<bleId>/monitors/<monitorId>

Resources
---------
TODO swagger file

Packages
--------

* flask
* flask-restful
* xmltodict
