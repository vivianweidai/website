# recursion

<table>
<tr><th>Label</th><th>Formula / Concept</th><th>Description</th></tr>
<tr><td>recursion</td><td>iteratively use same function</td><td>to solve a problem</td></tr>
<tr><td>recursion</td><td>base case and recursive case</td><td>call stack with iterative work</td></tr>
<tr><td>recursion</td><td>can be used to make</td><td>subsets and permutations</td></tr>
<tr><td>recursion</td><td colspan="2">vector&lt;int&gt; subset; int n = 3; void search (int k) { if (k == n+ 1) { // process subset } else { // recurse with k in subset subset.push_back(k); search(k+1); // recurse without k in subset subset.pop_back(k); search(k+1); } } search(1);</td></tr>
<tr><td>quicksort</td><td>divide and conquer</td><td>for a more efficient sort</td></tr>
<tr><td>quicksort</td><td>recursion can be used</td><td>for average $O(n\log n)$</td></tr>
</table>
