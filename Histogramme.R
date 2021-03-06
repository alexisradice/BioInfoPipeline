histo <- read.table('flagstat.csv', header=TRUE, sep=',', dec='.')
# read.table permet de charger un jeu de donn�es
# il faut commencer par lui indiquer le chemin par lequel on acc�de au fichier, le nom du fichier et son format
# ensuite tu lui dis si il y a des noms de colonne dans le fichier: header=TRUE
# le s�parateur entre chaque colonne: sep=''
# dec='': pour indiquer le format des nombres d�cimaux
head(histo) # on te montre les 6 premi�res lignes de ton fichier
summary(histo) # on te montre un r�sum� de ton fichier par colonne, �a permet de voir si le logiciel a bien compris que tes colonnes de nombres sont des colonnes de nombres 

#?barplot # permet de demander � R des informations sur une fonction et de savoir sur quel param�tre on peut agir

par(mar=c(5.5,4,4,1)) # on d�finit les marges autour du graphique
barplot(histo[,2], # quelle colonne on veut repr�senter
                ylim=c(0,100), # limites de l'axe y, �a te permet de zoomer et de d�zoomer autant que tu veux
                names.arg=histo[,1], # le nom des �chantillons
                las=2, # l'orientation du nom des �chantillons
                main="Histogramme representant le pourcentage de reads qui mappent le genome de reference", # choisit le titre
                cex.names=0.7, # la taille du texte des echantillons
		cex.main=0.9,
                ylab='Pourcentage', # nom de l'axe y
                col=c('green','blue','yellow')) # les couleurs, tu peux le retirer, ils seront tout gris. 
                                                # Sinon tu peux choisir autant de couleurs que tu veux 



