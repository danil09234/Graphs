import unittest
from main import parse_input_file, find_nearest_insertion, write_result_to_file

if __name__ == "__main__":
    EXAMPLE_FILE_TEMPLATE = "Unittests/example{}.txt"
    EXAMPLE_FILE_RESULT_TEMPLATE = "Unittests/example{}_nearest_insertion_of_arbitrary_city.txt"
else:
    EXAMPLE_FILE_TEMPLATE = "example{}.txt"
    EXAMPLE_FILE_RESULT_TEMPLATE = "example{}_nearest_insertion_of_arbitrary_city.txt"


class TestNearestInsertion(unittest.TestCase):
    def example(self, example: int):
        all_input_edges = parse_input_file(f"example{example}.txt")
        nearest_insertion = find_nearest_insertion(all_input_edges)
        write_result_to_file(f"example{example}_result.txt", nearest_insertion, all_input_edges)

        with open(f"example{example}_result.txt", "r", encoding="utf-8") as result:
            result = result.read()

        with open(EXAMPLE_FILE_RESULT_TEMPLATE.format(example), "r", encoding="utf-8") as example_result:
            example_result = example_result.read()

        self.assertEqual(example_result, result)

    def test_example_1(self):
        self.example(1)

    def test_example_2(self):
        self.example(2)

    def test_example_3(self):
        self.example(3)

    def test_example_4(self):
        self.example(4)

    def test_example_5(self):
        self.example(5)

    def test_example_6(self):
        self.example(6)

    def test_example_7(self):
        self.example(7)

    def test_example_8(self):
        self.example(8)

    def test_example_9(self):
        self.example(9)

    def test_example_10(self):
        self.example(10)

    def test_example_11(self):
        self.example(11)

    def test_example_12(self):
        self.example(12)

    def test_example_13(self):
        self.example(13)

    def test_example_14(self):
        self.example(14)

    def test_example_15(self):
        self.example(15)

    def test_example_16(self):
        self.example(16)

    def test_example_17(self):
        self.example(17)

    def test_example_18(self):
        self.example(18)

    def test_example_19(self):
        self.example(19)

    def test_example_20(self):
        self.example(20)
