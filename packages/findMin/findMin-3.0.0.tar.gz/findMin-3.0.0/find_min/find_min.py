#
# The core class to find min in an array
#
from find_min.sample.sample_file import SampleFile 


class FindMin:


    def printSample(self):
        sf = SampleFile()
        samples = sf.load('samples.json')

        fm = FindMin()
        fm.printMin(samples)


    def findMin(self, nums):
        i = 1
        size = len(nums)
        minimum = None
        
        if (size == 1):
            return nums[0]
        
        while i < size:
            minimum = nums[i]
            if (nums[i-1] < minimum):
                minimum = nums[i-1]
                break

            i += 1
        
        return minimum


    def printMin(self, samples):
        for sample in samples.values():
            min = self.findMin(sample["sample"])
            print("Min is ({0}) in {1}".format(min, sample["sample"]))


