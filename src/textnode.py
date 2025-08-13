from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD ="bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self,other):
        return self.text==other.text and self.text_type==other.text_type and self.url==other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    text=text_node.text
    text_type=text_node.text_type
    url=text_node.url
    
    match(text_type):
        case TextType.TEXT:   return LeafNode(None,text)
        case TextType.BOLD:   return LeafNode('b',text)
        case TextType.ITALIC: return LeafNode('i',text)
        case TextType.CODE:   return LeafNode('code',text)
        case TextType.LINK:   return LeafNode('a',text,{"href":url})
        case TextType.IMAGE:  return LeafNode('img',"",{"src":url,"alt":text})
        case _: Exception("Unknown text type")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
        else:
            new_node_parts=[]
            words=node.text.split(delimiter)
                
            if len(words)%2==0:
                raise ValueError("invalid markdown, formatted section not closed")
            
            for i,w in enumerate(words):
                if w=="":
                    continue
                if i%2==0:
                    new_node_parts.append(TextNode(w,TextType.TEXT))
                else:
                    new_node_parts.append(TextNode(w,text_type))
            new_nodes.extend(new_node_parts)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    

def split_nodes_image(old_nodes):
    new_nodes=[]
    for node in old_nodes:
        text=node.text
        matches = extract_markdown_images(text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        new_node_parts=[]
        
        for m in matches:
            image_alt=m[0]
            image_link=m[1]
            sections= text.split(f"![{image_alt}]({image_link})", 1)
            text=sections[1]
            if sections[0]!="":
                new_node_parts.append(TextNode(sections[0],TextType.TEXT))
            new_node_parts.append(TextNode(image_alt,TextType.IMAGE,image_link))
        
        if text!="":
            new_node_parts.append(TextNode(text,TextType.TEXT))
        new_nodes.extend(new_node_parts)
    return new_nodes
           
def split_nodes_link(old_nodes):
    new_nodes=[]
    for node in old_nodes:
        text=node.text
        matches = extract_markdown_links(text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        new_node_parts=[]
        
        for m in matches:
            link_alt=m[0]
            link_url=m[1]
            sections= text.split(f"[{link_alt}]({link_url})", 1)
            text=sections[1]
            if sections[0]!="":
                new_node_parts.append(TextNode(sections[0],TextType.TEXT))
            new_node_parts.append(TextNode(link_alt,TextType.LINK,link_url))
        
        if text!="":
            new_node_parts.append(TextNode(text,TextType.TEXT))
        new_nodes.extend(new_node_parts)
    return new_nodes

def text_to_textnodes(text):
    base_node=[TextNode(text,TextType.TEXT)]
    new_nodes=split_nodes_image(base_node)
    new_nodes=split_nodes_link(new_nodes)
    new_nodes=split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
    new_nodes=split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    new_nodes=split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    return new_nodes
    
                
        
    
            