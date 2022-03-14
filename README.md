# Bio Info Pipeline

## Introduction

The goal of the project was to design a computer pipeline that collects and performs a cleanup, identification and analysis of the mass of available bread and beer yeast genome data. This would provide a genotype table that would allow biological researchers to estimate the evolutionary history of natural and domesticated yeast. 

DNA molecules are the carriers of genetic information. They are composed of chromosomes. They are made of nucleotides A, C, G, T. All the DNA molecules of a living being form its genome. The expression of the latter gives a part of the phenotype (set of observable characteristics of an individual: morphological, physiological or biochemical). At the creation of a new individual, the genome can mutate. That is to say that it has one or several parts of its DNA which was modified, removed or added. If this mutation is beneficial in the environment of the living being then it will proliferate. By comparing the genomes of these different strains, we can trace the evolutionary history of the species. In the case of the yeasts studied, their environment was controlled by man, forcing the direction of their evolution to meet his needs. This is domestication. We wish to retrace their evolution, and to do this we will be able to study their genome which has been sequenced.
Here, the sequencing is done by Illumina technology which consists in cutting the DNA into small strands, making them single-stranded with oligonucleotides at the ends. The latter allow the DNA to be attached to a glass plate called a flow cell. On this cell we recreate the complementary strand and then remove the original strand. The complementary strand hybridizes to another attachment point of the cell and a new complementary strand is created, then the two strands are detached. This step is repeated several times until the cell is filled. Once done, we remove all the complementary strands to keep only the copies of the original. Once this part is done, we start the real sequencing by incorporating one type of nucleotide at a time that emits light of a precise color which allows us to determine them. 

From a computer point of view, the objective was to create a pipeline, that is to say a series of tasks that run one after the other, without any external intervention and that can include verifications, creation of intermediate files, user's choices and parallelization to minimize its duration. In this pipeline, written in Python, we had to integrate R scripts to obtain histograms and diagrams, or algorithms like Gatk, bcfTools, BedTools, Bwa, samtools, Vcftools.

## Presentation

The pipeline is written in python 3.9.2 under linux (Manjaro). It uses R scripts and a multitude of external tools (scripts, algorithms etc.) specialized for Bio-Informatics. From a TSV file, the pipeline produces new types of files, temporary or not, stored in folders as well as tables, graphs, text documents and histograms. The TSV contains the information for each sample line by line, including the single-alias, reload link and md5. If the sample is a single-end, there would be only one link and one md5, otherwise there are 2 and it is a pair-end. It is composed of 4 main parts: collection, cleaning, identification, analysis.

## Usage

To launch the script you must first check that the tools: bcftools, bedtools, bwa, gatk, samtools and vcftools are present in the folder containing the project and installed (`make` command).
The tool folders must be named as above.

The R scripts Histogram.R, Filtration.R and PCA.R as well as the files intervals.list, TSV.txt (TSV file) and refGenome.fasta (Reference genome file) must also be in the project folder.

Then to run: `python pipeline.py`

## Results

Comming Soon...