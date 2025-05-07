import sys
from typing import List, Tuple


def string_to_list(input_string: str) -> List[int]:
    list_num = [int(x) for x in input_string.split(
        ", ")]  # Так как в условие сказано что будут числа можем не проверять на это и сразу их преобразовывать

    return list_num


def find_even_num(input_list: List[int]) -> List[int]:
    res_list = []

    for num in input_list:
        if num % 2 == 0:
            res_list.append(num)

    return res_list


# Можно использовать min(input_list) и max(input_list), но это слишком тривиально, поэтому я напишу свою реализацию
def find_min_and_max_num(input_list: List[int]) -> Tuple[int, int]:
    min_num = sys.maxsize
    max_num = -sys.maxsize

    for num in input_list:
        if num < min_num:
            min_num = num
        if num > max_num:
            max_num = num

    return min_num, max_num


# Обычная быстрая сортировка, её сложность в среднем n*lon(n)
def sort_list_asc(input_list: List[int]) -> List[int]:
    if len(input_list) <= 1:
        return input_list

    pivot = input_list[len(input_list) // 2]

    left = [x for x in input_list if x < pivot]

    middle = [x for x in input_list if x == pivot]

    right = [x for x in input_list if x > pivot]

    return sort_list_asc(left) + middle + sort_list_asc(right)


if __name__ == '__main__':
    input_str = input()

    int_list = string_to_list(input_str)
    print(f"Четные числа: {find_even_num(int_list)}")

    tuple_num_max_min = find_min_and_max_num(int_list)
    print(f"Максимальное число: {tuple_num_max_min[0]}")
    print(f"Минимальное число: {tuple_num_max_min[1]}")

    print(f"Отсортированный список: {sort_list_asc(int_list)}")