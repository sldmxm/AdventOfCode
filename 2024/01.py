import heapq
from collections import Counter

def read_data(file_name: str) -> list[list[int], list[int]]:
   res = [[],[]]
   with open(file_name, 'r') as f:
       for row in f:
           left, right = row.split('   ')
           res[0].append(int(left))
           res[1].append(int(right))
   return res


def get_total_distance(nums1: list[int], nums2: list[int]) -> int:
    heapq.heapify(nums1)
    heapq.heapify(nums2)
    res = 0
    while nums1:
        res += abs(heapq.heappop(nums1) - heapq.heappop(nums2))
    return res

def get_similarity_score(nums1: list[int], nums2: list[int]) -> int:
    nums2_freq = Counter(nums2)
    res = 0
    for num in nums1:
        res += num * nums2_freq.get(num, 0)
    return res

if __name__ == '__main__':
    data = read_data('data/01_input.txt')
    print(f'{get_similarity_score(*data)=}')
    print(f'{get_total_distance(*data)=}')