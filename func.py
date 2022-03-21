from statistics import median


class Words:
    def __init__(self, str_input, k: int, n: int) -> None:
        self.str_input = str_input
        self.K: int = k
        self.N: int = n
        self.split_str: str = ""
        self.word_dict: dict = {}
        self.ngrams_dict: dict = {}
        self.res_str: str = ""

    def count_words(self):
            self.res_str = self.str_input.replace('?', ' ').replace('!', ' ').replace(',', ' ').replace('.', ' ').split()
            for key in self.res_str:
                if not self.word_dict.get(key):
                    self.word_dict[key] = 1
                else:
                    self.word_dict[key] += 1

    def print_dictionary(self):
        print(self.word_dict)

    def find_median(self) -> float:
        return median(self.word_dict.values())

    def find_average(self) -> float:
            return len(self.res_str)/(self.str_input.count('.') + self.str_input.count('?') + self.str_input.count('!'))

    def find_ngrams(self):
        joined_str = ""
        for i in range(len(self.res_str)):
            joined_str += self.res_str[i]
        for i in range(len(joined_str)):
            if (i + self.N) > len(joined_str):
                break
            ngram = joined_str[i:i + self.N]
            if not self.ngrams_dict.get(ngram):
                self.ngrams_dict[ngram] = 1
            else:
                self.ngrams_dict[ngram] += 1

    def print_top_k(self):
        sorted_dict = dict()
        sorted_keys = sorted(self.ngrams_dict, key=self.ngrams_dict.get, reverse=True)
        k = 0
        for key in sorted_keys:
            sorted_dict[key] = self.ngrams_dict[key]
        for key in sorted_keys:
            print(key, sorted_dict[key])
            if k == self.K:
                break
            k += 1
