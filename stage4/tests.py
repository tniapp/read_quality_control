from hstest import *
import re


class RepeatsChecker(StageTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        if not program.is_waiting_input():
            raise WrongAnswer("You program should input the path to the file")

        reply = program.execute("data/SRR16506265_1.fastq")

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
            substring_low = substring.replace(" ", "").lower()
            if substring_low == "gccontentaverage=":
                number_search = re.search(pattern="gccontentaverage=([0-9]+\.[0-9]+)", string=total_reply)
            else:
                number_search = re.search(pattern=f"{substring_low}([0-9]+)", string=total_reply)

            if number_search is None:
                raise WrongAnswer(f"Didn't find numerical answer in the \"{substring}\" line. Please, check if the answer format is correct")

            number = float(number_search.group(1))
            if number != correct_number:
                raise WrongAnswer(f"The value of \"{substring}\" is incorrect")

        # list of points for checking
        answer_points = ["Reads in the file =", "Reads sequence average length =", "Repeats =", "GC content average ="]

        # run checking!
        for point in answer_points:
            check_format(reply_low, point)
        check_number(reply_low, answer_points[0], 1071863)  # reads amount
        check_number(reply_low, answer_points[1], 75)  # average length
        check_number(reply_low, answer_points[2], 236842)  # repeats
        check_number(reply_low, answer_points[3], 51.25)  # GC

        return CheckResult.correct()


if __name__ == "__main__":
    RepeatsChecker().run_tests()
