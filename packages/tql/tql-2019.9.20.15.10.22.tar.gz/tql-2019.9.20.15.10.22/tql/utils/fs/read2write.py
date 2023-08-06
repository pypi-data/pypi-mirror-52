#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'read2write'
__author__ = 'JieYuan'
__mtime__ = '19-3-15'
"""

from tqdm import tqdm


def read2write(input_file, output_file, progress_func=lambda x: x, lower=True, overwrite=True):
    with open(input_file, 'r', encoding='utf8') as input, \
            open(output_file, 'w' if overwrite else 'a', encoding='utf8') as output:
        for line in tqdm(input):
            if line:
                _ = progress_func(line.lower() if lower else line).strip()
                if _:
                    output.write(_ + '\n')


if __name__ == '__main__':
    read2write('/Users/yuanjie/Desktop/notebook/0_MI/training/17/part-00000',
               '/Users/yuanjie/Desktop/notebook/0_MI/test.json',
               lambda x: str(eval(x)))
