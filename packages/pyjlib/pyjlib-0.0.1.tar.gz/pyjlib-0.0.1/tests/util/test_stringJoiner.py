from unittest import TestCase

from pyjlib.util.stringjoiner import StringJoiner


class TestStringJoiner(TestCase):
    def test_creation_01(self):
        sj = StringJoiner()
        expected__str__ = ''
        self.assertEqual(expected__str__, str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "", "suffix": "", ' \
                           '"nelem": 0, "str_length": 0, "elements": []}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_creation_02(self):
        sj = StringJoiner("_", "[", "]")
        expected__str__ = '[]'
        self.assertEqual(expected__str__, str(sj))

        expected__repr__ = '{"separator": "_", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 0, "str_length": 2, "elements": []}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_creation_03(self):
        sj = StringJoiner(prefix="(", suffix=")")
        expected__str__ = '()'
        self.assertEqual(expected__str__, str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "(", "suffix": ")", ' \
                           '"nelem": 0, "str_length": 2, "elements": []}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_properties_01(self):
        sj = StringJoiner(prefix="[", suffix="]")

        self.assertEqual(",", sj.separator)
        self.assertEqual("[", sj.prefix)
        self.assertEqual("]", sj.suffix)
        self.assertEqual(0, sj.nelem)

        sj.add("e1").add("e2").add("e3")
        self.assertEqual(3, sj.nelem)

    def test_properties_02(self):
        sj = StringJoiner(prefix="[", suffix="]")

        sj.separator = "something else"
        sj.prefix = "something else"
        sj.suffix = "something else"
        sj.nelem = 42

        self.assertEqual(",", sj.separator)
        self.assertEqual("[", sj.prefix)
        self.assertEqual("]", sj.suffix)
        self.assertEqual(0, sj.nelem)

        sj.add("e1").add("e2").add("e3")
        self.assertEqual(3, sj.nelem)

    def test_adding_01(self):
        sj = StringJoiner()
        sj.add("e1")

        self.assertEqual("e1", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "", "suffix": "", ' \
                           '"nelem": 1, "str_length": 2, "elements": ["e1"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_adding_02(self):
        sj = StringJoiner()
        sj.add("e1").add("e2")

        self.assertEqual("e1,e2", str(sj))
        print("Sample Default String Joiner Output:", sj)

        expected__repr__ = '{"separator": ",", "prefix": "", "suffix": "", ' \
                           '"nelem": 2, "str_length": 5, "elements": ["e1", "e2"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_adding_03(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        self.assertEqual("[e1,e2,3]", str(sj))
        print("Sample String Joiner Output (default separator, prefix = [, suffix = ]:", sj)

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 3, "str_length": 9, "elements": ["e1", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_adding_04(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)
        sj.add("e0", 0)

        self.assertEqual("[e0,e1,e2,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 4, "str_length": 12, "elements": ["e0", "e1", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_adding_05(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)
        sj.add("e4", 3)

        self.assertEqual("[e1,e2,3,e4]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 4, "str_length": 12, "elements": ["e1", "e2", "3", "e4"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_adding_06(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        sj.add("anything", -1)

        self.assertEqual("[e1,e2,anything,3]", str(sj))

        expected = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                   '"nelem": 4, "str_length": 18, "elements": ["e1", "e2", "anything", "3"]}'
        self.assertEqual(expected, repr(sj))

        with self.assertRaises(IndexError):
            sj.add("something", -5)

    def test_adding_07(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        with self.assertRaises(IndexError):
            sj.add("anything", 42)

    def test_removing_01(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        sj.remove("e2")

        self.assertEqual("[e1,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 2, "str_length": 6, "elements": ["e1", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_removing_02(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        with self.assertRaises(ValueError):
            sj.remove("non-existing")

    def test_get_item_01(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        with self.assertRaises(IndexError):
            sj[-4]
        self.assertEqual("e1", sj[-3])
        self.assertEqual("e2", sj[-2])
        self.assertEqual("3", sj[-1])
        self.assertEqual("e1", sj[0])
        self.assertEqual("e2", sj[1])
        self.assertEqual("3", sj[2])
        with self.assertRaises(IndexError):
            sj[3]
        with self.assertRaises(IndexError):
            sj[4]

    def test_set_item_01(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        sj[3] = "e4"

        self.assertEqual("[e1,e2,3,e4]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 4, "str_length": 12, "elements": ["e1", "e2", "3", "e4"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_set_item_02(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        sj[0] = "1e"

        self.assertEqual("[1e,e2,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 3, "str_length": 9, "elements": ["1e", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_set_item_03(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        sj[0] = "e"

        self.assertEqual("[e,e2,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 3, "str_length": 8, "elements": ["e", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_set_item_04(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        sj[0] = "e11"

        self.assertEqual("[e11,e2,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 3, "str_length": 10, "elements": ["e11", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_set_item_05(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        with self.assertRaises(IndexError):
            sj[-42] = "something"

        sj[-3] = "e11"
        self.assertEqual("[e11,e2,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 3, "str_length": 10, "elements": ["e11", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

        with self.assertRaises(IndexError):
            sj[42] = "something"

    def test_delete_item_01(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        del sj[1]

        self.assertEqual("[e1,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 2, "str_length": 6, "elements": ["e1", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_delete_item_02(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        del sj[-3]

        self.assertEqual("[e2,3]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 2, "str_length": 6, "elements": ["e2", "3"]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_delete_item_03(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        with self.assertRaises(IndexError):
            del sj[3]

    def test_delete_item_04(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add("e1").add("e2").add(3)

        with self.assertRaises(IndexError):
            del sj[-4]

    def test_merge_01(self):
        sj1 = StringJoiner(prefix="[", suffix="]")
        sj1.add("e1").add("e2").add(3)

        sj2 = StringJoiner(prefix="(", suffix=")")
        sj2.add("o1").add("o2")
        sj2.merge(sj1)

        self.assertEqual("(o1,o2,e1,e2,3)", str(sj2))

        expected__repr__ = '{"separator": ",", "prefix": "(", "suffix": ")", ' \
                           '"nelem": 5, "str_length": 15, "elements": ["o1", "o2", "e1", "e2", "3"]}'
        self.assertEqual(expected__repr__, sj2.__repr__())

    def test_merge_02(self):
        sj1 = StringJoiner(prefix="[", suffix="]")
        sj1.add("e1").add("e2").add(3)

        sj2 = StringJoiner(prefix="(", suffix=")")
        sj2.add("o1").add("o2")
        sj2.merge(sj1, 1)

        self.assertEqual("(o1,e1,e2,3,o2)", str(sj2))

        expected__repr__ = '{"separator": ",", "prefix": "(", "suffix": ")", ' \
                           '"nelem": 5, "str_length": 15, "elements": ["o1", "e1", "e2", "3", "o2"]}'
        self.assertEqual(expected__repr__, sj2.__repr__())

    def test_merge_03(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.merge([1, 2, 3, "str", 4.0, ","])

        self.assertEqual("[1,2,3,str,4.0,,]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 6, "str_length": 17, "elements": ["1", "2", "3", "str", "4.0", ","]}'
        self.assertEqual(expected__repr__, sj.__repr__())

    def test_add_multi_01(self):
        sj = StringJoiner(prefix="[", suffix="]")
        sj.add_multi(1, 2, 3, "e4")

        self.assertEqual("[1,2,3,e4]", str(sj))

        expected__repr__ = '{"separator": ",", "prefix": "[", "suffix": "]", ' \
                           '"nelem": 4, "str_length": 10, "elements": ["1", "2", "3", "e4"]}'
        self.assertEqual(expected__repr__, repr(sj))

    # def test_iterating_01(selfs):
    #     sj = StringJoiner(prefix="[", suffix="]")
    #     sj.add_multi(1, 2, 3, "e4")
    #
    #     for e in sj:
    #         print(e)

    def test_adding_two_sj_01(self):
        sj1 = StringJoiner()
        sj2 = StringJoiner(prefix="(", suffix=")")

        sj1.add_multi("sj1_e1", "sj1_e2")
        sj2.add_multi("sj2_e1", "sj2_e2")

        sj1_2 = sj1 + sj2  # the sum is not cumulative. You get a different results if you change the order.
        self.assertEqual('sj1_e1,sj1_e2,sj2_e1,sj2_e2', str(sj1_2))

        sj2_1 = sj2 + sj1
        self.assertEqual('(sj2_e1,sj2_e2,sj1_e1,sj1_e2)', str(sj2_1))

        self.assertEqual('sj1_e1,sj1_e2', str(sj1))
        self.assertEqual('(sj2_e1,sj2_e2)', str(sj2))

    def test_subtract_two_sj_01(self):
        sj1 = StringJoiner()
        sj1.add_multi("e1", "e2", "e3")

        sj2 = StringJoiner()
        sj2.add_multi("e2", "e3", "e4")

        sj1_2 = sj1 - sj2
        self.assertEqual("e1", str(sj1_2))
        expected__repr__ = '{"separator": ",", "prefix": "", "suffix": "", ' \
                           '"nelem": 1, "str_length": 2, "elements": ["e1"]}'
        self.assertEqual(expected__repr__, repr(sj1_2))

        sj2_1 = sj2 -sj1
        self.assertEqual("e4", str(sj2_1))
        expected__repr__ = '{"separator": ",", "prefix": "", "suffix": "", ' \
                           '"nelem": 1, "str_length": 2, "elements": ["e4"]}'
        self.assertEqual(expected__repr__, repr(sj2_1))
