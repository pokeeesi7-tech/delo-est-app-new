#!/usr/bin/env python3
"""Apply shared UI cleanup and cross-screen visual-system refinements to Flutter source."""
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

# A coherent component theme: cards, menus, buttons, chips, switches, dialogs and navigation now share tokens.
p, s = read("theme.dart")
if "// DELO_CLEAN_UNIFIED_V3" not in s:
    s = s.replace(
        "    visualDensity: VisualDensity.standard,\n",
        """    visualDensity: VisualDensity.standard,
    // DELO_CLEAN_UNIFIED_V3: common component language used on every screen.
    textTheme: TextTheme(
      displayLarge: TextStyle(color: p.tx, fontWeight: FontWeight.w800, letterSpacing: -1.4, height: 1.05),
      displayMedium: TextStyle(color: p.tx, fontWeight: FontWeight.w800, letterSpacing: -1.0, height: 1.08),
      headlineLarge: TextStyle(color: p.tx, fontWeight: FontWeight.w800, letterSpacing: -.7, height: 1.12),
      headlineMedium: TextStyle(color: p.tx, fontWeight: FontWeight.w800, letterSpacing: -.45, height: 1.15),
      titleLarge: TextStyle(color: p.tx, fontSize: 20, fontWeight: FontWeight.w800, letterSpacing: -.4, height: 1.2),
      titleMedium: TextStyle(color: p.tx, fontSize: 16, fontWeight: FontWeight.w700, height: 1.25),
      bodyLarge: TextStyle(color: p.tx, fontSize: 16, height: 1.4),
      bodyMedium: TextStyle(color: p.tx, fontSize: 14, height: 1.4),
      bodySmall: TextStyle(color: p.mu, fontSize: 12.5, height: 1.35),
      labelLarge: TextStyle(color: p.tx, fontSize: 14, fontWeight: FontWeight.w800),
    ),
""", 1)
    s = s.replace(
        "    dividerColor: p.bd,\n",
        """    dividerColor: p.bd,
    cardTheme: CardTheme(
      color: p.card,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20), side: BorderSide(color: p.bd)),
    ),
    listTileTheme: ListTileThemeData(
      iconColor: p.mu,
      textColor: p.tx,
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: p.bg2,
      selectedColor: p.ac.withOpacity(.13),
      disabledColor: p.bg2,
      side: BorderSide(color: p.bd),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(99)),
      labelStyle: TextStyle(color: p.tx, fontSize: 12, fontWeight: FontWeight.w700),
      secondaryLabelStyle: TextStyle(color: p.ac, fontSize: 12, fontWeight: FontWeight.w800),
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
    ),
    iconButtonTheme: IconButtonThemeData(
      style: IconButton.styleFrom(
        foregroundColor: p.tx,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    dividerTheme: DividerThemeData(color: p.bd, thickness: 1, space: 1),
""", 1)
    # Ensure built-in controls follow the same rounded, low-noise style.
    s = s.replace(
        "    outlinedButtonTheme: OutlinedButtonThemeData(\n",
        """    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        foregroundColor: Colors.white,
        backgroundColor: p.ac,
        elevation: 0,
        minimumSize: const Size(0, 46),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        textStyle: const TextStyle(fontWeight: FontWeight.w800, fontSize: 15),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
""", 1)
    s = s.replace(
        "    progressIndicatorTheme: ProgressIndicatorThemeData(color: p.ac),\n",
        """    progressIndicatorTheme: ProgressIndicatorThemeData(color: p.ac, linearTrackColor: p.bg2),
    floatingActionButtonTheme: FloatingActionButtonThemeData(
      backgroundColor: p.ac, foregroundColor: Colors.white, elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(17)),
    ),
""", 1)
    write(p, s)

# Shared cards and inputs: slightly less bulky, more consistent across all views.
p, s = read("theme.dart")
s = s.replace(
    "boxShadow: [BoxShadow(color: p.ac.withOpacity(.035), blurRadius: 14, offset: const Offset(0, 4))],",
    "boxShadow: [BoxShadow(color: p.tx.withOpacity(.025), blurRadius: 16, offset: const Offset(0, 4))],"
)
write(p, s)

# Cabinet: remove duplicate affordances, duplicated notification banners and contact clutter.
p, s = read("cabinet.dart")
if "DELO_CLEAN_UNIFIED_V3_CONTACTS" not in s:
    contact_block = """            const SizedBox(height: 8),
            Wrap(spacing: 6, runSpacing: 6, children: [
              contact(S.i.login.contains('@') ? Icons.mail_outline : Icons.person_outline, mail),
              if (S.i.phone.isNotEmpty) contact(Icons.call_outlined, fmtPhone(S.i.phone)),
            ]),
"""
    s = s.replace(contact_block, "            // DELO_CLEAN_UNIFIED_V3_CONTACTS: contact data is available in profile editing.\n", 1)
    s = re.sub(r"    final mail = .*?;\n", "", s, count=1)
    # Remove the now-unused local chip builder, keeping the rest of the header logic intact.
    s = re.sub(r"    Widget contact\(IconData icon, String label\) => Container\(.*?\n        \);\n\n    return Container\(", "    return Container(", s, count=1, flags=re.S)
# Continue patching the same cabinet source after removing its redundant contact chips.
s = s.replace("                      ..._alerts(p),\n", "                      // Notification counts live on their destination tabs; no duplicate banner cards here.\n")
old_avatar = """          GestureDetector(
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ProfileEditPage())),
            child: Avatar(S.i.name, data: av, size: 64),
          ),"""
new_avatar = """          // Keep one clear edit action (the pencil button); the avatar is display-only.
          Avatar(S.i.name, data: av, size: 64),"""
s = s.replace(old_avatar, new_avatar)
write(p, s)

# Bottom navigation: selected item gets a quiet tinted surface like the site's tab controls.
p, s = read("home.dart")
if "DELO_CLEAN_UNIFIED_V3" not in s:
    old_nav = """                  child: InkWell(
                    onTap: () => S.i.goTab((it[0] as int) == 2 && !S.i.logged ? 3 : (it[0] as int)),
                    child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
"""
    new_nav = """                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: () => S.i.goTab((it[0] as int) == 2 && !S.i.logged ? 3 : (it[0] as int)),
                    child: AnimatedContainer(
                      // DELO_CLEAN_UNIFIED_V3
                      duration: const Duration(milliseconds: 160),
                      margin: const EdgeInsets.symmetric(horizontal: 3, vertical: 4),
                      decoration: BoxDecoration(
                        color: S.i.tab == (it[0] as int) ? p.ac.withOpacity(.10) : Colors.transparent,
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
"""
    if old_nav not in s:
        raise SystemExit("Couldn't locate bottom navigation block in home.dart")
    s = s.replace(old_nav, new_nav, 1)
    old_end = """                    ]),
                  ),
                ),
"""
    new_end = """                    ]),
                    ),
                  ),
                ),
"""
    if old_end not in s:
        raise SystemExit("Couldn't locate bottom navigation closing block in home.dart")
    s = s.replace(old_end, new_end, 1)
    s = s.replace("""          height: 60,
          child: Row(children: [""", """          height: 64,
          child: Row(children: [""", 1)
    write(p, s)

print(f"Patched Flutter UI source under {root}")
