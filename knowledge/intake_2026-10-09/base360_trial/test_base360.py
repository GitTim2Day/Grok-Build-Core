from fractions import Fraction as F
import unittest
from base360 import encode,decode,terminating_digits,guard_then_remove

class Tests(unittest.TestCase):
    def test_common_fractions_exact_one_digit(self):
        for d in (2,3,4,5,6,8,9,10,12,15,18,20,24,30,36,40,45,60,72,90,120,180,360):
            with self.subTest(d=d):
                r=encode(F(1,d),digits=1);self.assertTrue(r['exact']);self.assertEqual(r['digits'],[360//d]);self.assertEqual(decode(r),F(1,d))
    def test_two_digits(self):
        for d in (16,25,27,64,81,125):
            r=encode(F(1,d),digits=2)
            self.assertEqual(r['exact'],360**2%d==0)
    def test_seven_does_not_terminate(self):
        r=encode(F(1,7),digits=6)
        self.assertEqual(r['digits'],[51,154,102,308,205,257]);self.assertFalse(r['exact']);self.assertIsNone(terminating_digits(F(1,7)))
    def test_integer_no_fractional_digits(self):
        r=encode(F(17),digits=20);self.assertTrue(r['exact']);self.assertEqual(r['digits'],[]);self.assertEqual(decode(r),17)
    def test_declared_accuracy_stops(self):
        r=encode(F(1,7),digits=100,accuracy=F(1,1000000))
        self.assertTrue(r['accuracy_met']);self.assertLessEqual(F(*r['absolute_error']),F(1,1000000));self.assertEqual(len(r['digits']),3);self.assertGreater(F(*encode(F(1,7),digits=2)['absolute_error']),F(1,1000000))
    def test_unmet_accuracy_explicit(self):
        r=encode(F(1,7),digits=1,accuracy=F(1,10**20));self.assertFalse(r['accuracy_met'])
    def test_error_identity_and_bound_many_ratios(self):
        for n in range(-20,21):
            for d in range(1,501):
                v=F(n,d);r=encode(v,digits=3);x=decode(r)
                self.assertEqual(abs(v-x),F(*r['absolute_error']))
                self.assertLess(abs(v-x),F(1,360**len(r['digits'])))
                if r['exact']:self.assertEqual(x,v)
    def test_finite_classifier(self):
        for d in range(1,1001):
            steps=terminating_digits(F(1,d))
            if steps is not None:self.assertTrue(encode(F(1,d),digits=steps)['exact'])
    def test_guard_removes_token_not_character(self):
        r=guard_then_remove(F(1,7),2)
        self.assertEqual(r['stored_fractional_tokens'],'051:154')
        self.assertEqual(F(*r['retained_ratio']),F(51,360)+F(154,360**2))
    def test_positive_and_negative_symmetry(self):
        for n in (1,7,13):
            self.assertEqual(decode(encode(F(-n,11))),-decode(encode(F(n,11))))
    def test_invalid_parameters(self):
        for kwargs in ({'base':True},{'base':1},{'digits':-1},{'accuracy':F(0)}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):encode(F(1,3),**kwargs)
        with self.assertRaises(ValueError):encode(0.5)

if __name__=='__main__':unittest.main(verbosity=2)
