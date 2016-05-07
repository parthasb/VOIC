#################################################################################################
# This file has the necessary functions for RDFlizing couchdb data and loading to Sesame/GraphDB
# Author: Partha
# Contact: partha.msg@gmail.com
####################################################################################################

import rdflib
import couchdb
from rdflib import Graph, plugin, BNode, URIRef, Namespace
from SPARQLWrapper import SPARQLWrapper
import json, rdflib_jsonld
import pprint
from rdflib.plugin import register, Serializer
from rdflib_sparql.processor import processUpdate
import gc
import settings

def rdfLizer(item):
	for rdfLizerItem in item:
		context = {
		"@context": {
		"isAdministered": URIRef('<'+'https://w3id.org/voic#isAdministered'+rdfLizerItem['VaccineByAntigen']+'>'),
		"administeredAs": URIRef('<'+'https://w3id.org/voic#administeredAs'+'>'),
		"type":URIRef('<'+'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'+'>'),
		"@base": '.'
		}
		}
		recipient=URIRef('<https://w3id.org/voic#'+rdfLizerItem['VaccineRecipient']+'>')
		dose =  URIRef('<'+settings.varVoic + rdfLizerItem['Dose']+'>')
		vaccineByAntigen = URIRef('<'+settings.varVoic+rdfLizerItem['VaccineByAntigen']+'>')
		dummyBrand = URIRef('<'+settings.varVoic+rdfLizerItem['VaccineByAntigen']+'BrandAdministeredTo'+rdfLizerItem['VaccineRecipient']+'>')
		jsonldOutputIsAdmin = {"@id": recipient, "isAdministered":dose}
		jsonldOutputAdminAs = {"@id":dummyBrand,"type":vaccineByAntigen,"administeredAs": dose}
		settings.graph1.parse(data=json.dumps(jsonldOutputIsAdmin), format='json-ld', context=context)
		settings.graph1.parse(data=json.dumps(jsonldOutputAdminAs), format='json-ld', context=context)

def graphAdder(graph1):
	for s,p,o in settings.graph1:
		s = str(s)
		s1 =s.replace('https:/w','https://w')
		s = URIRef(s1)
		settings.graph2.add((s,p,o))

def queryRunner(item):
	for isAdminItem in item:
		subj = rdflib.URIRef('<https://w3id.org/voic#' + isAdminItem['VaccineRecipient']+'>')
		prop = rdflib.URIRef('<https://w3id.org/voic#isAdministered'+isAdminItem['VaccineByAntigen']+'>')
		obj = URIRef('<'+settings.varVoic + isAdminItem['Dose']+'>')

		settings.varList1.append([subj,prop,obj])
	gc.collect()

def notAdminFinder():
	# print ('settings.varList1: ', settings.varList1)
	for recipientRecord in settings.varList1:
		# print ('recipientRecord: ', recipientRecord)
		# adminVacList = []
		# lenCounter = []
		global stdScheduleBeninDict
		stdScheduleBeninDict = [
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredBCG>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredDTwPHibHep>'): 	rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredDTwPHibHep>'): 	rdflib.term.URIRef(u'<https://w3id.org/voic#dose2>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredDTwPHibHep>'): 	rdflib.term.URIRef(u'<https://w3id.org/voic#dose3>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredIPV>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredMeasles>'): 		rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredOPV>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredOPV>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose2>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredOPV>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose3>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredOPV>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose4>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredPneumo_conj>'): 	rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredPneumo_conj>'): 	rdflib.term.URIRef(u'<https://w3id.org/voic#dose2>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredPneumo_conj>'): 	rdflib.term.URIRef(u'<https://w3id.org/voic#dose3>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredTT>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredTT>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose2>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredTT>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose3>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredTT>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose4>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredTT>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		{rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredYF>'): 			rdflib.term.URIRef(u'<https://w3id.org/voic#dose1>')},
		]
		adminVacDose = {recipientRecord[1]:recipientRecord[2]}
		settings.adminVacList.append(adminVacDose)
	
	notAdminVacListwip = [x for x in stdScheduleBeninDict if x not in settings.adminVacList]
	# print ('adminVacList: ',settings.adminVacList)
	# print ('notAdminVacListwip: ', notAdminVacListwip)
	negateList = {
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredBCG>'):		rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredBCG>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredDTwPHibHep>'):rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredDTwPHibHep>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredIPV>'):		rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredIPV>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredMeasles>'):	rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredMeasles>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredOPV>'):		rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredOPV>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredTT>'):		rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredTT>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredYF>'):		rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredYF>'),
	rdflib.term.URIRef(u'<https://w3id.org/voic#isAdministeredPneumo_conj>'):rdflib.term.URIRef(u'<https://w3id.org/voic#isNotAdministeredPneumo_conj>')
	}

	for s in notAdminVacListwip:
		for k1,v1 in s.iteritems():
			for k2,v2 in negateList.iteritems():
				if k1==k2:
					nonDict = {recipientRecord[0]:{v2:v1}}
					global subj
					subj = URIRef(recipientRecord[0])
					pred = URIRef(v2)
					obj = URIRef(v1)
					settings.graph2.add((subj,pred,obj))
	settings.varList1 = []
	settings.adminVacList = []
		

def graphDBInserter():
	for s,p,o in settings.graph2:
		queryStringUpload = 'INSERT DATA {%s %s %s}'  %(s,p,o)
		#Uncomment the line below if you want to delete previously inserted statements
		# queryStringUpload = 'DELETE DATA {%s %s %s}'  %(s,p,o)
		# print queryStringUpload
		sparql = SPARQLWrapper(settings.graphdb_url)
		sparql.method = 'POST'
		sparql.setQuery(queryStringUpload)
		sparql.query()
		gc.collect()
def graphCleaner():
	global graph1
	processUpdate(settings.graph1, '''DELETE WHERE {?s ?p ?o }''')
	global graph2
	processUpdate(settings.graph2, '''DELETE WHERE {?s ?p ?o }''')