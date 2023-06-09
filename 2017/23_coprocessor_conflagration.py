#############################################
# --- Day 23: Coprocessor Conflagration --- #
#############################################

import AOCUtils

class Program:
    def __init__(self, code, mode=0):
        self.pc = 0
        self.code = code
        
        self.registers = {r: 0 for r in 'abcdefgh'}
        self.registers['a'] = mode
        
        self.mul_count = 0

    def run(self):
        while self.pc < len(self.code):
            # print(self.pc, '=>', self.code[self.pc])
            
            cmd = self.code[self.pc].split()

            inst = cmd[0]

            x = cmd[1]
            if x.isalpha() and x not in self.registers:
                self.registers[x] = 0
            x_val = int(x) if not x.isalpha() else self.registers[x]

            y = cmd[2]
            if y.isalpha() and y not in self.registers:
                self.registers[y] = 0
            y_val = int(y) if not y.isalpha() else self.registers[y]

            if inst == 'set':
                self.registers[x] = y_val
            elif inst == 'sub':
                self.registers[x] -= y_val
            elif inst == 'mul':
                self.registers[x] *= y_val
                self.mul_count += 1
            elif inst == 'jnz':
                if x_val != 0:
                    self.pc += y_val - 1

            # print(' | '.join(k+': '+'{:<7}'.format(str(v)) for k, v in self.registers.items()))

            self.pc += 1

def is_prime(n):
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

#############################################

code = AOCUtils.load_input(23)

program = Program(code)
program.run()
AOCUtils.print_answer(1, program.mul_count)

# program = Program(code, 1)
# program.run()
# AOCUtils.print_answer(2, program.registers['h']))

b0 = int(code[0].split()[-1]) * 100 + 100000

non_primes_amount = 0
for b in range(b0, b0+17000+1, 17):
    if not is_prime(b):
        non_primes_amount += 1

AOCUtils.print_answer(2, non_primes_amount)

AOCUtils.print_time_taken()

'''
  0 | set b 81      |                       |
  1 | set c b       |                       |
  2 | jnz a 2       |                       |
  3 | jnz 1 5       |                       |
  4 | mul b 100     |                       |
  5 | sub b -100000 | b = 108100            |
  6 | set c b       |                       |
  7 | sub c -17000  | c = 125100            | constant
  8 | set f 1       | f = 1 <<<<<<<<<<<<<<< | flag
  9 | set d 2       | d = 2               ^ | counter in [2, b]
 10 | set e 2       | e = 2 <<<<<<<<<<<<  ^ | counter in [2, b]
 11 | set g d       | <<<<<<<<<<<<<<<  ^  ^ |
 12 | mul g e       |               ^  ^  ^ |
 13 | sub g b       |               ^  ^  ^ | inner loop: range(2, b) # O(b)
 14 | jnz g 2       | if d*e == b:  ^  ^  ^ | middle loop: range(2, b) # O(b)
 15 | set f 0       |    f = 0      ^  ^  ^ | outer loop: range(b, b+17000+1, 17) # 1000x
 16 | sub e -1      | e += 1        ^  ^  ^ |
 17 | set g e       |               ^  ^  ^ | 
 18 | sub g b       |               ^  ^  ^ |
 19 | jnz g -8      | if e != b: >>>>  ^  ^ |
 20 | sub d -1      | d += 1           ^  ^ |
 21 | set g d       |                  ^  ^ |
 22 | sub g b       |                  ^  ^ |
 23 | jnz g -13     | if d != b: >>>>>>^  ^ |
 24 | jnz f 2       | if f == 0:          ^ | check if d*e == b in any of
 25 | sub h -1      |    h += 1           ^ | the innermost iterations (pc 14)
 26 | set g b       |                     ^ |
 27 | sub g c       |                     ^ |
 28 | jnz g 2       | if b != c:          ^ |
 29 | jnz 1 3       |                     ^ |
 30 | sub b -17     |    b += 17          ^ |
 31 | jnz 1 -23     |    >>>>>>>>>>>>>>>>>> |
'''