import sys
import urllib.request
import re

files = {
'Athaliana':[],
'Bdistachyon':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286247/SRR3286247.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286248/SRR3286248.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286249/SRR3286249.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286250/SRR3286250.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286251/SRR3286251.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286252/SRR3286252.sra'],
'Osativa':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949542/SRR949542.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949543/SRR949543.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949544/SRR949544.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949545/SRR949545.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949546/SRR949546.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949547/SRR949547.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949548/SRR949548.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949549/SRR949549.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949550/SRR949550.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949551/SRR949551.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX153/SRX153035/SRR949552/SRR949552.sra'],
'Ppersica':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656929/SRR3286303/SRR3286303.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656929/SRR3286304/SRR3286304.sra'],
'Ptrichocarpa':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656930/SRR3286305/SRR3286305.sra'],
'Sbicolor':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656933/SRR3286309/SRR3286309.sra'],
'Slycopersicum':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX200/SRX2008738/SRR4013312/SRR4013312.sra'],
'Vvinifera':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286315/SRR3286315.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286316/SRR3286316.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286317/SRR3286317.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286318/SRR3286318.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286319/SRR3286319.sra'],
'Zmays':[]
}

for i in files.get(sys.argv[1]):
	print(re.sub('ftp.*\/','',i))	
	urllib.request.urlretrieve(i,re.sub('ftp.*\/','',i))

