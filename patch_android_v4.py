#!/usr/bin/env python3
"""V4: make Android home native-first and remove duplicated feed details."""
from pathlib import Path
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

def read(name):
    p = root / name
    if not p.exists():
        raise SystemExit(f"Missing source file: {p}")
    return p, p.read_text(encoding="utf-8")

def write(p, s):
    p.write_text(s, encoding="utf-8")

def remove_between(src, start, end):
    a = src.find(start)
    if a < 0:
        return src
    b = src.find(end, a + len(start))
    if b < 0:
        raise SystemExit(f"Could not locate end marker after {start}")
    return src[:a] + src[b:]

# Feed previews show city/date, not a low-value view count.
p, s = read("widgets.dart")
if "DELO_CLEAN_UNIFIED_V4" not in s:
    old = """child: Tap(
        onTap: onTap,
        scale: .99,
        child: Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(12),
          decoration: cardDeco(p, r: 20),"""
    new = """child: Tap(
        onTap: onTap,
        scale: .99,
        child: Container(
          // DELO_CLEAN_UNIFIED_V4: compact, consistent marketplace preview.
          margin: const EdgeInsets.only(bottom: 10),
          padding: const EdgeInsets.all(12),
          decoration: cardDeco(p, r: 18),"""
    if old not in s:
        raise SystemExit("Couldn't locate shared AdCard container")
    s = s.replace(old, new, 1)
    s = s.replace("final thumb = width >= 600 ? 112.0 : 92.0;", "final thumb = width >= 640 ? 104.0 : 80.0;", 1)
    d = chr(36)
    s = s.replace("                      Icon(Icons.visibility_outlined, size: 13, color: p.mu),\n                      Text('" + d + "{ad.opens}', style: TextStyle(fontSize: 12, color: p.mu)),\n", "", 1)
    s = s.replace("""                    Text(ad.desc.trim(), maxLines: 2, overflow: TextOverflow.ellipsis,
                        style: TextStyle(fontSize: 12.5, height: 1.25, color: p.mu)),""",
        """                    Text(ad.desc.trim(), maxLines: width < 480 ? 1 : 2, overflow: TextOverflow.ellipsis,
                        style: TextStyle(fontSize: 12.5, height: 1.3, color: p.mu)),""", 1)
    write(p, s)

# The main tab of a native app should prioritize tasks, not mirror the website's entire long landing page.
p, s = read("landing.dart")
if "DELO_CLEAN_UNIFIED_V4_HOME" not in s:
    s = s.replace("        final reviews = siteLines(_site['reviews']);\n        final faq = siteLines(_site['faq']);\n", "", 1)
    pattern = re.compile(r"                  _topBar\(p\),\s*_hero\(p\),.*?                  _footer\(p\),", re.S)
    replacement = """                  // DELO_CLEAN_UNIFIED_V4_HOME: native marketplace, not a long website-style landing page.
                  _topBar(p),
                  _hero(p),
                  _sectionTitle(p, 'Категории', 'Быстрый переход к подходящим заданиям.'),
                  _categories(p),
                  _sectionTitle(p, 'Свежие объявления', 'Новые предложения рядом с вами.', action: 'Все', onAction: () => S.i.goTab(1)),
                  if (S.i.loading && recent.isEmpty)
                    Padding(padding: const EdgeInsets.all(30), child: Center(child: CircularProgressIndicator(color: p.ac)))
                  else if (recent.isEmpty)
                    _emptyAds(p)
                  else
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Column(children: [
                        for (final ad in recent.take(S.i.logged ? 6 : 4))
                          AdCard(ad: ad, onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => AdPage(ad: ad)))),
                      ]),
                    ),
                  const SizedBox(height: 12),"""
    s, count = pattern.subn(replacement, s, count=1)
    if count != 1:
        raise SystemExit("Couldn't locate LandingPage home content")
    # Category choices already have their own section directly beneath the hero.
    s, count = re.subn(
        r"        const SizedBox\(height: 13\),\n        SingleChildScrollView\(\n          scrollDirection: Axis\.horizontal,.*?\n        \),\n      \]\),\n    \);",
        "        // Category selection appears once, in the dedicated section below.\n      ]),\n    );",
        s, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("Couldn't locate duplicated category shortcuts in native hero")
    s = s.replace("""          const SizedBox(height: 8),
          Text('Продолжайте находить заказы и исполнителей рядом.', textAlign: TextAlign.center,
              style: TextStyle(color: p.mu, fontSize: 14, height: 1.4)),
""", "", 1)
    # Website-specific marketing sections are not shown in the native app home.
    s = remove_between(s, "  void _openInfo({required int section, required String title}) {", "  @override\n  Widget build(BuildContext context) {")
    s = remove_between(s, "  Widget _stats(Pal p, List<List<String>> stats) {", "  Widget _sectionTitle(Pal p, String title, String sub, {String? action, VoidCallback? onAction}) =>")
    s = remove_between(s, "  Widget _how(Pal p) {", "  Widget _reviews(Pal p, List<List<String>> reviews) {")
    s = remove_between(s, "  Widget _reviews(Pal p, List<List<String>> reviews) {", "  Widget _faq(Pal p, List<List<String>> faq) {")
    s = remove_between(s, "  Widget _faq(Pal p, List<List<String>> faq) {", "  Widget _business(Pal p) =>")
    s = remove_between(s, "  Widget _business(Pal p) =>", "  Widget _footer(Pal p) =>")
    idx = s.find("  Widget _footer(Pal p) =>")
    if idx >= 0:
        tail = s.rfind("\n}")
        if tail < idx:
            raise SystemExit("Couldn't locate end of LandingPage class")
        s = s[:idx] + s[tail:]
    s = s.replace("import 'info.dart';\n", "", 1)
    write(p, s)

print(f"Applied V4 Android cleanup under {root}")
