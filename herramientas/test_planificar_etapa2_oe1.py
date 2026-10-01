"""Contrastes de límites exactos, simetría, conteos y presupuesto del plan."""
import math
import unittest
from scipy.stats import binomtest
from planificar_etapa2_oe1 import cp, interval, manifest, TARGET_N


class PlanTests(unittest.TestCase):
    def test_exact_reference(self):
        for n in (1, 25, 1000):
            for k in (0, n//2, n):
                ref = binomtest(k, n).proportion_ci(confidence_level=.975, method='exact')
                for actual, expected in zip(cp(k,n), (ref.low, ref.high)):
                    self.assertAlmostEqual(actual, expected, places=10)

    def test_zero_formula_and_nonzero_uncertainty(self):
        lo, hi = interval([TARGET_N,0,0,0])['interval95_conservative_per_million']
        exact = -math.expm1(math.log(.0125)/TARGET_N)*1e6
        self.assertAlmostEqual(hi, exact, places=9)
        self.assertEqual(lo, -hi)
        self.assertGreater(hi, 0)

    def test_swap(self):
        x=interval([99990,7,2,1]); y=interval([99990,2,7,1])
        self.assertEqual(x['delta_per_million'], -y['delta_per_million'])
        self.assertEqual(x['interval95_conservative_per_million'], [-v for v in reversed(y['interval95_conservative_per_million'])])

    def test_decisions(self):
        for counts, decision in [([TARGET_N,0,0,0],'dentro_del_margen'),([TARGET_N-1,1,0,0],'dentro_del_margen'),([TARGET_N-2,2,0,0],'inconcluso'),([TARGET_N-20,20,0,0],'diferencia_relevante')]:
            self.assertEqual(interval(counts)['decision_numerica'], decision)

    def test_invalid(self):
        for counts in ([0,0,0,0], [10,-1,0,0], [1.5,0,0,0]):
            with self.assertRaises(ValueError): interval(counts)

    def test_manifest_pairing(self):
        rows=manifest(); self.assertEqual(len(rows),55)
        self.assertEqual(sum(r['n'] for r in rows),48700000)
        original=[r for r in rows if not r['repeat_of']]
        self.assertEqual(len({r['run_id'] for r in rows}),55)
        self.assertEqual(len({r['source_seed'] for r in original}),27)
        self.assertEqual(len({r['transport_seed'] for r in original}),27)
        for b in (r for r in original if r['variant']=='B'):
            a=next(r for r in original if r['geometry_id']==b['geometry_id'] and r['replica']==b['replica'] and r['variant']=='A')
            for key in ('n','view','source_seed','transport_seed'): self.assertEqual(a[key],b[key])


if __name__ == '__main__': unittest.main()
