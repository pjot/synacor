def parse_file():
    m = []
    with open('challenge.bin', 'rb') as f:
        bs = f.read(2)
        while bs:
            m.append(int.from_bytes(bs, 'little'))
            bs = f.read(2)
    return m


class Computer:
    def __init__(self, program):
        self.position = 0
        self.registers = [0] * 8
        self.stack = []
        self.inputs = []
        self.tape = {k: v for k, v in enumerate(program)}

    def read(self, delta=0):
        return self.tape.get(self.position + delta)

    def value(self, pos):
        if pos < 32768:
            return pos
        return self.registers[pos - 32768]

    def write(self, register, value):
        self.registers[register - 32768] = value

    def run(self):
        while True:
            op_code = self.read()

            if op_code == 0:
                return

            if op_code == 1:
                a = self.read(1)
                b = self.read(2)
                self.write(a, self.value(b))
                self.position += 3

            elif op_code == 2:
                a = self.read(1)
                self.stack.append(self.value(a))
                self.position += 2

            elif op_code == 3:
                a = self.read(1)
                self.write(a, self.stack.pop())
                self.position += 2

            elif op_code == 4:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = 1 if self.value(b) == self.value(c) else 0
                self.write(a, value)
                self.position += 4

            elif op_code == 5:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = 1 if self.value(b) > self.value(c) else 0
                self.write(a, value)
                self.position += 4

            elif op_code == 6:
                a = self.read(1)
                self.position = a

            elif op_code == 7:
                a = self.read(1)
                b = self.read(2)
                if self.value(a) != 0:
                    self.position = self.value(b)
                else:
                    self.position += 3

            elif op_code == 8:
                a = self.read(1)
                b = self.read(2)
                if self.value(a) == 0:
                    self.position = self.value(b)
                else:
                    self.position += 3

            elif op_code == 9:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = (self.value(b) + self.value(c)) % 32768
                self.write(a, value)
                self.position += 4

            elif op_code == 10:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = (self.value(b) * self.value(c)) % 32768
                self.write(a, value)
                self.position += 4

            elif op_code == 11:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = self.value(b) % self.value(c)
                self.write(a, value)
                self.position += 4

            elif op_code == 12:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = self.value(b) & self.value(c)
                self.write(a, value)
                self.position += 4

            elif op_code == 13:
                a = self.read(1)
                b = self.read(2)
                c = self.read(3)
                value = self.value(b) | self.value(c)
                self.write(a, value)
                self.position += 4

            elif op_code == 14:
                a = self.read(1)
                b = self.read(2)
                value = self.value(b)^(2**15 -1)
                self.write(a, value)
                self.position += 3

            elif op_code == 15:
                a = self.read(1)
                b = self.read(2)
                self.write(a, self.tape[self.value(b)])
                self.position += 3

            elif op_code == 16:
                a = self.read(1)
                b = self.read(2)
                self.tape[self.value(a)] = self.value(b)
                self.position += 3

            elif op_code == 17:
                a = self.read(1)
                self.stack.append(self.position + 2)
                self.position = self.value(a)

            elif op_code == 18:
                self.position = self.stack.pop()

            elif op_code == 19:
                a = self.read(1)
                print(chr(self.value(a)), end='')
                self.position += 2

            elif op_code == 20:
                a = self.read(1)
                if not self.inputs:
                    vals = input('> ')
                    self.inputs = [ord(c) for c in vals]
                    self.inputs.append(ord('\n'))
                val = self.inputs.pop(0)
                self.write(a, val)
                self.position += 2

            elif op_code == 21:
                self.position += 1

            else:
                raise Exception('MISSING', op_code)


c = Computer(parse_file())
print('running')
c.run()

