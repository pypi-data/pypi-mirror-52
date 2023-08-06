import copy


class ReadsWithCloseStartMapping(object):
    """
    Contains all reads with the same (or close) start mapping.
    The reads are stored as positions of start and end of all exons

    Args:
        max_dist_internal_edge_from_average                (int): maximum distance of position of exon from the average
        max_dist_first_edge_from_average    (int): maximum distance of position of first exon from the average
        max_dist_last_edge_from_average       (int): maximum distance of position of end of last exon from the average
        local_average_max_num_positions           (int): maximum number of positions for calculate the average.
        is_stranded_protocol                      (bool): is stranded portocol or not

    Attributes:
        exons_start_positions                (dict of pysam.AlignedSegment: list of int):
                                                            keys: pysam.AlignedSegment (read)
                                                            value: list of start positions of the exons
        exons_end_positions                  (dict of pysam.AlignedSegment: list of int):
                                                            keys: pysam.AlignedSegment (read)
                                                            value: list of end positions of the exons
        exons_start_average                  (list of PositionAverage object): positions average of the starts of the exons
        exons_end_average                    (list of PositionAverage object): positions average of the ends of the exons
    """

    def __init__(self, max_dist_internal_edge_from_average, max_dist_first_edge_from_average,
                 max_dist_last_edge_from_average, local_average_max_num_positions, is_stranded_protocol):
        self.max_dist_internal_edge_from_average = max_dist_internal_edge_from_average
        self.max_dist_first_edge_from_average = max_dist_first_edge_from_average
        self.max_dist_last_edge_from_average = max_dist_last_edge_from_average
        self.local_average_max_num_positions = local_average_max_num_positions
        self.is_stranded_protocol = is_stranded_protocol
        self.exons_start_positions = {}
        self.exons_end_positions = {}
        self.exons_start_average = []
        self.exons_end_average = []

    def __len__(self):
        """
        Returns:
            reads_number    (int): number of reads in the object (their start mapping in close)
        """
        return len(self.exons_start_positions.keys())

    def add_read(self, read, read_start_positions, read_end_positions):
        """
        - Find if read is belong to this object. If the start mapping of the read is close to average of the start
          mapping position of the other reads that belongs to this object.(first item in self.exons_start_positions
          list).
        - The distance need to be at most self.max_dist_first_edge_from_average.
        - If the read is close the read will be added to the objcet by not close return False and not add it.

        Args:
            read:                   (pysam.AlignedSegment object): one read from the input file
            read_start_positions    (list of int): list of start positions of the exons of the read
            read_end_positions      (list of int): list of end positions of the exons of the read
        Returns:
            flag    (bool): close or not close
        """
        if not self.exons_start_average:
            self.exons_start_average.append(
                PositionAverage(local_average_max_num_positions=self.local_average_max_num_positions))
        if self.exons_start_average[0].close_to(coordinate=read_start_positions[0], is_internal_exon=False,
                                                max_dist_from_average=self.get_max_distance(read=read,
                                                                                            is_internal_exon=False,
                                                                                            start_pos=True)):
            self.exons_start_positions[read] = read_start_positions
            self.exons_end_positions[read] = read_end_positions
            self.exons_start_average[0].update_average_of_position(read=read, coordinate=read_start_positions[0],
                                                                   is_internal_exon=False)
            return True
        else:
            return False

    def get_max_distance(self, read, is_internal_exon, start_pos):
        if is_internal_exon:
            return self.max_dist_internal_edge_from_average
        if start_pos:
            if read.is_reverse:
                return self.max_dist_last_edge_from_average
            else:
                return self.max_dist_first_edge_from_average
        else:
            if read.is_reverse:
                return self.max_dist_first_edge_from_average
            else:
                return self.max_dist_last_edge_from_average

    def find_positions_average(self, exons_positions, exons_average, start_positions=False):
        """
        Go over all exon positions (start positions or end positions) of all reads that start in the same location (or
        close), except the first position (use with skip first=True for this).
        The fucntion finds the average of each position
        across all reads. If the position of read is far away from the average the position of the read is shifted to the next exon, and the current position is filled with None.

        Args:
            exons_positions     (dict of pysam.AlignedSegment: list of int):
                                                either self.exons_start_positions or self.exons_end_positions
            exons_average       (list of PositionAverage object):
                                                either self.exons_start_average or self.exons_env_average
            start_positions     (bool): start positions or end positions. if start positions - skip on the first
                                        position. It is True for exons_start_positions because the first position
                                        average already calculated in add_read function.
        """
        exons_positions_thin = copy.deepcopy(exons_positions)
        i = 1 if start_positions else 0
        while True:  # run on all exons
            # i=2
            # exons_positions = {1: [1,2], 3: [1,4], 4: [1,3], 2: [1,1], 0: [5]}
            exons_positions_list = []
            for read, exons in exons_positions_thin.items():
                if len(exons) > i:
                    exons_positions_list.append((read, exons))
                else:
                    del exons_positions_thin[read]
            if not exons_positions_list:  # the while loop have terminated to pass on all the exons
                break
            exons_positions_list_sorted = sorted(exons_positions_list, key=lambda x: x[1][i])
            # go over the all reads, and take from each read only the i position
            for read, positions in exons_positions_list_sorted:
                # in start positions we skip on the first
                is_internal_exon = True if start_positions or not (i + 1 == len(positions)) else False
                # Add a new PositionAverage object if not exists (in the first iteration in the loop - first read in the position)
                if len(exons_average) == i:
                    exons_average.append(PositionAverage(self.local_average_max_num_positions))
                read_position = positions[i]
                exon_average = exons_average[i]
                if exon_average.close_to(coordinate=read_position, is_internal_exon=is_internal_exon,
                                         max_dist_from_average=self.get_max_distance(read=read,
                                                                                     is_internal_exon=is_internal_exon,
                                                                                     start_pos=False)):
                    exon_average.update_average_of_position(read=read, coordinate=read_position,
                                                            is_internal_exon=is_internal_exon)
                else:  # The position is far away from the average
                    exons_positions[read] = exons_positions[read][0:i] + [None] + exons_positions[read][i:]
                    exons_positions_thin[read] = exons_positions_thin[read][0:i] + [None] + exons_positions_thin[
                                                                                                read][i:]
            i += 1

    def find_average_of_all_exons(self):
        """
        Run on start and end positions separately, and update the averages of them in self.exons_start_average and
        self.exons_end_average list respectively.
        """
        self.find_positions_average(self.exons_start_positions, self.exons_start_average, start_positions=True)
        self.find_positions_average(self.exons_end_positions, self.exons_end_average)

    def find_differnt_transcripts(self):
        """
        - Find the average of exons positions for each read, by taking only average positions that are not None in the
          positions of the read (None accepeted when we shift the exon of the reads to the next exon because its
          distance from the average)
        - take the unique of the transcripts between the reads.

        Returns:
            transcripts_num     (dict of tuple of tuples (int, int): int):
                                    key: list of tuples that contains the coordinates of the exons [(start, end),(start, end)...]
                                    value: number of reads in this transcript
            transcripts_reads   (dict of tuple of tuples (int, int): list of pysam.AlignedSegment):
                                    key: list of tuples that contains the coordinates of the exons [(start, end),(start, end)...]
                                    value: list of reads in this transcript.
            is_reverse          (bool): is minus strans or not. It return true value only in stranded protocol. In non-stranded
                                        protocol you need to ignore this value (because it is check only one read in the group of
                                        the reads, but in non-stranded the group contains reads from plus and minus strands toghether.).
        """
        transcripts_num = {}
        transcripts_reads = {}
        is_reverse = None
        for read, read_start_positions_with_none in self.exons_start_positions.items():
            is_reverse = read.is_reverse
            read_start_averages = [self.exons_start_average[i] for i, start_position in
                                   enumerate(read_start_positions_with_none)
                                   if start_position is not None]  # if start position is not None because shift.
            read_end_positions = self.exons_end_positions[read]
            read_end_averages = [self.exons_end_average[i] for i, end_position in enumerate(read_end_positions) if
                                 end_position is not None]
            read_start_positions = [start_position for start_position in read_start_positions_with_none if
                                    start_position is not None]
            read_end_positions = [end_position for end_position in read_end_positions if end_position is not None]
            transcript_list = [self.find_start_end(start, end, read_start_positions[i], read_end_positions[i])
                               for i, (start, end) in enumerate(zip(read_start_averages, read_end_averages))]
            transcript = tuple(transcript_list)
            if transcript not in transcripts_num.keys():
                transcripts_num[transcript] = 0
                transcripts_reads[transcript] = []
            transcripts_num[transcript] += 1
            transcripts_reads[transcript].append(read)
        return transcripts_num, transcripts_reads, is_reverse

    def find_start_end(self, start_average, end_average, read_start_position, read_end_position):
        start_average, end_average = int(start_average), int(end_average)
        if start_average >= end_average:
            if start_average >= read_end_position:
                if read_start_position >= end_average:
                    return (
                        read_start_position, read_end_position)
                else:
                    return (read_start_position, end_average)
            else:
                return (start_average, read_end_position)
        else:
            return (start_average, end_average)

    def build_transcripts(self):
        self.find_average_of_all_exons()
        return self.find_differnt_transcripts()


