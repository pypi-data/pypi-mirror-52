from bt_flor.reads_with_closed_start_mapping import ReadsWithCloseStartMapping
from test_base import TestBase


# class TestCurrent(TestBase):
#     def test_current(self):
#
# class EndCurrent(TestBase):
#     def end_current(self):
#
#

class TestReadsWithCloseStartMapping(TestBase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_len(self):
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=2,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.exons_start_positions = {self.build_read(name=str(i)): [20] for i in xrange(5)}
        self.assertEqual(len(closed_reads), 5)

    def test_add_read(self):
        """
        max_dist_first_edge_from_average=5

        |20   |25
        ---------- added (start: 20, average: 20)
        ---------- added (start: 20, average: 20)
              ---------- failed (start: 26, average: 20)
             ---------- added  (start: 25, average: 21.666)
               ---------- failed  (start: 27, average: 21.666)
              ---------- added (start: 26, average: 22.749)
        """
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        # Added success: for now the average in first start and end are None and None respectively.
        closed_reads.add_read(self.build_read(name='a'), [20], [30])
        self.assertEqual(len(closed_reads), 1)
        self.assertItemsEqual(closed_reads.exons_start_positions.values(), [[20]])
        self.assertItemsEqual(closed_reads.exons_end_positions.values(), [[30]])
        self.assertAlmostEqual(closed_reads.exons_start_average[0].average, 20, places=3)
        # Added success: for now the average in first start and end are 20 and 20 respectively.
        closed_reads.add_read(self.build_read(name='b'), [20], [30])
        self.assertEqual(len(closed_reads), 2)
        self.assertItemsEqual(closed_reads.exons_start_positions.values(), [[20], [20]])
        self.assertItemsEqual(closed_reads.exons_end_positions.values(), [[30], [30]])
        self.assertAlmostEqual(closed_reads.exons_start_average[0].average, 20, places=3)
        # Added failed: for now the average in first start and end are 20 and 30 respectively.
        closed_reads.add_read(self.build_read(name='c'), [26], [36])
        self.assertEqual(len(closed_reads), 2)
        self.assertItemsEqual(closed_reads.exons_start_positions.values(), [[20], [20]])
        self.assertItemsEqual(closed_reads.exons_end_positions.values(), [[30], [30]])
        self.assertAlmostEqual(closed_reads.exons_start_average[0].average, 20, places=3)
        # Added success: for now the average in first start and end are 20 and 30 respectively.
        closed_reads.add_read(self.build_read(name='d'), [25], [35])
        self.assertEqual(len(closed_reads), 3)
        self.assertItemsEqual(closed_reads.exons_start_positions.values(), [[20], [20], [25]])
        self.assertItemsEqual(closed_reads.exons_end_positions.values(), [[30], [30], [35]])
        self.assertAlmostEqual(closed_reads.exons_start_average[0].average, 21.666, places=2)
        # Added failed: for now the average in first start and end are 21.666 and 31.6666 respectively.
        closed_reads.add_read(self.build_read(name='e'), [27], [37])
        self.assertEqual(len(closed_reads), 3)
        self.assertItemsEqual(closed_reads.exons_start_positions.values(), [[20], [20], [25]])
        self.assertItemsEqual(closed_reads.exons_end_positions.values(), [[30], [30], [35]])
        self.assertAlmostEqual(closed_reads.exons_start_average[0].average, 21.666, places=2)
        # Added sucess: for now the average in first start and end are 21.666 and 31.6666 respectively.
        closed_reads.add_read(self.build_read(name='f'), [26], [36])
        self.assertEqual(len(closed_reads), 4)
        self.assertItemsEqual(closed_reads.exons_start_positions.values(), [[20], [20], [25], [26]])
        self.assertItemsEqual(closed_reads.exons_end_positions.values(), [[30], [30], [35], [36]])
        self.assertAlmostEqual(closed_reads.exons_start_average[0].average, 22.749, places=2)

    def test_find_positions_average(self):
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 70])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 2)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='c'), [20, 60], [30, 70])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 3)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='c'), [20, 60], [30, 70])
        closed_reads.add_read(self.build_read(name='d'), [20, 40, 60], [30, 50, 70])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 4)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='c'), [20], [30])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 2)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='c'), [20, 40], [30, 50])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 2)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='c'), [20, 80], [30, 90])
        closed_reads.add_read(self.build_read(name='d'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        self.assertEqual(closed_reads.exons_start_average[3].average, 80.0)
        self.assertEqual(closed_reads.exons_start_average[4].average, 100.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[4].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[5].average, 110.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[3].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[3].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[4].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[4].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[4].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[4].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[5].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[5].total_reads_in_pos, 3)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='c'), [20, 60, 100], [30, 70, 110])
        closed_reads.add_read(self.build_read(name='d'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        self.assertEqual(closed_reads.exons_start_average[3].average, 80.0)
        self.assertEqual(closed_reads.exons_start_average[4].average, 100.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[4].average, 110.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[3].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[3].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[4].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[4].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[4].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[4].total_reads_in_pos, 4)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='c'), [20, 100], [30, 110])
        closed_reads.add_read(self.build_read(name='d'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        self.assertEqual(closed_reads.exons_start_average[3].average, 80.0)
        self.assertEqual(closed_reads.exons_start_average[4].average, 100.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[4].average, 110.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[3].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[3].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_start_average[4].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[4].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[4].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[4].total_reads_in_pos, 4)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='b'), [20, 42, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='c'), [20, 44, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='d'), [20, 49, 60, 80, 100], [30, 54, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertAlmostEqual(closed_reads.exons_start_average[1].average, 42.0, places=2)
        self.assertEqual(closed_reads.exons_start_average[2].average, 49.0)
        self.assertEqual(closed_reads.exons_start_average[3].average, 60.0)
        self.assertEqual(closed_reads.exons_start_average[4].average, 80.0)
        self.assertEqual(closed_reads.exons_start_average[5].average, 100.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 51.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[4].average, 110.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 3)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[3].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[3].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[4].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[4].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[4].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[4].total_reads_in_pos, 4)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60, 80, 106], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='b'), [20, 42, 66, 86, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='c'), [20, 44, 60, 86, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='d'), [20, 49, 60, 80, 100], [30, 54, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertAlmostEqual(closed_reads.exons_start_average[1].average, 42.0, places=2)
        self.assertEqual(closed_reads.exons_start_average[2].average, 49.0)
        self.assertEqual(closed_reads.exons_start_average[3].average, 60.0)
        self.assertEqual(closed_reads.exons_start_average[4].average, 66.0)
        self.assertEqual(closed_reads.exons_start_average[5].average, 80.0)
        self.assertEqual(closed_reads.exons_start_average[6].average, 86.0)
        self.assertEqual(closed_reads.exons_start_average[7].average, 100.0)
        self.assertEqual(closed_reads.exons_start_average[8].average, 106.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 51.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[4].average, 110.0)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 1)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[3].total_reads_in_pos, 3)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[4].total_reads_in_pos, 1)
        self.assertEqual(closed_reads.exons_end_average[4].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[5].total_reads_in_pos, 2)
        self.assertEqual(closed_reads.exons_start_average[6].total_reads_in_pos, 2)
        self.assertEqual(closed_reads.exons_start_average[7].total_reads_in_pos, 3)
        self.assertEqual(closed_reads.exons_start_average[8].total_reads_in_pos, 1)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60, 80, 106], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='b'), [20, 42, 66, 86, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='c'), [20, 44, 60, 86, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(self.build_read(name='d'), [20, 49, 60, 80, 100], [30, 54, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertAlmostEqual(closed_reads.exons_start_average[1].average, 42.0, places=2)
        self.assertEqual(closed_reads.exons_start_average[2].average, 49.0)
        self.assertEqual(closed_reads.exons_start_average[3].average, 60.0)
        self.assertEqual(closed_reads.exons_start_average[4].average, 66.0)
        self.assertEqual(closed_reads.exons_start_average[5].average, 80.0)
        self.assertEqual(closed_reads.exons_start_average[6].average, 86.0)
        self.assertEqual(closed_reads.exons_start_average[7].average, 100.0)
        self.assertEqual(closed_reads.exons_start_average[8].average, 106.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 51.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 90.0)
        self.assertEqual(closed_reads.exons_end_average[4].average, 110.0)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 3)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 1)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[3].total_reads_in_pos, 3)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[4].total_reads_in_pos, 1)
        self.assertEqual(closed_reads.exons_end_average[4].total_reads_in_pos, 4)
        self.assertEqual(closed_reads.exons_start_average[5].total_reads_in_pos, 2)
        self.assertEqual(closed_reads.exons_start_average[6].total_reads_in_pos, 2)
        self.assertEqual(closed_reads.exons_start_average[7].total_reads_in_pos, 3)
        self.assertEqual(closed_reads.exons_start_average[8].total_reads_in_pos, 1)

        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='c'), [20, 60], [30, 52])
        closed_reads.add_read(self.build_read(name='d'), [20, 60], [30, 54])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 53.0)
        self.assertEqual(closed_reads.exons_end_average[3].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 4)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 4)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[3].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[3].total_reads_in_pos, 2)

        # separates between different strands in stranded protocol
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b', is_reverse=True), [20, 40, 60], [30, 50, 70])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 1)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 1)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 1)

        # Not separates between different strands in non-stranded protocol
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=False)
        closed_reads.add_read(self.build_read(name='a'), [20, 40, 60], [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b', is_reverse=True), [20, 40, 60], [30, 50, 70])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 40.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 70.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 2)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 2)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 2)

        # Not separates between different strands in non-stranded protocol. Example of the value of the end exon don't calculated in the average.
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=3,
                                                  max_dist_first_edge_from_average=2,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=False)
        closed_reads.add_read(self.build_read(name='a', is_reverse=True), [16, 44, 60],
                              [30, 50, 70])
        closed_reads.add_read(self.build_read(name='b'), [20, 40, 60], [30, 50, 65])
        closed_reads.add_read(self.build_read(name='c'), [20, 41, 60], [30, 50, 75])
        closed_reads.add_read(self.build_read(name='d'), [20, 43, 60], [30, 50, 76])
        closed_reads.add_read(self.build_read(name='e', is_reverse=True), [24, 42, 60], [30, 50, 72])
        closed_reads.add_read(self.build_read(name='f', is_reverse=True), [30, 40, 60], [30, 50, 70])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        self.assertEqual(closed_reads.exons_start_average[0].average, 20.0)
        self.assertEqual(closed_reads.exons_start_average[1].average, 42.0)
        self.assertEqual(closed_reads.exons_start_average[2].average, 60.0)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        self.assertEqual(closed_reads.exons_end_average[0].average, 30.0)
        self.assertEqual(closed_reads.exons_end_average[1].average, 50.0)
        self.assertEqual(closed_reads.exons_end_average[2].average, 71.0)
        self.assertEqual(len(closed_reads.exons_start_average[0].reads_names_in_pos), 5)
        self.assertEqual(closed_reads.exons_start_average[0].total_reads_in_pos, 5)
        self.assertEqual(len(closed_reads.exons_start_average[1].reads_names_in_pos), 5)
        self.assertEqual(closed_reads.exons_start_average[1].total_reads_in_pos, 5)
        self.assertEqual(len(closed_reads.exons_start_average[2].reads_names_in_pos), 5)
        self.assertEqual(closed_reads.exons_start_average[2].total_reads_in_pos, 5)
        self.assertEqual(len(closed_reads.exons_end_average[0].reads_names_in_pos), 5)
        self.assertEqual(closed_reads.exons_end_average[0].total_reads_in_pos, 5)
        self.assertEqual(len(closed_reads.exons_end_average[1].reads_names_in_pos), 5)
        self.assertEqual(closed_reads.exons_end_average[1].total_reads_in_pos, 5)
        self.assertEqual(len(closed_reads.exons_end_average[2].reads_names_in_pos), 5)
        self.assertEqual(closed_reads.exons_end_average[2].total_reads_in_pos, 5)

    def test_find_differnt_transcripts(self):
        read_a = self.build_read(name='a')
        read_b = self.build_read(name='b')
        read_c = self.build_read(name='c')
        read_d = self.build_read(name='d')
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(read_a, [20, 40, 60, 80, 106], [30, 50, 70, 90, 110])
        closed_reads.add_read(read_b, [20, 42, 66, 86, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(read_c, [20, 44, 60, 86, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(read_d, [20, 49, 60, 80, 100], [30, 54, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        transcripts_num = {((20, 30), (42, 51), (60, 70), (80, 90), (106, 110)): 1,
                           ((20, 30), (42, 51), (66, 70), (86, 90), (100, 110)): 1,
                           ((20, 30), (42, 51), (60, 70), (86, 90), (100, 110)): 1,
                           ((20, 30), (49, 51), (60, 70), (80, 90), (100, 110)): 1}
        transcripts_reads = {((20, 30), (42, 51), (60, 70), (80, 90), (106, 110)): [read_a],
                             ((20, 30), (42, 51), (66, 70), (86, 90), (100, 110)): [read_b],
                             ((20, 30), (42, 51), (60, 70), (86, 90), (100, 110)): [read_c],
                             ((20, 30), (49, 51), (60, 70), (80, 90), (100, 110)): [read_d]}
        self.assertEqual(closed_reads.find_differnt_transcripts()[0], transcripts_num)
        self.assertEqual(closed_reads.find_differnt_transcripts()[1], transcripts_reads)

        read_a = self.build_read(name='a')
        read_b = self.build_read(name='b')
        read_c = self.build_read(name='c')
        read_d = self.build_read(name='d')
        closed_reads = ReadsWithCloseStartMapping(max_dist_internal_edge_from_average=5,
                                                  max_dist_first_edge_from_average=5,
                                                  max_dist_last_edge_from_average=5,
                                                  local_average_max_num_positions=10, is_stranded_protocol=True)
        closed_reads.add_read(read_a, [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(read_b, [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.add_read(read_c, [20, 100], [30, 110])
        closed_reads.add_read(read_d, [20, 40, 60, 80, 100], [30, 50, 70, 90, 110])
        closed_reads.find_positions_average(closed_reads.exons_start_positions, closed_reads.exons_start_average,
                                            start_positions=True)
        closed_reads.find_positions_average(closed_reads.exons_end_positions, closed_reads.exons_end_average)
        transcripts_num = {((20, 30), (40, 50), (60, 70), (80, 90), (100, 110)): 3,
                           ((20, 30), (100, 110)): 1}
        transcripts_reads = {((20, 30), (40, 50), (60, 70), (80, 90), (100, 110)): [read_a, read_b, read_d],
                             ((20, 30), (100, 110)): [read_c]}
        self.assertEqual(closed_reads.find_differnt_transcripts()[0], transcripts_num)
        self.assertEqual(closed_reads.find_differnt_transcripts()[1].keys(), transcripts_reads.keys())
        # the order of the reads is different, so you need to sort.
        # sorted(transcripts_reads.values())[0] is the first transcript, contains 1 read
        # sorted(transcripts_reads.values())[1] is the second transcript, contains 3 read
        self.assertItemsEqual(sorted(closed_reads.find_differnt_transcripts()[1].values())[0],
                              sorted(transcripts_reads.values())[0])
        self.assertItemsEqual(sorted(closed_reads.find_differnt_transcripts()[1].values())[1],
                              sorted(sorted(transcripts_reads.values())[1]))

        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycharm
        # Protect against deletion of slowing pycha
