import sys
import re


class ChronospatialComputer:
    def __init__(self, program, a=0, b=0, c=0):
        self.inst = 0
        self.program = program
        self.registers = {"A": a, "B": b, "C": c}
        self.reg_map = {4: "A", 5: "B", 6: "C"}
        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        self.output = []

    def combo(self, operand: int) -> int:
        if operand <= 3:
            return operand
        return self.registers[self.reg_map[operand]]

    def adv(self, operand: int) -> int:
        self.registers["A"] //= 2 ** self.combo(operand)
        return 2

    def bxl(self, operand: int) -> int:
        self.registers["B"] ^= operand
        return 2

    def bst(self, operand: int) -> int:
        self.registers["B"] = self.combo(operand) % 8
        return 2

    def jnz(self, operand: int) -> int:
        return 2 if self.registers["A"] == 0 else operand - self.inst

    def bxc(self, _: int) -> int:
        self.registers["B"] ^= self.registers["C"]
        return 2

    def out(self, operand: int) -> int:
        self.output.append(str(self.combo(operand) % 8))
        return 2

    def bdv(self, operand: int) -> int:
        self.registers["B"] = self.registers["A"] // (2 ** self.combo(operand))
        return 2

    def cdv(self, operand: int) -> int:
        self.registers["C"] = self.registers["A"] // (2 ** self.combo(operand))
        return 2

    def run(self):
        while self.inst < len(self.program) - 1:
            opcode, operand = self.program[self.inst : self.inst + 2]
            self.inst += self.opcodes[opcode](operand)

        print(",".join(self.output))

    def self_referential(self) -> int:
        A = []
        i = -1
        start = 0
        while i >= -len(self.program):
            # because there's a single 0,3 op in the program
            A += ["0", "0", "0"]
            found = False
            for d in range(start, 8):
                a = int("".join(A), 2) + d
                # manual evaluation of the input program code
                if (((d ^ 1) ^ (a >> (d ^ 1))) ^ 4) % 8 == self.program[i]:
                    found = True
                    break
            if found:
                start = 0
                i -= 1
                j = -1
                while d > 0:
                    if d % 2 == 1:
                        A[j] = "1"
                    j -= 1
                    d >>= 1
            else:
                i += 1
                start = int("".join(A[-6:-3]), 2) + 1
                A = A[:-6]

        return int("".join(A), 2)


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as f:
        vals = list(map(int, re.findall(r"\d+", f.read())))

    comp = ChronospatialComputer(vals[3:], a=vals[0], b=vals[1], c=vals[2])
    comp.run()
    a_self = comp.self_referential()
    print(a_self)
    print(",".join(map(str, vals[3:])))
    comp = ChronospatialComputer(vals[3:], a=a_self, b=vals[1], c=vals[2])
    comp.run()
