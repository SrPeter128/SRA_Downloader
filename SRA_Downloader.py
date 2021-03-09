import os
import shutil
import multiprocessing
from optparse import OptionParser
import subprocess


def check_package():
	threads = 0

	if shutil.which("prefetch") is None:
		print("prefetch not found. Install prefetch!")
		exit(0)

	if shutil.which("parallel-fastq-dump") is not None:
		print("found parallel-fastq-dump!")

		# After 5 trys...there is no hope
		x = 5
		while x >= 0:
			if x == 0:
				print("Ufff... math is hard... but not this hard... ")
				print("you have ", multiprocessing.cpu_count(),
					  " threads. So you have to write a number between 1 and ", multiprocessing.cpu_count(), ".")
				exit(0)

			print("You can use ", multiprocessing.cpu_count(), " threads.")
			threads = input("Threads: ")

			if int(threads) > multiprocessing.cpu_count():
				print("Error! Only ", multiprocessing.cpu_count(), "Threads are available!")
				x -= 1
			else:
				return threads

	elif shutil.which("fastq-dump") is None:
		print("fastq-dump not found. Install fastq-dump!")
		exit(0)


def read_in(file_path, list):
	with open(file_path) as SRR_names_file:
		for line in SRR_names_file:
			list.append(line.strip())
	return list


def download(SRR_Name, working_path, tool_kit_path, paired_bool, singel_bool, threads):
	path = working_path
	os.chdir(path)
	SRR_File = SRR_Name + ".sra"

	# prefetch
	print("Downloading " + SRR_Name)
	subprocess.call(["prefetch", "--max-size", "60000000", SRR_Name])

	os.mkdir(SRR_Name)
	os.chdir(SRR_Name)
	os.mkdir("raw")
	os.chdir("raw")
	tool_kit_path_and_file = tool_kit_path + "/" + SRR_File
	shutil.move(tool_kit_path_and_file, os.getcwd() + "/" + SRR_File)

	if threads == 0:
		# Fastq-dump
		if (paired_bool == True):
			subprocess.call(["fastq-dump", "--gzip", "--split-files", SRR_File])
			print(SRR_File, "processed and ziped and splided as paird-end\n\n")

		elif (singel_bool == True):
			subprocess.call(["fastq-dump", "--gzip", SRR_File])
			print(SRR_File, "processed and ziped as single-end\n\n")
	elif threads != 0:
		if (paired_bool == True):
			subprocess.call(
				["parallel-fastq-dump", "--sra-id", SRR_File, "--threads", threads, "--split-files", "--gzip"])
			print(SRR_File, "processed and ziped and splided as paird-end\n\n")

		elif (singel_bool == True):
			subprocess.call(["parallel-fastq-dump", "--sra-id", SRR_File, "--threads", threads, "--gzip"])
			print(SRR_File, "processed and ziped as single-end\n\n")

	os.remove(SRR_File)  # entfernen des sra-files


def main():
	# uebergeben des Files mit den SRR Nummern
	parser = OptionParser()
	parser.add_option('-i', '--in_File', dest="in_file_path", help="File with Line-sperated SRR-Numbers")
	parser.add_option('-p', '--paird', action='store_true', dest="paired_bool", default=False,
					  help="If all SRR-Experiments Paird-End sequencings")
	parser.add_option('-s', '--singel', action='store_true', dest="singel_bool", default=False,
					  help="If all SRR-Experiments Singel-End sequencings")
	parser.add_option('-d', '--working_path', dest="working_path", default=os.getcwd(),
					  help="OPTIONAL! Only needed when the SRA_Downloader.py is NOT in the working_directory!")
	parser.add_option('-k', '--SRA_toolkit_path', dest="SRA_toolkit_path",
					  help="Path to the  ncbi/sra directory from the sra-toolkit")
	(options, args) = parser.parse_args()

	file_path = options.in_file_path
	SRR_list = []
	SRR_list = read_in(file_path, SRR_list)
	threads = check_package()
	for i in range(0, len(SRR_list)):
		download(SRR_list[i], options.working_path, options.SRA_toolkit_path, options.paired_bool, options.singel_bool,
				 threads)
		os.chdir(options.working_path)


if __name__ == "__main__":
	main()
