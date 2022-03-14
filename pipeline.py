import hashlib
import subprocess as sp
import os
import hashlib
import csv
from os import listdir
from os.path import isfile, join


words = open('TSV.txt')

os.system("mkdir FichiersERR")
os.system("mkdir FichiersBAM")
os.system("mkdir FichiersBED")
os.system("mkdir FichiersGenomicsDB")
os.system("mkdir FichiersMarkedDuplicates")
os.system("mkdir FichiersSAM")
os.system("mkdir FichiersSortedBAM")
os.system("mkdir FichiersVCFs")
os.system("mkdir VariantFiltration")
os.system("mkdir vcfPASS")
os.system("mkdir FichiersHaplotypeCaller")

premiereLigne = words.readline().split("\t")
#print(premiereLigne[0])

fastq_md5 = 0
fastq_ftp = 0
sample_alias = 0

for i in range(len(premiereLigne)):
    if (premiereLigne[i] == "fastq_md5"):
        fastq_md5 = i
    if (premiereLigne[i] == "fastq_ftp"):
        fastq_ftp = i
    if (premiereLigne[i] == "sample_alias"):
        sample_alias = i
    #print(i)

print(fastq_md5)
print(fastq_ftp)
print(sample_alias)

line = words.readline() # Stocker la ligne
CountError = 0          # Nombre d'erreur de comparaison md5 entre le fichier et le filereport 
TabListErrorMD5 = []
CountLines = 0          # Comptage des lignes pour le terminal

TabSampleAliasAll = []

while (line):                       #Boucle pour parcourir le fichier ligne par ligne
    CountLines = CountLines + 1
    Count = 0
    TabMD5 = []         #Le tableau qui stock tous les md5
    TabFTP = []         #Le tableau qui stock tous les liens
    TabSampleAlias = []
    BoolOK = False
    for char in line:       # Boucle pour remplir TabMD5 et TabFTP
        if char == "	":
            Count += 1
        if Count == fastq_md5:                  # Ajoute dans le tableau le string après la nème tabulation (md5)
            TabMD5.append(char)
        if Count == fastq_ftp:                  # Ajoute dans le tableau le string après la nème tabulation (liens)
            TabFTP.append(char)
        if Count == sample_alias:
            TabSampleAlias.append(char)
        if char == ";":
            BoolOK = True
        
    #print(TabMD5)
    #print(TabFTP)
    #print(TabSampleAlias)
    #print(Count)

    del TabSampleAlias[0] 
    del TabMD5[0]       #Supprime le 1er index car c'est une tabulation
    TabFTP[0] = "ftp://"        #ajoute avant le lien a la place de la tabulation
    StrTabMD5 = "".join(TabMD5)
    StrTabFTP = "".join(TabFTP)
    StrTabSampleAlias = "".join(TabSampleAlias)
    output = "FichiersERR"
    outputOpen = "FichiersERR/"

    print('Telechargement Ligne ' + str(CountLines))
    if(TabMD5 != []):
        TabSampleAliasAll.append(StrTabSampleAlias)
        if BoolOK == True:                          #Rentre dans la boucle quand on arrive au caractère ';'
            StrTabMD5 = StrTabMD5.split(';')        #Transforme le String en tableau avec les deux md5
            StrTabFTP = StrTabFTP.split(';')        #Transforme le String en tableau avec les deux liens
            StrTabFTP[1] = "ftp://" + StrTabFTP[1]      #Ajoute pour le 2ème index
            #print(StrTabMD5[0])
            #print(StrTabMD5[1])
            #print(StrTabFTP[0])
            #print(StrTabFTP[1])
            url = StrTabFTP[0]
            sp.call(['wget', '-P', output, url])        #Telecharge index 1 du tableau
            #print(output + url)
            url = StrTabFTP[1]
            sp.call(['wget', '-P', output, url])        #Telecharge index 2 du tableau
            StrTabFTP[0] = StrTabFTP[0].split('/')   
            StrTabFTP[1] = StrTabFTP[1].split('/')
            # print(StrTabFTP[0])
            # print(StrTabFTP[1])

            md5_hash = hashlib.md5()                            #Récupère le md5 pour le premier fichier _1 (double)
            a_file = open(outputOpen + StrTabFTP[0][8], "rb")
            content = a_file.read()
            md5_hash.update(content)
            digest = md5_hash.hexdigest()
            #print(digest)
            if (StrTabMD5[0] != digest):    #Compte les erreurs de md5
                CountError = CountError+1
                TabListErrorMD5.append(StrTabFTP[1][8]) #Ajoute les noms des ERR dans le tableaux des erreurs de MD5
            md5_hash = hashlib.md5()        #Récupère le md5 pour le deuxième fichier _2 (double)
            a_file = open(outputOpen + StrTabFTP[1][8], "rb")
            content = a_file.read()
            md5_hash.update(content)                                                                                                                                                               
            digest = md5_hash.hexdigest()
            #print(digest)
            if (StrTabMD5[1] != digest):        #Compte les erreurs de md5
                CountError = CountError+1
                TabListErrorMD5.append(StrTabFTP[1][8]) #Ajoute les noms des ERR dans le tableaux des erreurs de MD5
                
        else:
            #print(StrTabMD5)
            #print(StrTabFTP)
            url = StrTabFTP
            sp.call(['wget', '-P', output, url])
            StrTabFTP = StrTabFTP.split('/')
            # print(StrTabFTP)

            md5_hash = hashlib.md5()                        #Récupère le md5 pour le fichier seul
            a_file = open(outputOpen + StrTabFTP[8], "rb")
            content = a_file.read()
            md5_hash.update(content)
            digest = md5_hash.hexdigest()
            #print(digest)
            if (StrTabMD5 != digest):       #Compte les erreurs de md5
                CountError = CountError+1
                TabListErrorMD5.append(StrTabFTP[1][8]) #Ajoute les noms des ERR dans le tableaux des erreurs de MD5

    line = words.readline()                 #Avance à la ligne d'après

