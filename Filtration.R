#R script pour faire des distributions
#!/usr/bin/env Rscript
library(lattice)
library(VennDiagram)

# LECTURE DU FICHIER
annot.file = "projetIBI_annotations"
annotations = read.table(annot.file, h=TRUE,na.strings=".")

# INITIALISATION DES SEUILS
lim.QD = 5	#avant 10 pour garder monozigote et heterozigote
lim.MQ = 57	#juste avant le pic
lim.MQRankSum = -2.5	#enlever les premiers petites montés
lim.MQRankSum2 = 1.5	#enlever les premiers petites montés
lim.ReadPosRankSum = -2.5	#enlever les deux premières petites montés
lim.ReadPosRankSum2 = 2.5	#enlever les deux premières petites montés
lim.SOR = 3.0	#enlever les dernières petites montés

# CREATION DES FIGURES
pdf(paste(annot.file,"Filtres.pdf",sep="_"))
## FIGURE DE QD
  prop.QD=length( which(annotations$QD >lim.QD)) / nrow(annotations)
  plot(density(annotations$QD,na.rm=T),main="QD", sub = paste("Filtre: QD >",lim.QD,"( = ", signif(prop.QD,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.QD, col="red")

## FIGURE DE MQ
  prop.MQ=length( which(annotations$MQ >lim.MQ)) / nrow(annotations)
  plot(density(annotations$MQ,na.rm=T),main="MQ", sub = paste("Filtre: MQ >",lim.MQ,"( = ", signif(prop.MQ,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.MQ, col="red")

## FIGURE DE SOR
  prop.SOR=length( which(annotations$SOR <lim.SOR)) / nrow(annotations)
  plot(density(annotations$SOR,na.rm=T),main="SOR", sub = paste("Filtre: SOR <",lim.SOR,"( = ", signif(prop.SOR,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.SOR, col="red")

## FIGURE DE MQRankSum
  varMQRankSum = which(annotations$MQRankSum >lim.MQRankSum)
  prop.MQRankSum=length( which(annotations$MQRankSum >lim.MQRankSum & annotations$MQRankSum <lim.MQRankSum2)) / nrow(annotations)
  plot(density(annotations$MQRankSum,na.rm=T),main="MQRankSum", sub = paste("Filtre: ",lim.MQRankSum," < MQRankSum < ",lim.MQRankSum2,"( = ", signif(prop.MQRankSum,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.MQRankSum, col="red")
  abline(v=lim.MQRankSum2, col="red")

## FIGURE DE ReadPosRankSum
  prop.ReadPosRankSum=length( which(annotations$ReadPosRankSum >lim.ReadPosRankSum & annotations$ReadPosRankSum <lim.ReadPosRankSum2)) / nrow(annotations)
  plot(density(annotations$ReadPosRankSum,na.rm=T),main="ReadPosRankSum", sub = paste("Filtre: ",lim.ReadPosRankSum," < ReadPosRankSum < ",lim.ReadPosRankSum2,"( = ", signif(prop.ReadPosRankSum,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.ReadPosRankSum, col="red")
  abline(v=lim.ReadPosRankSum2, col="red")

dev.off()

# DIAGRAMME DE VENN
qd.pass = which(annotations$QD>lim.QD)
sor.pass = which(annotations$SOR < lim.SOR)
mq.pass = which(annotations$MQ > lim.MQ)
mqrs.pass= which(annotations$MQRankSum > lim.MQRankSum & annotations$MQRankSum < lim.MQRankSum2)
rprs.pass= which(annotations$ReadPosRankSum > lim.ReadPosRankSum & annotations$ReadPosRankSum < lim.ReadPosRankSum2)

venn.diagram(
  x=list(qd.pass,mq.pass,sor.pass,mqrs.pass,rprs.pass),
  category.names = c("QD", "MQ", "SOR","MQRankSum", "ReadPosRankSum"),
  fill = c("blue","orange","yellow","red","purple"),
  output=TRUE,
  filename = "DiagrammeVennDistributions"
  )


