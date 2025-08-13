import os
from markdown import markdown_to_html_node

def extract_title(markdown):
    title_line = markdown.strip().split('\n',1)[0]
    if  not title_line.startswith('#') or title_line.startswith('##'):
        raise Exception("Missing h1 title")
    return title_line.strip('# ')

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,'r') as f:
        markdown=f.read()
    with open(template_path,'r') as f:
        template=f.read()
    
    html_string=markdown_to_html_node(markdown).to_html()
    title=extract_title(markdown)
    template=template.replace('{{ Title }}',title)
    template=template.replace('{{ Content }}',html_string)
    template=template.replace('href="/',f'href="{basepath}')
    template=template.replace('src="/',f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path),exist_ok=True)
    with open(dest_path,'w') as f:
        f.write(template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,baspath):
    dir_list=os.listdir(dir_path_content)
    for name in dir_list:
        new_path=os.path.join(dir_path_content,name)
        new_dest=os.path.join(dest_dir_path,name)
        if os.path.isfile(new_path):
            generate_page(new_path,template_path,new_dest.replace('md','html'),baspath)
        else:
            generate_pages_recursive(new_path,template_path,new_dest,baspath)
                
                
        