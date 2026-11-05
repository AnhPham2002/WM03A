import os
import re
import glob
import html
import markdown
from bs4 import BeautifulSoup

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_DIR = os.path.join(BASE_DIR, "markdown")
HTML_DIR = os.path.join(BASE_DIR, "html")

os.makedirs(HTML_DIR, exist_ok=True)

CSS_STYLES = """
:root {
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --accent: #0284c7;
  --accent-light: #f0f9ff;
  --accent-dark: #0369a1;
  --bg: #f8fafc;
  --card-bg: #ffffff;
  --fg: #1e293b;
  --fg-muted: #64748b;
  --border: #e2e8f0;
  --sidebar-w: 280px;
  --header-h: 70px;
  --radius: 8px;
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg);
  color: var(--fg);
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Master Navigation Bar */
.master-nav-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 0.88rem;
}
.btn-back-master {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.95rem;
  background: #2563eb;
  color: #ffffff !important;
  font-weight: 600;
  border-radius: 6px;
  text-decoration: none !important;
  box-shadow: 0 2px 5px rgba(37, 99, 235, 0.25);
  transition: all 0.15s ease;
}
.btn-back-master:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.35);
}
.nav-divider {
  color: #94a3b8;
  font-weight: 500;
}
.nav-current-title {
  color: #475569;
  font-weight: 500;
}
.badge-master-doc {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.85rem;
  background: #f1f5f9;
  color: #0f172a;
  font-weight: 600;
  font-size: 0.84rem;
  border-radius: 20px;
  border: 1px solid #cbd5e1;
}

/* Header Banner */
.header {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: #fff;
  padding: 2rem 2.5rem;
  border-radius: var(--radius);
  margin-bottom: 2rem;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}
.header::after {
  content: "";
  position: absolute;
  top: -50%; right: -10%;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(37,99,235,0.15) 0%, transparent 70%);
  pointer-events: none;
}
.header h1 {
  font-size: 1.85rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  margin-bottom: 0.5rem;
  color: #f8fafc;
}
.header .meta {
  font-size: 0.85rem;
  color: #94a3b8;
  line-height: 2;
  opacity: 0.92;
}
.header .meta strong {
  color: #93c5fd;
}

/* Headings */
h2 {
  font-size: 1.375rem;
  font-weight: 700;
  margin: 2.5rem 0 1rem;
  padding: 0.6rem 0 0.6rem 1rem;
  border-left: 4px solid var(--accent);
  background: var(--accent-light);
  border-radius: 0 var(--radius) var(--radius) 0;
  color: var(--fg);
}
h2 a, h3 a, h4 a {
  color: inherit;
  text-decoration: none;
}
h2 a:hover, h3 a:hover, h4 a:hover {
  text-decoration: underline;
}
h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 1.75rem 0 0.75rem;
  color: var(--accent-dark);
}
h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 1.25rem 0 0.5rem;
  color: #475569;
}

p, ul, ol {
  margin-bottom: 1rem;
}
ul, ol {
  padding-left: 1.5rem;
}
li {
  margin-bottom: 0.3rem;
}

/* Links */
a {
  color: var(--primary);
  text-decoration: none;
  transition: color 0.15s;
}
a:hover {
  color: var(--primary-hover);
  text-decoration: underline;
}

/* Code & Pre */
code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  background: #f1f5f9;
  color: #0f172a;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}
pre {
  font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, 'DejaVu Sans Mono', 'Courier New', monospace;
  font-variant-ligatures: none;
  tab-size: 4;
  background: #0f172a;
  color: #f8fafc;
  padding: 1.25rem;
  border-radius: var(--radius);
  overflow-x: auto;
  margin: 1.25rem 0;
  font-size: 0.85rem;
  line-height: 1.5;
  box-shadow: var(--shadow);
}
pre code {
  font-family: inherit;
  white-space: pre;
  background: none;
  color: inherit;
  padding: 0;
  border: none;
}

/* Tables */
.table-wrap {
  width: 100%;
  overflow-x: auto;
  margin: 1.5rem 0;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  background: var(--card-bg);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
  margin: 0;
}
th, td {
  padding: 0.6rem 0.85rem;
  border: 1px solid var(--border);
  text-align: left;
  vertical-align: top;
  line-height: 1.5;
  min-width: 110px;
}
th {
  background: #f1f5f9;
  font-weight: 600;
  color: var(--fg);
}
td code, th code {
  white-space: nowrap;
  font-size: 0.8rem;
}
tr:nth-child(even) {
  background: #f8fafc;
}
tr:hover {
  background: #f1f5f9;
}

/* Alert Boxes */
.alert {
  padding: 1rem 1.25rem;
  border-radius: var(--radius);
  margin: 1.25rem 0;
  font-size: 0.9rem;
  border-left: 4px solid;
}
.alert-info {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #1e40af;
}
.alert-warning {
  background: #fffbebfb;
  border-color: #f59e0b;
  color: #92400e;
}
.alert-danger {
  background: #fef2f2;
  border-color: #ef4444;
  color: #991b1b;
}
.alert-success {
  background: #f0fdf4;
  border-color: #22c55e;
  color: #166534;
}

/* Revision History Styles */
.revision-table {
  border-collapse: separate;
  border-spacing: 0;
  border: 1px solid #cbd5e1;
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.revision-table th {
  background: #0f172a !important;
  color: #ffffff !important;
  font-weight: 600;
  padding: 0.85rem 1rem;
  letter-spacing: 0.02em;
  font-size: 0.86rem;
}
.revision-table th:nth-child(1), .revision-table td:nth-child(1) { width: 92px; white-space: nowrap; }
.revision-table th:nth-child(2), .revision-table td:nth-child(2) { width: 104px; white-space: nowrap; }
.revision-table th:nth-child(3), .revision-table td:nth-child(3) { width: 130px; }
.revision-table td {
  padding: 0.8rem 1rem;
  vertical-align: middle;
  border-color: #e2e8f0;
}
.revision-table tr:hover td {
  background-color: #f1f5f9;
}
.badge-version {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.25rem 0.65rem;
  background: #2563eb;
  color: #ffffff !important;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.8rem;
  font-family: 'JetBrains Mono', monospace;
  box-shadow: 0 1px 3px rgba(37, 99, 235, 0.3);
}
.badge-version-new {
  background: #059669;
  box-shadow: 0 1px 3px rgba(5, 150, 105, 0.3);
}
.qa-impact-cell {
  background: #fffbeb !important;
  color: #92400e;
  font-weight: 500;
  border-left: 3px solid #f59e0b !important;
  padding: 0.75rem 1rem;
  border-radius: 4px;
}
.qa-tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.15rem 0.5rem;
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
  border-radius: 4px;
  font-size: 0.76rem;
  font-weight: 700;
  margin-right: 0.4rem;
}

/* Layout */
.layout {
  display: flex;
  max-width: none;
  width: 100%;
  margin: 0;
  padding: 0 1.5rem 3rem;
  gap: 1.5rem;
}
.sidebar {
  width: var(--sidebar-w);
  flex-shrink: 0;
}
.main {
  flex: 1;
  min-width: 0;
  background: var(--card-bg);
  padding: 2.5rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}

/* Sticky TOC Sidebar */
.toc {
  position: sticky;
  top: 1rem;
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}
.toc-title {
  font-weight: 700;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  color: var(--accent-dark);
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}
.toc-title::before { content: "📑 "; }

/* Sidebar Master Link */
.toc-master-box {
  margin-bottom: 0.85rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.toc-master-link {
  display: flex !important;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.75rem !important;
  background: #eff6ff !important;
  color: #1d4ed8 !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  border: 1px solid #bfdbfe !important;
  text-decoration: none !important;
  font-size: 0.85rem !important;
  transition: all 0.15s ease;
}
.toc-master-link:hover {
  background: #2563eb !important;
  color: #ffffff !important;
  border-color: #2563eb !important;
}

.toc ol { list-style: none; padding: 0; margin: 0; }
.toc a {
  display: block;
  padding: 0.3rem 0.6rem;
  color: var(--fg-muted);
  text-decoration: none;
  font-size: 0.84rem;
  border-radius: 4px;
  transition: all 0.15s;
  border-left: 2px solid transparent;
}
.toc a:hover {
  color: var(--accent);
  background: var(--accent-light);
}
.toc a.active {
  color: var(--accent-dark);
  background: var(--accent-light);
  font-weight: 600;
  border-left-color: var(--accent);
}
.toc li.sub a {
  padding-left: 1.2rem;
  font-size: 0.8rem;
}

/* Mobile TOC toggle */
.toc-toggle {
  display: none;
  position: fixed;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 1001;
  width: 40px;
  height: 40px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 50%;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
}

/* Floating Master Quick Button */
.floating-master-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 5rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  background: #1e293b;
  color: #ffffff !important;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 30px;
  box-shadow: var(--shadow-lg);
  text-decoration: none !important;
  z-index: 998;
  transition: all 0.2s ease;
  border: 1px solid rgba(255,255,255,0.15);
}
.floating-master-btn:hover {
  background: #0f172a;
  transform: translateY(-2px);
  box-shadow: 0 12px 20px -4px rgba(0,0,0,0.3);
}

/* Back to Top */
.back-top {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 44px;
  height: 44px;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
  z-index: 999;
}
.back-top.visible {
  opacity: 1;
  visibility: visible;
}
.back-top:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

/* Diagram Card Wrapper & Responsive Styling */
.diagram-wrapper {
  margin: 2.2rem 0;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.2s ease;
}
.diagram-wrapper:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
  border-color: #93c5fd;
}
.diagram-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.65rem 1.1rem;
  background: #f8fafc;
  border-bottom: 1px solid var(--border);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--accent-dark);
}
.diagram-title {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.diagram-actions {
  display: flex;
  gap: 0.5rem;
}
.btn-diagram-action {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.85rem;
  font-size: 0.82rem;
  font-weight: 500;
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-diagram-action:hover {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
  transform: translateY(-1px);
}
.diagram-body {
  padding: 1.5rem;
  overflow-x: auto;
  background: #fafafa;
  text-align: center;
  cursor: zoom-in;
}
.diagram-body .mermaid {
  display: block;
  width: 100%;
}
.diagram-body .mermaid svg {
  display: block;
  margin: 0 auto;
  height: auto !important;
  font-family: 'Inter', sans-serif !important;
}

/* Diagram Lightbox Modal */
.diagram-modal {
  display: none;
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(6px);
  z-index: 9999;
  justify-content: center;
  align-items: center;
}
.diagram-modal.active {
  display: flex;
}
.diagram-modal-header {
  position: absolute;
  top: 1.2rem; right: 1.8rem; left: 1.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10000;
}
.diagram-modal-title {
  color: #ffffff;
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.diagram-modal-controls {
  display: flex;
  gap: 0.5rem;
}
.diagram-modal-btn {
  padding: 0.45rem 0.9rem;
  background: rgba(255, 255, 255, 0.18);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.diagram-modal-btn:hover {
  background: rgba(255, 255, 255, 0.35);
}
.diagram-modal-btn.close-btn {
  background: #ef4444;
  border-color: #dc2626;
}
.diagram-modal-btn.close-btn:hover {
  background: #dc2626;
}
.diagram-modal-content {
  width: 92vw;
  height: 84vh;
  margin-top: 3.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
  background: #ffffff;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  cursor: grab;
}
.diagram-modal-content:active {
  cursor: grabbing;
}
.diagram-modal-content svg {
  max-width: none !important;
  max-height: none !important;
  transform-origin: center center;
  transition: transform 0.1s ease-out;
}

@media (max-width: 992px) {
  .layout { flex-direction: column; padding: 0 1rem 2rem; }
  .sidebar {
    position: fixed;
    top: 0; left: -100%;
    width: 280px; height: 100vh;
    z-index: 1002;
    transition: left 0.3s ease;
  }
  .sidebar.open { left: 0; }
  .toc-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0,0,0,0.4);
    z-index: 1000;
  }
  .toc-overlay.show { display: block; }
  .toc-toggle { display: flex; align-items: center; justify-content: center; }
  .main { padding: 1.5rem; }
  .floating-master-btn { right: 4.5rem; padding: 0.5rem 0.8rem; font-size: 0.8rem; }
}

@media print {
  body { background: #fff; color: #000; font-size: 9.5pt; }
  .layout { display: block; padding: 0; }
  .sidebar { display: none !important; }
  .main { max-width: 100% !important; padding: 0 !important; border: none; box-shadow: none; }
  .header {
    background: #1e293b !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    padding: 1.25rem 1.5rem !important;
    margin-bottom: 1.5rem !important;
  }
  pre { white-space: pre-wrap; word-wrap: break-word; font-size: 8pt; }
  table { page-break-inside: auto; font-size: 8.5pt; width: 100% !important; margin: 1rem 0; }
  tr { page-break-inside: avoid; page-break-after: auto; }
  th, td { padding: 0.45rem 0.6rem !important; word-break: break-word; }
  h2, h3 { page-break-after: avoid; }
  .floating-master-btn, .master-nav-bar, .back-top, .toc-toggle, .progress-bar { display: none !important; }
}
"""

