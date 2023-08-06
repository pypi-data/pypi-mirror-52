import logging
import os

import numpy as np
import pysam

logger = logging.getLogger(__name__)


class GTF(object):
    """
    Prints the gtf output file and compares it to known gtf file

    Args:
        gtf_output_file           (BinaryIO): file handler (append mode) of the output file
        known_sorted_gtf_file     (str): Full path to known gtf file
    """

    def __init__(self, gtf_output_file_chr, known_sorted_gtf_file=None):
        self.gtf_output_file_chr_fha = open(gtf_output_file_chr, 'w')
        self.known_sorted_gtf_file = known_sorted_gtf_file
        if self.known_sorted_gtf_file:
            self.known_sorted_gtf_file_ziped, self.known_sorted_gtf_file_index = self.create_index_known_gtf_file()
            self.tabixfile = pysam.TabixFile(self.known_sorted_gtf_file_ziped)

    def create_index_known_gtf_file(self, force=False):
        """
        Compress the known gtf file (required for creating index) and create index of known gtf file.
        Args:
            force   (bool): override output files (for tests)
        Returns:
            File name of index of known gtf file
        """
        known_sorted_gtf_file_ziped = self.known_sorted_gtf_file + '.gz'
        if not os.path.isfile(known_sorted_gtf_file_ziped) or force:
            try:
                pysam.tabix_compress(self.known_sorted_gtf_file, known_sorted_gtf_file_ziped, force=True)
            except Exception as e:
                raise Exception(e)
        else:
            logger.info('Don\'t create compress file %s, because the file already exists' % known_sorted_gtf_file_ziped)
        known_sorted_gtf_file_index = known_sorted_gtf_file_ziped + '.tbi'
        if not os.path.isfile(known_sorted_gtf_file_index) or force:
            try:
                pysam.tabix_index(known_sorted_gtf_file_ziped, preset='gff', force=True)  # return the file name
            except Exception as e:
                raise Exception(e)
        else:
            logger.info(
                'Don\'t create index file %s, because the file already exists' % known_sorted_gtf_file_index)

        return known_sorted_gtf_file_ziped, known_sorted_gtf_file_index

    def find_intersection_in_gtf(self, chr, start, end, strand):
        """
        Find intersection of the coordinate in known gtf file.
        Find the percent of the intersection with the known gtf file and return the known with the maximum overlapping
        percent.

        Args:
            chr                 (str): chromosome name of the new transcript
            start               (int): start coordinate of the new transcript
            end                 (int): end coordinate of the new transcript

        Returns:
            known_transcript    (str): Record in known gtf of the transcript with the maximum overlapping with the new
                                       transcript. Including: overlap_percent, start, end, feature, attributes
        """
        known_list = []
        try:
            for gtf in self.tabixfile.fetch(chr, start, end, parser=pysam.asGTF()):
                # percent of overlapping with the known gtf
                if strand != '.':
                    if gtf.strand != strand:
                        continue
                overlap_percent = 100 * float(
                    min(gtf.end - start, end - gtf.start, end - start, gtf.end - gtf.start)) / (end - start)
                known_list.append(
                    [overlap_percent, ' overlap_percent "%s%%"; # known_gtf \"%s %s %s %s\";' % (
                        overlap_percent, str(gtf.start), str(gtf.end),
                        str(gtf.feature), str(gtf.attributes).replace('"', '\''))])
        except ValueError:
            # logger.info('Cannot find the coordinates %s:%s-%s in known gtf file' %(chr, start, end))
            pass
        if not known_list:
            return ''
        return '\t'.join(max(known_list, key=lambda x: x[0])[1:])

    def write_gtf(self, transcripts_num, chr, transcript_id, is_reverse, is_stranded_protocol):
        """
        Print to gtf file the transcripts that start in the same (or close) position.
        In case of stranded protocol and it is reverse reads (on minus strand), the printing start from the highest
        coordingate toward the lowest.

        Args:
            transcripts_num         (dict of tuple of tuples (int, int): int):
                                        key: list of tuples that contains the coordinates of the exons [(start, end),(start, end)...]
                                        value: number of reads in this transcript

            chr                     (str): chromosome. for example: chr2
            transcript_id           (list of int): id of the transcript. it is list in order the value will be increment inside this function for each group of close reads.
            is_reverse              (bool): if the reads in transcript are reversed (not relevant for non-stranded protocol, then strand of reads can be mixed.
            is_stranded_protocol    (bool): if it is stranded protocol.
        """
        for transcript, reads_num in transcripts_num.items():
            transcript_id[0] += 1
            transcript_id_str = chr + '_' + str(transcript_id[0])
            transcript_id_str += ('-' if is_reverse else '+') if is_stranded_protocol else ''
            # Numpy refer to list of tuples (that is not numpy object) as one long list
            strand = ('-' if is_reverse else '+') if is_stranded_protocol else '.'
            start_transcript, end_transcript = np.min(transcript), np.max(transcript)
            # if is_reverse and is_stranded_protocol:
            #     start_transcript, end_transcript = np.max(transcript), np.min(transcript)
            trans_coordinates = chr + ':' + str(start_transcript) + '-' + str(end_transcript)
            transcript_line = [chr, 'BT_FLOR', 'transcript', str(start_transcript), str(end_transcript),
                               str(reads_num), strand, '.', 'transcript_id "%s"; reads_num "%s"; coordinates "%s"' % (
                                   transcript_id_str, str(reads_num), trans_coordinates)]
            if self.known_sorted_gtf_file:
                transcript_line[-1] += self.find_intersection_in_gtf(chr, start_transcript, end_transcript, strand)

            self.gtf_output_file_chr_fha.write('\t'.join(transcript_line) + '\n')
            for exon_number, (start, end) in enumerate(transcript):
                exon_coordinates = chr + ':' + str(start) + '-' + str(end)
                exon_line = [chr, 'BT_FLOR', 'exon', str(start), str(end), str(reads_num), strand, '.',
                             'transcript_id "%s"; reads_num "%s"; coordinates "%s"; exon_number "%s"' % (
                             transcript_id_str, str(reads_num), exon_coordinates, exon_number+1)]
                if self.known_sorted_gtf_file:
                    exon_line[-1] += self.find_intersection_in_gtf(chr, start, end, strand)
                self.gtf_output_file_chr_fha.write('\t'.join(exon_line) + '\n')

    # def write_gtf(self, transcripts_num, chr, start_mapping_id, is_reverse, is_stranded_protocol):
    #     """
    #     Print to gtf file the transcripts that start in the same (or close) position.
    #     In case of stranded protocol and it is reverse reads (on minus strand), the printing start from the highest
    #     coordingate toward the lowest.
    #
    #     Args:
    #         transcripts_num     (dict of tuple of tuples (int, int): int):
    #                                 key: list of tuples that contains the coordinates of the exons [(start, end),(start, end)...]
    #                                 value: number of reads in this transcript
    #
    #         chr                 (str): chromosome. for example: chr2
    #         start_mapping_id    (int): id of the "gene". Each group of reads that start in the same (or close) position get
    #                                    specific id.
    #         is_reverse              (bool): if the reads in transcript are reversed (not relevant for non-stranded protocol, then strand of reads can be mixed.
    #         is_stranded_protocol    (bool): if it is stranded protocol.
    #     """
    #     for transcript_id, (transcript, reads_num) in enumerate(transcripts_num.items()):
    #         # Numpy refer to list of tuples (that is not numpy object) as one long list
    #         strand = ('-' if is_reverse else '+') if is_stranded_protocol else '.'
    #         start_transcript, end_transcript = np.min(transcript), np.max(transcript)
    #         # if is_reverse and is_stranded_protocol:
    #         #     start_transcript, end_transcript = np.max(transcript), np.min(transcript)
    #         transcript_line = [chr, 'BT_FLOR', 'transcript', str(start_transcript), str(end_transcript),
    #                            str(reads_num), strand, '.',
    #                            'start_mapping_id:%s; transcript_id:%s_%s;' % (
    #                                chr + '_' + str(start_mapping_id+1), chr + '_' + str(start_mapping_id+1), transcript_id+1)]
    #         if self.known_sorted_gtf_file:
    #             transcript_line[-1] += self.find_intersection_in_gtf(chr, start_transcript, end_transcript, strand)
    #
    #         self.gtf_output_file_chr_fha.write('\t'.join(transcript_line) + '\n')
    #         for exon_number, (start, end) in enumerate(transcript):
    #             exon_line = [chr, 'BT_FLOR', 'exon', str(start), str(end), str(reads_num), strand, '.',
    #                          'start_mapping_id:%s; transcript_id:%s_%s; exon_number:%s;' % (
    #                              chr + '_' + str(start_mapping_id+1), chr + '_' + str(start_mapping_id+1), transcript_id+1, exon_number+1)]
    #             if self.known_sorted_gtf_file:
    #                 exon_line[-1] += self.find_intersection_in_gtf(chr, start, end, strand)
    #             self.gtf_output_file_chr_fha.write('\t'.join(exon_line) + '\n')

    def close(self):
        """
        Close the output file
        """
        self.gtf_output_file_chr_fha.close()
