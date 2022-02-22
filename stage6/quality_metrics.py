import gzip

gz1, gz2, gz3 = input(), input(), input()


class QualityMetrics(object):
    """
    This code provides read quality control
    It calculates the total number of reads,
                  number of reads sequences with Ns,
                  average reads sequence length,
                  GC content,
                  Ns% per read sequence,
                  and number of repeats
    """

    def __init__(self, gz_archive):
        self.gz_archive = gz_archive

    def get_sequences(self, gz_file):
        read_sequences = []
        counter = 0
        with gzip.open(gz_file, 'r') as fh:
            for line in fh:
                line = line.decode("utf-8")
                line = line.split('\n')[0]
                if line.startswith("@SRR"):
                    counter = 1
                elif line == '+':
                    counter = 0
                elif counter == 1:
                    read_sequences.append(line)
                    counter = 0
                else:
                    counter = 0
        return read_sequences

    def average_length(self, reads_sequences):
        all_lengths = 0
        for read in reads_sequences:
            all_lengths += len(read)
        return all_lengths / len(reads_sequences)

    def gc_average(self, reads_sequences):
        N_per_read, GC_per_read = [], []
        GC, ATGCN, N = 0, 0, 0
        for sequence in reads_sequences:
            for nucleotide in sequence:
                if nucleotide == 'C' or nucleotide == 'G':
                    GC += 1
                if nucleotide == 'N':
                    N += 1
                ATGCN += 1
            N_per_read.append(N / ATGCN * 100)
            GC_per_read.append(GC / ATGCN * 100)
            GC, ATGCN, N = 0, 0, 0

        return [sum(GC_per_read) / len(GC_per_read), N_per_read]

    def repeats_amount(self, reads_sequences):
        repeats_dict = {}
        repeats_sum = 0
        for seq in reads_sequences:
            if seq not in repeats_dict.keys():
                repeats_dict[seq] = 1
            else:
                repeats_dict[seq] += 1
        for read_number in repeats_dict.values():
            if read_number > 1:
                repeats_sum += read_number - 1
        return repeats_sum

    def ns_counter(self, n_per_read):
        n_per_seq = sum(n_per_read) / len(n_per_read)
        reads_with_n = len([x for x in n_per_read if x != 0.0])
        return n_per_seq, reads_with_n

    def read_quality(self):
        reads_sequences_list = self.get_sequences(self.gz_archive)
        length_average = self.average_length(reads_sequences_list)
        gc_content_average = self.gc_average(reads_sequences_list)[0]
        repeats = self.repeats_amount(reads_sequences_list)

        n_value = self.gc_average(reads_sequences_list)[1]
        n_count = self.ns_counter(n_value)

        output = [f"Reads in the file = {len(reads_sequences_list)}",
                  f"Reads sequence average length = {round(length_average)}\n",
                  f"Repeats = {repeats}",
                  f"Reads with Ns = {n_count[1]}\n",
                  f"GC content average = {round(gc_content_average, 2)}%",
                  f"Ns per read sequence = {round(n_count[0], 2)}%"]

        return '\n'.join(output)


class MetricsSummary(object):

    def summary(self, *results):
        metric2values = {"Reads in the file": [],
                         "Reads sequence average length": [],
                         "Repeats": [],
                         "Reads with Ns": [],
                         "GC content average": [],
                         "Ns per read sequence": []}

        for result in results:
            for line in result.split('\n'):
                if not line:
                    continue
                if '%' in line:
                    line = line[:-1]
                line = line.split(' = ')
                value = float(line[-1])
                metric2values[line[0]].append(value)

        return metric2values

    def best_archive_list(self, metrics):
        best_archive_number = []

        amount = min(metrics["Reads in the file"])
        repeat = min(metrics["Repeats"])
        gc_level = max(metrics["GC content average"])
        read_n = min(metrics["Reads with Ns"])
        ns_per_read = min(metrics["Ns per read sequence"])

        best_archive_number.append(metrics["Reads in the file"].index(amount) + 1)
        best_archive_number.append(metrics["Repeats"].index(repeat) + 1)
        best_archive_number.append(metrics["GC content average"].index(gc_level) + 1)
        best_archive_number.append(metrics["Reads with Ns"].index(read_n) + 1)
        best_archive_number.append(metrics["Ns per read sequence"].index(ns_per_read) + 1)

        return best_archive_number


if __name__ == "__main__":
    gz1_result = QualityMetrics(gz1).read_quality()
    gz2_result = QualityMetrics(gz2).read_quality()
    gz3_result = QualityMetrics(gz3).read_quality()
    results_dict = {1: gz1_result, 2: gz2_result, 3: gz3_result}

    dict_metrics = MetricsSummary().summary(gz1_result, gz2_result, gz3_result)
    archive_list = MetricsSummary().best_archive_list(dict_metrics)
    best_archive = max(archive_list, key=archive_list.count)

    print(results_dict[best_archive])



