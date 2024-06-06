import os
import re
import sys
import importlib
from pathlib import Path

# TODO: move to a config file
MODULES_TO_IGNORE = ['os', 'src', 'sys', 'importlib', 'Path']

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def get_python_version():
    v_info = sys.version_info
    version = str(v_info.major) +  '.' + str(v_info.minor) + '.' + str(v_info.micro)
    return version

def get_project_module_names():
    folders = []
    imports = []
    
    path = get_project_root()
    for folder,dirs,file in os.walk(path):
        folders.append(folder)
        for files in file:
            if files.endswith('.py'):
                fullpath=open(os.path.join(folder,files),'r')
                for line in fullpath:
                    if import_line(line):
                        module_name = extract_module_name(line)
                        if module_name is not None and module_name not in imports and module_name not in MODULES_TO_IGNORE:
                            imports.append(module_name)
    print(imports)
    return imports                        
                        
def import_line(line):
    return re.search(r'\bimport\b', line)
                        
def extract_module_name(line):
    import_pattern = r'import\s+(\w+)(?:\s+as\s+\w+)?'
    match = re.search(import_pattern, line)
    if match:
        return match.group(1)
    
    from_import_pattern = r'from\s+(\w+)\s+import\s+\w+'
    match = re.search(from_import_pattern, line)
    if match:
        return match.group(1)
    
    return None

def get_module_version(module_name):
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', None)
        if version is None:
            return 'No __version__ attribute.' 
        else:
            return version 
    except ModuleNotFoundError:
        return 'Module not installed.'
    
def write_versions(file_name = None):
    # TODO: make a prettier output file
    if file_name is None:
        file_name = os.path.join(get_project_root(), 'versions.txt')
    module_names = get_project_module_names()
    with open(file_name, 'w') as file:
        file.write('python' + '\t\t' + get_python_version() + '\n')
        for name in module_names:
            file.write(name + '\t\t' + get_module_version(name) + '\n')