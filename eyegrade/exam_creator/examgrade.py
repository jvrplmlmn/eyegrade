import sys
import exam_gui as gui

def main():
    if len(sys.argv) >= 2:
        file = sys.argv[1]
    else:
        file = None
    interface = gui.Interface(file, [])
    interface.run()


if __name__ == '__main__':
    main()