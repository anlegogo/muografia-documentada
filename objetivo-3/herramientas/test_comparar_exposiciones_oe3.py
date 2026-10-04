"""Verifica sentido de comparación, datos inválidos y claves duplicadas."""
import unittest
from comparar_exposiciones_oe3 import relation,unique,mean
class Controls(unittest.TestCase):
    def test_direction(self):
        self.assertEqual(relation(.85,.80),'better')
        self.assertEqual(relation(.15,.01,False),'worse')
        self.assertEqual(relation(.01,.15,False),'better')
    def test_numerical_tie_not_acceptance_margin(self):
        self.assertEqual(relation(1.,1.+1e-14),'numerical_tie')
        self.assertEqual(relation(1.,1.+1e-8),'worse')
    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError):unique([{'id':1},{'id':1}],lambda r:r['id'])
    def test_invalid_support_rejected(self):
        for values in [[],[float('nan')],[float('inf')]]:
            with self.assertRaises(ValueError):mean(values)
        with self.assertRaises(ValueError):relation(float('nan'),1.)
if __name__=='__main__':unittest.main()
