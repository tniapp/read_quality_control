fastq = input()


def get_sequences(fastq_file):
    read_sequences = []
    counter = 0
    with open(fastq_file) as fh:
        for line in fh:
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


def average_length(reads_sequences):
    all_lengths = 0
    for read in reads_sequences:
        all_lengths += len(read)
    return all_lengths / len(reads_sequences)


def gc_average(reads_sequences):
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


def repeats_amount(reads_sequences):
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


def ns_counter(n_per_read):
    n_per_seq = sum(n_per_read) / len(n_per_read)
    reads_with_n = len([x for x in n_per_read if x != 0.0])
    return n_per_seq, reads_with_n


def read_quality(fastq_file):
    reads_sequences_list = get_sequences(fastq_file)
    length_average = average_length(reads_sequences_list)
    gc_content_average = gc_average(reads_sequences_list)[0]
    repeats = repeats_amount(reads_sequences_list)

    n_value = gc_average(reads_sequences_list)[1]
    n_count = ns_counter(n_value)

    output = [f"Reads in the file = {len(reads_sequences_list)}",
              f"Reads sequence average length = {round(length_average)}\n",
              f"Repeats = {repeats}",
              f"Reads with Ns = {n_count[1]}\n",
              f"GC content average = {round(gc_content_average, 2)}%",
              f"Ns per read sequence = {round(n_count[0], 2)}%"]

    return '\n'.join(output)


print(read_quality(fastq))
