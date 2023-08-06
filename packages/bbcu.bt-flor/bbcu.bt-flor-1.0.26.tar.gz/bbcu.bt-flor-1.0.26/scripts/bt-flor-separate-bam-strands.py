#!/usr/bin/env python

import argparse
import logging
import pysam
import os
from argparse import RawTextHelpFormatter, ArgumentDefaultsHelpFormatter

from bt_flor.split_bam import FilterBam, FilterAndSplitBam
from bt_flor.utils import config_logging

logger = logging.getLogger(__name__)


class myArgparserFormater(RawTextHelpFormatter, ArgumentDefaultsHelpFormatter):
    """
    RawTextHelpFormatter: can break lines in the help text, but don't print default values
    ArgumentDefaultsHelpFormatter: print default values, but don't break lines in the help text
    """
    pass


def pair(arg):
    # Custom type for argsparse
    return [x for x in arg.split(' ')]


def parse_args():
    help_txt = "Pre-process the input bam file"
    parser = argparse.ArgumentParser(description=help_txt, formatter_class=myArgparserFormater)

    parser.add_argument('--input-file', help='Full path to input .bam or .sam file', required=True)
    parser.add_argument('--min-mapq', help='Minimum quality of the read mapping', type=int, default=10, required=False)
    parser.add_argument('--max-gene-length',
                        help='Maximum length of the gene. Reads that will be mapped to longer \nbases will be discarded',
                        type=int, default=100000, required=False)
    parser.add_argument('--filter-cigar', help='Filter out reads with these characters in the cigar.\n'
                                               'For example:\n'
                                               'DSHI - filter reads with deletion/insertion/softclipped/hardclipped',
                        type=str, default='', required=False)
    parser.add_argument('--filter-tags',
                        metavar=('TAG_NAME,VALUE TAG_NAME,VALUE ...'),
                        help='Filter out the reads that contain the substring in the value of the tag.\n'
                             'For example:\n'
                             '--filter-tags XF,__\n'
                             'filter out reads with "__" in value of XF tag\n'
                             '(htseq-count indicate that the read mapped to non-genomic region)',
                        type=pair, nargs='+', default=None, required=False)
    parser.add_argument('--is-stranded-protocol', help='Is stranded protocol', action='store_true')
    parser.add_argument('--log-file', help='Log File', default=None, required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logging_args = {
        "level": logging.DEBUG,
        "filemode": 'w',
        "format": '%(asctime)s %(message)s',
        "datefmt": '%m/%d/%Y %H:%M:%S'
    }

    # set up log file
    if args.log_file is not None:
        logging_args["filename"] = args.logFile
    logging.basicConfig(**logging_args)


    if args.input_file.endswith('bam'): #bam file (not sam)
        if not os.path.exists(args.input_file + '.bai'):
            logger.info('The index file %s don\'t exists, creating the file ...' % args.input_file + '.bai')
            pysam.index(args.input_file)
            logger.info('Finished to create the index file: %s' %args.input_file + '.bai')

    logging.info('Starting process bam file')

    config_logging(args.log_file)
    if args.is_stranded_protocol:
        output_bam_minus = os.path.splitext(args.input_file)[0] + '-filtred-minus.bam'
        output_bam_plus = os.path.splitext(args.input_file)[0] + '-filtred-plus.bam'
        # if os.path.exists(output_bam_minus):
        #     raise IOError('The output file already exists: %s' % output_bam_minus)
        # if os.path.exists(output_bam_plus):
        #     raise IOError('The output file already exists: %s' % output_bam_plus)
        FilterAndSplitBam(args.input_file, args.min_mapq, args.max_gene_length,
                          args.filter_cigar, args.filter_tags).filter_and_split(output_bam_plus, output_bam_minus)
    else:
        output_bam = os.path.splitext(args.input_file)[0] + '-filtred.bam'
        if os.path.exists(output_bam):
            raise IOError('The output file already exists: %s' % output_bam)
        FilterBam(args.input_file, args.min_mapq, args.max_gene_length, args.filter_cigar, args.filter_tags).filter(output_bam)

    logging.info('The program has been completed')

# TODO:
"""
#Run on sura:

python setup.py sdist; pip install dist/bbcu.bt-flor-1.0.4.tar.gz; bt-flor-separate-bam-strands.py --input-file integration_tests/input-data-bigfiles/Undiff_RNA2_pass_trim.bam
python setup.py sdist; pip install dist/bbcu.bt-flor-1.0.4.tar.gz; bt-flor-separate-bam-strands.py --input-file integration_tests/input-data-bigfiles/Undiff_RNA2_pass_trim.bam --is-stranded-protocol

Pre-run commands:
#sam file:
samtools sort input_file.bam > input_file_sorted.bam
samtools index input_file_sorted.bam


#Run on bio:
cp /shareDB/iGenomes/Mus_musculus/UCSC/mm10/Annotation/Genes/genes.gtf mm10-iGenome.gtf
module load bedtools
bedtools sort -i mm10-iGenome.gtf > mm10-iGenome-sorted.gtf

#Run tests:
cd /data/users/pmrefael/workspace/bt_flor/bt_flor # must to go to folder of tests
python -m unittest -v
python -m unittest -v test_buildTranscripts

etc...


Installation:
=============
conda create -n btflor python=2.7
conda config --add channels r
conda config --add channels bioconda
conda install pysam
pip install bbcu.bt-flor
"""

# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
# protect pycharm deletion
