import filecmp
import os
from StringIO import StringIO

from bt_flor.gtf_writer import GTF
from test_base import TestBase


class TestGTF(TestBase):
    def test_create_index_known_gtf_file(self):
        # gtf_output = os.path.join('..', 'tests', 'input-data', 'gtf-output-small.gtf')
        gtf_output = StringIO()
        known_sorted_gtf_file = os.path.join('..', 'integration_tests', 'input-data', 'mm10-iGenome-sorted-small.gtf')
        known_sorted_gtf_file_gz = os.path.join('..', 'integration_tests', 'input-data',
                                                'mm10-iGenome-sorted-small-input-test.gtf.gz')
        known_sorted_gtf_file_gz_tbi = os.path.join('..', 'integration_tests', 'input-data',
                                                    'mm10-iGenome-sorted-small.gtf.gz.tbi')
        known_sorted_gtf_file_gz_output_test = os.path.join('..', 'integration_tests', 'input-data',
                                                            'mm10-iGenome-sorted-small-input-test.gtf.gz')
        known_sorted_gtf_file_gz_tbi_output_test = os.path.join('..', 'integration_tests', 'input-data',
                                                                'mm10-iGenome-sorted-small.gtf.gz.tbi')
        gtf_writer = GTF(gtf_output_file_fha=gtf_output, known_sorted_gtf_file=known_sorted_gtf_file)
        gtf_writer.create_index_known_gtf_file(force=True)
        # self.assertTrue(filecmp.cmp(known_sorted_gtf_file_gz, known_sorted_gtf_file_gz_output_test, shallow=False))
        # self.assertTrue(
        #     filecmp.cmp(known_sorted_gtf_file_gz_tbi, known_sorted_gtf_file_gz_tbi_output_test, shallow=False))
    #
    # def test_find_intersection_in_gtf(self):
    #     pass
    #
    # def test_write_gtf(self):
    #     gtf_output = StringIO()
    #     gtf_writer = GTF(gtf_output_file_fha=gtf_output, known_sorted_gtf_file=None)
    #     transcripts_num = {((20, 30), (40, 50), (60, 70), (80, 90), (100, 110)): 3, ((20, 30), (100, 110)): 1}
    #     gtf_writer.write_gtf(transcripts_num=transcripts_num, chr='chr1', start_mapping_id=1, is_reverse=False,
    #                          is_stranded_protocol=False)
    #     print gtf_output.getvalue()
    #
    # def test_close(self):
    #     pass
