fastq = input()

readSeqs = []
read_dict = {}
totalLen, cnt = 0, 0

with open(fastq) as fh:
    for line in fh:
        line = line.split('\n')[0]

        if line.startswith('@SRR'):
            cnt = 1
        elif line == "+":
            cnt = 0
        elif cnt == 1:
            readSeqs.append(line)
            cnt = 0
        else:
            cnt = 0

for read in readSeqs:
    totalLen += len(read)

meanLen = totalLen / len(readSeqs)

for read in readSeqs:
    if len(read) not in read_dict.keys():
        read_dict[len(read)] = 1
    else:
        read_dict[len(read)] += 1

print(f"Reads in the file = {len(readSeqs)}")

for length in sorted(read_dict.keys()):
    print(f"      with length {length} = {read_dict[length]}")

print(f"Reads sequence average length = {round(meanLen)}")

