export PATH=${PATH}:/opt/tophatfusion-0.1.0/:/opt/blast-2.2.24/bin/:/opt/bowtie-0.12.7/:/opt/samtools-0.1.17/
/opt/tophatfusion-0.1.0/tophat-fusion-post -p 2 --num-fusion-reads 1 --num-fusion-pairs 2 --num-fusion-both 5  /opt/bowtie-0.12.7/indexes/hg19/hg19 
