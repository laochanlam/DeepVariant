import sys
import random
import subprocess
import shlex

def main():
    if len(sys.argv) < 3:
        print "Usage %s <vcf> <candidate_variant> <start position> <chr>" % (sys.argv[0])
        exit()
    vcf_filename = sys.argv[1]
    candidate_filename = sys.argv[2]
    position = int(sys.argv[3])
    chrom = sys.argv[4][3:]

    # customize data
    bam = "data/elsa.bam"
    fa = "data/ucsc.hg19.fasta"

    with open(vcf_filename) as f:
        vcf = f.read().splitlines()
    with open(candidate_filename) as f:
        candidate = f.read().splitlines()


    # Select a range for search
    SNPS = []
    for vcf_line in vcf:
        line_vcf = vcf_line.split("\t")
        if line_vcf[0][0] != '#':
            if (int(line_vcf[1]) <= position + 1000000 + 200) & (int(line_vcf[1]) >= position - 200):
                if (len(line_vcf[3]) == 1) & (len(line_vcf[4]) == 1):
                    # chromsome determine
                    if line_vcf[0] == chrom:
                        SNPS.append(vcf_line)

    print "[Bounding Completed]"


    # Search
    for candidate_line in candidate:
        line = candidate_line.split(" ")
        timer = 0
        for SNP_line in SNPS:
            timer = timer + 1
            line_SNP = SNP_line.split("\t")

            ref = line_SNP[3]
            alt = line[0]
            pos = line[1]
            chrom = "chr" + line_SNP[0]

            if (line_SNP[0][0] != '#') & (line_SNP[0] != "0"):
                if int(line_SNP[1]) < int(line[1]):
                    continue

                # het or hom
                if (int(line[1]) == int(line_SNP[1])) & (line_SNP[4]  == line[0]):
                    if (line_SNP[9][0] == "1") & (line_SNP[9][2] == "1"):
                        genotype = "hom-alt"
                    else:
                        genotype = "het"
                    command = "image_generation/gen_image.sh %s %s %s %s %s %s" % (chrom, pos, alt, bam, fa, genotype)
                    subprocess.call(shlex.split(command))
                    break

                # Ref
                if int(line_SNP[1]) > int(line[1]):
                    genotype = "ref"
		            # 3/100 to call
                    if (random.randint(0,100) < 3):
                        command = "image_generation/gen_image.sh %s %s %s %s %s %s" % (chrom, pos, alt, bam, fa, genotype)
                        subprocess.call(shlex.split(command))
                    break

if __name__ == "__main__":
    main()
