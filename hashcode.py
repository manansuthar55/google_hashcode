import argparse


class HashCode:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.max_slices, self.pizza_type, self.pizza_list = self.read_file()
        self.max_summation = 0

    def read_file(self):
        with open(self.input_file, "r") as input_file:
            lines = input_file.readlines()

        first_line = lines[0][:-1]
        second_line = lines[1][:-1]

        # converting first line into two element array
        first_line_list = first_line.split(" ")

        max_slices = int(first_line_list[0])  # getting max_slices
        pizza_types = int(first_line_list[1])  # getting total nos of pizza

        # typecasting second line into list of integers
        pizza = list(map(int, second_line.split(" ")))

        return max_slices, pizza_types, pizza

    def create_output_file(self, required_list, no_of_pizzas):
        with open(self.output_file, "w") as f:
            f.write(str(no_of_pizzas) + "\n")
            f.write(" ".join(list(map(str, required_list))))

    def verify_indexes(self, index1, index2):
        # -1 because we are doing with indexes
        index2 = (self.pizza_type - 1) - index2

        if index1 != index2:
            return True, index2
        return False, None

    def run(self):
        for idx, item_i in enumerate(self.pizza_list):
            summation = item_i
            required_list = [idx]

            for jdx, item_j in enumerate(reversed(self.pizza_list)):
                temp_total = summation + item_j
                varified_index, index = self.verify_indexes(idx, jdx)
                if temp_total <= self.max_slices and varified_index:
                    summation = temp_total
                    required_list.append(index)

            if summation >= self.max_summation:
                self.max_summation = summation
                if summation == self.max_slices:
                    break
        print(summation)
        self.create_output_file(sorted(required_list), len(required_list))


parser = argparse.ArgumentParser()
parser.add_argument(
    "--filename", help="Filename you want to get output from it")
args = parser.parse_args()

input_file_name = args.filename
obj_hash = HashCode(input_file_name, input_file_name + ".out")

obj_hash.run()
