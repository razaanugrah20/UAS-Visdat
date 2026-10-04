import re
import os

filepath = r"d:\3SD2\Data UAS Visdat\WebStory.html"


with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()


# Update Google fonts
new_fonts = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">"""

html = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">', new_fonts, html, flags=re.DOTALL)

# Hide encoding-justification blocks (too dense)
html = html.replace('class="encoding-justification"', 'class="encoding-justification" style="display: none;"')

# Hide story-journey-tracker
html = html.replace('class="story-journey-tracker"', 'class="story-journey-tracker" style="display: none;"')

# Create a new style block
new_css = """
  <style>
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

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

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

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(193, 68, 14, 0.2); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(193, 68, 14, 0.4); }

    .glass-panel {
      background: var(--bg-card);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-glass);
      transition: var(--transition-smooth);
    }
    
    .glass-panel:hover {
      box-shadow: 0 15px 50px -10px rgba(139, 94, 52, 0.3);
      border-color: var(--border-accent);
    }

    .container { max-width: 1440px; margin: 0 auto; padding: 0 32px; }

    header {
      position: sticky; top: 0; z-index: 1000;
      background: rgba(250, 243, 232, 0.7);
      backdrop-filter: blur(24px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 16px 0;
    }

    .nav-wrapper { display: flex; justify-content: space-between; align-items: center; gap: 16px; }

    .brand { display: flex; align-items: center; gap: 16px; text-decoration: none; color: var(--text-main); }
    
    .brand-logo {
      width: 44px; height: 44px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border-radius: var(--radius-sm);
      display: flex; align-items: center; justify-content: center;
      color: white; box-shadow: 0 0 20px var(--primary-glow);
    }

    .brand-title { font-family: var(--font-head); font-weight: 700; font-size: 1.2rem; letter-spacing: -0.01em; display: flex; flex-direction: column; }
    .brand-subtitle { font-family: var(--font-sans); font-size: 0.75rem; color: var(--text-muted); font-weight: 400; }

    .nav-tabs { display: flex; align-items: center; gap: 8px; background: rgba(255, 248, 238, 0.5); padding: 6px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); }
    .nav-tab-btn {
      padding: 8px 16px; border: none; background: transparent; color: var(--text-muted);
      font-family: var(--font-sans); font-size: 0.85rem; font-weight: 500; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: var(--transition-fast); text-decoration: none;
    }
    .nav-tab-btn:hover { color: var(--text-main); background: rgba(193, 68, 14, 0.05); }
    .nav-tab-btn.active { color: var(--primary); background: rgba(193, 68, 14, 0.1); font-weight: 600; }

    .header-badge { display: inline-flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--primary); background: rgba(193, 68, 14, 0.08); border: 1px solid var(--border-accent); padding: 6px 14px; border-radius: 9999px; font-family: var(--font-mono); }

    .hero { position: relative; padding: 100px 0 60px; overflow: hidden; text-align: center; display: flex; flex-direction: column; align-items: center; }
    .hero-content { position: relative; max-width: 1000px; display: flex; flex-direction: column; align-items: center; }
    
    .hero-tag { display: inline-flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: var(--primary); margin-bottom: 24px; padding: 6px 16px; border-radius: 9999px; background: rgba(193, 68, 14, 0.08); border: 1px solid rgba(193, 68, 14, 0.2); }
    
    .hero-title { font-family: var(--font-head); font-size: clamp(3rem, 6vw, 5.5rem); font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; margin-bottom: 24px; color: var(--text-main); }
    .hero-title .accent-line { display: block; background: linear-gradient(100deg, var(--primary) 20%, var(--accent) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero-desc { font-size: 1.2rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 48px; max-width: 70ch; }

    .stat-ribbon { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; margin-bottom: 60px; width: 100%; max-width: 1200px; }
    .stat-card { padding: 28px 24px; display: flex; align-items: center; gap: 20px; text-align: left; }
    .stat-icon { width: 56px; height: 56px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0; background: rgba(193, 68, 14, 0.1); color: var(--primary); }
    .stat-val { font-size: 2.5rem; font-weight: 700; color: var(--primary); font-family: var(--font-mono); line-height: 1.05; }
    .stat-label { font-size: 0.8rem; color: var(--text-muted); margin-top: 6px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; font-family: var(--font-head); }

    .section-block { padding: 80px 0; border-top: 1px solid rgba(193, 68, 14, 0.1); }
    .section-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px; flex-wrap: wrap; gap: 16px; }
    .section-title-wrap { max-width: 900px; }
    .section-subtitle { font-size: 0.85rem; color: var(--primary); font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; font-family: var(--font-head); }
    .section-title { font-size: 2.4rem; font-weight: 700; font-family: var(--font-head); letter-spacing: -0.02em; color: var(--text-main); margin-bottom: 12px; }
    .section-lead { color: var(--text-muted); font-size: 1.05rem; line-height: 1.7; max-width: 80ch; }

    .control-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px 20px; margin-bottom: 24px; flex-wrap: wrap; box-shadow: var(--shadow-glass); }
    .btn-group { display: flex; align-items: center; gap: 8px; }
    .ctrl-btn { padding: 8px 16px; background: rgba(255, 255, 255, 0.5); border: 1px solid var(--border-subtle); color: var(--text-muted); font-family: var(--font-sans); font-size: 0.85rem; font-weight: 500; border-radius: var(--radius-sm); cursor: pointer; display: inline-flex; align-items: center; gap: 8px; transition: var(--transition-fast); }
    .ctrl-btn:hover { background: rgba(193, 68, 14, 0.08); color: var(--text-main); border-color: var(--border-accent); }
    .ctrl-btn.active { background: var(--primary); color: #FFFFFF; border-color: var(--primary); font-weight: 600; box-shadow: 0 4px 15px rgba(193, 68, 14, 0.3); }
    .select-dropdown { background: rgba(255, 255, 255, 0.8); border: 1px solid var(--border-subtle); color: var(--text-main); padding: 8px 14px; border-radius: var(--radius-sm); font-size: 0.85rem; font-family: var(--font-sans); outline: none; cursor: pointer; }
    .select-dropdown:focus { border-color: var(--primary); }

    .map-grid { display: grid; grid-template-columns: 1fr 380px; gap: 24px; height: 650px; }
    #geoMap { width: 100%; height: 100%; border-radius: var(--radius-md); background: #1C1917; z-index: 10; border: 1px solid var(--border-subtle); }
    .map-sidebar { display: flex; flex-direction: column; gap: 20px; height: 100%; overflow-y: auto; padding-right: 8px; }
    .map-sidebar::-webkit-scrollbar { width: 4px; }
    
    .info-card { padding: 24px; }
    .info-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border-subtle); }
    .info-card-title { font-family: var(--font-head); font-size: 1.1rem; font-weight: 700; color: var(--text-main); display: flex; align-items: center; gap: 8px; }
    .region-detail-empty { color: var(--text-dim); font-size: 0.9rem; text-align: center; padding: 40px 10px; }
    
    .data-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed rgba(193, 68, 14, 0.15); font-size: 0.9rem; }
    .data-row:last-child { border-bottom: none; }
    .data-row .data-val { font-weight: 700; font-family: var(--font-mono); color: var(--primary); }

    .legend-box { padding: 20px; }
    .legend-bar { height: 8px; border-radius: 4px; margin: 12px 0 8px; background: linear-gradient(to right, #FFF6E0, #F5C77E, #E08A3C, #B3471F, #5C2E0A); }
    .legend-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono); }

    .mv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
    .chart-card { padding: 24px; display: flex; flex-direction: column; min-height: 520px; position: relative; }
    .chart-card-full { grid-column: span 2; min-height: 480px; }
    .chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .chart-title { font-family: var(--font-head); font-size: 1.2rem; font-weight: 700; color: var(--text-main); display: flex; align-items: center; gap: 10px; }
    .chart-badge { font-size: 0.75rem; padding: 4px 10px; background: rgba(193, 68, 14, 0.1); border-radius: 6px; color: var(--primary); font-family: var(--font-mono); font-weight: 600; }
    .chart-body { flex: 1; width: 100%; min-height: 400px; position: relative; }

    /* Clean scrolly step design */
    .scrolly-wrap { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); gap: 40px; align-items: start; margin-top: 40px; }
    .scrolly-sticky { position: sticky; top: 100px; align-self: start; max-height: calc(100vh - 120px); display: flex; flex-direction: column; gap: 20px; }
    .scrolly-steps { display: flex; flex-direction: column; gap: 20px; }
    
    .scrolly-step {
      padding: 40px 32px; margin-bottom: 20px;
      border-radius: var(--radius-lg);
      background: rgba(255, 255, 255, 0.4);
      border: 1px solid transparent;
      opacity: 0.5; transform: translateY(10px);
      transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    .scrolly-step:hover { opacity: 0.8; }
    .scrolly-step.is-active {
      opacity: 1; transform: translateY(0);
      background: var(--bg-card);
      border-color: var(--border-accent);
      box-shadow: 0 15px 40px rgba(139, 94, 52, 0.15);
    }
    .scrolly-step-eyebrow { display: inline-flex; align-items: center; gap: 8px; font-family: var(--font-mono); font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--primary); font-weight: 700; margin-bottom: 16px; background: rgba(193, 68, 14, 0.1); padding: 4px 12px; border-radius: 999px; }
    .scrolly-step h3 { font-family: var(--font-head); font-size: 1.6rem; font-weight: 700; color: var(--text-main); margin-bottom: 16px; line-height: 1.2; }
    .scrolly-step p { font-size: 1rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 12px; }
    .scrolly-step strong { color: var(--primary); }

    /* Elegant Callout */
    .story-callout {
      background: rgba(255, 255, 255, 0.7);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border-accent);
      border-radius: var(--radius-lg);
      padding: 40px; margin: 40px auto;
      max-width: 900px; text-align: left;
      box-shadow: var(--shadow-glass);
      position: relative; overflow: hidden;
    }
    .story-callout::before {
      content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%;
      background: linear-gradient(to bottom, var(--primary), var(--accent));
    }
    .story-callout-header { display: flex; align-items: center; gap: 10px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; }
    .story-callout-title { font-family: var(--font-head); font-size: 2rem; font-weight: 700; color: var(--text-main); margin-bottom: 20px; line-height: 1.2; }
    .story-callout-desc { font-size: 1.1rem; line-height: 1.8; color: var(--text-muted); margin-bottom: 16px; }

    /* PCA Anatomy Simplified */
    .pca-anatomy-box { margin: 40px 0; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 32px; box-shadow: var(--shadow-glass); }
    .pca-anatomy-title { font-family: var(--font-head); font-size: 1.5rem; font-weight: 700; color: var(--text-main); display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
    .pca-grid-dimensions { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 24px; }
    .pca-dim-card { background: rgba(255, 255, 255, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 24px; transition: var(--transition-fast); }
    .pca-dim-card:hover { border-color: var(--border-accent); box-shadow: 0 10px 30px rgba(193, 68, 14, 0.1); }
    .pca-dim-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .pca-dim-name { font-family: var(--font-head); font-size: 1.2rem; font-weight: 700; color: var(--text-main); }
    .pca-dim-var { font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
    .dim1 .pca-dim-var { background: rgba(193, 68, 14, 0.1); color: var(--primary); }
    .dim2 .pca-dim-var { background: rgba(139, 94, 52, 0.1); color: var(--accent); }
    .pca-var-bar-list { margin-top: 20px; display: flex; flex-direction: column; gap: 12px; }
    .pca-var-bar-row { display: flex; flex-direction: column; gap: 6px; font-size: 0.9rem; }
    .pca-var-bar-label { display: flex; justify-content: space-between; color: var(--text-muted); font-weight: 500; }
    .pca-var-bar-label strong { font-family: var(--font-mono); color: var(--text-main); }
    .pca-var-bar-track { height: 8px; background: rgba(193, 68, 14, 0.1); border-radius: 4px; overflow: hidden; }
    .pca-var-bar-fill { height: 100%; border-radius: 4px; }
    .dim1 .pca-var-bar-fill { background: linear-gradient(90deg, #8B5E34, #C1440E); }
    .dim2 .pca-var-bar-fill { background: linear-gradient(90deg, #A33B20, #D9713C); }

    .story-tour-section { background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); border: 1px solid var(--border-accent); border-radius: var(--radius-lg); padding: 24px 32px; margin-bottom: 32px; }
    .story-tour-title { font-family: var(--font-head); font-size: 1.1rem; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }

    /* Hierarchy & Makalah adjustments for cleanliness */
    .hierarchy-container { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; min-height: 600px; }
    .story-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 32px; }
    .narrative-card { padding: 40px; }
    .narrative-card h3 { font-family: var(--font-head); font-size: 1.6rem; font-weight: 700; color: var(--text-main); margin-bottom: 20px; }
    .narrative-card p { color: var(--text-muted); font-size: 1.05rem; line-height: 1.8; margin-bottom: 20px; }
    .key-finding-box { background: rgba(193, 68, 14, 0.05); border: 1px solid var(--border-accent); border-radius: var(--radius-md); padding: 24px; margin: 24px 0; }
    
    footer { border-top: 1px solid rgba(193, 68, 14, 0.15); padding: 40px 0; background: transparent; color: var(--text-muted); font-size: 0.9rem; margin-top: 60px; }
    
    /* Global D3 Tooltip */
    .custom-tooltip { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid var(--border-accent); border-radius: var(--radius-sm); color: var(--text-main); padding: 12px 16px; font-size: 0.85rem; pointer-events: none; z-index: 9999; box-shadow: var(--shadow-glass); opacity: 0; transition: opacity 0.2s ease; max-width: 300px; font-family: var(--font-sans); }
    .custom-tooltip .tt-title { font-family: var(--font-head); font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: var(--primary); }

    /* D3 styling overrides */
    .axis text { font-family: var(--font-mono) !important; font-size: 10px !important; fill: var(--text-muted) !important; }
    
    @media (max-width: 1024px) {
      .pca-grid-dimensions, .map-grid, .hierarchy-container, .story-grid, .mv-grid, .scrolly-wrap { grid-template-columns: 1fr; }
      .chart-card-full { grid-column: span 1; }
      .scrolly-sticky { position: relative; top: 0; max-height: none; }
    }
  </style>
"""

# Replace the style block entirely
html = re.sub(r'<style>.*?</style>', new_css, html, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
