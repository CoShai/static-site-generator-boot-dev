import unittest

from generatepage import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title_line(self):
        md="""# Hello"""
        title=extract_title(md)
        self.assertEqual(title,"Hello")
        
    
    def test_extract_title_lines(self):
        md="""# Hello ABC
        ABC
        CDE
        """
        title=extract_title(md)
        self.assertEqual(title,"Hello ABC")
    
    def test_extract_title_lines(self):
        md="""# Hello ABC
        ABC
        CDE
        """
        title=extract_title(md)
        self.assertEqual(title,"Hello ABC")
        
    def test_extract_title_lines_exception(self):
        md="""## Hello ABC
        ABC
        CDE
        """
        with self.assertRaises(Exception):
            extract_title(md)
    
    def test_extract_title_lines_missing(self):
        md=""" Hello ABC
        ABC
        CDE
        """
        with self.assertRaises(Exception):
            extract_title(md)
    
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass
