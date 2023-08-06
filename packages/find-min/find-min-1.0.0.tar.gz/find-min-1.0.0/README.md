# FindMin Package

Given an array of elements that provide a less than operator, find the minimum using as few comparisons as possible. The array shall be given such that the first few elements are strictly monotonically decreasing, the remaining elements are strictly monotonically increasing. The less than operator be defined as the operator that works on such arrays where a < b if min(a,b) == a.


# Solution

If you could detect change in sequence from decreasing to increasing than you could find min with smallest number of comparisions.