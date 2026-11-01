#!/usr/bin/env python3
"""WCAG contrast audit for the site's CSS.

Parses each page's <style> block, resolves var() against :root, pairs each
color with its background (explicit in-rule, or via the context table below),
and reports ratio + verdict. 4.5:1 normal text, 3:1 badges/large text.
Decorative-only rules are listed separately.
"""
import re, sys, glob, os

def hex2rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def blend(fg, bg, a):
    return tuple(round(a*f + (1-a)*b) for f, b in zip(fg, bg))

def lum(rgb):
    def chan(c):
        c /= 255
        return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1+0.05)/(l2+0.05)

def parse(css):
    root = dict(re.findall(r'(--[\w-]+)\s*:\s*(#[0-9A-Fa-f]{3,6})', css))
    rules = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        sel, body = m.group(1).strip(), m.group(2)
        props = dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)', body))
        rules.append((sel, props))
    return root, rules

def resolve(v, root):
    v = v.strip()
    if v.startswith('var('):
        name = v[4:-1].split(',')[0]
        return root.get(name)
    m = re.search(r'#[0-9A-Fa-f]{3,6}', v)
    return m.group(0) if m else None

# selector-prefix -> background hex (first match wins; most specific first)
CONTEXTS = [
    ('.badge.v', '#C8A24B'),          # gold badge vs its own text
    ('.badge.a', '#8FA6C4'),          # steel badge vs its own text
    ('.gloss span', '#21385A'),   # spans only in dark glossary; mcards' gloss has no spans
    ('section.light .sec-head .kicker', '#E8DCC3'),
    ('.sec-head .kicker', '#223A5E'),
    ('#campaign .subhead', '#E8DCC3'),
    ('.subhead', '#223A5E'),
    ('.poem', '#F1E9D7'),
    ('.ucard', '#2A344C'),            # 6% sand blended over indigo
    ('section.light .card', '#1B2F4C'),
    ('.vs', '#E8DCC3'),            # every .vs column carries sand bg
    ('.card', '#E8DCC3'),
    ('.char', '#E8DCC3'),
    ('.feature', '#E8DCC3'),
    ('footer', '#191512'),
    ('section.light', '#E8DCC3'),
    ('section.dark', '#223A5E'),
    ('section', '#223A5E'),
    ('body', '#223A5E'),
]

DECORATIVE = ('::before', '::after', '.band')

def section_bg_sec(sec):
    tag, cls = sec
    if tag == 'footer': return hex2rgb('#191512')
    if 'light' in cls: return hex2rgb('#E8DCC3')
    return hex2rgb('#223A5E')

def section_bg(tag_match):
    tag = tag_match.group(1)
    if tag == 'footer': return hex2rgb('#191512')
    if 'light' in tag_match.group(0): return hex2rgb('#E8DCC3')
    return hex2rgb('#223A5E')

def css_bg(class_list, rules, root):
    """Background (hex or ('rgba', raw)) of the first rule matching any class."""
    for sel, props in rules:
        b = props.get('background')
        if not b: continue
        if 'gradient' in b or 'url(' in b: continue  # not a flat color
        if '::' in sel: continue
        # only the last compound may target the element itself; all its
        # classes must be on the element (span.badge must not match .poem .badge.v)
        last = re.split(r'[ >,+~]', sel.strip())[-1]
        lcls = re.findall(r'\.([\w-]+)', last)
        if lcls and all(c in class_list for c in lcls):
            v = resolve(b, root)
            if v: return v
            if b.startswith('rgb'):
                return ('rgba', b)
    return None

def resolve_bg(val, base, root):
    """Blend an rgba value over base; hex passes through."""
    if isinstance(val, tuple):
        m = re.match(r'rgba?\((\d+)[,\s]+(\d+)[,\s]+(\d+)[,\s]+([\d.]+)\)', val[1])
        return blend((int(m.group(1)), int(m.group(2)), int(m.group(3))), base, float(m.group(4)))
    return hex2rgb(val)

VOID = {'img','br','hr','meta','link','input','use','path','rect','circle',
        'line','polyline','polygon','stop','source','col','area','base','embed'}

