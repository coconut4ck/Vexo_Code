import sys
import os
from pathlib import Path
import ctypes
import tkinter as tk
from tkinter import filedialog

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

current_dir = os.path.dirname(os.path.abspath(__file__))
vexo_studio_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(vexo_studio_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from Lexer import Lexer
    from Parser import Parser
    from Interpreter import Interpreter

    print("Core modules imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    input("Press Enter to exit...")
    sys.exit(1)


def select_file_dialog():
    root = tk.Tk()
    root.tk.call('tk', 'scaling', 1.0)
    root.attributes('-topmost', True)
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Vexo File to Run",
        filetypes=[
            ("Vexo files", "*.vexo"),
            ("All files", "*.*")
        ]
    )

    root.destroy()
    return file_path


def run_file(file_path):
    if not file_path:
        print("No file selected")
        return False

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    try:
        print(f"\nRunning: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()

        print("\nExecution completed successfully")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    print("=" * 50)
    print("VEXO INTERPRETER")
    print("=" * 50)

    while True:
        file_path = None

        if len(sys.argv) >= 2 and file_path is None:
            file_path = sys.argv[1]
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                file_path = None

        if not file_path:
            print("Opening file selection dialog...")
            file_path = select_file_dialog()

        if file_path:
            run_file(file_path)

            print("\n" + "=" * 50)
            print("OPTIONS:")
            print("1. Run again")
            print("2. Exit")
            print("=" * 50)

            while True:
                choice = input("Enter your choice (1-2): ").strip()

                if choice == "1":
                    break
                elif choice == "2":
                    print("\nGoodbye!")
                    return
        else:
            print("No file selected. Exiting.")
            return


if __name__ == "__main__":
    main()
