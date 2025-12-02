#! /usr/bin/python3
import random

filename = f'README_{random.random()}.md'
with open(filename, 'a+') as f:
    f.write(f'\nHello\n')
