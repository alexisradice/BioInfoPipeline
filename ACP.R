#R script pour faire des distributions
#!/usr/bin/env Rscript
library(gdsfmt)
library("SNPRelate") # pour charger les donner et les manipuler
library(ape) # pour faire des arbres
library(RColorBrewer) # pour avoir de jolies couleurs

file="vcfPASS/database_PASS"
ofile=paste(file,".gds",sep="")
ifile=paste(file,".vcf.gz",sep="")
snpgdsVCF2GDS(ifile, ofile,verbose=TRUE)

genofile <- snpgdsOpen(ofile)
## A propos des échantillons ##
sample.id <- read.gdsn(index.gdsn(genofile, "sample.id"))

n <- 26
qual.col.pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
print(qual.col.pals)
col.vector = unlist(mapply(brewer.pal, qual.col.pals$maxcolors, rownames(qual.col.pals)))[1:n]



PCA <- snpgdsPCA(genofile,autosome.only=FALSE,remove.monosnp=TRUE, maf=NaN, missing.rate=NaN, eigen.cnt=0, sample.id=sample.id)

colnames(PCA$eigenvect)=PCA$varprop
rownames(PCA$eigenvect)=sample.id

pdf(paste(file,"PCA.pdf",sep="_"))
plot(x=PCA$eigenvect[,1],
    y=PCA$eigenvect[,2],
    main=paste("PCA (SNPRelate, no projection, ",length(PCA$snp.id)," SNPs)",sep=""), #Titre de la figure
    xlab=paste("Axe 1 (",round(as.numeric(colnames(PCA$eigenvect)[1])*100,2),"%)",sep=""), #On indique la proportion de variance expliquée par le premier axe
    ylab=paste("Axe 2 (",round(as.numeric(colnames(PCA$eigenvect)[2])*100,2),"%)",sep=""), #idem pour l'axe 2
    pch=0:25,
    col=col.vector) # forme et couleur des points

legend("topright", #on met la légende en haut à droite
    legend = sample.id, 
    pch=0:25, 
    col=col.vector,
    ncol=3)

dev.off()