# seqdataloader
Sequence data label generation and ingestion into deep learning models

## Installation
`pip install seqdataloader`

If you plan to modify the code, you can install it in development mode: 
`pip install -e seqdataloader` 

## Quick Start

tasks.tsv is a 4 column tab-delimited file

Column 1 -- User-specified task name

Column 2 -- path to narrowPeak file (optional if Column 3 is specified)

Column 3 -- path to bigwig file (optional if Column 2 is specified)

Column 4 -- bed file containing user-specified regions to label as ambiguous (i.e. "blacklist")

```
genomewide_labels --task_list tasks.tsv \
		  --outf classificationlabels.SummitWithin200bpCenter.tsv.gz \
		  --output_type gzip \ # (one of gzip, bz2, hdf5, pkl) 
		  --chrom_sizes hg38.chrom.sizes \
		  --bin_stride 50 \
		  --left_flank 400 \
		  --right_flank 400 \
		  --bin_size 200 \
		  --task_hreads 10 \
		  --chrom_threads 4 \
		  --allow_ambiguous \
		  --labeling_approach peak_summit_in_bin_classification 
```
And for regression: 
```
genomewide_labels --task_list tasks.tsv \
       --outf regressionlabels.allbins.hg38.hdf5 \
       --output_type hdf5 \
       --chrom_sizes hg38.chrom.sizes \
       --bin_stride 50 \
       --left_flank 400 \
       --right_flank 400 \
       --chrom_threads 24 \
       --task_threads 2 \
       --label_transformer asinh \ one of None, asinh, log10, log, default is asinh 
       --labeling_approach all_genome_bins_regression
```

labeling_approach can be one of:

    "peak_summit_in_bin_classification"

    "peak_percent_overlap_with_bin_classification"

    "peak_summit_in_bin_regression"

    "peak_percent_overlap_with_bin_regression"
    
    "all_genome_bins_regression"
    

## How to run 
Sample datasets are included in the folder `examples/peak_files_from_encode_for_label_comparison` and `examples/bigwig_files_from_encode_for_label_comparison`

### Executing seqdataloader as a script: 
Execute the script:

`examples/genomewide_labels.sh` for examples on how to generate classification and regression labels on sample datasets.
The script generates binary classification labels (1,0,-1 for ambiguous) or continuous regression labels reflective of bigWig coverage in a bin  in bed file format:

http://mitra.stanford.edu/kundaje/seqdataloader/classificationlabels.50PercentOverlap.tsv.gz

http://mitra.stanford.edu/kundaje/seqdataloader/classificationlabels.SummitWithin200bpCenter.tsv.gz

http://mitra.stanford.edu/kundaje/seqdataloader/regressionlabels.50PercentOverlap.tsv.gz

http://mitra.stanford.edu/kundaje/seqdataloader/regressionlabels.SummitWithin200bpCenter.tsv.gz

Corresponding WashU Browser Tracks with optimal narrowPeak and associated bin labels are here:
http://epigenomegateway.wustl.edu/legacy/?genome=hg38&session=GDB2BTMGnB&statusId=1154897038

### calling seqdataloader as a Python function: 
```
from seqdataloader import *
classification_params={
    'task_list':"tasks.tsv",
    'outf':"classificationlabels.SummitWithin200bpCenter.tsv.gz",
    'output_type':'gzip',
    'chrom_sizes':'hg38.chrom.sizes',
    'chroms_to_keep':['chr21'],
    "store_positives_only":True,
    'bin_stride':50,
    'left_flank':400,
    'right_flank':400,
    'bin_size':200,
    'chrom_threads':10,
    'task_threads':4,
    'allow_ambiguous':True,
    'labeling_approach':'peak_summit_in_bin_classification'
    }
genomewide_labels(classification_params)

regression_params={
    'task_list':"tasks.tsv",
    'outf':"regressionlabels.all_genome_bins_regression.hdf5",
    'output_type':'hdf5',
    'chrom_sizes':'hg38.chrom.sizes',
    'store_values_above_thresh': 0,
    'chroms_to_keep':['chr21'],
    'bin_stride':50,
    'left_flank':400,
    'right_flank':400,
    'bin_size':200,
    'chrom_threads':10,
    'task_threads':4,
    'labeling_approach':'all_genome_bins_regression',
    'label_transformer':'log10',
    'label_transfomer_pseudocount':0.001
    }
genomewide_labels(regression_params)
```


## Dependencies

Please make sure the following dependencies are installed on your system to use SeqDataLoader:
* pybedtools
* pyBigWig 
* pandas
* numpy
* multiprocessing

## Regression label transformations 

In regression mode (   "peak_summit_in_bin_regression", "peak_percent_overlap_with_bin_regression", "all_genome_bins_regression"), the generated labels can be transformed in one of several ways. You can use the arguments `label_transformer` and `label_transformer_pseudocount` to specify the desired tranformation. Allowed values are: 

* asinh --  numpy.arcsinh(values) will be computed (this is the default) 
* None -- no label transformation will be performed 
* log10 --  numpy.log10(values + pseudocount) will be computed using a pseudocount specified by `label_transformer_pseudocount` argument. If this argument is not provided,a default pseudocout of 0.001 is used. 
* log -- numpy.log(values + pseudocount) will be computed using a pseudcount as above. 

## A note on file outputs

The code supports several output types: `hdf5`, `gzip`, `pkl`, `bz2`.
Specify your desired output type with the flag `--output_type`. The default setting for this flag is `gzip`
Please note that the large bottleneck in the code is writing the files to disk. `hdf5` has negligible overhead, but using `gzip` or `bz2` may increase runtime. Timining benchmarks are provided in `examples/genomewide_labels.sh`

You may speed up i/o by writing chromosome outputs to separate files in parallel. This is currently only supported for the `gzip` and `bz2` output types, as i/o is less of a bottleneck for `hdf5` and `pkl` output formats. Use the flag `--split_output_by_chrom` to invoke this parallelized saving of chromosomes.

## Documentation and benchmarks

Testing, benchmarks, and documentation can be found in the `docs` folder
