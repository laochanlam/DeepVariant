import sys
import subprocess
import shlex

def main():
    if len(sys.argv) < 2:
        print "Usage %s <vcf> <candidate_variant>" % (sys.argv[0])
        exit()
    vcf_filename = sys.argv[1]
    candidate_filename = sys.argv[2]

    bingo = 0
    ref = 0

    with open(vcf_filename) as f:
        vcf = f.read().splitlines()
    with open(candidate_filename) as f:
        candidate = f.read().splitlines()


    #  Normal Version

    # for candidate_line in candidate:
    #     line = candidate_line.split(" ")
        # chromosome = line[2][3]
        # print chromosome

        # for vcf_line in vcf:
        #     line_vcf = vcf_line.split("\t")
        #     if line_vcf[0][0] != '#':
        #         # if chromosome == line_vcf[0]:
        #         # if (line[0] == line_vcf[4]):
        #         #     print "yo"
        #         if int(line_vcf[1]) < int(line[1]):
        #             continue
        #         if (int(line[1]) == int(line_vcf[1])) & (line_vcf[4]  == line[0]):
        #             # print line[1]
        #             # print "vcf : %s and candidate : %s" % (line_vcf[4], line[0])
        #             bingo = bingo + 1
        #             break
        #         if int(line_vcf[1]) > int(line[1]):
        #             ref = ref + 1
        #             break
    



    # Filter Version
    i = 0
    SNPS = [0]* 824
    for vcf_line in vcf:
        line_vcf = vcf_line.split("\t")
        if line_vcf[0][0] != '#':
            if (int(line_vcf[1]) <= 2000000 + 200) & (int(line_vcf[1]) >= 1000000 - 200):
                if (len(line_vcf[3]) == 1) & (len(line_vcf[4]) == 1):
                    if int(line_vcf[0]) == 1:
                        SNPS[i] = vcf_line
                        i = i + 1


    for candidate_line in candidate:
        line = candidate_line.split(" ")
        timer = 0
        for vcf_line in SNPS:
            timer = timer + 1
            if vcf_line != 0:
                line_vcf = vcf_line.split("\t")
                if (line_vcf[0][0] != '#') & (line_vcf[0] != "0"):
                    # if chromosome == line_vcf[0]:
                    # if (line[0] == line_vcf[4]):
                    #     print "yo"
                    if int(line_vcf[1]) < int(line[1]):
                        continue
                    if (int(line[1]) == int(line_vcf[1])) & (line_vcf[4]  == line[0]):
                        # print line[1]
                        # print "vcf : %s and candidate : %s" % (line_vcf[4], line[0])
                        bingo = bingo + 1
                        SNPS[timer-1] = "0"
                        break
                    if int(line_vcf[1]) > int(line[1]):
                        ref = ref + 1
                        break






    for SNPS_line in SNPS:
        print SNPS_line

    print bingo
    print ref

if __name__ == "__main__":
    main()
