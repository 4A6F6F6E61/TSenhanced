import os
import sys
import time
from decimal import Decimal, Context
from os.path import exists

def single_file(f, output_dir = "output/"):
    if f.endswith(".tsa"):
        with open(f, "r") as file_:
            start_time = time.time()
            remove_files("./" + output_dir)
            compile(file_, open( output_dir + f[:-4] + ".ts", "x"))
            process_time = ((time.time() - start_time)*1000)
            print("[INFO]: Successfully Compiled %s in %sms" % (file_.name ,Context(prec=1).create_decimal(process_time)))
            print("[INFO]: Deno Output:")
            print("--------------------")
            out = os.system("deno run " + output_dir + f[:-4] + ".ts")
            print("--------------------")

def multiple_files(output_dir = "output/"):
    remove_files("./" + output_dir)
    count = 0
    files = os.listdir(sys.argv[2])
    for f in files:
        if f.endswith(".tsa"):
            count += 1
            with open(f, "r") as file_:
                start_time = time.time()
                compile(file_, open( output_dir + f[:-4] + ".ts", "x"))
                process_time = ((time.time() - start_time)*1000)
                print("[INFO]: Successfully Compiled %s in %sms" % (file_.name ,Context(prec=1).create_decimal(process_time)))
        else:
            continue
    assert count != 0, "ERROR: no .tsa file found"

def compile(file_, output):
    for line in file_:
        line = line.lstrip()

        if line.endswith("=>\n"):
            line = line[:-1] + " {\n"             # arrow func

        if line.startswith("if "):
            line = "if(" + line[3:]             # replace 'if ' with 'if('
            line = line[:-2] + ") {\n"          # replace ':' with ') {'
        elif line.startswith("elif "):
            line = "} else if(" + line[4:]      # replace 'elif' with 'else if'     
            line = line[:-2] + ") {\n"          # replace : with ) {
        elif line.startswith("else:"):
            line = "} else {" + line[5:]      # replace 'elif' with 'else if'
        elif line.startswith("func "):
            line = "const" + line[4:] 
        elif line.startswith("end"):
            line = "}" + line[3:]               # replace 'end' with '}'
        elif line.startswith("string"):
            line = "let" + line[6:]
            if " =" in line:
                line = line.replace("=", ":string =")
            else:
                line = line[:-1]
                line += ":string\n"               # String
        elif line.startswith("int"):
                line = "let" + line[3:]
                if " =" in line:
                    line = line.replace("=", ":number =")
                else:
                    line = line[:-1]
                    line += ":number\n"

        if "printf(" in line:
            line = line.replace("printf(", "console.log(") # replace printf()

        output.write(line)          # push line

def remove_files(dir_):
    for filename in os.listdir(dir_):
        os.remove(dir_ + filename)

def main():
    if sys.argv[1] == "-f":
        if len(sys.argv) > 2:
            single_file(sys.argv[2])
        elif exists("index.tsa"):
            single_file("index.tsa")
        else:
            assert False, "ERROR: please provide a file"

    elif sys.argv[1] == "-d":
        if len(sys.argv) > 2:
            multiple_files()
        else:
            assert False, "ERROR: please provide a directory"
    

if __name__ == "__main__":
    main()
