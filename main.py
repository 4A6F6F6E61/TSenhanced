from io import TextIOWrapper
import os
import sys
import time
import re
from decimal import Context
from os.path import exists

def single_file(f: str, output_dir: str = "output/"):
    if f.endswith(".tsa"):
        with open(f, "r") as file_:
            start_time = time.perf_counter()
            remove_files(f"./{output_dir}")
            with open( f"{output_dir + f[:-4]}.ts", "x") as open_out:
                compile(file_, open_out)
            process_time = ((time.perf_counter() - start_time)*1000)
            print(f"[INFO]: Successfully Compiled {file_.name} in {Context(prec=1).create_decimal(process_time)}ms")
            print("[INFO]: Deno Output:")
            print("--------------------")
            out = os.system(f"deno run {output_dir + f[:-4]}.ts")
            print("--------------------")

def multiple_files(output_dir: str = "output/"):
    remove_files(f"./{output_dir}")
    count: int = 0
    files: list[str] = os.listdir(sys.argv[2])
    for f in files:
        if f.endswith(".tsa"):
            count += 1
            with open(f, "r") as file_:
                start_time = time.perf_counter()
                compile(file_, open(f"{output_dir + f[:-4]}.ts", "x"))
                process_time = ((time.perf_counter() - start_time)*1000)
                print(f"[INFO]: Successfully Compiled {file_.name} in {Context(prec=1).create_decimal(process_time)}ms")

        else:
            continue
    assert count != 0, "ERROR: no .tsa file found"

def compile(file_: TextIOWrapper, output: TextIOWrapper):
    for line in file_:
        line: str = line.lstrip()                       # remove whitespace from the left
        rm: tuple = remove_string(line)                 # remove string from line
        line: str = rm[0]                               # Line without String
        str_: str = rm[1]                               # String without Line

        if line.startswith("if "):
            line = "if(" + line[3:]                     # replace 'if ' with 'if('
            line = line[:-2] + ") {\n"                  # replace ':' with ') {'
        elif line.startswith("elif "):
            line = "} else if(" + line[5:]              # replace 'elif' with 'else if'     
            line = line[:-2] + ") {\n"                  # replace : with ) {
        elif line.startswith("else:"):
            line = "} else {" + line[5:]                # replace 'elif' with 'else if'
        elif line.startswith("func "):
            line = f"const{line[4:]}" 
        elif line.startswith("end"):
            line = "}" + line[3:]                       # replace 'end' with '}' 
        elif line.startswith("string"):
            line = f"let{line[6:]}"
            if " =" in line:
                line = line.replace("=", ":string =")
            else:
                line = line[:-1]
                line += ":string\n"               
        elif line.startswith("int"):
                line = "let" + line[3:]
                if " =" in line:
                    line = line.replace("=", ":number =")
                else:
                    line = line[:-1]
                    line += ":number\n"

        if "printf(" in line:
            line = line.replace("printf(", "console.log(") # replace printf() with console.log()
        if "~" in line:
            line = line.replace("~", str_)              # replace ~ with string
        if "=>" in line:
            line = line.replace("=>", "=> {")           # replace => with => {

        output.write(line)                              # push line

def remove_files(dir_: str):
    for filename in os.listdir(dir_):
        os.remove(dir_ + filename)

def remove_string(text: str) -> tuple:
    string: str = ""
    text_start: int = 0
    text_end: int = 0
    d: bool = True

    for m in re.finditer('\"', text):
        if d:
            d = False
            text_start = m.start()
        else:
            text_end = m.end()
    if text_start != 0 and text_end != 0:
        string = text[text_start:text_end]
        text = f"{text[:text_start]}~{text[text_end:]}"

    return (text, string)

def main():
    if sys.argv[1] == "-f":
        if len(sys.argv) > 2:
            single_file(sys.argv[2])
        elif exists("index.tsa"):
            single_file("index.tsa")
        else:
            assert False, "ERROR: please provide a file"

    elif sys.argv[1] == "-d":
        assert len(sys.argv) > 2, "ERROR: please provide a directory"
        multiple_files()
    

if __name__ == "__main__":
    main()
