#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
from timeit import timeit


def get_content(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n')
        content = [int(item) for item in content]
        return content


def split_content(content, parts=2):
    times = int(len(content) / parts)
    split_index = [times * part for part in range(parts)]
    return [content[i:j] for i, j in zip(split_index, split_index[1:] + [])]


def run_split(split, full, func):
    processes = []
    queue = Queue()
    result = []
    # full = [el for sublist in split for el in sublist]
    for sublist in split:
        p = Process(target=func, args=(full, queue, sublist))
        processes.append(p)
        p.start()
    for _ in processes:
        result.append(queue.get())
    for p in processes:
        p.join()
    result = [el for el in result if el is not None][0]
    return result
        

def run2(content, queue=None, sublist=None):
    result = [(item1, item2)
              for item1 in sublist or content
              for item2 in content
              if item1 + item2 == 2020]
    if not queue:
        return result[0]
    queue.put(result[0] if len(result) else None)


def run3(content, queue=None, sublist=None):
    result = [(item1, item2, item3)
              for item1 in sublist or content
              for item2 in content
              for item3 in content
              if item1 + item2 + item3 == 2020]
    if not queue:
        return result[0]
    queue.put(result[0] if len(result) else None)


def multiply_list(content):
    result = 1
    for el in content:
        result *= el
    return result


def printer(index, res, perf):
    perf = str(perf)[:10]
    res = multiply_list(res)
    print(f'problem {index} - the solution is: {res} (speed: {perf})')


if __name__ == '__main__':
    full_list = get_content('input')
    split_list = split_content(full_list, 8)

    print(f'{" MULTIPROCESSING ":~^57}')
    printer(1, run_split(split_list, full_list, run2),
            timeit(lambda: run_split(split_list, full_list, run2), number=1))
    printer(2, run_split(split_list, full_list, run3),
            timeit(lambda: run_split(split_list, full_list, run3), number=1))

    print(f'{" SINGLE PROCESSING ":~^57}')
    printer(1, run2(full_list), timeit(lambda: run2(full_list), number=1))
    printer(2, run3(full_list), timeit(lambda: run3(full_list), number=1))
