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
        }
        self.mem = mem
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pc = 0
        self.sp = 0
        self.bp = 0
        self.flags = [0, 0, 0, 0, 0, 0, 0, 0]

    def run_cmd_dummy(self, cmd):
        preprocessed_cmd = cmd.split(' ')
        if preprocessed_cmd[0] in ins_Dict:
            print(f'Running command: {preprocessed_cmd}')
            cmd_type = ins_Dict[preprocessed_cmd[0]][0]
            if cmd_type == 0:
                exec(ins_Dict[preprocessed_cmd[0]][1])
            elif cmd_type == 1:
                print('Command not implemented yet')
        else:
            print('Unknown command: ' + preprocessed_cmd[0])

if __name__ == '__main__':
    mem = 'nop\n' * 128
    vm = myVM(mem)
    while True:
        cmd = input('Enter command: ')
        vm.run_cmd_dummy(cmd)