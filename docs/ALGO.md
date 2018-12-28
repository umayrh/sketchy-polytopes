# Algorithms

## Themes

## Problems

#### Min intervals

> "(a) Given an array A[1..n] of real numbers and an integer k where 2 ≤ k ≤ n, 
> determine the minima of every interval of length k. The output should be an array 
> B[1..n-k+1] where  B[i]=min A[i..i+k-1]. Solve this in O(n log k).
> Hint: one possible solution uses a combination of divide-and-conquer and dynamic 
> programming. Another solution would use other tricks learned in class. 
>
> (b) (BONUS PROBLEM) Solve this in O(n). (12 points) -- Comment. The problem arose 
> in computational vision.
> 
> (c) (BONUS PROBLEM, same conditions as above.) In part (a), replace "minimum" by 
> "median" (assume k is odd). Now solve in O(n log k). (8 points). -- Comment. 
> I am not aware of an O(n) solution. Let me know if you find one, either 
> mentally or in the literature."

(a) Sort the first k numbers in O(k log k) time. For each new number k < i <= n, find
its position using binary search and insert in the new position. Net time = 
O(k log k) + (n - k) * O(log k) ~ O(n log k). Issue: what data structure would allow
O(1) insertion? Alternatively, use heap. Add first k numbers to a heap in O(k log k). 
Then, while tracking the minimum index in the interval, remove the number at the 
minimum interval and add a new number. Duplicates can be stored in the same heap node
along with a counter.

(b) Hmm...

(c) Indexed skip list

## References

* [CMSC 37000](https://www.classes.cs.uchicago.edu/archive/2007/winter/37000-1/hw.html)
