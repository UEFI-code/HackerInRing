from typing import Any


ins_Dict = {
    'sayhello': [0,'print("Hello, World!")'],
    'nop': [0, 'pass'],
    'sleep': [0, 'import time\ntime.sleep(1)'],
    'jmp': [1],
    'writemem': [1],
    'readmem': [1],
    'ret': [2],
    'sysenter': [3],
    'call': [4],
}

class myVM:
    def __init__(self, mem):
        self.ins_Dict = {
            'sayhello': [0,'print("Hello, World!")'],
            'nop': [0, 'pass'],
            'sleep': [0, 'import time\ntime.sleep(1)'],
            'jmp': [1],
            'writemem': [1],
            'readmem': [1],
            'ret': [2],
            'sysenter': [3],
            'call': [4],
            'getmember': [5],
            'kill': [6],
            'humanloop': [7],
        }
        self.mem = mem
        self.pc = 0
        self.sp = 0
        self.bp = 0
    
    def crash_handler(self):
        print('Oh my Emperor! The palace is collapsing!\nSave the empire!')
        self.run_cmd_humanloop()

    def run_cmd(self):
        while self.pc < len(self.mem):
            preprocess_cmd = self.mem[self.pc].split(' ')
            if preprocess_cmd[0] in ins_Dict:
                print(f'PC: {self.pc}, Running command: {preprocess_cmd}')
                cmd_type = ins_Dict[preprocess_cmd[0]][0]
                if cmd_type == 0:
                    exec(ins_Dict[preprocess_cmd[0]][1])
                self.pc += 1
            else:
                print('Unknown command: ' + preprocess_cmd[0])
        print('Code Pointer out of range!')
        self.crash_handler()
        
    def run_cmd_humanloop(self):
        while True:
            cmd = input('Enter command: ')
            preprocessed_cmd = cmd.split(' ')
            if preprocessed_cmd[0] in ins_Dict:
                print(f'Running command: {preprocessed_cmd}')
                cmd_type = ins_Dict[preprocessed_cmd[0]][0]
                if cmd_type == 0:
                    exec(ins_Dict[preprocessed_cmd[0]][1])
                elif cmd_type == 1:
                    self.pc = int(preprocessed_cmd[1])
                    if self.pc < 0 or self.pc >= len(self.mem):
                        print('Invalid address')
                        self.pc = 0
                        continue
                    sure = input(f'Are you sure you want to jump to {self.pc}? (y/n): ')
                    if sure == 'n':
                        self.pc = 0
                        print('You are so cowardly!!!')
                        continue
                    print('Jumping to ' + str(self.pc))
                    self.run_cmd()
            else:
                print('Unknown command: ' + preprocessed_cmd[0])

if __name__ == '__main__':
    mem = ['nop'] * 128
    vm = myVM(mem)
    vm.run_cmd_humanloop()