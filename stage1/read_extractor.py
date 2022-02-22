fastq = input()
fastqOpen = open(fastq, 'r')
fastqRead = fastqOpen.read()
# print("\n".join(fastqRead.split("\n")[:4]))  # another solution
print("@SRR" + fastqRead.split("@SRR")[1])