#!/usr/bin/env python

import argparse
import logging
import pysam
import os
from argparse import RawTextHelpFormatter, ArgumentDefaultsHelpFormatter

logger = logging.getLogger(__name__)

from bt_flor.bam_reader import BamWriter, BamReader


class myArgparserFormater(RawTextHelpFormatter, ArgumentDefaultsHelpFormatter):
    """
    RawTextHelpFormatter: can break lines in the help text, but don't print default values
    ArgumentDefaultsHelpFormatter: print default values, but don't break lines in the help text
    """
    pass


def parse_args():
    help_txt = "Fetch reads from bam file in specific area to output of bam file"
    parser = argparse.ArgumentParser(description=help_txt, formatter_class=myArgparserFormater)

    parser.add_argument('--bam-input', help='Full path to input .bam or .sam file', required=True)
    parser.add_argument('--bam-output', help='Full path to output bam file name', required=True)
    parser.add_argument('--chr', help='Name of the chromosom', type=str, required=True)
    parser.add_argument('--start', help='Start coordinamt', type=int, required=True)
    parser.add_argument('--end', help='End coordinamt', type=int, required=True)
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

    reader = BamReader(args.bam_input)
    writer = BamWriter(args.bam_output, args.bam_input)
    for read in reader.read(args.chr, args.start, args.end):
        writer.write(read)
    pysam.index(args.bam_output)
    if not os.path.isfile(args.bam_output + ".bai"):
        raise RuntimeError("samtools index failed, likely bam is not sorted")

    logging.info('Program finished')
