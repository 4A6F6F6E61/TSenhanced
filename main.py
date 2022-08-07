#!/usr/local/bin python3

from audioop import mul
from io import TextIOWrapper
import os
import sys
import time
import re
from decimal import Context
from os.path import exists
from colorama import init as initColorama
from termcolor import colored as c

initColorama()
class log:
    def info(msg: str):
        print(c("[INFO]", "green") + c(": ", "grey", attrs=["dark"]) + msg)

    def error(msg: str):
        print(c("[ERROR]", "red") + c(": ", "grey", attrs=["dark"]) + msg)
    
    def bar():
        print(c("--------------------", "grey", attrs=["dark"]))
    
    def runtime(msg: str, runtime: str):
        print(c(f"[{runtime}]", "green", attrs=["dark"]) + c(": ", "grey", attrs=["dark"]) + msg)

class Keywords:
    _if       = "if "
    _for      = "for "
    elseIf    = "elif "
    _else     = "else then"
    functionC = "function "
    function  = "function! "
    cBracket  = "end"
    oBracket  = "do"
    arrowB    = "begin"
    then      = "then"



def single_file(f: str, runtime: str, output_dir: str = "output/"):
    if not exists(f):
        log.error(f"File {f} not found")
        return

    if f.endswith(".tsa"):
        with open(f, "r") as file_:
            start_time = time.perf_counter()
            remove_files(f"./{output_dir}")
            with open( f"{output_dir + f[:-4]}.ts", "x") as open_out:
                compile(file_, open_out)
            process_time = ((time.perf_counter() - start_time)*1000)
            log.info(f"Successfully Compiled {file_.name} in {Context(prec=1).create_decimal(process_time)}ms")
            log.runtime(msg="Output:", runtime=runtime)
            log.bar()
            out = os.system(f"{runtime} run {output_dir + f[:-4]}.ts")
            log.bar()

def multiple_files(output_dir: str = "output/"):
    remove_files(f"./{output_dir}")
    count: int = 0
    files: list[str] = os.listdir(sys.argv[2])
    log.bar()
    for f in files:
        if f.endswith(".tsa"):
            count += 1
            with open(f, "r") as file_:
                start_time = time.perf_counter()
                compile(file_, open(f"{output_dir + f}.ts", "x"))
                process_time = ((time.perf_counter() - start_time)*1000)
                t = Context(prec=1).create_decimal(process_time)
                c_time = c(f"{t}ms", "cyan")
                log.info(f"Successfully Compiled {file_.name} in {c_time}")

        else:
            continue
    log.bar()
    if count == 0: log.error("No .tsa file found")


def compile(file_: TextIOWrapper, output: TextIOWrapper):
    for line in file_:
        line: str = line.lstrip()                       # remove whitespace from the left
        rm: tuple = remove_string(line)                 # remove string from line
        line: str = rm[0]                               # Line without String
        str_: str = rm[1]                               # String without Line

        if line.startswith(Keywords._if):
            line = "if(" + line[len(Keywords._if):]                     # replace 'if ' with 'if('
            #line = line[:-1] + ") {\n"                  # replace ':' with ') {'
            line = line.replace(Keywords.then, ") {")       # replace 'then' with ') {'
        if line.startswith(Keywords._for):
            line = "for(" + line[len(Keywords._for):]                     # replace 'for ' with 'for('
            line = line.replace(" do", ") {")       # replace 'then' with ') {'
        elif line.startswith(Keywords.elseIf):
            line = "} else if(" + line[len(Keywords.elseIf):]              # replace 'elif' with 'else if'     
            #line = line[:-2] + ") {\n"                  # replace : with ) {
            line = line.replace(Keywords.then, ") {")       # replace 'then' with ') {'
        elif line.startswith(Keywords._else):
            line = "} else {\n" + line[len(Keywords._else):]                # replace 'elif' with 'else if'
        elif line.startswith(Keywords.functionC):
            line = f"const {line[len(Keywords.functionC):]}"
        elif line.startswith(Keywords.function):
            line = f"function {line[len(Keywords.functionC):]}"
        elif line.startswith(Keywords.cBracket):
            line = "}" + line[len(Keywords.cBracket):]                       # replace 'end' with '}'
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
        if "do" in line:
            line = line.replace("do", "{")           # replace do with => {
        if "begin" in line:
            line = line.replace("begin", "=> {")           # replace do with => {

        output.write(line)                              # push line

def remove_files(dir_: str):
    for filename in os.listdir(dir_):
        os.remove(dir_ + filename)
    log.info("Successfully removed all files in output directory")

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
    runtime = "deno"
    if sys.argv[len(sys.argv)-1] == "-bun":
        runtime = "bun"
    if len(sys.argv) == 1:
        log.error("Please provide more arguments")
    elif sys.argv[1] == "-f":
        if len(sys.argv) > 2:
            if sys.argv[2] == "-bun":
                runtime = "bun"
                if exists("index.tsa"):
                    single_file("index.tsa", runtime)
                else:
                    log.error("Please provide a file")
            else:
                single_file(sys.argv[2], runtime)
        elif exists("index.tsa"):
            single_file("index.tsa", runtime)
        else:
            log.error("Please provide a file")

    elif sys.argv[1] == "-d":
        if not len(sys.argv) > 2:
            log.error("Please provide a directory")
        elif sys.argv[3].startswith("-o="):
            t_p = sys.argv[3][3:]
            t_p = t_p[1:] if t_p[0] == "\"" or t_p[0] == "/" else t_p
            t_p = t_p + "/" if not t_p.endswith("/") else t_p
            multiple_files(t_p)
        else:
            multiple_files()

if __name__ == "__main__":
    main()
