import csv
from time import time
from datetime import datetime
import sys
from pathlib import Path

class CSVBaseException(Exception):
    '''
    All csv-related exceptions should inherit from this class
    '''
    pass

class CSVBadHeadersException(CSVBaseException):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message

class Tasker():
    def __init__(self, taskFilePath = Path('tasks.txt'), skip_CSV_Validation = False):
        self.taskFilePath = taskFilePath
        self.taskFile = open(self.taskFilePath, 'a+')
        if not skip_CSV_Validation:
            try:
                self.validateCSVFile()
            except CSVBadHeadersException as e:
                print(e)

    '''
    CSV is valid if file is empty or the file contains 
    adequate headers and data types per row.
    '''
    def validateCSVFile(self) -> None:
        if self.taskFilePath.stat().st_size == 0:
            return

        with open(self.taskFilePath, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter = ' ')

            for row in csvreader:
                print(row)
            return

            # Validate headers
            headers = next(csvreader)
            print(f'headers: {headers}')
            if len(headers) != 4 or 'Task' != headers[0] or 'Category' != headers[1] or 'Start' != headers[2] or 'Stop' != headers[3]:
                raise CSVBadHeadersException(f'Missing headers in {csvfile.name}. File may be corrupted.')

            # Validate all rows less headers
            for lineNum, *fields in enumerate(csvreader, start = 2):
                try:
                    task, category, start, stop = fields
                    print(f'Fields: {fields}')
                    print(f'Task: {task} Category: {category} Start: {start} Stop: {stop}')
                except:
                    pass


def main(args):
    skip_CSV_validation = True if '--skip-csv-validation' in args else False
    tasker = Tasker(skip_CSV_Validation = skip_CSV_validation)

if __name__ == '__main__':
    main(sys.argv)