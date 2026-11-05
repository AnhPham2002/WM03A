import glob
import html as htmllib
import os
import re
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, "html")
MASTER_FILE = "README.html"
OUT_FILE = "WM03A.html"
PAGE_TITLE = "Tài liệu WM03A"
OTHER_TITLE = "Khác"

# Nhóm tài liệu hiển thị trên sidebar. Đường dẫn tương đối trong html/, dùng dấu "/".
# File không có trong nhóm nào sẽ được gom vào nhóm "Khác" ở cuối.
GROUPS = [
    ("Kiến trúc & đặc tả", [
        "architecture/architecture.html",
    ]),
    ("Phần cứng", [
        "hardware/hardware.html",
    ]),
    ("Firmware", [
        "firmware/firmware_architecture.html",
        "firmware/flash.html",
        "firmware/bootloader.html",
        "firmware/application.html",
        "firmware/sram.html",
        "firmware/eeprom.html",
    ]),
    ("Đo lường & cảm biến", [
        "measurement/pulse_meter.html",
        "measurement/modbus_meter.html",
        "measurement/pressure_sensor.html",
    ]),
    ("Bảo mật", [
        "security/security.html",
    ]),
    ("Giao tiếp & truyền thông", [
        "communication/protocol.html",
        "communication/rs485.html",
        "communication/cellular.html",
        "communication/server.html",
        "communication/ota.html",
    ]),
    ("Biên dịch & nạp", [
        "compilation/firmware_image_packing.html",
        "compilation/build_and_flash.html",
    ]),
]

EXTRA_CSS = """
.toc { padding: 0.9rem; }
.sb-search input {
  width: 100%; padding: 0.5rem 0.7rem; margin-bottom: 0.8rem;
  border: 1px solid var(--border); border-radius: 6px; font-size: 0.85rem;
  font-family: inherit; outline: none;
}
.sb-search input:focus { border-color: var(--accent); }
.sb-master {
  display: block; padding: 0.5rem 0.7rem; margin-bottom: 0.8rem;
  background: #eff6ff; color: #1d4ed8 !important; font-weight: 600;
  border-radius: 6px; border-left: 3px solid #2563eb; font-size: 0.86rem;
}
.sb-group { margin-bottom: 0.5rem; }
.sb-group-title {
  display: flex; justify-content: space-between; align-items: center;
  cursor: pointer; user-select: none; padding: 0.45rem 0.2rem;
  font-size: 0.78rem; font-weight: 700; color: #475569;
  text-transform: uppercase; letter-spacing: 0.03em;
}
.sb-group-title > span:first-child {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sb-group-title > span:last-child {
  flex-shrink: 0;
  margin-left: 0.5rem;
  transition: transform 0.2s;
  display: inline-block;
}
.sb-group.collapsed .sb-group-title > span:last-child {
  transform: rotate(-90deg);
}
.sb-group.collapsed .sb-list { display: none; }
.sb-list { list-style: none; padding: 0; margin: 0; }
.sb-list li { margin-bottom: 0.1rem; }
.sb-list a {
  display: block; padding: 0.35rem 0.5rem; font-size: 0.84rem;
  color: var(--fg-muted); border-radius: 4px; border-left: 2px solid transparent;
}
.sb-list a:hover { background: var(--accent-light); color: var(--accent); }
.sb-list a.active {
  background: var(--accent-light); color: var(--accent-dark);
  font-weight: 600; border-left-color: var(--accent);
}
.doc-section { display: none; }
.doc-section.active { display: block; }
.doc-title {
  font-size: 1.6rem; font-weight: 700; margin: 0 0 1.25rem;
  padding-bottom: 0.6rem; border-bottom: 2px solid var(--accent);
  color: var(--fg);
}
.main > hr { border: none; border-top: 3px dashed var(--border); margin: 3rem 0; }
"""

