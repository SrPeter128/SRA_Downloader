# SRA_Downloader


Automated download of NextSeq datasets. Simply submit a .txt with SRR or SRA numbers (or similar). The numbers must be line separated.

'''
Options:
  -h, --help            show this help message and exit
  -i IN_FILE_PATH, --in_File=IN_FILE_PATH
                        File with Line-sperated SRR-Numbers (or similar naming)
  -p, --paird           If all SRR-Experiments Paird-End sequencings
  -s, --singel          If all SRR-Experiments Singel-End sequencings
  -d WORKING_PATH, --working_path=WORKING_PATH
                        OPTIONAL! Only needed when the SRA_Downloader.py is
                        NOT in the working_directory!
  -k SRA_TOOLKIT_PATH, --SRA_toolkit_path=SRA_TOOLKIT_PATH
                        Path to the  ncbi/sra directory from the sra-toolkit
'''
