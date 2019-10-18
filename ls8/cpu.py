"""CPU functionality."""

import sys

LDI  = 0b10000010
PRN  = 0b01000111
HLT  = 0b00000001
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
ADD  = 0b10100000
RET  = 0b00010001
CMP  = 0b10100111
JEQ  = 0b01010101
JNE  = 0b01010110
JMP  = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = 7
        self.fl = [0] * 8 #00000LGE


    def load(self, file):
        """Load a program into memory."""

        try:
            address = 0
            with open(file) as f:
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#")

                    # Convert any numbers from binary strings to integers
                    num = comment_split[0].strip()
                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue

                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):

        return self.ram[address]

    def ram_write(self, address, value):

        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
    # Do stuff
            command = self.ram[self.pc]

            if command == LDI: #LDI, needs register and numer
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                self.pc += 3

            elif command == PRN: #PRN, needs register to print
                print(self.reg[self.ram[self.pc+1]])
                self.pc += 2

            elif command == HLT:
                running = False
                self.pc += 1

            elif command == CMP:
                self.fl[7] = 0
                self.fl[6] = 0
                self.fl[5] = 0

                a = self.reg[self.ram[self.pc+1]]
                b = self.reg[self.ram[self.pc+2]]

                if a == b:
                    self.fl[7] = 1
                elif a > b: 
                    self.fl[6] = 1
                else:
                    self.fl[5] = 1

                self.pc += 3
       
            elif command == JEQ:
                if self.fl[7] == 1:
                    self.pc = self.reg[self.ram[self.pc+1]]
                else:
                    self.pc += 2
            
            elif command == JNE:
                if self.fl[7] == 0:
                    self.pc = self.reg[self.ram[self.pc+1]]
                else:
                    self.pc += 2
                    
            elif command == JMP:           
                self.pc = self.reg[self.ram[self.pc+1]]
            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)