SIDEBAR_JS = """
(() => {
  const docSections = document.querySelectorAll('.doc-section');
  const sbLinks = document.querySelectorAll('.sb-list a, .sb-master');

  function renderMermaid(sid) {
    if (!window.mermaid) return;
    const sec = document.getElementById(sid);
    if (!sec) return;
    const nodes = sec.querySelectorAll('.mermaid');
    if (nodes.length) mermaid.run({ nodes: Array.from(nodes) });
  }

  // Hiện section chứa tài liệu sid, rồi cuộn tới target (nếu có)
  function showSection(sid, target) {
    if (!document.getElementById(sid)) sid = 'master';
    docSections.forEach(sec => sec.classList.toggle('active', sec.id === sid));
    sbLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + sid));
    renderMermaid(sid);
    if (target && target.id !== sid) {
      target.scrollIntoView({ block: 'start' });
    } else {
      window.scrollTo({ top: 0 });
    }
  }

  // Xử lý hash: có thể là tài liệu (#doc-...) hoặc một mục bên trong (#doc-...--bang-1)
  function navigateTo(hash, fallbackToMaster = false) {
    const id = (hash || '').replace('#', '');
    if (!id) return showSection('master');
    const el = document.getElementById(id);
    if (!el) {
      console.warn('Không tìm thấy mục tiêu:', id);
      if (fallbackToMaster) showSection('master');
      return;
    }
    const sec = el.closest('.doc-section');
    if (sec) showSection(sec.id, el);
  }

  sbLinks.forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const sid = a.getAttribute('href').replace('#', '');
      history.replaceState(null, '', '#' + sid);
      showSection(sid);
    });
  });

  window.addEventListener('hashchange', () => navigateTo(location.hash));

  const sbSearch = document.getElementById('sbSearch');
  if (sbSearch) {
    sbSearch.addEventListener('input', () => {
      const q = sbSearch.value.trim().toLowerCase();
      document.querySelectorAll('.sb-group').forEach(group => {
        let anyVisible = false;
        group.querySelectorAll('li').forEach(li => {
          const show = !q || li.textContent.toLowerCase().includes(q);
          li.style.display = show ? '' : 'none';
          if (show) anyVisible = true;
        });
        group.style.display = anyVisible ? '' : 'none';
        if (q && anyVisible) group.classList.remove('collapsed');
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => navigateTo(location.hash));
})();
"""


def load(rel):
    with open(os.path.join(HTML_DIR, rel), encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def section_id(rel):
    if rel == MASTER_FILE:
        return "master"
    slug = re.sub(r"[^\w]+", "-", os.path.splitext(rel)[0]).strip("-").lower()
    return f"doc-{slug}"


def build_section(rel, soup, sid, sid_map):
    main = soup.select_one(".main")
    h1 = soup.select_one(".header h1")
    title = h1.get_text(strip=True) if h1 else os.path.splitext(os.path.basename(rel))[0]

    # Tiền tố id và anchor nội bộ để tránh trùng giữa các file
    for el in main.find_all(id=True):
        el["id"] = f"{sid}--{el['id']}"
    for a in main.find_all("a", href=True):
        if a["href"].startswith("#"):
            a["href"] = f"#{sid}--{a['href'][1:]}"

    # Link sang trang HTML khác thành link nhảy trong bản gộp
    base = os.path.dirname(rel)
    for a in main.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("#", "http://", "https://", "mailto:")) or ".html" not in href:
            continue
        path, _, frag = href.partition("#")
        target = os.path.normpath(os.path.join(base, path)).replace(os.sep, "/")
        if target in sid_map:
            a["href"] = f"#{sid_map[target]}--{frag}" if frag else f"#{sid_map[target]}"

    return {"rel": rel, "sid": sid, "title": title, "inner": main.decode_contents()}


