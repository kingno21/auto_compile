#!/usr/bin/python
import os, glob, sys
import subprocess
import re
import read_json as rj


def find_class_name(contents):
    pattern = "(?<=class )\w+"
    for index, line in enumerate(contents):
        if "class" in line:
            contents[index] = line.replace('public', '')
            return re.search(pattern, line).group(0), contents


def run_cmd(cmd, test=None):
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    try:
        outs, errs = proc.communicate(test)
        print outs, errs
    except OSError:
        proc.kill()


def main():
    if len(sys.argv) < 1:
        print 'Use test case'
        return

    test_case = rj.get_case(sys.argv[-1])

    for index, file in enumerate(glob.glob("*.java")):

        if os.stat(file).st_size == 0:
            continue
        class_name = ""
        tmp_name = "tmp.java"
        test_tmp = "test{}".format(index + 1)

        with open(file, 'r') as f:
            class_name, contents = find_class_name(f.readlines())
            with open(tmp_name, 'w') as f1:
                f1.writelines(contents)

        run_cmd(["javac", tmp_name])

        print 'run: {}'.format(test_tmp)
        
        for test in test_case[test_tmp]:
            run_cmd(["java", class_name], test)

        os.remove(tmp_name)
        os.remove(class_name + '.class')


if __name__ == '__main__':
    main()
