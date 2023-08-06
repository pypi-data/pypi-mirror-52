from StringIO import StringIO
from contextlib import contextmanager
from unittest import TestCase
import sys
import pysam



class TestBase(TestCase):
    maxDiff = None

    #show the print commands
    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def build_read(self, name=None, is_reverse=False):
        """
        build an default read.
        See examples of tests on pysam: https://github.com/pysam-developers/pysam/blob/master/tests/AlignedSegment_test.py
        """
        # read = pysam.AlignedSegment.from_dict(default_read.to_dict(), default_read.header)

        header = pysam.AlignmentHeader.from_references(["chr1", "chr2"], [10000000, 10000000])

        a = pysam.AlignedSegment(header)
        a.query_name = "read_12345" if not name else name
        a.query_sequence = "ATGC" * 10
        a.flag = 0 if not is_reverse else 16
        a.reference_id = 0
        a.reference_start = 0
        a.mapping_quality = 20
        a.cigartuples = ((0, 10), (2, 1), (0, 9), (1, 1), (0, 20))
        a.next_reference_id = 0
        a.next_reference_start = 200
        a.template_length = 167
        a.query_qualities = pysam.qualitystring_to_array("1234") * 10
        return a
