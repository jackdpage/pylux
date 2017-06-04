Creating plot background images
===============================

Plot background images must be made in pure SVG and there are several very
specific conditions which must be met for the plot to display correctly.

1. The objects in the plot must be scaled such that one user unit is 1mm.
2. The top-left corner of the image is the intersection of the plaster line and
centre line.
3. Any lines which should have USITT standard line weights have classes
applied.
4. The plot image is taken from the first group found in the SVG file, so
everything must be grouped in a container group.
