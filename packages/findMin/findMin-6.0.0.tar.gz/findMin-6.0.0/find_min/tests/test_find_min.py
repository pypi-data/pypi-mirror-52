#
# Unit tests for class FindMin
#

import unittest
from find_min.find_min import FindMin
from find_min.sample.sample_file import SampleFile 


class FindMinTests(unittest.TestCase):


    def run_all(self):
        sf = SampleFile()
        samples = sf.load('..\samples.json')


    def test_equal(self, samples):
        fm = FindMin()

        for sample in samples.values():
            result = fm.findMin(sample["sample"])
            self.assertEqual(result, sample["output"])
            print("✓ Test passed for sample {0}".format(sample["sample"]))


if __name__ == '__main__':
    unittest.main()