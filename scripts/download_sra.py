import sys
import urllib.request

files = {
'Athaliana':[],
'Bdistachyon':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286247/SRR3286247.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286248/SRR3286248.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286249/SRR3286249.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286250/SRR3286250.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286251/SRR3286251.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656912/SRR3286252/SRR3286252.sra'],
'Osativa':[],
'Ppersica':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656929/SRR3286303/SRR3286303.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656929/SRR3286304/SRR3286304.sra'],
'Ptrichocarpa':[],
'Sbicolor':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656933/SRR3286309/SRR3286309.sra'],
'Slycopersicum':[],
'Vvinifera':['ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286315/SRR3286315.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286316/SRR3286316.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286317/SRR3286317.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286318/SRR3286318.sra',
'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX165/SRX1656936/SRR3286319/SRR3286319.sra'],
'Zmays':[]
}

for v in files.get(sys.arv[0]):
    urllib.request.urlretrieve(i,re.sub('ftp.*\/','',i))
