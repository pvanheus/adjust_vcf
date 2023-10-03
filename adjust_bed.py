#!/usr/bin/env python3

import argparse
import sys

from intervaltree import IntervalTree

from adjust_vcf import read_intervals

def adjust_pos(adjustment_tree: IntervalTree, pos: int) -> int:
    if adjustment_tree.overlaps(pos):
            intervals = list(adjustment_tree[pos])
            assert len(intervals) == 1
            offset = intervals[0].data
            pos += offset
    return pos


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bed_input', type=argparse.FileType())
    parser.add_argument('tabular_input', type=argparse.FileType())
    parser.add_argument('bed_output', type=argparse.FileType('w'), nargs='?', default=sys.stdout)
    args = parser.parse_args()

    adjustment_trees = read_intervals(args.tabular_input)
    for line in args.bed_input:
        if line.startswith('#'):
            args.bed_output.write(line)
        
        fields = line.split('\t')
        (src_chrom, start_str, end_str) = fields[:3]
        start = int(start_str)
        end = int(end_str)
        if src_chrom not in adjustment_trees:
             print(f"Warning: {src_chrom} has no known adjustment offets", file=sys.stderr)
             args.bed_output.write(line)
             continue
        
        (dest_chrom, adjustment_tree) = list(adjustment_trees[src_chrom].items())[0]  # we ensure that there is only one item by the assert above
        start = max(adjust_pos(adjustment_tree, start), 0)
        end = adjust_pos(adjustment_tree, end)
        fields = [dest_chrom, str(start), str(end)] + fields[3:]
        args.bed_output.write('\t'.join(fields))
