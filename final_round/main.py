import argparse

from Book import Book
from Library import Library

from termcolor import colored, cprint
import operator
from tqdm import tqdm


class PlayBookTeam:
    def __init__(self, deadline, book_score_list, libraries):
        self.deadline = deadline
        self.pile_of_libraries = self.populate_libraries(
            book_score_list, libraries)
        self.in_process_library = None  # if any library is in signup process
        self.registered_libraries = []
        self.pile_of_libraries.sort(
            key=operator.attrgetter('l_score'))  # sorting here

    def populate_libraries(self, book_score_list, libraries):
        my_libraries = []
        # Distributing books to libraries
        books_data = [Book(b_id, b_score)
                      for b_id, b_score in enumerate(book_score_list)]
        for l_id, library in enumerate(tqdm(libraries)):
            prop, books = library
            desirable_books_list = []

            for book_id in books:
                book_score = book_score_list[book_id]
                # book_obj = Book(b_id=book_id, b_score=book_score)
                for b_obj in books_data:
                    if b_obj.b_id == book_id:
                        desirable_books_list.append(b_obj)
            _, buff_time, capacity = prop

            my_libraries.append(
                Library(l_id, buff_time, capacity, desirable_books_list, self.deadline))
        return my_libraries

    # def get_custom_list(self):

    def set_new_inprocess_library(self):
        for library in self.pile_of_libraries:
            if not library.registered:
                self.in_process_library = library
                self.in_process_library.processing = True
                self.in_process_library.processing_left -= 1
                break

    def regular_process_books(self):
        for library in self.registered_libraries:
            library.process_books()

    def regular_team_check(self):
        if self.in_process_library:
            if self.in_process_library.processing_left > 0:
                self.in_process_library.processing_left -= 1

            else:
                self.in_process_library.registered = True
                self.in_process_library.processing = False
                self.registered_libraries.append(self.in_process_library)
                self.in_process_library = None
        else:
            self.set_new_inprocess_library()

    def main(self):
        for _ in tqdm(range(self.deadline)):

            self.regular_team_check()
            self.regular_process_books()

            if not self.in_process_library:
                self.set_new_inprocess_library()

    def save_file(self, filename, write=True):
        line1 = str(len(self.registered_libraries))+'\n'
        lines = ""
        total_score = 0
        for library in self.registered_libraries:
            lines = lines + str(library.l_id)+" " + str(len(library.scanned_books)) + \
                "\n"+" ".join([str(book.b_id)
                               for book in library.scanned_books])+"\n"
            for books in library.scanned_books:
                total_score += books.b_score
        print(f"Total Score {total_score}")
        if write:
            with open(filename, "w") as f:
                f.write(line1)
                f.write(lines)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--filename", help="Filename you want to get output from it")
args = parser.parse_args()

input_file_name = args.filename or 'data/a_example.txt'
with open(input_file_name, 'r') as f:
    NO_OF_BOOKS, NO_OF_LIBRARY, DEADLINE = [
        int(i) for i in f.readline()[:-1].split(" ")]
    BOOK_SCORE_LIST = [int(i) for i in f.readline()[:-1].split(" ")]
    LIBRARIES = []
    temp = []
    for lines in f.readlines():
        try:
            temp.append([int(i) for i in lines[:-1].split(" ")])
        except:
            pass
        if len(temp) == 2:
            LIBRARIES.append(temp)
            temp = []


obj_playbooks = PlayBookTeam(DEADLINE, BOOK_SCORE_LIST, LIBRARIES)
obj_playbooks.main()
obj_playbooks.save_file(input_file_name+".out")
