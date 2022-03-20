import os
from func import Words
try:
    N: int = int(input("Enter N: "))
    K: int = int(input("Enter K: "))
    if N == 0 or K == 0:
        raise ValueError("Incorrect input")
    with open(r'/lab_1/Text.txt', encoding="utf8") as file_to_open:
        if os.path.getsize('/lab_1/Text.txt') == 0:
            raise EOFError("File is empty")
        str_input: str = file_to_open.read()
        words: Words = Words(str_input, K, N)
        words.count_words()
        words.print_dictionary()
        print(f"\nMedian: {words.find_median()}")
        print(f"Average: {words.find_average()}\n")
        words.find_ngrams()
        words.print_top_k()
        file_to_open.close()

except ValueError as value_error:
    print(value_error)

except EOFError as exception:
    print(exception)
