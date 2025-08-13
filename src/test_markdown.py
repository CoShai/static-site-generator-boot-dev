import unittest
from markdown import *

class TestMarkDownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_empty_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type_paragraph(self):
        block="This is **bolded** paragraph"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_longer(self):
        block="This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
        
    def test_block_to_block_type_unordered_list(self):
        block="- This is a list\n- with items"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block="1. This is a list\n2. with items"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.ORDERED_LIST)

    def test_block_to_block_type_heading(self):
        block="#### This is a heading"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.HEADING)
        
    def test_block_to_block_type_code(self):
        block="``` This is a heading ```"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block=">This is a heading\n>second quote"
        block_type=block_to_block_type(block)
        self.assertEqual(block_type,BlockType.QUOTE)
    
    def test_block_to_block_type_paragraph_not_eq(self):
        block=">This is **bolded** paragraph"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.PARAGRAPH)
        
    def test_block_to_block_type_ordered_list__not_eq(self):
        block="1.This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.ORDERED_LIST)
        
    def test_block_to_block_type_unordered_list_not_eq(self):
        block="< This is a list\n- with items"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list_no_eq(self):
        block="- This is a list\n2. with items"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.ORDERED_LIST)

    def test_block_to_block_type_heading_no_eq(self):
        block=" This is a heading"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.HEADING)
        
    def test_block_to_block_type_code_no_eq(self):
        block=" This is a heading ```"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.CODE)
    
    def test_block_to_block_type_quote_no_eq(self):
        block="<This is a heading\n>second quote"
        block_type=block_to_block_type(block)
        self.assertNotEqual(block_type,BlockType.QUOTE)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_heading(self):
        md = """
        ### HELLO WORLD!
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h3>HELLO WORLD!</h3></div>",
    )