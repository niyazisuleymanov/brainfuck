#!/usr/bin/env python3
import os
import sys

CELL_SIZE = 9.223372036854776e+18

def format(code: str) -> str:
  commands = ['>', '<', '+', '-', '.', ',', '[', ']']
  return ''.join(filter(lambda x: x in commands, code))

def run(filename: str) -> None:
  if not os.path.isfile(filename):
    print(f'No file named "{filename}" was found')
  else:
    with open(filename, 'r') as input_stream:
      code, lines = '', input_stream.readlines()
      for line in lines:
        code += line
      process(format(code))

def safe_pop(stack: list[str], index: int) -> int:
  try:
    return stack.pop()
  except IndexError:
    print(f'Mismatched bracket: command number {index + 1}.')
    exit()

def locate_brackets(code: str) -> list[int]:
  loop_brackets, brackets = [], [-1] * len(code)

  for position, command in enumerate(code):
    if command == '[':
      loop_brackets.append(position)
    if command == ']':
      start = safe_pop(loop_brackets, position)
      brackets[start] = position
      brackets[position] = start
  return brackets

def process(code: str) -> None:
  cells, cell_ptr, code_ptr, brackets = [0], 0, 0, locate_brackets(code)

  while code_ptr < len(code):
    if code[code_ptr] == '>':
      cell_ptr += 1
      if cell_ptr == len(cells): cells.append(0)

    elif code[code_ptr] == '<':
      if cell_ptr == 0: cell_ptr = 0
      else: cell_ptr -= 1

    elif code[code_ptr] == '+':
      if cells[cell_ptr] == CELL_SIZE - 1: 
        print('Maximum cell size overflow.')
        cells[cell_ptr] = -CELL_SIZE
      else: 
        cells[cell_ptr] += 1

    elif code[code_ptr] == '-':
      if cells[cell_ptr] == -CELL_SIZE: 
        print('Minimum cell size overflow.')
        cells[cell_ptr] = CELL_SIZE - 1
      else: 
        cells[cell_ptr] -= 1
      
    elif code[code_ptr] == '.':
      print(chr(cells[cell_ptr]), end='')  

    elif code[code_ptr] == ',':
      cells[cell_ptr] = int(input())

    elif code[code_ptr] == '[' and cells[cell_ptr] == 0:
      code_ptr = brackets[code_ptr]

    elif code[code_ptr] == ']' and cells[cell_ptr] != 0: 
      code_ptr = brackets[code_ptr]

    code_ptr += 1

def main():
  if len(sys.argv) == 2: run(sys.argv[1])
  else: print(f'Usage: {sys.argv[0]} filename')

if __name__ == '__main__': main()
