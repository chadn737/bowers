import sys
import urllib.request
import re

files = {
'Athaliana':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX096/SRX096372/SRR342382/SRR342382.sra'],
'Bdistachyon':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286247/SRR3286247.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286248/SRR3286248.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286249/SRR3286249.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286250/SRR3286250.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286251/SRR3286251.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286252/SRR3286252.sra'],
'Osativa':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX374/SRX374427/SRR1036000/SRR1036000.sra'],
'Ppersica':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656929/SRR3286303/SRR3286303.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656929/SRR3286304/SRR3286304.sra'],
'Ptrichocarpa':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656930/SRR3286305/SRR3286305.sra'],
'Sbicolor':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656933/SRR3286309/SRR3286309.sra'],
'Slycopersicum':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX203/SRX2030487/SRR4039351/SRR4039351.sra'],
'Vvinifera':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286315/SRR3286315.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286316/SRR3286316.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286317/SRR3286317.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286318/SRR3286318.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286319/SRR3286319.sra'],
'Zmays':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX107/SRX1073669/SRR2079447/SRR2079447.sra']
}

for i in files.get(sys.argv[1]):
	print(re.sub('ftp.*\/','',i))
	urllib.request.urlretrieve(i,re.sub('ftp.*\/','',i))
