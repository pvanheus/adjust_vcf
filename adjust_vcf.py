#!/usr/bin/env python3

import argparse
import sys

from typing import TextIO

from intervaltree import IntervalTree, Interval


def read_intervals(interval_bed_file: TextIO) -> dict[str, IntervalTree]:
    adjustment_intervals = IntervalTree()
    adjustment_trees = {}
    for line in interval_bed_file:
        if line.startswith('#'):
            continue
        (dest_chrom, start_str, end_str, offset_str, src_chrom) = line.strip().split('\t')
        if src_chrom not in adjustment_trees:
            adjustment_trees[src_chrom] = {}
        if dest_chrom not in adjustment_trees[src_chrom]:
            adjustment_trees[src_chrom][dest_chrom] = IntervalTree()
            assert len(adjustment_trees[src_chrom]) == 1, "Error: currently only a single src chromosome to destination chromosome mapping is supported"
        start = int(start_str)
        end = int(end_str)
        offset = int(offset_str)
        interval = Interval(start, end, offset)
        adjustment_trees[src_chrom][dest_chrom].add(interval)
    return adjustment_trees

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('vcf_input', type=argparse.FileType())
    parser.add_argument('bed_input', type=argparse.FileType())
    parser.add_argument('vcf_output', type=argparse.FileType('w'), nargs='?', default=sys.stdout)
    args = parser.parse_args()

    
    adjustment_trees = read_intervals(args.bed_input)
    for line in args.vcf_input:
        if line.startswith('#'):
            args.vcf_output.write(line)
            continue
        fields = line.split('\t')
        src_chrom = fields[0]
        (dest_chrom, adjustment_intervals) = list(adjustment_trees[src_chrom].items())[0]  # we ensure that there is only one item by the assert above
        pos = int(fields[1]) - 1  # VCF is 1-based, BED is 0-based
        if adjustment_intervals.overlaps(pos):
            intervals = list(adjustment_intervals[pos])
            assert len(intervals) == 1
            offset = intervals[0].data
            pos += offset
        # VCF is in one-based coordinates so add 1
        pos += 1
        fields[0] = dest_chrom
        fields[1] = str(pos)
        args.vcf_output.write('\t'.join(fields))
