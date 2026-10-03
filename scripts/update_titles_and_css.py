import re

with open(r'd:\3SD2\Data UAS Visdat\WebStory.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix titles (Remove 'Bab X:', 'Topik X', etc.)
replacements = {
    'Bab 1: Eksodus Industri': 'Eksodus Industri',
    'Bab 2: Lanskap Geospasial': 'Lanskap Geospasial',
    'Bab 3: Inti PCA &amp; Variabel Dominan': 'Inti PCA &amp; Variabel Dominan',
    'Bab 4: Profiling Multivariat': 'Profiling Multivariat',
    'Bab 5: Dekomposisi Sektoral': 'Dekomposisi Sektoral',
    'Bab 6: Sintesis Kebijakan &amp; Makalah': 'Sintesis Kebijakan',
    'Bab 1 &bull; Prolog Cerita Data': 'Prolog Cerita Data',
    'Mulai Menelusuri Cerita: Bab 2 &rarr;': 'Mulai Menelusuri Cerita &rarr;',
    'Topik 1 &bull; Data Geospasial': 'Eksplorasi Geospasial',
    'Topik 2 &bull; Data Berdimensi Tinggi (Multivariat)': 'Dinamika Multivariat',
    'Langkah 1 &bull; Gambaran Nasional': 'Gambaran Nasional',
    'Langkah 2 &bull; Koridor Upah Tinggi': 'Koridor Upah Tinggi',
    'Langkah 3 &bull; Kontras Jawa Tengah': 'Kontras Jawa Tengah',
    'Lanjut ke Bab 3: Mengurai Multivariat &amp; Inti PCA': 'Lanjut ke Analisis Multivariat',
    'Transisi ke Bab 3': 'Fokus Jawa Tengah',
    'Bab 3: Multivariat': 'Multivariat',
    'data-dot-label="Langkah 1: Nasional"': 'data-dot-label="Nasional"',
    'data-dot-label="Langkah 2: Koridor Upah Tinggi"': 'data-dot-label="Koridor Upah Tinggi"',
    'data-dot-label="Langkah 3: Kontras Jateng"': 'data-dot-label="Kontras Jateng"',
    'data-dot-label="Bab 1: Prolog"': 'data-dot-label="Prolog"'
}

for old, new in replacements.items():
    html = html.replace(old, new)

# Fix Parallel Coordinates CSS (make it more contrasty and less transparent)
html = html.replace('.pcp-line { fill: none; stroke-opacity: 0.35; stroke-width: 1.6; transition: stroke-opacity 0.2s, stroke-width 0.2s; }',
                    '.pcp-line { fill: none; stroke-opacity: 0.85; stroke-width: 2.5px; transition: stroke-opacity 0.2s, stroke-width 0.2s; }')
html = html.replace('.pcp-line.highlighted { stroke-opacity: 1 !important; stroke-width: 3.5 !important; stroke: #E8A33D !important; }',
                    '.pcp-line.highlighted { stroke-opacity: 1 !important; stroke-width: 4px !important; stroke: #C1440E !important; z-index: 100; }')
html = html.replace('.pcp-line.dimmed { stroke-opacity: 0.06 !important; }',
                    '.pcp-line.dimmed { stroke-opacity: 0.08 !important; stroke-width: 1px !important; }')

# Fix map height squishing issue
html = html.replace('<div class="glass-panel" style="overflow: hidden; position: relative; height: 480px;">',
                    '<div class="glass-panel" style="overflow: hidden; position: relative; height: 520px; flex-shrink: 0;">')

# Fix heatmap opacity / contrast if explicitly set in CSS, but likely it's D3 JS. Let's see if we can find heatmap JS
# Usually d3.scaleSequential(d3.interpolateOranges) is used.
# If opacity is used in heatmap drawing:
html = html.replace('.style("opacity", 0.8)', '.style("opacity", 1)')

with open(r'd:\3SD2\Data UAS Visdat\WebStory.html', 'w', encoding='utf-8') as f:
    f.write(html)
