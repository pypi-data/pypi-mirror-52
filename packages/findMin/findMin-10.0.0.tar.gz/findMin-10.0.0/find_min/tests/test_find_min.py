#
# Unit tests for class FindMin
#

import unittest
from find_min.find_min import FindMin
from find_min.sample.sample_file import SampleFile 


class FindMinTests(unittest.TestCase):


    def test_sample(self):
        sf = SampleFile()
        samples = sf.load()
        self.test_equal(samples)

    def test_equal(self, samples):
        fm = FindMin()

        for sample in samples.values():
            result = fm.find_min(sample["sample"])
            self.assertEqual(result, sample["output"])
            print("✓ Test passed for sample {0}".format(sample["sample"]))


if __name__ == '__main__':
    unittest.main()