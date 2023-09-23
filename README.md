# adjust_vcf

Scripts to adjust coordinates in VCF. The adjustements are specified in a tabular format file with the following files:

dest_chrom start_coord end_coord offset src_chrom

where:

* dest_chrom is the destination chromosome (or sequence) name
* start_coord is the starting coordinate of a block on the src chromosome
* end_coord is the ending coordinate (half-open, i.e. the base is not included) of a segment on the src chromosome
* offset is the offset to convert coordinates in this segment from src to destination coordinates
* src_chrom is the name of the src chromosome (or sequence)

An example of this format:

```
KR063671.1      0       18398   -1      DRCMAN2018REF
KR063671.1      18398   18620   0       DRCMAN2018REF
KR063671.1      18620   18958   -6      DRCMAN2018REF
```

The `psl_to_tabular.py` script computes this format output from [PSL format](http://www.ensembl.org/info/website/upload/psl.html) input.

The `adjust_vcf.py` uses the tabular format to convert VCF from src_chrom to dest_chrom. It is assumed that src_chrom to dest_chrom is a 1-to-1 mapping. This script requires the [intervaltree](https://github.com/chaimleib/intervaltree/tree/master) Python module.

*Note* that the tabular format uses 0-based half-open coordinates (base at start coordinate is included, base at end coordinate is excluded), whereas VCF uses 1-based coordinates.

These scripts are very rough and might contain bugs.
