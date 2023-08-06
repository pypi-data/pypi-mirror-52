from bt_flor.reads_with_closed_start_mapping import PositionAverage, ExternalPositionAverage
from unittests.test_base import TestBase


class TestPositionAverage(TestBase):
    def setUp(self):
        self.pos_ave = PositionAverage(max_dist_internal_edge_from_average=5, local_average_max_num_positions=10)
        self.pos_ave_ext_stranded = ExternalPositionAverage(max_dist_last_edge_from_average=20,
                                                            max_dist_first_edge_from_average=5,
                                                            local_average_max_num_positions=10,
                                                            is_stranded_protocol=True)
        self.pos_ave_ext_non_stranded = ExternalPositionAverage(max_dist_last_edge_from_average=20,
                                                                max_dist_first_edge_from_average=5,
                                                                local_average_max_num_positions=10,
                                                                is_stranded_protocol=False)

        def tearDown(self):
            pass

    def test_close_to(self):
        self.pos_ave.local_average = 10
        self.pos_ave._reads_names_in_pos = [self.build_read() for i in xrange(5)]
        self.assertEqual(self.pos_ave.close_to(coordinate=12, max_distance=2, is_reverse=False, is_internal_exon=True),
                         True)
        self.assertEqual(self.pos_ave.close_to(coordinate=8, max_distance=2, is_reverse=False, is_internal_exon=True),
                         True)
        self.assertEqual(self.pos_ave.close_to(coordinate=13, max_distance=2, is_reverse=False, is_internal_exon=True),
                         False)
        self.assertEqual(self.pos_ave.close_to(coordinate=7, max_distance=2, is_reverse=False, is_internal_exon=True),
                         False)
        self.pos_ave.local_average = None
        self.assertEqual(self.pos_ave.close_to(coordinate=7, max_distance=2, is_reverse=False, is_internal_exon=True),
                         True)

    def test_update_average_of_position(self):
        self.pos_ave._average = 10
        self.pos_ave.local_average = 10
        self.pos_ave._total_reads_in_pos = 5
        self.pos_ave.local_average_total_reads = 5
        self.pos_ave._reads_names_in_pos = [self.build_read() for i in xrange(5)]
        self.pos_ave.update_average_of_position(self.build_read(), 12)
        self.assertEqual(self.pos_ave.total_reads_in_pos, 6)
        self.assertEqual(self.pos_ave.local_average_total_reads, 6)
        self.assertAlmostEqual(self.pos_ave.average, 10.333, places=3)
        self.assertAlmostEqual(self.pos_ave.local_average, 10.333, places=3)
        self.pos_ave.update_average_of_position(self.build_read(), 20)
        self.pos_ave.update_average_of_position(self.build_read(), 20)
        self.pos_ave.update_average_of_position(self.build_read(), 20)
        self.pos_ave.update_average_of_position(self.build_read(), 20)
        self.pos_ave.update_average_of_position(self.build_read(), 20)
        self.assertEqual(self.pos_ave.total_reads_in_pos, 11)
        self.assertEqual(self.pos_ave.local_average_total_reads, 11)
        self.assertAlmostEqual(self.pos_ave.average, 14.727, places=3)
        self.assertAlmostEqual(self.pos_ave.local_average, 14.727, places=3)

    def test_int(self):
        self.pos_ave._average = 5.44444444444
        self.assertEqual(int(self.pos_ave), 5)

    def test_close_to_external_stranded(self):
        self.pos_ave_ext_stranded.local_average = 10
        # internal exon
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=12, max_distance=2, is_reverse=False, is_internal_exon=True),
            False)
        # is not reverse first read
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=8, max_distance=2, is_reverse=False, is_internal_exon=False),
            True)
        # is reverse first read
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=8, max_distance=2, is_reverse=True, is_internal_exon=False),
            True)
        # is NOT reverse after other reversed read
        self.pos_ave_ext_stranded.is_reverse = True
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=8, max_distance=2, is_reverse=False, is_internal_exon=False),
            False)
        # is reverse after other non reversed read
        self.pos_ave_ext_stranded.is_reverse = False
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=8, max_distance=2, is_reverse=True, is_internal_exon=False),
            False)

        # for all tests for now it is not reverse
        self.pos_ave_ext_stranded.is_reverse = False

        # No read before it - each read is close
        self.pos_ave_ext_stranded.local_average = None
        self.pos_ave_ext_stranded.average_include_last_exons = None
        self.assertEqual(self.pos_ave_ext_stranded.close_to(coordinate=10000, max_distance=0, is_reverse=False,
                                                            is_internal_exon=False), True)
        # no read before it, except end exon, determined by max_dist_last_edge_from_average=20
        self.pos_ave_ext_stranded.local_average = None
        self.pos_ave_ext_stranded.average_include_last_exons = 10
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=30, max_distance=0, is_reverse=False, is_internal_exon=False),
            True)
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=31, max_distance=0, is_reverse=False, is_internal_exon=False),
            False)

        # if it is not the first non-last exon, calculate the distance from local_average (not _average and not average_include_last_exons)
        self.pos_ave_ext_stranded._average = 10
        self.pos_ave_ext_stranded.local_average = 25
        self.pos_ave_ext_stranded.average_include_last_exons = 25
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=15, max_distance=5, is_reverse=False, is_internal_exon=False),
            False)
        self.assertEqual(
            self.pos_ave_ext_stranded.close_to(coordinate=30, max_distance=5, is_reverse=False, is_internal_exon=False),
            True)

    def test_close_to_external_non_stranded(self):
        self.pos_ave_ext_non_stranded.local_average = 10
        # is not reverse first read
        self.assertEqual(
            self.pos_ave_ext_non_stranded.close_to(coordinate=8, max_distance=2, is_reverse=False,
                                               is_internal_exon=False), True)
        # is reverse first read
        self.assertEqual(
            self.pos_ave_ext_non_stranded.close_to(coordinate=8, max_distance=2, is_reverse=True,
                                               is_internal_exon=False), True)
        # is NOT reverse after other reversed read
        self.pos_ave_ext_non_stranded.is_reverse = True
        self.assertEqual(
            self.pos_ave_ext_non_stranded.close_to(coordinate=8, max_distance=2, is_reverse=False,
                                               is_internal_exon=False), True)
        # is reverse after other non reversed read
        self.pos_ave_ext_non_stranded.is_reverse = False
        self.assertEqual(
            self.pos_ave_ext_non_stranded.close_to(coordinate=8, max_distance=2, is_reverse=True,
                                               is_internal_exon=False), True)


        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pycharm
        #Protect against deletion of slowing pych