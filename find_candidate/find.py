import sys

def expand_cigar(cigar):
    num = 0
    if cigar == '*':
        return cigar
    ret = ""
    for c in cigar:
        if c.isdigit():
            num = num * 10 + int(c)
        else:
            ret = ret + c * num
            num = 0
    return ret

def main():
    if len(sys.argv) <= 2:
        print "Usage %s <chr> <filename prefix> <pos>" % (sys.argv[0])
        exit()
    filename = sys.argv[2]
    with open(filename+".fa") as f:
        ref = f.read().translate(None,"\n")
    with open(filename+".sam") as f:
        sam = f.read().splitlines()
   
    call_pos = int(sys.argv[3])
    chromosome = sys.argv[1]

    read_range = 1000500
    count_A = [0]*read_range
    count_G = [0]*read_range
    count_C = [0]*read_range
    count_T = [0]*read_range
    total_counts = [0]*read_range

    min_count = 2
    min_fraction = 0

    for sam_line in sam:
        line = sam_line.split("\t")
        pos = int(line[3])
        mapq = line[4]
        seq = line[9]
        qual = line[10]
        flag = int(line[1])
        cigar = expand_cigar(line[5])

        ref_pos = pos - call_pos + 200
        read_pos = 0
        for cigar_index in range(len(cigar)):
            this_cigar = cigar[cigar_index]
            if this_cigar == 'M':
                if seq[read_pos] == ref[ref_pos].upper():
                    read_pos = read_pos + 1
                    ref_pos = ref_pos + 1
                    continue    
                else:
                    if seq[read_pos] == "A":
                        count_A[ref_pos] = count_A[ref_pos] + 1
                    if seq[read_pos] == "C":
                        count_C[ref_pos] = count_C[ref_pos] + 1
                    if seq[read_pos] == "G":
                        count_G[ref_pos] = count_G[ref_pos] + 1
                    if seq[read_pos] == "T":
                        count_T[ref_pos] = count_T[ref_pos] + 1
                    read_pos = read_pos + 1
                    ref_pos = ref_pos + 1
                continue
            elif this_cigar == 'I' or this_cigar == 'S':
                read_pos = read_pos + 1
                continue
            elif this_cigar == 'D':
                ref_pos = ref_pos + 1
                continue
            elif this_cigar == 'H':
                continue
            else:
                continue

    for i in range(0,read_range):
        total_counts[i] = count_A[i] + count_C[i] + count_G[i] + count_T[i]
        if total_counts[i] != 0:
            if count_A[i] >= min_count:
                if float(count_A[i]) / float(total_counts[i]) >= min_fraction:
                    print "A %d %s" % (i + call_pos - 200, chromosome)
            if count_G[i] >= min_count:
                 if float(count_G[i]) / float(total_counts[i]) >= min_fraction:
                    print "G %d %s" % (i + call_pos - 200, chromosome)
            if count_C[i] >= min_count:
                 if float(count_C[i]) / float(total_counts[i]) >= min_fraction:
                    print "C %d %s" % (i + call_pos - 200, chromosome)
            if count_T[i] >= min_count:
                 if float(count_T[i]) / float(total_counts[i]) >= min_fraction:
                    print "T %d %s" % (i + call_pos - 200, chromosome)

if __name__ == "__main__":
    main()