JS_SCRIPT = """
// ── Thanh tiến trình đọc ──
window.addEventListener('scroll', () => {
  const h = document.documentElement;
  const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
  const pb = document.getElementById('progressBar');
  if (pb) pb.style.width = pct + '%';
});

// ── Nút Back-to-top ──
const backTop = document.getElementById('backTop');
if (backTop) {
  window.addEventListener('scroll', () => {
    backTop.classList.toggle('visible', window.scrollY > 300);
  });
  backTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ── Toggle TOC trên Mobile ──
const tocToggle = document.getElementById('tocToggle');
const sidebar   = document.getElementById('sidebar');
const overlay   = document.getElementById('tocOverlay');
function closeToc() {
  if (sidebar) sidebar.classList.remove('open');
  if (overlay) overlay.classList.remove('show');
}
if (tocToggle) {
  tocToggle.addEventListener('click', () => {
    if (sidebar) sidebar.classList.toggle('open');
    if (overlay) overlay.classList.toggle('show');
  });
}
if (overlay) overlay.addEventListener('click', closeToc);

// ── TOC active highlight khi cuộn ──
const tocLinks = document.querySelectorAll('.toc a');
const sections = [];
tocLinks.forEach(a => {
  const href = a.getAttribute('href');
  if (href && href.startsWith('#')) {
    const target = document.getElementById(href.substring(1));
    if (target) sections.push({ el: target, link: a });
  }
});
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => {
    if (s.el.getBoundingClientRect().top <= 100) current = '#' + s.el.id;
  });
  tocLinks.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === current);
  });
});

// ── Diagram Modal & Zoom Logic ──
let currentZoom = 1;
let currentSvg = null;
let isPanning = false, startX = 0, startY = 0, scrollLeft = 0, scrollTop = 0;

function openDiagramModal(btnElement) {
  const wrapper = btnElement.closest('.diagram-wrapper');
  if (!wrapper) return;
  const svg = wrapper.querySelector('.mermaid svg');
  if (!svg) return;

  const modal = document.getElementById('diagramModal');
  const modalContainer = document.getElementById('diagramModalContainer');
  if (!modal || !modalContainer) return;
  
  modalContainer.innerHTML = '';
  const clonedSvg = svg.cloneNode(true);
  const vb = svg.viewBox && svg.viewBox.baseVal;
  if (vb && vb.width > 0) {
    clonedSvg.setAttribute('width', vb.width);
    clonedSvg.setAttribute('height', vb.height);
  }
  clonedSvg.style.transform = 'scale(1)';
  clonedSvg.style.maxWidth = 'none';
  clonedSvg.style.maxHeight = 'none';
  clonedSvg.style.height = 'auto';
  modalContainer.appendChild(clonedSvg);

  currentSvg = clonedSvg;
  currentZoom = 1;

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeDiagramModal() {
  const modal = document.getElementById('diagramModal');
  if (modal) modal.classList.remove('active');
  document.body.style.overflow = '';
}

function zoomDiagram(delta) {
  if (!currentSvg) return;
  currentZoom = Math.min(Math.max(0.4, currentZoom + delta), 4);
  currentSvg.style.transform = `scale(${currentZoom})`;
}

function resetDiagramZoom() {
  if (!currentSvg) return;
  currentZoom = 1;
  currentSvg.style.transform = 'scale(1)';
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.diagram-body').forEach(body => {
    body.addEventListener('click', (e) => {
      if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
      const btn = body.closest('.diagram-wrapper').querySelector('.btn-zoom');
      if (btn) openDiagramModal(btn);
    });
  });

  const modalContainer = document.getElementById('diagramModalContainer');
  if (modalContainer) {
    modalContainer.addEventListener('mousedown', (e) => {
      isPanning = true;
      startX = e.pageX - modalContainer.offsetLeft;
      startY = e.pageY - modalContainer.offsetTop;
      scrollLeft = modalContainer.scrollLeft;
      scrollTop = modalContainer.scrollTop;
    });

    modalContainer.addEventListener('mouseleave', () => isPanning = false);
    modalContainer.addEventListener('mouseup', () => isPanning = false);
    modalContainer.addEventListener('mousemove', (e) => {
      if (!isPanning) return;
      e.preventDefault();
      const x = e.pageX - modalContainer.offsetLeft;
      const y = e.pageY - modalContainer.offsetTop;
      const walkX = (x - startX) * 1.5;
      const walkY = (y - startY) * 1.5;
      modalContainer.scrollLeft = scrollLeft - walkX;
      modalContainer.scrollTop = scrollTop - walkY;
    });

    modalContainer.addEventListener('wheel', (e) => {
      e.preventDefault();
      if (e.deltaY < 0) zoomDiagram(0.15);
      else zoomDiagram(-0.15);
    }, { passive: false });
  }
});
"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text or "section"

def convert_md_file(md_path):
    filename = os.path.basename(md_path)
    base_name = os.path.splitext(filename)[0]
    rel_path = os.path.relpath(md_path, MD_DIR)
    html_path = os.path.join(HTML_DIR, os.path.splitext(rel_path)[0] + ".html")
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    is_master = (base_name == "README")

    rel_dir = os.path.dirname(os.path.relpath(md_path, MD_DIR))
    depth = 0 if rel_dir in ("", ".") else len(rel_dir.split(os.sep))
    master_prefix = "../" * depth if depth else "./"
    master_href = f"{master_prefix}README.html"

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Extract title & metadata
    title = base_name.replace('_', ' ').title()
    h1_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        # Remove top h1 from md_text as it will go into header banner
        md_text = re.sub(r'^#\s+.+$\n?', '', md_text, count=1, flags=re.MULTILINE)

    # Dynamic metadata extraction: Ưu tiên lấy từ bảng Revision History
    rev_pattern = r'##\s*(?:[0-9.]*\s*)?(?:Lịch sử sửa đổi|Revision History|LỊCH SỬ SỬA ĐỔI)[^\n]*\n([\s\S]*?)(?=\n##|\Z)'
    rev_match = re.search(rev_pattern, md_text, re.IGNORECASE)
    doc_version = None
    doc_date = None
    if rev_match:
        rev_lines = [line.strip() for line in rev_match.group(1).strip().split('\n') if line.strip().startswith('|')]
        for line in rev_lines:
            if re.match(r'\|\s*:?-+:?\s*\|', line):
                continue
            cols = [c.strip() for c in line.strip('|').split('|')]
            if len(cols) >= 4 and not any(k in cols[0].lower() for k in ['phiên bản', 'version']):
                doc_version = re.sub(r'[*_`]', '', cols[0]).strip()
                doc_date = cols[1].strip()
                break

    if not doc_version:
        ver_m = re.search(r'[*_]{1,2}(?:Phiên bản(?:\s+tài liệu)?|Version):[*_]{1,2}\s*([^\n\r*|_]+)', md_text, re.IGNORECASE)
        doc_version = ver_m.group(1).strip() if ver_m else "1.0.1"
    if not doc_date:
        date_m = re.search(r'[*_]{1,2}(?:Ngày(?:\s+cập nhật)?|Date):[*_]{1,2}\s*([^\n\r*|_]+)', md_text, re.IGNORECASE)
        doc_date = date_m.group(1).strip() if date_m else "2026-11-05"

    author_m = re.search(r'[*_]{1,2}(?:Tác giả|Author):[*_]{1,2}\s*([^\n\r*|_]+)', md_text, re.IGNORECASE)
    doc_author = author_m.group(1).strip() if author_m else "Phạm Tuấn Anh"

    # Convert markdown to html using markdown library
    md_converter = markdown.Markdown(extensions=[
        'extra',
        'fenced_code',
        'tables',
        'sane_lists',
        'nl2br'
    ])
    raw_html = md_converter.convert(md_text)

    # Parse with BeautifulSoup for clean DOM transformations
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Convert .md links to .html links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith('.md') or '.md#' in href or '.md?' in href:
            a_tag['href'] = re.sub(r'\.md(?=$|#|\?)', '.html', href)

    # Handle Mermaid blocks with card wrappers and zoom controls
    has_mermaid = False
    diagram_count = 0
    for code_tag in soup.find_all('code'):
        classes = code_tag.get('class', [])
        if 'language-mermaid' in classes or 'mermaid' in classes:
            has_mermaid = True
            pre_tag = code_tag.parent
            if pre_tag and pre_tag.name == 'pre':
                diagram_count += 1
                wrapper = soup.new_tag('div', attrs={'class': 'diagram-wrapper'})
                
                header = soup.new_tag('div', attrs={'class': 'diagram-header'})
                title_span = soup.new_tag('span', attrs={'class': 'diagram-title'})
                title_span.string = f"📊 Sơ Đồ Kiến Trúc / Luồng Operations #{diagram_count}"
                
                actions = soup.new_tag('div', attrs={'class': 'diagram-actions'})
                zoom_btn = soup.new_tag('button', attrs={
                    'class': 'btn-diagram-action btn-zoom',
                    'onclick': 'openDiagramModal(this)',
                    'title': 'Xem phóng to toàn màn hình'
                })
                zoom_btn.string = "🔍 Phóng To / Zoom"
                actions.append(zoom_btn)
                
                header.append(title_span)
                header.append(actions)
                
                body = soup.new_tag('div', attrs={'class': 'diagram-body', 'title': 'Click để xem phóng to'})
                mermaid_div = soup.new_tag('div', attrs={'class': 'mermaid'})
                mermaid_div.string = code_tag.get_text()
                body.append(mermaid_div)
                
                wrapper.append(header)
                wrapper.append(body)
                
                pre_tag.replace_with(wrapper)

    # Transform Blockquotes into Alerts
    for bq in soup.find_all('blockquote'):
        bq_text = bq.get_text()
        alert_class = "alert-info"
        if any(w in bq_text.upper() for w in ['WARNING', 'CẢNH BÁO', 'CHÚ Ý']):
            alert_class = "alert-warning"
        elif any(w in bq_text.upper() for w in ['DANGER', 'CAUTION', 'ERROR', 'NGUY HIỂM', 'LỖI', 'CẤM']):
            alert_class = "alert-danger"
        elif any(w in bq_text.upper() for w in ['SUCCESS', 'HOÀN THÀNH', 'THÀNH CÔNG', 'OK', 'TIP']):
            alert_class = "alert-success"
        
        div = soup.new_tag('div', attrs={'class': f'alert {alert_class}'})
        div.extend(bq.contents)
        bq.replace_with(div)

    # Format Revision History tables with high-contrast styling
    for h in soup.find_all(['h2', 'h3']):
        h_text = h.get_text().lower()
        if 'lịch sử sửa đổi' in h_text or 'revision history' in h_text:
            next_table = h.find_next_sibling('table')
            if next_table:
                next_table['class'] = next_table.get('class', []) + ['revision-table']
                for tr in next_table.find_all('tr'):
                    tds = tr.find_all('td')
                    if len(tds) >= 4:
                        # Version badge
                        ver_text = tds[0].get_text().strip()
                        tds[0].clear()
                        badge_span = soup.new_tag('span', attrs={'class': 'badge-version'})
                        badge_span.string = f"v{ver_text.lstrip('v')}"
                        tds[0].append(badge_span)
                        tds[0]['style'] = 'text-align: center;'

                        # QC / QA Note highlight
                        if len(tds) >= 5:
                            qa_text = tds[4].get_text().strip()
                            tds[4].clear()
                            div_qa = soup.new_tag('div', attrs={'class': 'qa-impact-cell'})
                            tag_span = soup.new_tag('span', attrs={'class': 'qa-tag-badge'})
                            tag_span.string = '🧪 QC/QA Note'
                            div_qa.append(tag_span)
                            div_qa.append(BeautifulSoup(qa_text, 'html.parser'))
                            tds[4].append(div_qa)

    # Bọc mỗi bảng trong khung cuộn ngang (trừ bảng Revision History đã có style riêng)
    for tbl in soup.find_all('table'):
        if 'revision-table' in (tbl.get('class') or []):
            continue
        wrapper = soup.new_tag('div', attrs={'class': 'table-wrap'})
        tbl.wrap(wrapper)

    # Build TOC and add IDs / anchor links to Headings
    toc_items = []
    used_ids = set()

    for heading in soup.find_all(['h2', 'h3', 'h4']):
        text = heading.get_text().strip()
        slug = slugify(text)
        
        # Ensure unique ID
        unique_slug = slug
        count = 1
        while unique_slug in used_ids:
            unique_slug = f"{slug}-{count}"
            count += 1
        used_ids.add(unique_slug)
        
        heading['id'] = unique_slug
        
        # Wrap inner HTML in link
        inner_html = heading.decode_contents()
        heading.clear()
        a_tag = soup.new_tag('a', href=f"#{unique_slug}")
        a_tag.append(BeautifulSoup(inner_html, 'html.parser'))
        heading.append(a_tag)

        if heading.name in ['h2', 'h3']:
            toc_items.append({
                'level': heading.name,
                'id': unique_slug,
                'text': text
            })

    # Build TOC HTML
    toc_ol = soup.new_tag('ol')
    for item in toc_items:
        li = soup.new_tag('li')
        if item['level'] == 'h3':
            li['class'] = 'sub'
        a = soup.new_tag('a', href=f"#{item['id']}")
        a.string = item['text']
        li.append(a)
        toc_ol.append(li)

    # Add Master Document Return Link at top of Sidebar TOC
    sidebar_master_link = ""
    if not is_master:
        sidebar_master_link = """
        <div class="toc-master-box">
          <a href="{master_href}" class="toc-master-link">
            🏠 Về Tài liệu Master
          </a>
        </div>
        """

    toc_nav = f"""
      <nav class="toc" id="tocNav">
        {sidebar_master_link}
        <div class="toc-title">Mục lục</div>
        {toc_ol.decode_contents()}
      </nav>
    """

    # Top Master Nav Breadcrumb
    if not is_master:
        top_nav_bar = f"""
        <div class="master-nav-bar">
          <a href="{master_href}" class="btn-back-master">
            <span>🏠</span> Quay lại Tài liệu Master
          </a>
          <span class="nav-divider">/</span>
          <span class="nav-current-title">{html.escape(title)}</span>
        </div>
        """
        floating_master_button = """
        <a href="{master_href}" class="floating-master-btn" title="Quay lại Tài liệu Master">
          🏠 Master Doc
        </a>
        """
    else:
        top_nav_bar = """
        <div class="master-nav-bar">
          <span class="badge-master-doc">📚 EW-15S2 Master Architecture & Specification Document</span>
        </div>
        """
        floating_master_button = ""

    # Assemble full page HTML
    mermaid_head = ""
    if has_mermaid:
        mermaid_head = """
  <!-- Mermaid JS -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", () => {
      mermaid.initialize({
        startOnLoad: true,
        theme: 'base',
        flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
        sequence: { useMaxWidth: true, showSequenceNumbers: true, wrap: true, width: 200, actorMargin: 60, messageMargin: 40, boxMargin: 10, noteMargin: 10, messageAlign: 'center' },
        gantt: { useMaxWidth: true },
        state: { useMaxWidth: true },
        themeVariables: {
          fontSize: '15px',
          fontFamily: 'Inter, sans-serif',
          primaryColor: '#eff6ff',
          primaryTextColor: '#1e3a8a',
          primaryBorderColor: '#2563eb',
          lineColor: '#64748b',
          secondaryColor: '#f0fdf4',
          tertiaryColor: '#fff7ed',
          clusterBkg: '#f8fafc',
          clusterBorder: '#cbd5e1'
        }
      });
      // Sơ đồ hẹp giữ kích thước tự nhiên; sơ đồ rộng co vừa khung nhưng không nhỏ hơn 900px (card cuộn ngang)
      const fitWideDiagram = (svg) => {
        const vb = svg.viewBox && svg.viewBox.baseVal;
        if (vb && vb.width > 900) svg.style.minWidth = '900px';
      };
      new MutationObserver((records) => {
        records.forEach(r => r.addedNodes.forEach(n => {
          if (n.nodeName && n.nodeName.toLowerCase() === 'svg') fitWideDiagram(n);
        }));
      }).observe(document.body, { childList: true, subtree: true });
    });
  </script>
        """

    modal_html = """
  <!-- Modal Xem Phóng To Sơ Đồ -->
  <div class="diagram-modal" id="diagramModal">
    <div class="diagram-modal-header">
      <div class="diagram-modal-title">📊 Sơ Đồ Kiến Trúc Chi Tiết (Bản Phóng To High-Resolution)</div>
      <div class="diagram-modal-controls">
        <button class="diagram-modal-btn" onclick="zoomDiagram(0.2)" title="Phóng to">+</button>
        <button class="diagram-modal-btn" onclick="zoomDiagram(-0.2)" title="Thu nhỏ">-</button>
        <button class="diagram-modal-btn" onclick="resetDiagramZoom()" title="Về kích thước chuẩn">Reset</button>
        <button class="diagram-modal-btn close-btn" onclick="closeDiagramModal()">✕ Đóng</button>
      </div>
    </div>
    <div class="diagram-modal-content" id="diagramModalContainer"></div>
  </div>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} — EW-15S2 Đặc Tả Kỹ Thuật</title>

  <!-- Google Fonts: Inter + JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <!-- MathJax for formula rendering -->
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }}
    }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
{mermaid_head}
  <style>
{CSS_STYLES}
  </style>
