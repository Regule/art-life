'''
This is script that allows for simultaneous printing to file and console.
IMPORTANT - this is not how you actually should use the logger for logging, this is 
only a small stupid trick to save your scripts output.
'''
import os
import logging 


logger = logging.getLogger()
iprint = logger.info
wprint = logger.warning
eprint = logger.error

def setup_logger(dataset_path, output_file='console_output.txt'):
    log_formatter = logging.Formatter('%(message)s')

    logfile_path = os.path.join(dataset_path, output_file)
    file_handler = logging.FileHandler(logfile_path)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)


def main():
    setup_logger('local')
    iprint('This is info')
    wprint('This is warrning')
    eprint('This is error')

    # You can now make your output silent like that
    logger.setLevel(logging.ERROR)
    iprint('This is info')
    wprint('This is warrning')
    eprint('This is error')

if __name__ == '__main__':
    main()
