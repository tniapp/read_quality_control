from hstest import *

testData = """@SRR345678.45 GWZHISEQ01:153:C1W31ACXX:5:1101:5069:2307 length=101
GCTTCTCTTAACTGAGGTCACCATCATGCCGTTAAGTCCCTACCTCTCTTTTGCCGGTAACTGTTCCGCCGCGATTGCCTTTTATCTGTCTCTTATACACC
+
??<DBD;4C2=<BB>:AC;<CF<CE@FE9@E1C@891CD*9:?:3D@DD4?D<DD:0;@A=AEIDDA##################################
@SRR1345678.46 GWZHISEQ01:153:C1W31ACXX:5:1101:5178:2440 length=101
GCATAAGGACGATCGCTCCAGAGTAAAATAAATACGCGCATGTGATACTCACAATACCAATGGTGAAGTTACGGGACTTAAACAAACTGAGATCAAGAATC
+
CCCFFFFFHHHHHJJJJJJJJJJFFHIJJJJJJJJJJJJJJJJJJJJJJJIJHHHHHHFDEDF;AEEEEEEDDDDDBBACDDDCDDDDCCDDDDDDCCDC3
@SRR345678.53 GWZHISEQ01:153:C1W31ACXX:5:1101:6707:2460 length=101
TCATTAAGCCGTGGTGGATGTGCCATAGCGCACCGCAAAGTTAAGAAACCGAATATTGGGTTTAGTCTTGTTTCATAATTGTTGCAATGAAACGCGGTGAA
+
CCCFFFFFHHHHHJHIIJIIIIJJJJJJGIJJJJJIJJIIGHJJJJJIIJJDHFFFFFEDACDDDCDDDDCCDDECACCDCCCDACDDDDCCDDDDDBD@A"""

CORRECT = ["@SRR345678.45 GWZHISEQ01:153:C1W31ACXX:5:1101:5069:2307 length=101",
           "GCTTCTCTTAACTGAGGTCACCATCATGCCGTTAAGTCCCTACCTCTCTTTTGCCGGTAACTGTTCCGCCGCGATTGCCTTTTATCTGTCTCTTATACACC",
           "+",
           "??<DBD;4C2=<BB>:AC;<CF<CE@FE9@E1C@891CD*9:?:3D@DD4?D<DD:0;@A=AEIDDA##################################"]


class ReadExtract(StageTest):
    @dynamic_test(files={'test.fastq': testData})
    def test(self):
        program = TestedProgram()
        program.start()

        if not program.is_waiting_input():
            raise WrongAnswer("You program should input the path to the file")

        reply = program.execute('test.fastq')
        reply_as_list = reply.strip().split('\n')
        if not reply:
            raise WrongAnswer("You gave an empty answer")
        elif len(reply_as_list) > 4:
            extra_lines = list(set(reply_as_list) - set(CORRECT))
            raise WrongAnswer(f"There are {len(reply_as_list)} lines in your answer. "
                              f"It should be 4. Extra lines are:\n{extra_lines}")
        elif len(reply_as_list) < 4:
            raise WrongAnswer(f"Not enough lines for the first read ({len(reply_as_list)} instead of 4)")
        else:
            if reply_as_list != CORRECT:
                raise WrongAnswer("Check the content of the first read once more")
            else:
                return CheckResult.correct()


if __name__ == '__main__':
    ReadExtract().run_tests()
