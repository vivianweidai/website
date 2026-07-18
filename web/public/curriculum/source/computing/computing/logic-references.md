# references

<table>
<tr><th>Label</th><th>Formula / Concept</th><th>Description</th></tr>
<tr><td>references</td><td>link two variables</td><td>with flow through updates</td></tr>
<tr><td>references</td><td>int b = a; copies value</td><td>int&amp; b = a; reference other</td></tr>
<tr><td>references</td><td>if referenced variable changes</td><td>so does reference variable</td></tr>
<tr><td>swap</td><td>void swap(int&amp; a, int &amp; b) { int temp = a; a = b; b = temp; }</td><td>permanently alters pass in array</td></tr>
<tr><td>pairs</td><td>auto [a, b] = p;</td><td>copies values only</td></tr>
<tr><td>pairs</td><td>auto&amp; [a, b] = p;</td><td>updates the pair variable</td></tr>
</table>
