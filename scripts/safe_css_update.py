import re
import os

filepath = r"d:\3SD2\Data UAS Visdat\WebStory.html"
backup = r"d:\3SD2\Data UAS Visdat\WebStory_backup.html"

with open(backup, 'r', encoding='utf-8') as f:
    html = f.read()

# Update Google fonts
new_fonts = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">"""

html = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">', new_fonts, html, flags=re.DOTALL)

# Hide encoding-justification
html = html.replace('class="encoding-justification"', 'class="encoding-justification" style="display: none;"')

# Hide story-journey-tracker
html = html.replace('class="story-journey-tracker"', 'class="story-journey-tracker" style="display: none;"')

# Replace the CSS variables to match the new style, but keep original structure intact
new_vars = """
    :root {
      --bg-base: #FAF3E8;
      --bg-surface: #FFFFFF;
      --bg-card: rgba(255, 255, 255, 0.75);
      --bg-card-hover: rgba(255, 250, 240, 0.95);
      --border-subtle: rgba(193, 68, 14, 0.15);
      --border-accent: rgba(193, 68, 14, 0.35);
      --primary: #C1440E;
      --primary-glow: rgba(193, 68, 14, 0.25);
      --accent: #8B5E34;
      --success: #7C9A3C;
      --warning: #D98324;
      --danger: #A33B20;
      --text-main: #3B2615;
      --text-muted: #6B4E32;
      --text-dim: #967A5D;
      
      --font-sans: 'Outfit', sans-serif;
      --font-head: 'Rajdhani', sans-serif;
      --font-mono: 'Orbitron', monospace;
      
      --radius-sm: 12px;
      --radius-md: 20px;
      --radius-lg: 24px;
      --shadow-glass: 0 10px 40px -10px rgba(139, 94, 52, 0.2);
      --transition-fast: 0.3s ease;
      --transition-smooth: 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
"""
html = re.sub(r':root\s*\{.*?(?=\})\}', new_vars, html, flags=re.DOTALL, count=1)

# Add the animated background to body
body_bg = """
    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.7;
      overflow-x: hidden;
      scroll-behavior: smooth;
    }

    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(193, 68, 14, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(193, 68, 14, 0.04) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
      z-index: -2;
    }
    
    body::after {
      content: '';
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at 80% 20%, rgba(193, 68, 14, 0.08) 0%, transparent 60%),
                  radial-gradient(circle at 20% 80%, rgba(139, 94, 52, 0.08) 0%, transparent 60%);
      pointer-events: none;
      z-index: -1;
    }
"""
html = re.sub(r'body\s*\{.*?(?=\})\}', body_bg, html, flags=re.DOTALL, count=1)

# Modify fonts on key classes
html = re.sub(r'(\.hero-title\s*\{[^\}]*)', r'\1 font-family: var(--font-head); ', html)
html = re.sub(r'(\.section-title\s*\{[^\}]*)', r'\1 font-family: var(--font-head); ', html)
html = re.sub(r'(\.brand-title\s*\{[^\}]*)', r'\1 font-family: var(--font-head); ', html)
html = re.sub(r'(\.stat-label\s*\{[^\}]*)', r'\1 font-family: var(--font-head); ', html)
html = re.sub(r'(\.scrolly-step h3\s*\{[^\}]*)', r'\1 font-family: var(--font-head); ', html)
html = re.sub(r'(\.story-callout-title\s*\{[^\}]*)', r'\1 font-family: var(--font-head); ', html)
html = re.sub(r'(\.stat-val\s*\{[^\}]*)', r'\1 font-family: var(--font-mono); ', html)

# Change .glass-panel background 
html = re.sub(r'(\.glass-panel\s*\{.*?background:\s*)var\(--bg-card\)(.*?\})', r'\1var(--bg-card)\2', html, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
