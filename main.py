from typing import Any

class myVM:
    def __init__(self, mem):
        self.ins_Dict = {
            'sayhello': [0,'print("Hello, World!")'],
            'printpc': [0, 'print(self.pc)'],
            'printretaddr': [0, 'print(self.ret_addr)'],
            'printmemsize': [0, 'print(len(self.mem))'],
            'nop': [0, 'pass'],
            'sleep': [0, 'import time\ntime.sleep(1)'],
            'jmp': [1],
            'writemem': [2],
            'readmem': [3],
            'ret': [4],
            'sysenter': [5],
            'call': [6],
            'getmember': [7],
            'kill': [8],
            'humanloop': [9],
        }
        self.mem = mem
        self.ret_addrs = [0] * 128
        self.syscall_table = [0] * 128
        self.pc = 0
        self.supareg = [0] * 128
    
    def crash_handler(self):
        print('Oh my Emperor! The palace is collapsing!\nSave the empire!')
        self.run_cmd_humanloop()

    def run_cmd(self):
        try:
            while self.pc < len(self.mem):
                preprocess_cmd = self.mem[self.pc].split(' ')
                if preprocess_cmd[0] in self.ins_Dict:
                    print(f'PC: {self.pc}, Running command: {preprocess_cmd}')
                    cmd_type = self.ins_Dict[preprocess_cmd[0]][0]
                    if cmd_type == 0:
                        exec(self.ins_Dict[preprocess_cmd[0]][1])
                    elif cmd_type == 1:
                        self.pc = int(preprocess_cmd[1])
                        if self.pc < 0 or self.pc >= len(self.mem):
                            print('Code Pointer out of range!')
                            self.crash_handler()
                        print('Jumping to ' + str(self.pc))
                        continue
                    elif cmd_type == 2:
                        addr = int(preprocess_cmd[1])
                        val = ' '.join(preprocess_cmd[2:])
                        if addr < 0 or addr >= len(self.mem):
                            print('Memory address out of range!')
                            self.crash_handler()
                        self.mem[addr] = val
                        print('Writing ' + str(val) + ' to addr ' + str(addr))
                    elif cmd_type == 3:
                        addr = int(preprocess_cmd[1])
                        if addr < 0 or addr >= len(self.mem):
                            print('Memory address out of range!')
                            self.crash_handler()
                        print(f'Memory value at {addr}: {self.mem[addr]}')
                    elif cmd_type == 4:
                        self.pc = self.ret_addrs.pop()
                        if self.pc < 0 or self.pc >= len(self.mem):
                            print('Code Pointer out of range!')
                            self.crash_handler()
                        print('Returning to ' + str(self.pc))
                        continue
                    elif cmd_type == 5:
                        syscall_num = int(preprocess_cmd[1])
                        if syscall_num < 0 or syscall_num >= len(self.syscall_table):
                            print('Invalid syscall number!')
                            self.crash_handler()
                        callpc = self.syscall_table[syscall_num]
                        if callpc < 0 or callpc >= len(self.mem):
                            print('Code Pointer out of range!')
                            self.crash_handler()
                        self.ret_addrs.append(self.pc + 1)
                        self.pc = callpc
                        print('Entering syscall ' + str(syscall_num) + ' at ' + str(self.pc))
                        continue
                    elif cmd_type == 6:
                        addr = int(preprocess_cmd[1])
                        if addr < 0 or addr >= len(self.mem):
                            print('Code Pointer out of range!')
                            self.crash_handler()
                        self.ret_addrs.append(self.pc + 1)
                        self.pc = addr
                        print('Calling ' + str(addr))
                        continue
                    elif cmd_type == 9:
                        self.run_cmd_humanloop()
                    self.pc += 1
                else:
                    print('Unknown command: ' + preprocess_cmd[0])
                    self.crash_handler()
            print('Code Pointer out of range!')
            self.crash_handler()
        except Exception as e:
            print('Error: ' + str(e))
            self.crash_handler()
        
    def run_cmd_humanloop(self):
        try:
            while True:
                cmd = input('Enter command: ')
                preprocessed_cmd = cmd.split(' ')
                if preprocessed_cmd[0] in self.ins_Dict:
                    print(f'Running command: {preprocessed_cmd}')
                    cmd_type = self.ins_Dict[preprocessed_cmd[0]][0]
                    if cmd_type == 0:
                        exec(self.ins_Dict[preprocessed_cmd[0]][1])
                    elif cmd_type == 1:
                        self.pc = int(preprocessed_cmd[1])
                        if self.pc < 0 or self.pc >= len(self.mem):
                            print('Invalid address')
                            continue
                        sure = input(f'Are you sure you want to jump to {self.pc}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        print('Jumping to ' + str(self.pc))
                        self.run_cmd()
                    elif cmd_type == 2:
                        addr = int(preprocessed_cmd[1])
                        val = ' '.join(preprocessed_cmd[2:])
                        if addr < 0 or addr >= len(self.mem):
                            print('Invalid address')
                            continue
                        self.mem[addr] = val
                        print('Writing ' + str(val) + ' to addr ' + str(addr))
                    elif cmd_type == 3:
                        addr = int(preprocessed_cmd[1])
                        if addr < 0 or addr >= len(self.mem):
                            print('Invalid address')
                            continue
                        print(f'Memory value at {addr}: {self.mem[addr]}')
                    elif cmd_type == 4:
                        self.pc = self.ret_addrs.pop()
                        if self.pc < 0 or self.pc >= len(self.mem):
                            print('Invalid address')
                            continue
                        sure = input(f'Are you sure you want to return to {self.pc}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        print('Returning to ' + str(self.pc))
                        self.run_cmd()
                    elif cmd_type == 5:
                        syscall_num = int(preprocessed_cmd[1])
                        if syscall_num < 0 or syscall_num >= len(self.syscall_table):
                            print('Invalid syscall number!')
                            continue
                        callpc = self.syscall_table[syscall_num]
                        if callpc < 0 or callpc >= len(self.mem):
                            print('Invalid address')
                            continue
                        sure = input(f'Are you sure you want to enter syscall {syscall_num} at {callpc}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        self.pc = callpc
                        print('Entering syscall ' + str(syscall_num) + ' at ' + str(self.pc))
                        self.run_cmd()
                    elif cmd_type == 6:
                        addr = int(preprocessed_cmd[1])
                        if addr < 0 or addr >= len(self.mem):
                            print('Invalid address')
                            continue
                        sure = input(f'Are you sure you want to call {addr}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        self.pc = addr
                        print('Calling ' + str(addr))
                        self.run_cmd()
                    elif cmd_type == 9:
                        print('Stupid human, you cannot run humanloop in humanloop!')
                else:
                    print('Unknown command: ' + preprocessed_cmd[0])
        except Exception as e:
            print('Error: ' + str(e))
            self.crash_handler()

if __name__ == '__main__':
    mem = ['nop'] * 128
    vm = myVM(mem)
    vm.run_cmd_humanloop()