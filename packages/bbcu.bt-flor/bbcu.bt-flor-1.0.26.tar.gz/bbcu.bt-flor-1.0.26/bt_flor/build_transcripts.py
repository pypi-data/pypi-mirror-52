import os
import shutil
import random
import string
import logging
from multiprocessing import Process

from bt_flor.bam_reader import BamReader
from bt_flor.gtf_writer import GTF
from bt_flor.reads_with_closed_start_mapping import ReadsWithCloseStartMapping

logger = logging.getLogger(__name__)



class BuildTranscripts(object):
    """
    Main class for building transcripts:
    - Iterates on chromosomes separately in parallel (optionaly)
    - Builds the transcripts.
    - Print GTF file

    Args:
        input_file                                  (str): Full path to sam or bam file (if bam file, bai file must be exists in the same folder)
        gtf_output_file_fha                         (BinaryIO): file handler (append mode) of the output file
        max_dist_internal_edge_from_average                  (int): maximum distance of position of exon from the average
        max_dist_first_edge_from_average      (int): maximum distance of position of first exon from the average
        max_dist_last_edge_from_average         (int): maximum distance of position of end of last exon from the average
        local_average_max_num_positions             (int): maximum number of positions for calculate the average.
        is_stranded_protocol                        (bool): is stranded portocol or not
        known_sorted_gtf_file                       (str): Optional. If you want to compare the output to known genes
        run_in_parallel                             (bool): Run each chromosome in parallel or not

    Attributes:
        chr_list                            (list of str): list of chromosomes names. Initialized in run function for enable run test without input_folder)

    """

    def __init__(self, input_file, gtf_output_file, max_dist_internal_edge_from_average,
                 max_dist_first_edge_from_average, max_dist_last_edge_from_average,
                 local_average_max_num_positions, is_stranded_protocol, known_sorted_gtf_file=None,
                 threads=1):
        self.input_file = input_file
        self.gtf_output_file = gtf_output_file
        self.max_dist_internal_edge_from_average = max_dist_internal_edge_from_average
        self.max_dist_first_edge_from_average = max_dist_first_edge_from_average
        self.max_dist_last_edge_from_average = max_dist_last_edge_from_average
        self.local_average_max_num_positions = local_average_max_num_positions
        self.is_stranded_protocol = is_stranded_protocol
        self.known_sorted_gtf_file = known_sorted_gtf_file
        self.threads = threads

    def create_transcripts_per_chrom(self, chr, gtf_output_file_chr):
        gtf = GTF(gtf_output_file_chr, self.known_sorted_gtf_file)
        bam_reader = BamReader(self.input_file)
        transcript_id = [0]
        close_reads = ReadsWithCloseStartMapping(self.max_dist_internal_edge_from_average,
                                                 self.max_dist_first_edge_from_average,
                                                 self.max_dist_last_edge_from_average,
                                                 self.local_average_max_num_positions,
                                                 self.is_stranded_protocol)
        for alignment in bam_reader.read(chr=chr):
            read_start_positions, read_end_positions = self.get_exons_start_end_coordinates(alignment)
            # Try to add the read to ReadsWithCloseStartMapping object. If return False (the read is far away from
            # the average start mapping of the ReadsWithCloseStartMapping object, start a new transcript, and build
            # and print the previous transcript.
            if not close_reads.add_read(alignment, read_start_positions, read_end_positions):
                transcripts_num, transcripts_reads, is_reverse = close_reads.build_transcripts()
                gtf.write_gtf(transcripts_num, chr, transcript_id, is_reverse, self.is_stranded_protocol)
                close_reads = ReadsWithCloseStartMapping(self.max_dist_internal_edge_from_average,
                                                         self.max_dist_first_edge_from_average,
                                                         self.max_dist_last_edge_from_average,
                                                         self.local_average_max_num_positions,
                                                         self.is_stranded_protocol)

                close_reads.add_read(alignment, read_start_positions, read_end_positions)
        # for the last alignment in the chromosome.
        transcripts_num, transcripts_reads, is_reverse = close_reads.build_transcripts()
        gtf.write_gtf(transcripts_num, chr, transcript_id, is_reverse, self.is_stranded_protocol)
        gtf.close()

    def combine_gtf_of_chrom(self, chr_list, gtf_output_files_chr):
        with open(self.gtf_output_file, 'w') as gtf_out:
            for file in gtf_output_files_chr:
                with open(file, 'r') as fd:
                    shutil.copyfileobj(fd, gtf_out)
            for file in gtf_output_files_chr:
                os.remove(file)

    def chunks(self, l, n):
        """
        Deny to run on more than maximum number of threads that user determined.
        """
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def run(self):
        chr_list = BamReader.get_chr_list(self.input_file)
        if self.threads < len(chr_list):
            logger.info('You run only %s threads, you can run until %s processes in parallel (as the number of the chromosoms)' %(self.threads, len(chr_list)))
        if self.threads > len(chr_list):
            logger.info('The program run only %s threads, you can run until %s processes in parallel (as the number of the chromosoms)' %(len(chr_list), self.threads))

        processes = []
        gtf_output_files_chr = []
        for chr in chr_list:
            gtf_output_file_chr = self.gtf_output_file + '_' + chr + '_' + ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            gtf_output_files_chr.append(gtf_output_file_chr)
            p = Process(target=self.create_transcripts_per_chrom, args=(chr, gtf_output_file_chr))
            processes.append(p)
        for p_chunk in self.chunks(processes, self.threads):
            for p in p_chunk:
                p.start()
            for p in p_chunk:
                p.join()
        self.combine_gtf_of_chrom(chr_list, gtf_output_files_chr)

    def get_exons_start_end_coordinates(self, read):
        """
        - Extract the a list of start and end positions of aligned gapless blocks with get_blocks() function (M - match blocks).
        - Combine the adjacent blocks to one (of two matches with insertion or deletion between them (See get_block documentation:
          https://buildmedia.readthedocs.org/media/pdf/pysam/latest/pysam.pdf)

        Args:
            read:                                         (pysam.AlignedSegment object): one read from the input file

        Returns:
            (read_start_positions, read_end_positions)    (tuple of 2 lists: int): list of start positions of the exons
                                                                                   and another list of their end
                                                                                   positions
        """
        exons_blocks = read.get_blocks()
        read_start_positions = []
        read_end_positions = []
        cigar = list(read.cigartuples)
        match_blocks = self.cigar_next_match(cigar)
        for start, end in exons_blocks:
            block_match, block_types = match_blocks.next()
            # if an intron (N) exists before this block, this is a new exon, or it is the first block
            if 3 in block_types or not read_end_positions:
                read_start_positions.append(start)
                read_end_positions.append(end)
            else:  # if insertion (I) or deletion (D) or other types: combine 2 adjacent blocks with insersion between them.
                read_end_positions[-1] = end
        return (read_start_positions, read_end_positions)

    def cigar_next_match(self, cigar):
        """
        Remove from the start of cigar the blocks that are not Match (M), such that the first item in cigar will be
        Match.

        M	BAM_CMATCH	0
        I	BAM_CINS	1
        D	BAM_CDEL	2
        N	BAM_CREF_SKIP	3
        S	BAM_CSOFT_CLIP	4
        H	BAM_CHARD_CLIP	5
        P	BAM_CPAD	6
        =	BAM_CEQUAL	7
        X	BAM_CDIFF	8
        B	BAM_CBACK	9

        Args:
            cigar      (list of tuples of (int,int)): item in list contain block that represented by tuple:
                                                first item in tuple is block type, and second is number of bases

        Returns:
            (cigar, block_types)    (tuple of (cigar, list)): the list contains the skipped block types
        """
        block_types = []
        # In end of while, the first item in cigar will be Match (M), that corresponding to current block
        for block in cigar:
            if block[0] == 0:
                yield (block, block_types)
                block_types = []
            else:
                block_types.append(block[0])
