#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0

from __future__ import division, absolute_import, print_function, unicode_literals
import unittest

import six

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from amethyst.core import Object, Attr

class Exception_Eager(Exception): pass
class Counter(object):
    def __init__(self):
        self.value = 0
    def step(self):
        self.value += 1
        return self.value

# package-level object for testing string attrs
class TestAttrObject(Object):
    foo = Attr("TestAttrObject")
    bar = Attr(".Counter")

class MyTest(unittest.TestCase):

    def test_basic(self):
        class MyObject(Object):
            amethyst_register_type = False
            foo = Attr(int)
            bar = Attr(isa=six.text_type).strip()

        myobj = MyObject(dict(foo=23, bar=" Hello "))

        self.assertEqual(myobj.foo, 23)
        self.assertEqual(myobj.bar, "Hello")

        myobj.set("foo", 15, foo=5)
        self.assertEqual(myobj.foo, 15, ".set() takes positional or kwargs and prefers positional")


    def test_Attr_standalone(self):
        chk = Attr(int)

        self.assertTrue(callable(chk))
        self.assertEqual(chk("42"), 42)

        with self.assertRaises(TypeError):
            chk(None)
        with self.assertRaises(ValueError):
            chk("plugh")

        for chk in (Attr(int, default=0), Attr(int, default=lambda: 0)):
            self.assertTrue(callable(chk))
            self.assertEqual(chk("42"), 42)

            with self.assertRaises(TypeError):
                chk(None)
            with self.assertRaises(ValueError):
                chk("plugh")
            self.assertEqual(chk.get_default(), 0)


    def test_Attr_classes(self):
        counter = Counter()
        obj1 = TestAttrObject()
        obj2 = TestAttrObject(foo=dict(foo=obj1), bar=counter)

        self.assertTrue(isinstance(obj2.foo, TestAttrObject))
        self.assertTrue(obj2.foo.foo is obj1)
        self.assertTrue(obj2.foo is not obj1)
        self.assertTrue(obj2.bar is counter)


    def test_Attr_unit(self):
        counter = Counter()

        def boom_eager():
            raise Exception_Eager("boom!")

        class MyObject(Object):
            amethyst_verifyclass = False
            amethyst_register_type = False
            a = Attr(int)
            b = Attr(float)
            c = Attr(verify=(lambda x: 0 < x < 10))
            d = Attr(isa=int)
            e = Attr(isa=(int, list))
            f = Attr(default=42)
            g = Attr(default=(lambda: 22))
            h = Attr(default=(lambda: counter.step()))
            i = Attr(builder=(lambda: self.assertFalse(True, "builder called lazily")))
            j = Attr(builder=(lambda: 12))
            k = Attr(float) & Attr(verify=(lambda x: 0 < x < 10))
            l = Attr(float) | Attr(int)
            m = Attr(int) | Attr(float)
            n = Attr(int) == (2,3,6,7,8)
            o = Attr(int) != (0, 1)

        class MyEagerTest(Object):
            amethyst_verifyclass = False
            amethyst_register_type = False
            k = Attr(default=(lambda: boom_eager()))

        myobj = MyObject()

        self.assertIsNone(myobj.a, "unset is none")

        myobj.set("a", "23")
        self.assertEqual(myobj.a, 23, "Attr(int)")
        with self.assertRaises(ValueError):
            myobj.set("a", "34.2")
        with self.assertRaises(ValueError):
            myobj.set("a", "Not an int")

        myobj.set("b", "23.3")
        self.assertEqual(myobj.b, 23.3, "Attr(float)")

        myobj.set("c", 3.3)
        self.assertEqual(myobj.c, 3.3, "verify 0 < x < 10")
        with self.assertRaises(ValueError):
            myobj.set("c", 12)

        myobj.set("d", 3)
        self.assertEqual(myobj.d, 3, "isa int")
        with self.assertRaises(ValueError):
            myobj.set("c", 12)

        myobj.set(e=23)
        self.assertEqual(myobj.e, 23, "isa tuple:int")
        myobj.set(e=["foo", "bar"])
        self.assertEqual(myobj.e, ["foo", "bar"], "isa tuple:list")
        with self.assertRaises(ValueError):
            myobj.set("e", "Not an int or list")

        self.assertEqual(myobj.f, 42, "default")
        self.assertEqual(myobj.g, 22, "default callable")

        self.assertEqual(myobj.h, 1, "default callable caches (first)")
        self.assertEqual(myobj.h, 1, "default callable caches (second)")

        myobj2 = MyObject()
        myobj3 = MyObject()
        self.assertEqual(myobj2.h, 2, "default callable distinct each object (2)")
        self.assertEqual(myobj3.h, 3, "default callable distinct each object (3)")

        # DO NOT get .i, need to test builder is lazy
        # self.assertEqual(myobj.i, 12, "builder")
        self.assertEqual(myobj.j, 12, "builder")

        myobj.k = "5"
        self.assertEqual(myobj.k, 5)
        with self.assertRaises(ValueError):
            myobj.k = "Not an int or list"
        with self.assertRaises(ValueError):
            myobj.k = 12

        myobj.l = "5"
        self.assertEqual(myobj.l, 5)
        self.assertTrue(not isinstance(myobj.l, int))
        myobj.l = "5.0"
        self.assertEqual(myobj.l, 5)
        self.assertTrue(not isinstance(myobj.l, int))
        myobj.m = "5"
        self.assertEqual(myobj.m, 5)
        self.assertTrue(isinstance(myobj.m, int))
        myobj.m = "5.0"
        self.assertEqual(myobj.m, 5)
        self.assertTrue(not isinstance(myobj.m, int))

        myobj.n = "2"
        self.assertEqual(myobj.n, 2)
        myobj.n = 7
        self.assertEqual(myobj.n, 7)
        with self.assertRaises(ValueError):
            myobj.n = 4
        with self.assertRaises(ValueError):
            myobj.n = 12

        myobj.o = "2"
        self.assertEqual(myobj.o, 2)
        myobj.o = 234299993
        self.assertEqual(myobj.o, 234299993)
        with self.assertRaises(ValueError):
            myobj.o = 0
        with self.assertRaises(ValueError):
            myobj.o = 1

        with self.assertRaises(Exception_Eager):
            myobj = MyEagerTest()


    def test_Attr_docs(self):
        # The Attr() docs specify a few specific odd cases:
        class MyObject(Object):
            amethyst_register_type = False
            foo_int      = Attr(int)
            foo_floatint = Attr(float).int()
            foo_posint   = 0 < Attr(int)
            foo_proofint = (0 <= Attr(int)) <= 200     # Parens are necessary!

        myobj = MyObject()

        myobj.set("foo_int", "23")
        self.assertEqual(myobj.foo_int, 23)

        myobj.set("foo_int", 23.6)
        self.assertEqual(myobj.foo_int, 23)

        myobj.set("foo_floatint", "23.3")
        self.assertEqual(myobj.foo_floatint, 23)

        myobj.set("foo_floatint", 23.6)
        self.assertEqual(myobj.foo_floatint, 23)

        myobj.set("foo_posint", "500")
        self.assertEqual(myobj.foo_posint, 500)

        myobj.set("foo_proofint", "150")
        self.assertEqual(myobj.foo_proofint, 150)

        myobj.set("foo_proofint", 200)
        self.assertEqual(myobj.foo_proofint, 200)

        myobj.set("foo_proofint", 0)
        self.assertEqual(myobj.foo_proofint, 0)

        with self.assertRaises(ValueError):
            myobj.set("foo_int", "23.4")
        with self.assertRaises(ValueError):
            myobj.set("foo_floatint", "sdf")
        with self.assertRaises(ValueError):
            myobj.set("foo_posint", 0)
        with self.assertRaises(ValueError):
            myobj.set("foo_posint", -5)
        with self.assertRaises(ValueError):
            myobj.set("foo_proofint", -5)
        with self.assertRaises(ValueError):
            myobj.set("foo_proofint", 201)



if __name__ == '__main__':
    unittest.main()
