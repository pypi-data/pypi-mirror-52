# -*- coding: utf-8 -*-
import psutil
import os
from .test_func import Image, path, jpg_path, setup_function, teardown_function, check_md5
from . import test_func


def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())

    for _ in range(1000):
        test_func.test_read_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        test_func.test_read_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.01, "memory leaks when reading"
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())

    for _ in range(1000):
        test_func.test_modify_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        test_func.test_modify_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.01, "memory leaks when writing"


def test_stack_overflow():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "(test_stack_overflow)" * 1000,
             "Exif.Image.Orientation": "0123456789"* 1000}

    for _ in range(10):
        Image(path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(10):
        Image(path).modify_exif(dict1)
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory leaks when writing"


def test_transfer_various_values():
    """
    Test whether various values can be transfered correctly between Python and C++ API.
    Even if a value is correctly transmitted, it does not mean that it will be successfully saved by C++ API.
    """
    import string
    from ..core import SEP, EOL, EOL_replaced
    i = Image(path)
    values = (string.digits * 5,
              string.ascii_letters * 5,
              string.punctuation * 5,
              string.whitespace * 5,
              "test-中文-" * 5,
              (SEP + EOL_replaced) * 5,
              )
    for v in values:
        i.modify_exif({"Exif.Image.ImageDescription": v})
        assert i.read_exif().get("Exif.Image.ImageDescription") == v

        i.modify_iptc({"Iptc.Application2.ObjectName": v})
        assert i.read_iptc().get("Iptc.Application2.ObjectName") == v

        # A known problem: XMP text does not support \v \f
        _v = v.replace("\v", "").replace("\f", "")
        i.modify_xmp({"Xmp.dc.creator": _v})
        assert i.read_xmp().get("Xmp.dc.creator") == _v


def _test_recover():
    """ a strict test, for whether it can delete metadata and recover it completely. """
    i = Image(path)
    all_dict = i.read_all()
    i.clear_all()
    for v in i.read_all().values():
        assert not v

    # recover the metadata
    i.modify_all(all_dict)
    new_dict = i.read_all()
    for sort in all_dict.keys():
        for key in all_dict[sort].keys():
            assert all_dict[sort][key] == new_dict[sort][key], "{} didn't recover".format(key)
