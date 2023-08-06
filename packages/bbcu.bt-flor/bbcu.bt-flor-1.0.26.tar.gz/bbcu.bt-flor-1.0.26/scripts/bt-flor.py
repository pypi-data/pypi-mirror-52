#!/usr/bin/env python

import argparse
import logging
import pysam
import os
from argparse import RawTextHelpFormatter, ArgumentDefaultsHelpFormatter

from bt_flor.build_transcripts import BuildTranscripts
from bt_flor.utils import config_logging

logger = logging.getLogger(__name__)


class myArgparserFormater(RawTextHelpFormatter, ArgumentDefaultsHelpFormatter):
    """
    RawTextHelpFormatter: can break lines in the help text, but don't print default values
    ArgumentDefaultsHelpFormatter: print default values, but don't break lines in the help text
    """
    pass


def parse_args():
    help_txt = "Acurate assembly of transcripts according mapped reads"
    parser = argparse.ArgumentParser(description=help_txt, formatter_class=myArgparserFormater)

    parser.add_argument('--input-file', help='Full path to input .bam or .sam file', required=True)
    parser.add_argument('--gtf-output-file', help='Full path to output file name', required=True)
    parser.add_argument('--is-stranded-protocol', help='Is stranded protocol', action='store_true')
    parser.add_argument('--max-dist-internal-edge-from-average',
                        help='Maximum distance between reads in start and end of the internal exons of the \n'
                             'trancript (except the start of the first exon and end of the last exon)',
                        type=int, default=3, required=False)
    parser.add_argument('--max-dist-external-edge-from-average',
                        help='For non-stranded protocol: maximum distance between reads in start of the first \n'
                             'exon and the end of the last exon of the trancript',
                        type=int, default=3, required=False)
    parser.add_argument('--max-dist-first-edge-from-average',
                        help='For stranded protocol: maximum distance between reads in start of the first \n'
                             'exon of the trancript',
                        type=int, default=3, required=False)
    parser.add_argument('--max-dist-last-edge-from-average',
                        help='For stranded protocol: maximum distance between reads in end of the last exon \n'
                             'in the trancript (sometimes the enzyme drops before the end of the transcript)',
                        type=int, default=50, required=False)
    parser.add_argument('--local-average-max-num-positions',
                        help='Maximum neighbors positions for which the average will be calculated and the \n'
                             'distance from this average will be considered)',
                        type=int, default=5, required=False)
    parser.add_argument('--known-sorted-gtf-file',
                        help='Full path the known gtf file sorted by chromosome and then by start position \n'
                             'in ascending order (you can use the command: bedtools sort -i <gtf-file>).\n'
                             'The program will create *.gz (compressed) and *.gz.tbi (index) files in the \n'
                             'same location of the known-gtf-file if they don\'t exists.',
                        required=False)
    parser.add_argument('--threads',
                        help='number of threads. Each chromosome can run in parallel.',
                        type=int, default=1, required=False)
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

    logging.info('Program started')

    logger.info('Run with the parameters: %s' %args)

    # if os.path.exists(args.gtf_output_file):
    #     raise IOError('The output file already exists: %s' % args.gtf_output_file)

    if args.known_sorted_gtf_file:
        if not os.path.exists(args.known_sorted_gtf_file):
            raise IOError('The file %s don\'t exists' % args.known_sorted_gtf_file)
    else:
        logger.info('You did\'t supply known gtf file, the program will not find intersection with known gtf file.')

    if args.input_file.endswith('bam'): #bam file (not sam)
        if not os.path.exists(args.input_file + '.bai'):
            logger.info('The index file %s don\'t exists, creating the file ...' % args.input_file + '.bai')
            pysam.index(args.input_file)
            logger.info('Finished to create the index file: %s' %args.input_file + '.bai')

    config_logging(args.log_file)
    BuildTranscripts(args.input_file, args.gtf_output_file, args.max_dist_internal_edge_from_average,
                     args.max_dist_first_edge_from_average if args.is_stranded_protocol else args.max_dist_external_edge_from_average,
                     args.max_dist_last_edge_from_average if args.is_stranded_protocol else args.max_dist_external_edge_from_average,
                     args.local_average_max_num_positions, args.is_stranded_protocol,
                     args.known_sorted_gtf_file, args.threads).run()

    logging.info('The program has been completed')

"""
#Run on sura:
cd /data/users/pmrefael/workspace/bt_flor
# rm /data/users/pmrefael/workspace/bt_flor/tests/output-data/gtf-output.gtf; python  -m trace --timing --count -C . /data/users/pmrefael/workspace/bt_flor/bt_flor/main_bt_flor.py --input-file /data/users/pmrefael/workspace/bt_flor/tests/input-data/small.bam --gtf-output-file /data/users/pmrefael/workspace/bt_flor/tests/output-data/gtf-output.gtf --max-dist-exon-from-average 5 --max-dist-first-exon-from-average 5 --known-sorted-gtf-file /data/users/pmrefael/workspace/bt_flor/tests/input-data-bigfiles/Mus_musculus.GRCm38.96-sorted.gtf --is-stranded-protocol


starting run:
7/8/2019 4:37

python setup.py sdist; pip install dist/bbcu.bt-flor-1.0.8.tar.gz; bt-flor.py --input-file integration_tests/input-data-bigfiles/Undiff_RNA2_pass_trim-filtred.bam --gtf-output-file integration_tests/output-data/gtf-output.gtf --known-sorted-gtf-file integration_tests/input-data-bigfiles/mm10-iGenome-sorted.gtf --threads 30 &
python setup.py sdist; pip install dist/bbcu.bt-flor-1.0.8.tar.gz; bt-flor.py --input-file integration_tests/input-data-bigfiles/Undiff_RNA2_pass_trim-filtred.bam --gtf-output-file integration_tests/output-data/gtf-output-without-known-gtf.gtf --threads 30 &
python setup.py sdist; pip install dist/bbcu.bt-flor-1.0.8.tar.gz; bt-flor.py --input-file integration_tests/input-data-bigfiles/Undiff_RNA2_pass_trim-filtred-minus.bam --gtf-output-file integration_tests/output-data/gtf-output-minus.gtf --known-sorted-gtf-file integration_tests/input-data-bigfiles/mm10-iGenome-sorted.gtf --is-stranded-protocol --threads 30 &
python setup.py sdist; pip install dist/bbcu.bt-flor-1.0.8.tar.gz; bt-flor.py --input-file integration_tests/input-data-bigfiles/Undiff_RNA2_pass_trim-filtred-plus.bam --gtf-output-file integration_tests/output-data/gtf-output-plus.gtf --known-sorted-gtf-file integration_tests/input-data-bigfiles/mm10-iGenome-sorted.gtf --is-stranded-protocol --threads 30 &



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

"""