print("Il y a donc " + str(CountError) + " problemes de MD5 : ")
print(TabListErrorMD5)


# Lancement Script Mapping

#print("Démarrage du mapping avec bwa") #Ajouter if pour verifier si le fichier est déjà présent pour ne pas retelecharger ou retransformer

tab1 = os.popen('ls -R FichiersERR/ | grep \'_1\'').read().split()      # Récupère la sous liste contenant les ERR_1 
tab2 = os.popen('ls -R FichiersERR/ | grep -v \'_\'').read().split()    # Récupère la sous liste contenant les ERR  
del tab2[0]     #Retirer la première case inutile de tab2

#print(tab1)
#print(tab2)
#print(len(tab1))

for i in range(len(tab1)):              #Split tab1 et récupère juste l'intitulé
    tab1[i] = tab1[i].split("_")[0]

for i in range(len(tab2)):              #Split tab2 et récupère juste l'intitulé
    tab2[i] = tab2[i].split(".")[0]

#print(tab1)
#print(tab2)


os.system("bwa/./bwa index refGenome.fasta")        #Index BWA Utilisable avec fasta ou fsa (si fsa il faut le renommer en fasta)
os.system("samtools faidx refGenome.fasta")         #Creer le fichier fasta.fai pour le HaplotypeCaller
os.system("gatk/gatk CreateSequenceDictionary -R refGenome.fasta")  #Creer le fichier .dict pour le HaplotypeCaller


for i in range(len(tab1)):
    RG = "\"@RG\\tID:" + tab1[i] + "\\tPL:ILLUMINA\\tPI:0\\tSM:" + tab1[i] + "\\tLB:1\""
    cmd = "bwa/./bwa mem -R " + RG + " refGenome.fasta FichiersERR/" + tab1[i] + "_1.fastq.gz FichiersERR/" + tab1[i] + "_2.fastq.gz | gzip -3 > FichiersSAM/" + tab1[i] + ".sam.gz"    # Commande BWA pour les duos
    decompresser = "gzip -d FichiersSAM/" + tab1[i] + ".sam.gz"
    os.system(cmd)
    os.system(decompresser)

for i in range(len(tab2)):
    RG = "\"@RG\\tID:" + tab2[i] + "\\tPL:ILLUMINA\\tPI:0\\tSM:" + tab2[i] + "\\tLB:1\""
    cmd = "bwa/./bwa mem -R " + RG + " refGenome.fasta FichiersERR/" + tab2[i] + ".fastq.gz | gzip -3 > FichiersSAM/" + tab2[i] + ".sam.gz" # Commande BWA pour les solos
    decompresser = "gzip -d FichiersSAM/" + tab2[i] + ".sam.gz"
    os.system(cmd)
    os.system(decompresser)

tab3 = os.popen('ls -R FichiersSAM/').read().split()      # Récupère la sous liste contenant les SAM
del tab3[0]     #Retirer la première case inutile de tab3

for i in range(len(tab3)):              #Split tab2 et récupère juste l'intitulé
    tab3[i] = tab3[i].split(".")[0]

