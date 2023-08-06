#
# The core class to find min in an array
#
from find_min.sample.sample_file import SampleFile 


class FindMin:


    def print_all(self):
        sf = SampleFile()
        samples = sf.load()

        fm = FindMin()
        fm.print_min(samples)


    def find_min(self, nums):
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


    def print_min(self, samples):
        for sample in samples.values():
            min = self.find_min(sample["sample"])
            print("Min is ({0}) in {1}".format(min, sample["sample"]))


