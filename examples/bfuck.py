from interpreters import BrainFuckInterpreter

HELLO_WORLD = "+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-."

if __name__ == '__main__':
    interpreter = BrainFuckInterpreter(HELLO_WORLD)
    interpreter.execute()