#print(tab3)
#print(TabSampleAliasAll)


#Partie pour générer le flagstat pour chaque fichier : DEBUT

os.system("rm flagstat.txt") 
os.system("touch flagstat.txt")     
flagstat = open('flagstat.txt', "a")
csvFlagstat = "flagstat.csv"
file = open(csvFlagstat, "w")
writer = csv.writer(file)
writer.writerow(('ERR','Pourcentage'))
tempmin = 100
tempmax = 0

for i in range(len(tab3)):              #Split tab3 et récupère juste l'intitulé
    tab3[i] = tab3[i].split(".")[0]     
    flags = os.popen("samtools/samtools flagstat FichiersSAM/" + tab3[i] + ".sam").readlines()          #Execute la commande flagstat et ajoute chaque ligne dans une case de tableau
    flags = flags[4].split("(")     #Split une première fois à partir du caractère '('  sur la ligne numéro 4 contenant le pourcentage
    flags = flags[1].split(" ")     #Deuxième split pour isoler le pourcentage
    rate = flags[0]                 #Stockage du pourcentage
    pourcentageFloat = float(rate.split("%")[0])
    if (pourcentageFloat < tempmin):
        tempmin = pourcentageFloat
    if (pourcentageFloat > tempmax):
        tempmax = pourcentageFloat
    rate = rate.split(".")
    rate = rate[0] + "," + rate[1]
    flagstat.write(TabSampleAliasAll[i] + "\t" + rate + "\n")    #Ecrit dans le fichier les informations (Nom    %)
    writer.writerow((TabSampleAliasAll[i],pourcentageFloat))
    #print(rate)
    #print(pourcentageFloat/100)
flagstat.write("Minimum : " + str(tempmin) + "\n" + "Maximum : " + str(tempmax) + "\n")
flagstat.close()        #Ferme le fichier
file.close()
#   FIN


#Partie pour générer un fichier txt les sample_alias et gvcf : DEBUT

os.system("rm sample.map") 
os.system("touch sample.map")     
sample = open('sample.map', "a")

for i in range(len(TabSampleAliasAll)):
    TabSampleAliasAll[i] = TabSampleAliasAll[i] + "\t" +  "FichiersHaplotypeCaller/" + tab3[i] + ".g.vcf.gz" + "\n"  
    sample.write(TabSampleAliasAll[i])
    #print(TabSampleAliasAll[i])
sample.close()        #Ferme le fichier

#   FIN



for i in range(len(tab3)):
    cmd1 = "samtools/samtools view -S -b FichiersSAM/" + tab3[i] + ".sam > FichiersBAM/" + tab3[i] + ".bam" # Commande SAM 
    cmd2 = "samtools sort FichiersBAM/" + tab3[i] + ".bam -o FichiersSortedBAM/" + tab3[i] + ".sorted.bam" # Commande SAMSorted 
    cmd3 = "samtools/samtools view FichiersBAM/" + tab3[i] + ".bam | head" #Preview Fichier SAM
    cmd4 = "bedtools/bin/bedtools genomecov -ibam FichiersSortedBAM/" + tab3[i] + ".sorted.bam -bga > FichiersBED/" + tab3[i] + ".bed"
    cmd5 = "gatk/gatk MarkDuplicatesSpark -I FichiersSortedBAM/" + tab3[i] + ".sorted.bam -O FichiersMarkedDuplicates/" + tab3[i] +".bam"    #Commande MarkedDuplicates
    cmd6 = "gatk/gatk --java-options \"-Xmx4g\" HaplotypeCaller -R refGenome.fasta -I FichiersMarkedDuplicates/" + tab3[i] + ".bam -O FichiersHaplotypeCaller/" + tab3[i] + ".g.vcf.gz -ERC GVCF"  #Commande HaplotypeCaller

    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)



#Partie BED : DEBUT
minMap=0
maxMap=0
sortie=open('CouvertureMoyenneGenomeEchantillons', 'w')
for i in range(len(tab3)):
    text=open("FichiersBED/"+tab3[i] +'.bed', "r")
    line=text.readline()
    line=line.split('\t')
    ref=line[0]
    couvRef=0
    totRef=0
    refMax=""
    refMin=""
    minErr=0
    maxErr=0
    moyenErr=0
    cptEch=0
    boolLastLine = False
    while(line and boolLastLine == False):
        if(ref!=line[0]):
            tpr=couvRef/totRef
            moyenErr=moyenErr+tpr
            cptEch=cptEch+1
            if(tpr>maxErr):
                maxErr=tpr
                refMax=ref
            if(tpr<minErr or minErr == 0):
                minErr=tpr
                refMin=ref
            couvRef=0
            totRef=0
            ref=line[0]

        
        tpr=float(line[2])-float(line[1])
        couvRef=couvRef+tpr*float(line[3])
        totRef=totRef+tpr
        line=text.readline()
        #print(len(line))
        if(len(line) == 0):
            print(len(line))
            boolLastLine = True
            #print(len(line))
        line=line.split('\t')

