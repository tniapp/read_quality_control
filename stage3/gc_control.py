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

    return sum(GC_per_read) / len(GC_per_read)


reads_sequences_list = get_sequences(fastq)
length_average = average_length(reads_sequences_list)
gc_content_average = gc_average(reads_sequences_list)

print(f"Reads in the file = {len(reads_sequences_list)}")
print(f"Reads sequence average length = {round(length_average)}")
print()
print(f"GC content average = {round(gc_content_average, 2)}%")
