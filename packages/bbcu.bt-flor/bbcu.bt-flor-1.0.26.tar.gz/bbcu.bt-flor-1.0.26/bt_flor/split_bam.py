import os

import pysam

from bt_flor.bam_reader import BamReader, BamWriter


class CareBam(object):
    def __init__(self, input_bam, min_mapq, max_gene_length, filter_cigar, filter_tags):
        self.input_bam = input_bam
        self.bam_reader = BamReader(self.input_bam, min_mapq, max_gene_length, filter_cigar, filter_tags)

    def create_bai_file(self, bam_file):
        pysam.index(bam_file)
        if not os.path.isfile(bam_file + ".bai"):
            raise RuntimeError("samtools index failed, likely bam is not sorted")

class FilterBam(CareBam):
    def __init__(self, input_bam, min_mapq, max_gene_length, filter_cigar, filter_tags):
        super(FilterBam, self).__init__(input_bam, min_mapq, max_gene_length, filter_cigar, filter_tags)

    def write_new_reads(self, output_bam):
        bam_writer = BamWriter(output_bam, self.input_bam)
        for read in self.bam_reader.read():
            bam_writer.write(read)
        bam_writer.close_file()

    def filter(self, output_bam):
        self.write_new_reads(output_bam)
        self.create_bai_file(output_bam)


class FilterAndSplitBam(CareBam):
    def __init__(self, input_bam, min_mapq, max_gene_length, filter_cigar, filter_tags):
        super(FilterAndSplitBam, self).__init__(input_bam, min_mapq, max_gene_length, filter_cigar, filter_tags)

    def write_new_reads_split(self, output_bam_plus, output_bam_minus):
        bam_writer_minus = BamWriter(output_bam_minus, self.input_bam)
        bam_writer_plus = BamWriter(output_bam_plus, self.input_bam)
        for read in self.bam_reader.read():
            if not read.is_reverse:
                bam_writer_plus.write(read)
            else:
                bam_writer_minus.write(read)
        bam_writer_plus.close_file()
        bam_writer_minus.close_file()

    def filter_and_split(self, output_bam_plus, output_bam_minus):
        self.write_new_reads_split(output_bam_plus, output_bam_minus)
        self.create_bai_file(output_bam_plus)
        self.create_bai_file(output_bam_minus)

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