</head>
<body>

  <!-- Thanh tiến trình đọc -->
  <div class="progress-bar" id="progressBar"></div>

  <!-- Nút mở TOC trên Mobile -->
  <button class="toc-toggle" id="tocToggle" aria-label="Mục lục">☰</button>
  <div class="toc-overlay" id="tocOverlay"></div>

  <!-- HEADER toàn chiều rộng -->
  <div style="padding:1.5rem 1.5rem 0">
    {top_nav_bar}
    <div class="header">
      <h1>{html.escape(title)}</h1>
      <div class="meta">
        <strong>Sản phẩm:</strong> WM03A-Water Data Logger &nbsp;|&nbsp; <strong>Phiên bản:</strong> v{html.escape(doc_version)}<br>
        <strong>Tác giả:</strong> {html.escape(doc_author)} &nbsp;|&nbsp; <strong>Cập nhật:</strong> {html.escape(doc_date)}
      </div>
    </div>
  </div>

  <!-- LAYOUT: Sidebar + Main -->
  <div class="layout">
    <div class="sidebar" id="sidebar">
      {toc_nav}
    </div>

    <div class="main">
      {str(soup)}
    </div>
  </div>

  {modal_html if has_mermaid else ""}

  {floating_master_button}

  <!-- Nút Back-to-top -->
  <button class="back-top" id="backTop" aria-label="Về đầu trang">↑</button>

  <!-- JavaScript tương tác -->
  <script>
{JS_SCRIPT}
  </script>
</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"Successfully converted: {filename} -> {os.path.basename(html_path)}")

EXCLUDE_MD_FILES = {"nb_iot_design.md"}

def main():
    # Remove deprecated nb_iot_design.html if exists
    for old_file in ["nb_iot_design.html"]:
        old_path = os.path.join(HTML_DIR, old_file)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
                print(f"Removed deprecated HTML file: {old_file}")
            except Exception as e:
                print(f"Warning: Could not remove {old_file}: {e}")

    md_files = [p for p in glob.glob(os.path.join(MD_DIR, "**", "*.md"), recursive=True) if os.path.basename(p) not in EXCLUDE_MD_FILES]
    print(f"Found {len(md_files)} markdown files to convert (excluding deprecated: {', '.join(EXCLUDE_MD_FILES)}).")
    for md_path in md_files:
        convert_md_file(md_path)
    print("All markdown files converted successfully!")

    # Auto build standalone single-file bundle
    try:
        from build_standalone_master import main as build_bundle_main
        print("\n--- Building Standalone Single-File Master HTML Bundle ---")
        build_bundle_main()
    except Exception as e:
        print(f"Warning: Could not build standalone bundle: {e}")

if __name__ == "__main__":
    main()
