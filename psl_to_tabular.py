#!/usr/bin/env python3

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create a BED like adjustment file from a PSL genome-to-genome alignment file")
    parser.add_argument('psl_file', type=argparse.FileType())
    args = parser.parse_args()

    for line in args.psl_file:
        fields = line.strip().split('\t')
        qname = fields[9]
        tname = fields[13]
        qlength = int(fields[10])
        tlength = int(fields[14])
        qstarts = [int(pos) for pos in fields[19].split(",") if pos.strip() != ""]
        tstarts = [int(pos) for pos in fields[20].split(",") if pos.strip() != ""]
        num_blocks = len(qstarts)
        for i in range(num_blocks):
            offset = tstarts[i] - qstarts[i]
            if i < (num_blocks - 1):
                end = tstarts[i+1]
            else:
                end = tlength + 1
            print(tname, tstarts[i], end, offset, qname, sep='\t')