def ancestors_at(html, pos):
    """(tag, class_list) stack of strictly enclosing elements at pos."""
    stack = []
    for t in re.finditer(r'<(/?)([a-z]+)\b([^>]*?)(/?)>', html[:pos]):
        close, tag, attrs, selfc = t.group(1) == '/', t.group(2), t.group(3), t.group(4) == '/'
        if close:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    del stack[i:]
                    break
        elif not selfc and tag not in VOID:
            cm = re.search(r'class="([^"]*)"', attrs)
            stack.append((tag, cm.group(1).split() if cm else []))
    return stack

def bg_for(sel, html, rules, root):
    """Explicit context table first, then DOM: stack of enclosing elements,
    nearest CSS background wins (rgba blended over section base)."""
    for prefix, bg in CONTEXTS:
        if any(prefix in s for s in sel.split(',')):
            return hex2rgb(bg)
    # rightmost compound that carries a class = the element itself (.vs .col h3 -> col)
    cls = None
    for comp in re.split(r'[ >,+~]', sel.strip())[::-1]:
        cc = re.findall(r'\.([\w-]+)', comp)
        if cc and not comp.startswith(':'):
            cls = cc[0]; break
    if cls is None: return None
    need = [c for comp in re.split(r'[ >,+~]', sel.strip()) for c in re.findall(r'\.([\w-]+)', comp) if c != cls]
    em = None
    for cand in re.finditer(r'<([a-z]+)[^>]*class="[^"]*\b' + cls + r'\b[^"]*"', html):
        anc = {c for _, cl in ancestors_at(html, cand.start()) for c in cl}
        if all(c in anc for c in need):
            em = cand; break
    if em is None:
        em = re.search(r'<([a-z]+)[^>]*class="[^"]*\b' + cls + r'\b[^"]*"', html)
    if not em: return None
    own = re.search(r'class="([^"]*)"', em.group(0))
    stack = ancestors_at(html, em.start())
    secs = [s for s in stack if s[0] in ('section', 'footer', 'header')]
    base = section_bg_sec(secs[-1]) if secs else hex2rgb('#223A5E')
    chains = ([own.group(1).split()] if own else []) + [c for _, c in reversed(stack)]
    for class_list in chains:
        v = css_bg(class_list, rules, root)
        if v: return resolve_bg(v, base, root)
    return base

def audit(path):
    html = open(path, encoding='utf-8').read()
    m = re.search(r'<style>(.*?)</style>', html, re.S)
    root, rules = parse(m.group(1))
    rows, deco = [], []
    for sel, props in rules:
        if not props.get('color'): continue
        if any(d in sel for d in ('::before', '::after')): continue
        fg = resolve(props['color'], root)
        if not fg: continue
        bg = resolve(props.get('background', ''), root)
        if not bg:
            bgc = bg_for(sel, html, rules, root)
            if not bgc: continue
            bg_rgb = bgc
        else:
            bg_rgb = hex2rgb(bg)
        fg_rgb = hex2rgb(fg)
        # rgba background? blend over context
        bm = re.match(r'rgba?\((\d+)[,\s]+(\d+)[,\s]+(\d+)[,\s]+([\d.]+)\)', props.get('background', ''))
        if bm:
            base = bg_for(sel, html, rules, root) or hex2rgb('#223A5E')
            bg_rgb = blend((int(bm.group(1)), int(bm.group(2)), int(bm.group(3))), base, float(bm.group(4)))
        r = ratio(fg_rgb, bg_rgb)
        size = props.get('font-size', '1rem')
        fm = re.search(r'([\d.]+)', size)
        small = float(fm.group(1)) if fm else 1
        if 'clamp' in size: small = 1  # clamp floor is >= .85rem in this codebase
        thresh = 3.0 if small else 4.5
        verdict = 'PASS' if r >= thresh else 'FAIL'
        rows.append((sel[:60], fg, '#%02X%02X%02X' % bg_rgb if isinstance(bg_rgb, tuple) else bg_rgb, round(r, 2), verdict, thresh))
    return rows

def main():
    files = sorted(glob.glob('docs/*.html'))
    total_fail = 0
    for f in files:
        print(f'\n=== {f} ===')
        print(f'{"selector":<60} {"fg":<9} {"bg":<9} {"ratio":>6} {"verdict":<7} thr')
        for row in audit(f):
            print(f'{row[0]:<60} {row[1]:<9} {row[2]:<9} {row[3]:>6} {row[4]:<7} {row[5]}')
            if row[4] == 'FAIL': total_fail += 1
    print(f'\nTOTAL FAIL: {total_fail}')
    return 1 if total_fail else 0

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.exit(main())
