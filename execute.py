#################################################################################################
# This is the file for RDFlizing couchdb data and loading to Sesame/GraphDB
# Author: Partha
# Contact: partha.msg@gmail.com
####################################################################################################

import rdflib
import couchdb
# from pyld import jsonld
from rdflib import Graph, plugin, BNode, URIRef, Namespace
from SPARQLWrapper import SPARQLWrapper
import json, rdflib_jsonld
import pprint
from rdflib.plugin import register, Serializer
from rdflib_sparql.processor import processUpdate
import gc
from couchToGraphDB_wip9 import rdfLizer, graphAdder, notAdminFinder, queryRunner, graphDBInserter, graphCleaner
import settings
import itertools

settings.init()
# print ('Number of unique records: ', len(set(settings.dbScans)))
register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')

def usefulDataExtracter():
	for doc_id in settings.dbScans:
		settings.docScans = settings.dbScans.get(doc_id)
		settings.docScans_list.append(settings.docScans)
		doc_id = settings.docScans['_id']
		settings.doc_id_list.append(doc_id)
		#Extracting the fields of interest from original data
		settings.docScans = settings.dbScans.get(doc_id)
		settings.docScansProps = settings.docScans['properties']

		if (settings.docScansProps['clinic_id'] not in settings.testClinic_ID and settings.docScansProps['series']!='None' and settings.docScansProps['patient_id']!='NA' and settings.docScansProps['vaccine_name']!='VitaminA'):
			settings.docRefined1 = {
			'VaccineRecipient':str(settings.docScansProps['patient_id']),
			'VaccineByAntigen':str(settings.docScansProps['vaccine_name']),
			'Dose':'dose' + str(int(settings.docScansProps['series'])+1)} #Adding the series value by 1 for consistency with ontology
			settings.docRefinedList.append(settings.docRefined1)
			# print ('Included: '+str(len(settings.docRefinedList)) +'-'+ settings.docScansProps['clinic_id'])
		else:
			settings.countExcludedRecordsList.append(settings.docScansProps['clinic_id'])
			# print ('Excluded: '+str(len(settings.countExcludedRecordsList)) +'-'+ settings.docScansProps['clinic_id'])
	recordSorter()

def recordSorter():
	# print ('docRefinedList: ', settings.docRefinedList)
	settings.sortedDocRefinedList = sorted(settings.docRefinedList, key=lambda k: k['VaccineRecipient'])
	# print ('sortedRefinedList: ',settings.sortedDocRefinedList)
	for k,v in itertools.groupby(settings.sortedDocRefinedList, key=lambda x:x['VaccineRecipient']):
		settings.sortedDocRefinedSplitList.append(list(v))
	counter = 0
	for item in settings.sortedDocRefinedSplitList:
		rdfLizer(item)
		graphAdder(settings.graph1)
		queryRunner(item)
		notAdminFinder()
		graphDBInserter()
		graphCleaner()
		counter = counter+1
		print counter
		
usefulDataExtracter()



