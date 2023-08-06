from bt_flor.build_transcripts import BuildTranscripts
from unittests.test_base import TestBase


class TestBuildTranscripts(TestBase):
    def setUp(self):
        self.build_trans = BuildTranscripts(input_file=None, gtf_output_file_fha=None, max_dist_internal_edge_from_average=None,
                                            max_dist_first_edge_from_average=None,
                                            max_dist_last_edge_from_average=None,
                                            local_average_max_num_positions=None,
                                            is_stranded_protocol=True,
                                            known_sorted_gtf_file=None, run_in_parallel=False)

    def tearDown(self):
        pass

    def test_run(self):
        pass

    def test_get_exons_start_end_coordinates(self):
        read = self.build_read()
        read.cigartuples = ((0, 10), (2, 1), (0, 9), (1, 1), (0, 20))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0], [40]))
        read.cigartuples = ((0, 10), (3, 11), (0, 20))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0, 21], [10, 41]))
        read.cigartuples = ((0, 2), (2, 2), (0, 2), (1, 2), (0, 2))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0], [8]))
        read.cigartuples = ((0, 2), (3, 2), (0, 2))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0, 4], [2, 6]))
        read.cigartuples = ((0, 1), (2, 1), (0, 1), (1, 1), (0, 1))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0], [4]))
        read.cigartuples = ((0, 1), (3, 1), (0, 1))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0, 2], [1, 3]))
        read.cigartuples = ((0, 1), (3, 1), (0, 1), (2, 1))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0, 2], [1, 3]))
        read.cigartuples = ((0, 1), (3, 1), (0, 1), (2, 1), (0, 1))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0, 2], [1, 5]))
        read.cigartuples = ((0, 1), (3, 1), (0, 1), (1, 1), (0, 1))  # Combine 2 matches with instersion and deletions
        self.assertEqual(self.build_trans.get_exons_start_end_coordinates(read), ([0, 2], [1, 4]))

    def test_cigar_next_match(self):
        cigar = ((4, 3), (0, 4))  # '3S4M' (type of block, number of bases in the block)
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 4), [4])])
        cigar = ((0, 4),)  # '4M'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 4), [])])
        cigar = ((0, 4), (1, 3))  # '4M3I'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 4), [])])
        cigar = ((0, 3), (0, 4))  # '3M4M'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 3), []), ((0, 4), [])])
        cigar = ((0, 3), (0, 4), (1, 3))  # '3M4M3I'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 3), []), ((0, 4), [])])
        cigar = ((4, 3), (1, 4), (0, 5))  # '3S4I5M'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 5), [4, 1])])
        cigar = ((4, 3), (1, 4), (0, 5), (0, 4))  # '3S4I5M4M'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)), [((0, 5), [4, 1]), ((0, 4), [])])
        cigar = ((4, 3), (1, 4), (0, 5), (0, 4), (2, 3), (0, 3))  # '3S4I5M4M3D3M'
        self.assertEqual(list(self.build_trans.cigar_next_match(cigar=cigar)),
                         [((0, 5), [4, 1]), ((0, 4), []), ((0, 3), [2])])