def main():
    if not os.path.exists(os.path.join(HTML_DIR, MASTER_FILE)):
        print(f"Không tìm thấy {MASTER_FILE}, bỏ qua bước gộp.")
        return

    all_rels = []
    for p in glob.glob(os.path.join(HTML_DIR, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, HTML_DIR).replace(os.sep, "/")
        if rel not in (MASTER_FILE, OUT_FILE):
            all_rels.append(rel)

    sid_map = {rel: section_id(rel) for rel in all_rels + [MASTER_FILE]}

    master_soup = load(MASTER_FILE)
    master_header = str(master_soup.select_one(".header") or "")
    master_body_scripts = []
    if master_soup.body:
        for s in master_soup.body.find_all("script"):
            js = s.string or ""
            start = js.find("// ── TOC active highlight")
            end = js.find("// ── Diagram Modal")
            if start != -1 and end != -1:
                js = js[:start] + js[end:]
            master_body_scripts.append(f"<script>{js}</script>")

    seen = {str(s) for s in master_soup.head.find_all("script")} if master_soup.head else set()
    extra_head_scripts = []
    modal = ""
    sections = {}

    for rel in sorted(all_rels):
        soup = load(rel)
        if not modal and soup.select_one(".diagram-modal"):
            modal = str(soup.select_one(".diagram-modal"))
        if soup.head:
            for s in soup.head.find_all("script"):
                key = str(s)
                if key not in seen:
                    seen.add(key)
                    extra_head_scripts.append(key)
        if soup.select_one(".main") is None:
            print(f"Bỏ qua {rel}: không có nội dung .main")
            continue
        sections[rel] = build_section(rel, soup, sid_map[rel], sid_map)

    # Gom file theo nhóm, theo đúng thứ tự khai báo trong GROUPS
    groups = []
    used = set()
    for title, rels in GROUPS:
        items = []
        for r in rels:
            if r in sections:
                items.append(sections[r])
                used.add(r)
            else:
                print(f"Cảnh báo: '{r}' trong GROUPS không tồn tại trong html/")
        if items:
            groups.append((title, items))

    rest = [sections[r] for r in sorted(sections) if r not in used]
    if rest:
        groups.append((OTHER_TITLE, rest))
        print("Các file không có trong GROUPS (xếp vào 'Khác'):", *[s["rel"] for s in rest], sep="\n  ")

    ordered = [s for _, items in groups for s in items]

    # Sidebar
    group_html = []
    for title, items in groups:
        lis = "".join(
            f'<li><a href="#{s["sid"]}" title="{htmllib.escape(s["rel"])}">'
            f'{htmllib.escape(s["title"])}</a></li>'
            for s in items
        )
        group_html.append(
            f'<div class="sb-group">'
            f'<div class="sb-group-title" onclick="this.parentElement.classList.toggle(\'collapsed\')">'
            f'<span>{htmllib.escape(title)}</span><span>▼</span></div>'
            f'<ul class="sb-list">{lis}</ul></div>'
        )

    sidebar_html = f"""
      <nav class="toc" id="tocNav">
        <div class="sb-search"><input id="sbSearch" type="search" placeholder="Tìm kiếm tài liệu..."></div>
        <a class="sb-master" href="#master">📌 Master Document</a>
        {''.join(group_html)}
      </nav>
    """

    # Nội dung
    parts = []
    for s in ordered:
        parts.append(
            f'<section class="doc-section" id="{s["sid"]}">'
            f'<h1 class="doc-title">{htmllib.escape(s["title"])}</h1>{s["inner"]}</section>'
        )
    body_sections = (
        f'<section class="doc-section" id="master">{"" }</section>'
        if False else ""
    )
    master_info = build_section(MASTER_FILE, master_soup, "master", sid_map)
    master_block = f'<section class="doc-section" id="master">{master_info["inner"]}</section>'
    body_sections = master_block + "".join(parts)

    if master_soup.title:
        master_soup.title.string = PAGE_TITLE
    head_html = str(master_soup.head).replace(
        "</head>",
        "\n".join(extra_head_scripts) + f"\n<style>{EXTRA_CSS}</style>\n</head>",
    )
    head_html = head_html.replace("startOnLoad: true", "startOnLoad: false")

    page = f"""<!DOCTYPE html>
<html lang="vi">
{head_html}
<body>
  <div class="progress-bar" id="progressBar"></div>
  <button class="toc-toggle" id="tocToggle" aria-label="Mục lục">☰</button>
  <div class="toc-overlay" id="tocOverlay"></div>
  <div style="padding:1.5rem 1.5rem 0">{master_header}</div>
  <div class="layout">
    <div class="sidebar" id="sidebar">{sidebar_html}</div>
    <div class="main">{body_sections}</div>
  </div>
  {modal}
  <button class="back-top" id="backTop" aria-label="Về đầu trang">↑</button>
  {"".join(master_body_scripts)}
  <script>{SIDEBAR_JS}</script>
</body>
</html>
"""

    out_path = os.path.join(HTML_DIR, OUT_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Đã tạo bản gộp: {out_path} ({len(ordered)} tài liệu)")


if __name__ == "__main__":
    main()