#-----------------------------dernier echantillon du fichier bed----------------------------

    tpr=(couvRef/totRef)
    moyenErr=moyenErr+tpr
    cptEch=cptEch+1
    if(tpr>maxErr):
        maxErr=tpr
        refMax=ref
    if(tpr<minErr or minErr == 0):
        minErr=tpr
        refMin=ref

#-----------------------------Moyen mapping read-------------------------------------------

    moyenMap=moyenErr/cptEch
    sortie.write(TabSampleAliasAll[i] + ': ' + str(moyenMap) + '\t\tminimum: ' + str(minErr) + ' ('+refMin+')\tmaximum: ' + str(maxErr) + ' (' + refMax + ')\n')
    if(minMap>moyenMap or minMap == 0):
        minMap=moyenMap
        ErrMin=TabSampleAliasAll[i]
    if(maxMap<moyenMap):
        maxMap=moyenMap
        ErrMax=TabSampleAliasAll[i]

text.close()
sortie.write('Maximum: ' + str(maxMap) + '(' + ErrMax + ')\nMinimum: ' + str(minMap) + '(' + ErrMin + ')')
sortie.close()
#FIN Partie BED



cmd7 = "gatk/gatk GenomicsDBImport -L intervals.list --genomicsdb-workspace-path FichiersGenomicsDB/database_" + "DATABASE" + " --sample-name-map sample.map"  #Commande GenomicsDBImport
cmd8 = "gatk/gatk --java-options \"-Xmx4g\" GenotypeGVCFs -R refGenome.fasta -V gendb://FichiersGenomicsDB/database_DATABASE/ -O FichiersVCFs/database.vcf.gz"  #Commande GenotypeGVCFs
cmd9 = "gatk/gatk SelectVariants -R refGenome.fasta -V FichiersVCFs/database.vcf.gz --select-type-to-include SNP -O FichiersVCFs/databaseSNP.vcf.gz"    #Commande selection des snp

os.system("rm projetIBI_annotations") 
cmd10 = "echo -e QD\tFS\tMQ\tSOR\tMQRankSum\tReadPosRankSum >> projetIBI_annotations"   #Commande header
cmd11 = "bcftools/bcftools query -f '%QD\t%FS\t%MQ\t%SOR\t%MQRankSum\t%ReadPosRankSum\n' FichiersVCFs/databaseSNP.vcf.gz >> projetIBI_annotations" #Commande fichier pour R
cmd12 = "Rscript Filtration.R" #Pour lancer le script R 
cmd13 = "Rscript Histogramme.R" #Pour lancer le script R 
cmd14 = "gatk/gatk VariantFiltration -R refGenome.fasta -V FichiersVCFs/database.vcf.gz -O VariantFiltration/database_filtered.vcf.gz --filter-name \"QD\" --filter-expression \"QD < 5.0\" --filter-name \"MQ\" --filter-expression \"MQ < 57.0\" --filter-name \"SOR\" --filter-expression \"SOR > 3.0\" --filter-name \"MQRankSum\" --filter-expression \"MQRankSum < -2.5\" --filter-name \"MQRankSum2\" --filter-expression \"MQRankSum > 1.5\" --filter-name \"ReadPosRankSum\" --filter-expression \"ReadPosRankSum < -2.5\" --filter-name \"ReadPosRankSum2\" --filter-expression \"ReadPosRankSum > 2.5\"" #Commande VariantFiltration
cmd15 = "vcftools/bin/vcftools --gzvcf VariantFiltration/database_filtered.vcf.gz --remove-filtered-all --recode --stdout | gzip -c > vcfPASS/database_PASS.vcf.gz" #Commande vcftools
cmd16 = "Rscript ACP.R" #Pour lancer le script R 

os.system(cmd7)
os.system(cmd8)
os.system(cmd9)
os.system(cmd10)
os.system(cmd11)
os.system(cmd12)
os.system(cmd13)
os.system(cmd14)
os.system(cmd15)
os.system(cmd16)
