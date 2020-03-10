import operator


class Library:
    def __init__(self, l_id, buffer_time, capacity, books, deadline):
        self.books = books
        self.no_of_books = len(self.books)
        self.capacity = capacity
        self.buffer_time = buffer_time
        self.l_id = l_id
        self.deadline = deadline
        self.l_score = self.get_library_score()
        self.processing_left = buffer_time
        self.scanned_books = []
        self.processing = False
        self.registered = False
        self.scanned_all_books = False
        self.books.sort(key=operator.attrgetter('b_score'))

    def get_library_score(self):
        '''
        Main formula for defining library score and makes easy to 
        take which library will be scanned first
        '''

        score_list = sorted(
            [book.b_score for book in self.books], reverse=True)
        # sum(score_list)/(self.deadline-self.buffer_time)
        # print(score_list)
        total_cost_of_books = sum(
            score_list[:(self.deadline-self.buffer_time)*self.capacity])
        return total_cost_of_books

    def process_books(self):
        '''
        process book according it's capacity
        '''
        if not self.scanned_all_books and self.registered:
            count = 0
            for book in self.books:
                # only scan book if it's not scanned and some capacity is left today
                if not book.is_scanned and count < self.capacity:
                    book.is_scanned = True
                    self.scanned_books.append(book)
                    count += 1
