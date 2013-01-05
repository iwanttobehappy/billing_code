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
ratesHNL=dict()
cptCodesHNL=dict()
totalDirectBill=0
unpricedCPT=set()

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
	
def showDirectBill():
	global totalDirectBill
	for k,v in cptCodesHNL.items():
		if v!=0:
			print k+'\t'+"{0:.2f}".format(v)
			totalDirectBill +=v
	print '\t'+"{0:.2f}".format(totalDirectBill)
	
	
def tallyUpDirectBill(cptcode):
	real=ratesHNL.get(cptcode)
	if real != None:
		cptCodesHNL[cptcode] += float(real)
	else:
		unpricedCPT.add(cptcode)



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


#read expected and actual for payor rates	
reportReader=csv.reader(open(filename,'rb'),delimiter=',',quotechar='\'')
reportReader.next()

	
for row in reportReader:
	ratesExpected[row[0]]=row[2]
	ratesActual[row[0]]=row[3]
	cptCodes[row[0]]=0
	cptCodesCollected[row[0]]=0
	
#read direct bill file rates
rr=csv.reader(open(hnlRates,'rb'),delimiter=',',quotechar='\'')

for row in rr:
	ratesHNL[row[0]]=row[1]
	cptCodesHNL[row[0]]=0
	
	
reportReader2=csv.reader(open(hl7file,'rU'),delimiter='|',quotechar='\'')
reportReader2.next()

for row in reportReader2:
	if row[0]=='PV1':
		if isDirectBill(row[7]):
			DirectBill=True
		else:
			DirectBill=False
	if row[0]=='FT1' and row[7].isdigit():
		if DirectBill==False:
			tallyUp(row[7])
		else:
			tallyUpDirectBill(row[7])
	
	#if row[0]=='PV1':
	#	print row[7],isDirectBill(row[7])
		
print "Payor Expected and Actual"
print "CPT"+'\t'+"Expected"+'\t'+"Actual"
showExpectedAndActual()
print
print "Direct Bill HNL"
print "CPT"+'\t'+"Actual"
showDirectBill()
print "Unpriced CPT's for direct bill"
print unpricedCPT


	
	
	
	
	
	