class PositionAverage(object):
    """
    Contains information of average of position between the reads.

    Args:
        max_dist_internal_edge_from_average                  (int): maximum distance of position of exon from the average
        local_average_max_num_positions             (int): maximum number of positions for calculate the average.
    Attributes:
        _average                                    (int): average of positions between the reads
        _total_reads_in_pos                         (int): number of reads that belongs to this position
        _reads_names_in_pos                         (list of pysam.AlignedSegment object): the read in the position
        local_average                               (int): average of position in neighbours of the current position
        local_average_total_reads                   (int): total reads in the neghbours positions
        local_average_positions_and_num_reads       (list of lists of [int, int]: list of lists of the neighbors of the
                                                        current position. Each internal list contains the position and
                                                        the number of reads in the position.

    """

    def __init__(self, local_average_max_num_positions):
        self.local_average_max_num_positions = local_average_max_num_positions
        self.is_internal_exon = None
        self._average = None
        self._total_reads_in_pos = 0
        self._reads_names_in_pos = []
        self.local_average = None
        self.local_average_total_reads = 0
        self.local_average_positions_and_num_reads = []

    def update_local_average(self, coordinate):
        """
        Updates the local average. This is average of the neighbours (self.local_average_max_num_positions) of the current position.

        Args:
            coordinate      (int): the position of the read
        """
        # If the last position different than current position
        if not self.local_average_positions_and_num_reads or coordinate != \
                self.local_average_positions_and_num_reads[-1][0]:
            self.local_average_positions_and_num_reads.append([coordinate, 1])
        else:
            self.local_average_positions_and_num_reads[-1][1] += 1
        # If the last insertion of the new position (if the above condition is true), enlarge the last position more
        # then the allowed maximum, remove the first position (the oldest) and update the local_average
        if len(self.local_average_positions_and_num_reads) > self.local_average_max_num_positions:
            self.local_average -= float(
                self.local_average_positions_and_num_reads[0][1] * self.local_average_positions_and_num_reads[0][
                    0]) / self.local_average_total_reads
            self.local_average *= self.local_average_total_reads
            self.local_average_total_reads -= self.local_average_positions_and_num_reads[0][1]
            self.local_average /= self.local_average_total_reads
            self.local_average_positions_and_num_reads = self.local_average_positions_and_num_reads[1:]

        # update the local average with the new position.
        if self.local_average is None:
            self.local_average = 0

        self.local_average = float(self.local_average * self.local_average_total_reads + coordinate) / (
                self.local_average_total_reads + 1)
        self.local_average_total_reads += 1

    def update_average_of_position(self, read, coordinate, is_internal_exon):
        """
        Get a new read that sould to be belonged to this position and update the average of the position according the
        position of the new read

        Args:
            read               (pysam.AlignedSegment object): the new read to adding
            coordinate         (int): the position of the read
        """
        self.is_internal_exon = is_internal_exon
        if self._average is None:
            self._average = 0
        self._average = float(self.average * self.total_reads_in_pos + coordinate) / (self.total_reads_in_pos + 1)
        self._reads_names_in_pos.append(read)
        self._total_reads_in_pos += 1
        self.update_local_average(coordinate)

    def close_to(self, coordinate, is_internal_exon, max_dist_from_average):
        if self.is_internal_exon is not None and self.is_internal_exon != is_internal_exon:
            return False
        # return True if self.average is None or abs(self.average - coordinate) <= max_distance else False
        return True if self.local_average is None or abs(
            self.local_average - coordinate) <= max_dist_from_average else False

    @property
    def average(self):
        return self._average

    @property
    def total_reads_in_pos(self):
        return self._total_reads_in_pos

    @property
    def reads_names_in_pos(self):
        return self._reads_names_in_pos

    def __int__(self):
        """
        Returns:
            average     (int): round of the average of the position among all reads.
        """
        return int(self._average)
