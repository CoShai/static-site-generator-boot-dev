from enum import Enum
from htmlnode import *
from textnode import text_to_textnodes,text_node_to_html_node,TextNode,TextType

class BlockType(Enum):
    PARAGRAPH='paragraph'
    HEADING='heading'
    CODE='code'
    QUOTE='quote'
    UNORDERED_LIST='unordered_list'
    ORDERED_LIST='ordered_list'
    

def block_to_block_type(markdown_block):
    if markdown_block.startswith(('# ','## ','### ','#### ','##### ','###### ')):
        return BlockType.HEADING
    
    if markdown_block.startswith('```') and markdown_block.endswith('```'):
        return BlockType.CODE
    
    is_quote_list=list(map(lambda line:line.startswith('>'),markdown_block.split('\n')))
    if not False in is_quote_list:
        return BlockType.QUOTE
    
    is_unordered_list=list(map(lambda line:line.startswith('- '),markdown_block.split('\n')))
    if not False in is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    for i,line in enumerate(markdown_block.split('\n'),1):
        if not line.startswith(f'{i}.'):
           return BlockType.PARAGRAPH
    
    return  BlockType.ORDERED_LIST

def markdown_to_blocks(markdown):
    blocks=markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block=block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def text_to_children(text):
    children=[]
    nodes=text_to_textnodes(text)
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    block_children=[]
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type=block_to_block_type(block)
        match(block_type):
            case BlockType.PARAGRAPH:
                lines=block.split('\n')
                paragraph=" ".join(lines)
                block_children.append(ParentNode('p',text_to_children(paragraph)))
            case BlockType.HEADING:
                count=block.count('#',0,6)
                block_children.append(ParentNode(f'h{count}',text_to_children(block.lstrip('#'*count)[1:])))
            case BlockType.QUOTE:
                lines=block.split('\n')
                children=[]
                for line in lines:
                    children.append(line[1:].strip())
                block_children.append(ParentNode('blockquote',text_to_children(" ".join(children))))
            case BlockType.UNORDERED_LIST:
                lines=block.split('\n')
                children=[]
                for line in lines:
                    children.append(ParentNode('li',text_to_children(line[2:])))
                block_children.append(ParentNode('ul',children))
            case BlockType.ORDERED_LIST:
                lines=block.split('\n')
                children=[]
                for line in lines:
                    children.append(ParentNode('li',text_to_children(line[3:])))
                block_children.append(ParentNode('ol',children))
            case BlockType.CODE:
                child=text_node_to_html_node(TextNode(block[4:-3],TextType.TEXT))
                code=ParentNode("code",[child])
                block_children.append(ParentNode('pre' ,[code]))
    return ParentNode('div',block_children)