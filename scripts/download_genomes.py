import sys
import urllib.request

files = {
'Athaliana.fa':'https://genomevolution.org/coge/api/v1/genomes/25869/sequence',
'Bdistachyon.fa':'https://genomevolution.org/coge/api/v1/genomes/25040/sequence',
'Osativa.fa':'https://genomevolution.org/coge/api/v1/genomes/29143/sequence',
'Ppersica.fa':'https://genomevolution.org/coge/api/v1/genomes/22743/sequence',
'Ptrichocarpa.fa':'https://genomevolution.org/coge/api/v1/genomes/23993/sequence',
'Sbicolor.fa':'https://genomevolution.org/coge/api/v1/genomes/31607/sequence',
'Slycopersicum.fa':'https://genomevolution.org/coge/api/v1/genomes/24769/sequence',
'Vvinifera.fa':'https://genomevolution.org/coge/api/v1/genomes/19990/sequence',
'Zmays.fa':'https://genomevolution.org/coge/api/v1/genomes/33766/sequence',
}

urllib.request.urlretrieve(files.get(sysargv[0]+'.fa'),sys.argv[0]+'.fa')
