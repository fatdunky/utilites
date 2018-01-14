'''
Created on 23Nov.,2016

@author: fatdunky
'''
import gzip, logging, tarfile, os, tempfile, re, time
from pydoc import locate
from contextlib import closing, contextmanager


def read_gz_file(file_name):
    input_file = gzip.open(file_name, 'rt') 
    try:
        return_lines=input_file.readlines()        
    finally:
        input_file.close()
        return return_lines

def read_file(file_name):
    input_file = open(file_name, 'rt') 
    try:
        return_lines=input_file.readlines()        
    finally:
        input_file.close()
        return return_lines


def write_tar_file(tar_file_name, file_names):
    with closing(tarfile.open(tar_file_name, "w:gz")) as tar:
        for file_name in file_names:
            tar.add(file_name, arcname=os.path.sep + os.path.basename(file_name))

        
def write_temp_file(data, direct=None, delete=True):
    output = tempfile.NamedTemporaryFile('wt',dir=direct,delete=delete)
    try:
        for line in data:
            output.write(line)
    finally:
        name = output.name
        output.close()
    
    return name


def write_gz_file(data, filename):
    output = gzip.open(filename, 'wt')
    try:
        for line in data:
            output.write(line)
    finally:
        output.close()

 
def write_file(data, filename):
    output = open(filename, 'wt')
    try:
        for line in data:
            output.write(line)
    finally:
        output.close()


def append_write_file(data, filename):
    output = open(filename, 'at')
    try:
        for line in data:
            output.write(str(line))
    finally:
        output.close()

def load_class(class_name):
    return_value = locate(class_name)
    if return_value == None:
        logging.error("%s not found!",class_name)
        exit(1)
        #TODO: throw exception here instead
    return return_value


def get_file_directory(ifile):
    return os.path.dirname(os.path.abspath(ifile))


def compress_existing_file(input_file):
    retval = False
    if (not input_file.endswith('.gz')):
        try:
            f_in = open(input_file)
            f_out = gzip.open(input_file + '.gz', 'wb')
            f_out.writelines(f_in)
            retval = True
        finally:
            f_out.close()
            f_in.close()
            
    return retval

def clean_up_directory(directories, file_patterns, age_limit, compress_limit):
    # TODO: catch  raise error, v # invalid expression
    
    now = time.time()
    remove_age = now - (int(age_limit) * 86400)
    compress_age = now - (int(compress_limit) * 86400)
    
    for directory in directories:
        file_dir = os.path.abspath(directory)
        files = os.listdir(file_dir)
        filtered_files = []
        
        for mfile in files:
            for file_pattern in file_patterns:
                if (re.match(file_pattern, mfile)):
                    filtered_files.append(mfile)
        
        for mfile in filtered_files:
            full_file_name = os.path.join(file_dir, mfile)
            if os.path.isfile(full_file_name):
                file_stats = os.stat(full_file_name)
                file_time = file_stats.st_mtime
                
                if (file_time < remove_age):
                    os.remove(full_file_name)
                elif (file_time < compress_age):
                    if (compress_existing_file(full_file_name)):
                        os.remove(full_file_name)
    
    
    
    
    
    
    
