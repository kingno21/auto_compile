import os, glob
import subprocess
import re

test_case = {
	"test1": [""],
	"test2": [""],
	"test3": [""],
	"test4": [""],
	"test5": [""],
	"test6": ["125489\n", "1112233\n"],
	"test7": ["0\n100\n200\n300\n400\n500\n600\n700\n800\n900\n999\n"],
}

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
	for index, file in enumerate(glob.glob("*.java")):
		class_name = ""
		tmp_name = "tmp.java"
		test_tmp = "test{}".format(index+1)

		with open(file, 'r') as f:
			class_name, contents = find_class_name(f.readlines())
			with open(tmp_name, 'w') as f1:
				f1.writelines(contents)

		run_cmd(["javac", tmp_name])

		for test in test_case[test_tmp]:
			run_cmd(["java", class_name], test)

		os.remove(tmp_name)
		os.remove(class_name + '.class')


if __name__ == '__main__':
	main()


