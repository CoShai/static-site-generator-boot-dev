from generatepage import generate_pages_recursive
import os,shutil
import sys


public_dir='./docs/'
template_dir='template.html'
source_dir=source=os.path.abspath('./static')
target_dir=os.path.abspath(public_dir)
content_dir='./content/'



def main():
    basepath='/'
    if len(sys.argv)>1:
        basepath=sys.argv[1]
    
    create_public()    
    copy_recursive(source_dir,target_dir)
    generate_pages_recursive(content_dir,template_dir,public_dir,basepath)
    

def create_public():
    if os.path.exists(public_dir):    
        shutil.rmtree(public_dir)
        os.mkdir(public_dir)
        print("Created public directory")
    else:
        os.mkdir(public_dir)
        print("Created public directory")

def copy_recursive(source,target):
    paths=os.listdir(source)
    for name in paths:
        path=os.path.join(source,name)
        if os.path.isdir(path):
            new_target=os.path.join(target,name)
            new_path=os.path.join(source,name)
            print(f"Creating directory: {new_target}")
            os.mkdir(new_target)
            copy_recursive(new_path,new_target)
        else:
            print(f"Copying file: {path} to {target}")
            shutil.copy(path,target)
        
main()