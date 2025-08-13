from textnode import TextNode,TextType
from htmlnode import LeafNode
from generatepage import generate_pages_recursive
import os,shutil


def main():
    create_public()
    source=os.path.abspath('./static')
    target=os.path.abspath('./public')
    copy_recursive(source,target)
    
    generate_pages_recursive('./content/','template.html','./public/')
    

def create_public():
    if os.path.exists('./public'):    
        shutil.rmtree('./public')
        os.mkdir('./public')
        print("Created public folder")
    else:
        os.mkdir('./public')
        print("Created public folder")

def copy_recursive(source,target):
    paths=os.listdir(source)
    print(paths)
    for name in paths:
        path=os.path.join(source,name)
        if os.path.isdir(path):
            new_target=os.path.join(target,name)
            new_path=os.path.join(source,name)
            print(f"Creating directory: {new_target}")
            os.mkdir(new_target)
            copy_recursive(new_path,new_target)
        else:
            print(f"copying file: {path} to {target}")
            shutil.copy(path,target)
        


        




main()