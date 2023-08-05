

import sys

# importing the sibling folder is not as easy as it should be..
import os, sys
here = os.path.split(os.path.abspath(os.path.dirname(__file__)))
src = os.path.join(here[0], "src/stay")
sys.path.insert(0,src)

from stay import loads


def test_docs():
    text = ""
    assert list(loads(text)) == [{}]
    
    text = """
===
===
"""
    assert list(loads(text)) == [{}, {}, {}]
    
def test_dict():
    text = """
a: b
b: a
"""
    assert list(loads(text)) == [{'a': 'b', 'b': 'a'}]

    
def test_comments():
    text = "# adsf"
    assert list(loads(text)) == [{}]
    
    text = """
###
asdf
###
a: b
"""
    assert list(loads(text)) == [{'a': 'b'}]
    
    text = """
### asdf ###
a: b
"""
    assert list(loads(text)) == [{'a': 'b'}]
    
def test_long():
    text = """
foo:::
1
2
3


:::   
"""
    assert list(loads(text)) == [{'foo': '1\n2\n3\n\n'}]

def test_complex():
    text = """
name: 
    family: adsf
    call: 
        foo:::
1
2
:::    
"""
    assert list(loads(text)) == [{'name': {"family": "adsf", "call": {"foo": "1\n2"}}}]
    
def test_list():
    text = """
matrix:::[

[1 2 3]
[4 5 6]
[7 8 9]
foo bar
]:::
"""
    assert list(loads(text)) == [{"matrix": [['1','2','3'], ['4','5','6'], ['7','8','9'], "foo bar"]}]
