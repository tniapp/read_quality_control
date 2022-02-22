from hstest import *
import re


class NsChecker(StageTest):

    def common_test(self, file_name, AMOUNT, AVERAGE, REPEATS, READSN, GC, NSPER):
        program = TestedProgram()
        program.start()

        if not program.is_waiting_input():
            raise WrongAnswer("You program should input the path to the file")

        reply = program.execute(file_name)

        # if the reply is empty
        if not reply:
            raise WrongAnswer("You gave an empty answer")
        reply_low = reply.replace(" ", "").lower()

        # if each point presents only once
        def check_format(line, substring):
            substring_low = substring.replace(" ", "").lower()
            if line.count(substring_low) != 1:
                raise WrongAnswer(f"Substring \"{substring}\" should occur once in the output.\n"
                                  f"Found {line.count(substring_low)} occurrence(s).\n"
                                  f"Check the output format in the Examples section.\n"
                                  f"Make sure there is no typos in the output of your program.")

        # check values
        def check_number(total_reply, substring, correct_number):
            float_lines = ["gccontentaverage=", "nsperreadsequence="]
            substring_low = substring.replace(" ", "").lower()
            pattern = f"{substring_low}([0-9]+)"

            if substring_low in float_lines:
                pattern = pattern[:-1] + "\.[0-9]+)"
            number_search = re.search(pattern=pattern, string=total_reply)

            if number_search is None:
                raise WrongAnswer(f"Didn't find numerical answer in the \"{substring}\" line. Please, check if the answer format is correct")
            number = float(number_search.group(1))
            if number != correct_number:
                raise WrongAnswer(f"The value of \"{substring}\" is incorrect")

        # dict of points for checking + correct values
        answer_points = {"Reads in the file =": AMOUNT,
                         "Reads sequence average length =": AVERAGE,
                         "Repeats =": REPEATS,
                         "GC content average =": GC,
                         "Reads with Ns =": READSN,
                         "Ns per read sequence =": NSPER}

        # run checking!
        for point in answer_points.keys():
            check_format(reply_low, point)
        for point, correct_result in answer_points.items():
            check_number(reply_low, point, correct_result)
        return CheckResult.correct()

    @dynamic_test
    def test1(self):
        return self.common_test("data/test1.fastq", AMOUNT=4, AVERAGE=101, REPEATS=0,
                                READSN=4, GC=38.61, NSPER=20.3)

    @dynamic_test
    def test2(self):
        return self.common_test("data/test2.fastq", AMOUNT=4, AVERAGE=133, REPEATS=0,
                                READSN=1, GC=44.49, NSPER=0.17)


if __name__ == '__main__':
    NsChecker().run_tests()
