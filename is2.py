import sys
import csv
import string
from datetime import date
import datetime


ratesExpected=dict()
ratesActual=dict()
cptCodes=dict()
cptCodesCollected=dict()
hnlCptCodes=dict()
totalExpected=0
totalActual=0

#direct bill stuff 
directBillDoctors=['Cornfield','Gheith']

def isDirectBill(doctorstring):
	for doc in directBillDoctors:
		if doc in doctorstring:
			return True
	return False
	

def showExpectedAndActual():
	global totalExpected
	global totalActual
	for k,v in cptCodes.items():
		if v !=0:
			print k+'\t'+"{0:.2f}".format(v).rjust(7)+'\t'+"{0:.2f}".format(cptCodesCollected[k]).rjust(7)
			totalExpected += v
			totalActual += cptCodesCollected[k]
	print '\t'+"{0:.2f}".format(totalExpected).rjust(7)+'\t'+"{0:.2f}".format(totalActual).rjust(7)
	




def tallyUp(cptcode):
	e=ratesExpected.get(cptcode)
	a=ratesActual.get(cptcode)
	if a != None and e != None:
		cptCodes[cptcode] += float(e)
		cptCodesCollected[cptcode] += float(a)
	

if len(sys.argv)== 4:
	filename=sys.argv[1]
	hl7file=sys.argv[2]
	hnlRates=sys.argv[3]
	
else:
	print "USAGE: python is.py <rates_csvfile> <hl7 file> <hnl_rates>"
	print "bye bye"
	sys.exit()


	
reportReader=csv.reader(open(filename,'rb'),delimiter=',',quotechar='\'')
reportReader.next()

	
for row in reportReader:
	ratesExpected[row[0]]=row[2]
	ratesActual[row[0]]=row[3]
	cptCodes[row[0]]=0
	cptCodesCollected[row[0]]=0
	
	
reportReader2=csv.reader(open(hl7file,'rU'),delimiter='|',quotechar='\'')
reportReader2.next()

for row in reportReader2:
	if row[0]=='FT1' and row[7].isdigit():
		tallyUp(row[7])
	#if row[0]=='PV1':
	#	print row[7],isDirectBill(row[7])
		
print "CPT"+'\t'+"Expected"+'\t'+"Actual"
showExpectedAndActual()


	
	
	
	
	
	

