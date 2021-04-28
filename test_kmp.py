import kmp
import pytest

def test_kmp():
    kmp_table = []
    text = "abcabc"
    pattern = "abc"
    assert kmp.kmp(text,pattern,kmp_table) == 0
    text = "abcda"
    pattern = "da"
    assert kmp.kmp(text,pattern,kmp_table) == 3
    text = "akuuka"
    pattern = "uu"
    assert kmp.kmp(text,pattern,kmp_table) == 2