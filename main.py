from typing import Any
import traceback
import time

class myVM:
    def __init__(self, mem):
        self.ins_Dict = {
            'sayhello': [0,'print("Hello, World!")'],
            'printpc': [0, 'print(self.pc)'],
            'printmemsize': [0, 'print(len(self.mem))'],
            'printbacktrace': [0, "print(''.join(traceback.format_stack()))"],
            'nop': [0, 'pass'],
            'sleep': [0, 'time.sleep(1)'],
            'jmp': [1],
            'writemem': [2],
            'readmem': [3],
            'ret': [4],
            'sysenter': [5],
            'call': [6],
            'humanloop': [7],
            'printretaddr': [8],
            'printsyscalltable': [9],
            'printsupareg': [10],
            'setretaddr': [11],
            'setsyscalltable': [12],
            'setsupareg': [13],
            'getmember': [],
            'kill': [],
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
                        addr = int(preprocess_cmd[1])
                        if addr < 0 or addr >= len(self.mem):
                            print('Code Pointer out of range!')
                            self.crash_handler()
                        self.pc = addr
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
                        addr = self.ret_addrs.pop()
                        if addr < 0 or addr >= len(self.mem):
                            print('Code Pointer out of range!')
                            self.crash_handler()
                        self.pc = addr
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
                    elif cmd_type == 7:
                        self.run_cmd_humanloop()
                    elif cmd_type == 8:
                        index = int(preprocess_cmd[1])
                        print(f'Return address at {index}: {self.ret_addrs[index]}')
                    elif cmd_type == 9:
                        index = int(preprocess_cmd[1])
                        print(f'Syscall table at {index}: {self.syscall_table[index]}')
                    elif cmd_type == 10:
                        index = int(preprocess_cmd[1])
                        print(f'Supareg at {index}: {self.supareg[index]}')
                    elif cmd_type == 11:
                        index = int(preprocess_cmd[1])
                        val = int(preprocess_cmd[2])
                        self.ret_addrs[index] = val
                        print(f'Setting return address at {index} to {val}')
                    elif cmd_type == 12:
                        index = int(preprocess_cmd[1])
                        val = int(preprocess_cmd[2])
                        self.syscall_table[index] = val
                        print(f'Setting syscall table at {index} to {val}')
                    elif cmd_type == 13:
                        index = int(preprocess_cmd[1])
                        val = ' '.join(preprocess_cmd[2:])
                        self.supareg[index] = val
                        print(f'Setting supareg at {index} to {val}')
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
                        addr = int(preprocessed_cmd[1])
                        if addr < 0 or addr >= len(self.mem):
                            print('Invalid address')
                            continue
                        sure = input(f'Are you sure you want to jump to {self.pc}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        self.pc = addr
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
                        addr = self.ret_addrs.pop()
                        if addr < 0 or addr >= len(self.mem):
                            print('Return to Invalid address')
                            continue
                        sure = input(f'Are you sure you want to return to {self.pc}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        self.pc = addr
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
                            print('Call Invalid address')
                            continue
                        sure = input(f'Are you sure you want to call {addr}? (y/n): ')
                        if sure == 'n':
                            print('You are so cowardly!!!')
                            continue
                        self.pc = addr
                        print('Calling ' + str(addr))
                        self.run_cmd()
                    elif cmd_type == 7:
                        print('Stupid human, you cannot run humanloop in humanloop!')
                    elif cmd_type == 8:
                        index = int(preprocessed_cmd[1])
                        print(f'Return address at {index}: {self.ret_addrs[index]}')
                    elif cmd_type == 9:
                        index = int(preprocessed_cmd[1])
                        print(f'Syscall table at {index}: {self.syscall_table[index]}')
                    elif cmd_type == 10:
                        index = int(preprocessed_cmd[1])
                        print(f'Supareg at {index}: {self.supareg[index]}')
                    elif cmd_type == 11:
                        index = int(preprocessed_cmd[1])
                        val = int(preprocessed_cmd[2])
                        self.ret_addrs[index] = val
                        print(f'Setting return address at {index} to {val}')
                    elif cmd_type == 12:
                        index = int(preprocessed_cmd[1])
                        val = int(preprocessed_cmd[2])
                        self.syscall_table[index] = val
                        print(f'Setting syscall table at {index} to {val}')
                    elif cmd_type == 13:
                        index = int(preprocessed_cmd[1])
                        val = ' '.join(preprocessed_cmd[2:])
                        self.supareg[index] = val
                        print(f'Setting supareg at {index} to {val}')
                else:
                    print('Unknown command: ' + preprocessed_cmd[0])
        except Exception as e:
            print('Error: ' + str(e))
            self.crash_handler()

if __name__ == '__main__':
    mem = ['nop'] * 128
    vm = myVM(mem)
    vm.run_cmd_humanloop()