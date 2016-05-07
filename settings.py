###############################################################################################################
# This is the settings file for RDFlizing couchdb data and loading to Sesame/GraphDB
# Author: Partha
# Contact: partha.msg@gmail.com
#################################################################################################################


import couchdb
from rdflib import Graph, plugin, BNode, URIRef, Namespace

def init():
	#import scan and clinic location data from couchdb. Enter the name of your Sesame/CouchDB repository on line 9
	global couch
	couch = couchdb.Server('http://localhost:5984/')
	global graphdb_url
	graphdb_url = 'http://127.0.0.1:7200/repositories/repository/statements'
	global dbScans
	dbScans = couch ['database_name']
	global docRefinedList
	docRefinedList = []
	global sortedDocRefinedList
	sortedDocRefinedList = []
	global sortedDocRefinedSubList
	sortedDocRefinedSubList = []
	global doc_id_list
	doc_id_list = []
	global docScans_list
	docScans_list = []
	global countExcludedRecordsList
	countExcludedRecordsList = []
	global docRefined1
	docRefined1 = {}
	global varVoic
	varVoic = 'https://w3id.org/voic#'
	global graph1
	graph1 = Graph()
	global graph2
	graph2 = Graph()
	global varList1
	varList1 = []
	global varList2
	varList2 = []
	global notAdminVacList
	notAdminVacList = []
	global values
	values = []
	global sortedDocRefinedSplitList
	sortedDocRefinedSplitList = []
	global adminVacList
	adminVacList = []