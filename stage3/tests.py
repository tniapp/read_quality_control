from hstest import *
import re


class GcContent(StageTest):
    files_dict = {
            "test1.fastq": """@SRR12345678.1 1 length=75\nGCACACAACCGTGATGCTGAGCTGGCGTCGGTGGTATCAAATATGTCCAGCGAGCCGCACGTTACCCCTCCACTT\n+SRR12345678.1 1 length=75\n-ABCCGGFGGGGG9FFFEACFFGC<FEBC++8,+C9FG9<,C,CEFEFC,C@++8:+++8+C@,89C@,8,,,99\n@SRR12345678.2 2 length=76\nCACTGACTGGGATTTTTTGCAGCGAGTTTGCCAGCAGGTGGGATTTTCACCGGTTGTTATTCGCGAAGTTAATGAA\n+SRR12345678.2 2 length=76\n@BCCCGGGGGGGGGGGGGGGGGGGDGFGGCFG9EFCFDGG?7,CFFFFCFF7+@C+BC,CCC,:++++:C,,<,,,""",
            "test2.fastq": """@SRR98765432.1 1 length=71\nCGGTAATAGTCACGGTGCTCATGCTTGCTCCTTAAGGGCGTTAACACGCAAAGTAACGGCATTTTTGTGGT\n+SRR98765432.1 1 length=71\nACCCCGGGGGGGGFGGGGGGGGGGGGGGGGGGGCAEFDFEEFDFFFF7B:+@8F9,C,+8+@EFFF+C,,,\n@SRR98765432.2 2 length=76\nGTTTCCCGCTTCGTGCACTGAAATTTTATGATAACGATGGTGCGCGGCAGGAAGTGATTTCCGAAGCCTTTAAATT\n+SRR98765432.2 2 length=76\n-ACCCGGGGEGGGGFGGFGFCCDFFGGGGF,C@EF@7FDDE,C+@+::++6,,,:,,<<,<6,,,+86C,:,,,,6\n@SRR98765432.3 3 length=53\nGTGGATGACGGCCCATAACATCGCCTTCGTCGTGGTCAATATCAATATTAACT\n+SRR98765432.3 3 length=53\n-CCCCGGGGGGGGGGGGGGGGGGGGGGGGGGGGDGGFCFFAFFC,F9EF9<EE\n@SRR98765432.4 4 length=75\nTGGCAGAACAGCTTGATCAGATGGGCGGCGAGCAGCTGCGTCGCAAAATCGAAAGTATTTGCTTGCGCTTTCACA\n+SRR98765432.4 4 length=75\n@@CCCGGGGGFGGGGFFFGCFGGFCFCDF7@+@FAEFCF+BF@C:C7CFE7,,,+C,C,,,<,C,:+7+?D<,C,""",
            "test3.fastq": """@SRR123456722\nAGTCTNCGNTAGAGNGNCANAGGGGNANAANNTCANGTGTAGNNTGAATGCNCANNNCNNNNACNGCTANGCNTAG\n+\n????????????????????????????????????????????????????????????????????????????\n@SRR123456723\nAANGTGGTATTGGAACCNANGTGNCANAAGGNCAAACTANCAAGNNGATANCGCCCGNGGGCTNTTCCTCTTGNTC\n+\n????????????????????????????????????????????????????????????????????????????\n@SRR123456724\nNGTGGGATCCTGCCCAGGCGACTTCGNCGNCACTTAGNAAATGCAAGNTANCAGGNCNATTCTGCTGAACANGAGN\n+\n????????????????????????????????????????????????????????????????????????????\n@SRR123456725\nNTNNCCCCANTCTGNGNNTNCNGNTTGGCCTGGTTATGAGCACGNNNGTGCTNGGGAAGGGTACAAANGNNNCGGT\n+\n????????????????????????????????????????????????????????????????????????????\n@SRR12345673\nACGTAGNNNCAATNGTCTCNCTTTCACANCGAACGTACGAANTCNAAANCTACGNGNCCNGNGCACTNACGTTACCGNGTGCGNAANGANGCGNGCNATN\n+\n????????????????????????????????????????????????????????????????????????????????????????????????????"""
    }

    def common_test(self, file_name, AMOUNT, AVERAGE, GC):
        program = TestedProgram()
        program.start()

        if not program.is_waiting_input():
            raise WrongAnswer("You program should input the path to the file")

        reply = program.execute(file_name)

        if not reply:
            raise WrongAnswer("You gave an empty answer")
        reply_low = reply.replace(" ", "").lower()

        def check_format(line, substring):
            substring_low = substring.replace(" ", "").lower()
            if line.count(substring_low) != 1:
                raise WrongAnswer(f"Substring \"{substring}\" should occur once in the output.\n"
                                  f"Found {line.count(substring_low)} occurrence(s).\n"
                                  f"Check the output format in the Examples section.\n"
                                  f"Make sure there is no typos in the output of your program.")

        def check_amount(reply_amount, correct_amount):
            number_search = re.search(pattern="readsinthefile=([0-9]+)", string=reply_amount)
            if number_search is None:
                raise WrongAnswer("Didn't find numerical answer in the 'Reads in the file' line. Please, check if the answer format is correct")
            reads_amount = int(number_search.group(1))
            if reads_amount != correct_amount:
                raise WrongAnswer("Reads in the file value is incorrect")

        def check_average(reply_avg, average):
            average_search = re.search(pattern="readssequenceaveragelength=([0-9]+)", string=reply_avg)
            if average_search is None:
                raise WrongAnswer("Didn't find numerical answer in 'Reads average' line. Please, check if the answer format is correct")
            average_number = int(average_search.group(1))
            if average_number != average:
                raise WrongAnswer("Reads average is incorrect")

        def check_gc(reply_gc, gc_correct):
            gc_search = re.search(pattern="gccontentaverage=([0-9]+\.[0-9]+)", string=reply_gc)
            if gc_search is None:
                raise WrongAnswer("Didn't find numerical answer in 'GC content' line. Please, check if the answer format is correct")
            gc_number = float(gc_search.group(1))
            if gc_number != gc_correct:
                raise WrongAnswer("GC content average is incorrect")

        check_format(reply_low, "Reads in the file")
        check_format(reply_low, "Reads sequence average length =")
        check_format(reply_low, "GC content average =")
        check_amount(reply_low, AMOUNT)
        check_average(reply_low, AVERAGE)
        check_gc(reply_low, GC)

        return CheckResult.correct()

    @dynamic_test(files=files_dict)
    def test1(self):
        return self.common_test("test1.fastq", AMOUNT=2, AVERAGE=76, GC=51.69)

    @dynamic_test(files=files_dict)
    def test2(self):
        return self.common_test("test2.fastq", AMOUNT=4, AVERAGE=69, GC=47.48)

    @dynamic_test(files=files_dict)
    def test3(self):
        return self.common_test("test3.fastq", AMOUNT=5, AVERAGE=81, GC=42.35)


if __name__ == "__main__":
    GcContent().run_tests()
