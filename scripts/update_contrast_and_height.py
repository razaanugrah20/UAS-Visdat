import re

with open(r'd:\3SD2\Data UAS Visdat\WebStory.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Heatmap Contrast (Avoid pale colors looking transparent)
html = html.replace("range(['#5C2E0A', '#FBEFDC', '#C1440E'])", "range(['#4A2511', '#E5D0B5', '#B83200'])")
html = html.replace('d3.interpolateYlOrBr', 'd3.interpolateOranges')

# Fix Parallel Coordinates line stroke width more explicitly if needed
# Make sure un-highlighted lines are easily visible
html = html.replace('.pcp-line { fill: none; stroke-opacity: 0.85; stroke-width: 2.5px; transition: stroke-opacity 0.2s, stroke-width 0.2s; }',
                    '.pcp-line { fill: none; stroke-opacity: 0.7; stroke-width: 3px; transition: stroke-opacity 0.2s, stroke-width 0.2s; }')
html = html.replace(".style('stroke-width', '1.6px')", ".style('stroke-width', '3px')")
html = html.replace(".style('stroke-width', '1.2px')", ".style('stroke-width', '2px')")

# The map container was set to 480px inline, let's make it taller.
html = html.replace('height: 480px;', 'height: 550px; flex-shrink: 0;')
html = html.replace('height: 520px; flex-shrink: 0;', 'height: 550px; flex-shrink: 0;')

# Make map-grid even taller if it constraints the sticky container
html = html.replace('height: 650px;', 'height: 700px;')
html = html.replace('height: 600px;', 'height: 700px;')

# Fix the PCP SVG being too faint
html = html.replace('.pcp-line.dimmed { stroke-opacity: 0.08 !important; stroke-width: 1px !important; }',
                    '.pcp-line.dimmed { stroke-opacity: 0.15 !important; stroke-width: 1.5px !important; }')
html = html.replace('.pcp-line.dimmed { stroke-opacity: 0.06 !important; }',
                    '.pcp-line.dimmed { stroke-opacity: 0.15 !important; stroke-width: 1.5px !important; }')

# Heatmap dimming opacity
html = html.replace(".style('opacity', 0.15)", ".style('opacity', 0.3)")
html = html.replace(".style('opacity', 0.25)", ".style('opacity', 0.4)")

# Highlight specific lines
html = html.replace("stroke-opacity: 1 !important; stroke-width: 4px !important;", "stroke-opacity: 1 !important; stroke-width: 5px !important;")

with open(r'd:\3SD2\Data UAS Visdat\WebStory.html', 'w', encoding='utf-8') as f:
    f.write(html)
