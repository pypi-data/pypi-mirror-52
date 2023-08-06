import logging
import re
import sys

import pysam

logger = logging.getLogger(__name__)


class BamReader(object):
    """
    Read bam input file sorted by coordinates. Read the records of one chromosom.

    Args:
        bam_input                   (str): path to input file (bam format sorted by coordinates). Must to be bam.bai file in the same folder
        min_mapq            (int): Minimum quality of the read mapping
        max_gene_length     (int): Maximum length of the gene. Reads that will be mapped to longer bases will be discarded
        filter_cigar        (str): Filter out reads with these characters in the cigar.
                                   for exaple: DSHI - filter reads with deletion/insertion/softclipped/hardclipped
        filter_tags        (list of lists of (str, str)): list of tuples that contain tag and substring.
                                   Filter out the reads that contain the substring in the value of the tag.
                                   For example: [('XF', '__')] - filter out reads with '__' in value of XF tag
                                   (htseq-count indicate that the read mapped to non-genomic region).

    Attributes:
        prev_sam_record             (pysam.AlignedSegment object): save the previous read

    """

    def __init__(self, bam_input, min_mapq=0, max_gene_length=sys.maxsize, filter_cigar='', filter_tags=None):
        self.bam_input = bam_input
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
        self.filter_cigar = filter_cigar
        self.filter_tags = filter_tags
        if not self.filter_cigar:
            self.filter_cigar = '\'\''
        self.bam_reader = pysam.AlignmentFile(self.bam_input, "rb")
        self.prev_sam_record = None

    def close_file(self):
        self.bam_reader.close()

    @staticmethod
    def get_chr_list(bam_input):
        """
        Get the list of chromosoms from the header lines of the bam file
        Also check that the file is sorted by coordinates

        Args:
            bam_input    (str): path of the input file

        Returns:
            chrs_list    (list of str): list of chromosoms
        """

        bam_reader = pysam.AlignmentFile(bam_input, "rb")
        chrs_list = []

        try:
            if bam_reader.header['HD']['SO'] != "coordinate":
                raise ValueError("Bam is not sorted by coordinate")
            for line in bam_reader.header['SQ']:
                chrs_list.append(line['SN'])
        except Exception:
            raise IOError(
                "The bam file don't contain header lines with information on the chromosomes. Maybe you forgot use in -h parameter when you convert sam file to bam with samtools ? ")
        return chrs_list

    def read(self, chr=None, start=None, end=None):
        """
        - Get the reads from input file for specific chromosome.
        - Filter reads according self.min_mapq and self.max_gene_length

        Args:
            chr             (str): the name of the chromosome

        Returns:
            read            (iterator of pysam.AlignedSegment object): iterator for reads
        """

        logger.info("Start to read alignments from %s" %(chr if chr else 'all chromosomes)'))

        for alignment in self.bam_reader.fetch(contig=chr, start=start, end=end):
            if self.filter_record(alignment):
                continue
            self.prev_sam_record = alignment  # not in use
            yield alignment
        self.close_file()

    def filter_record(self, record):
        """
        Args:
            record              (pysam.AlignedSegment object): one read

        Returns:
            filtered            (bool): True if filtered out, else False
        """
        if re.findall(r"([%s]+)" % self.filter_cigar, record.cigarstring):
            return True
        if self.filter_tags:
            for tag, value in self.filter_tags:
                if value in record.get_tag(tag):
                    return True
        if record.mapping_quality < self.min_mapq:  # Mapq 10 and above is uniquely mapped
            return True
        if record.reference_length > self.max_gene_length:
            return True
        else:
            return False



class BamWriter(object):
    """
    Read bam input file sorted by coordinates. Read the records of one chromosom.

    Args:
        bam_output          (str): path to output file.

    """

    def __init__(self, bam_output, bam_input):
        self.bam_input = bam_input
        bam_input_template = pysam.AlignmentFile(self.bam_input, 'rb')
        self.bam_output = bam_output
        self.bam_writer = pysam.AlignmentFile(self.bam_output, "wb", template=bam_input_template)

    def write(self, read):
        self.bam_writer.write(read)

    def close_file(self):
        self.bam_writer.close()



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
