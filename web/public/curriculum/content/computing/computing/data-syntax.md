# syntax

<table>
<tr><th>Label</th><th>Formula / Concept</th><th>Description</th></tr>
<tr><td>integer</td><td>int a = -3; 32 bit</td><td>$2^{31} \approx 10^{9}$ silent overflow</td></tr>
<tr><td>integer</td><td>unsigned int = 3; 32 bit</td><td>$2^{32}$ positive only larger than int</td></tr>
<tr><td>integer</td><td>long long a = 3; 64 bit</td><td>$2^{63} \approx 10^{18}$ no silent overflow</td></tr>
<tr><td>pairs</td><td>pair&lt;int, string&gt; p;</td><td>p = make_pair(10, "ten");</td></tr>
<tr><td>pairs</td><td>auto [a, b] = p; retrieve</td><td>p.first p.second set and get</td></tr>
<tr><td>arrays</td><td>legacy from C</td><td>vectors have better protections</td></tr>
<tr><td>arrays</td><td>int a [10]; []</td><td>int a[3] = {}; [0, 0, 0]</td></tr>
<tr><td>arrays</td><td>int grid[10][10];</td><td>two dimensional</td></tr>
<tr><td>vectors</td><td>dynamic array</td><td>with changeable size</td></tr>
<tr><td>vectors</td><td>vector&lt;int&gt; v;</td><td>vector&lt;int&gt; a(3); [0, 0, 0]</td></tr>
<tr><td>vectors</td><td>v.push_back(10); add to end</td><td>int i = pop_back(); get from end</td></tr>
<tr><td>vectors</td><td>vector&lt;vector&lt;int&gt;&gt; v;</td><td>two dimensional</td></tr>
<tr><td>vectors</td><td>sort(v.begin(), v.end());</td><td>unique(v.begin(), v.end());</td></tr>
<tr><td>graphs</td><td>edges of each node</td><td>array of dynamic arrays</td></tr>
<tr><td>graphs</td><td>matrix of all edges</td><td>a double array</td></tr>
<tr><td>graphs</td><td>all edges</td><td>dynamic array of pairs</td></tr>
</table>
