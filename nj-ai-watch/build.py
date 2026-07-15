#!/usr/bin/env python3
"""Build NJ AI Watch: renders data/entries.json into index.html.

Usage:  python3 build.py
Output: nj-ai-watch/index.html (fully static, committed like any other asset)

Note: the spec suggested Jinja2, but this machine's stock Python has no
third party packages and the page is one template, so this uses only the
standard library. No pip, no venv, nothing to break.

To add or edit entries: edit data/entries.json, run this script, deploy.
"""
import html
import json
import pathlib
from datetime import date

ROOT = pathlib.Path(__file__).parent
ENTRIES = json.loads((ROOT / "data" / "entries.json").read_text())

# TODO(Pete): replace with your real Buttondown username once the account exists.
BUTTONDOWN_USERNAME = "916consulting"

JURISDICTION = {
    "nj_state": "NJ State",
    "nj_legislative": "NJ Legislative",
    "federal": "Federal",
    "healthcare_regional": "Healthcare Regional",
}
AFFECTS = {
    "municipality": "Municipality",
    "county": "County",
    "school_district": "School District",
    "authority": "Authority",
    "hospital": "Hospital",
    "practice": "Practice",
}
STATUS = {"proposed": "Proposed", "enacted": "Enacted", "guidance": "Guidance"}


def fmt_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


def entry_html(e: dict) -> str:
    eid = html.escape(e["id"])
    affects_attr = " ".join(e["affects"])
    affects_tags = "".join(
        f'<span class="tag">{html.escape(AFFECTS[a])}</span>' for a in e["affects"]
    )
    return f"""
<article class="entry" id="{eid}" data-jurisdiction="{html.escape(e['jurisdiction'])}" data-affects="{html.escape(affects_attr)}">
  <div class="entry-meta">
    <span class="caps date">{fmt_date(e['date_published'])}</span>
    <span class="caps juris">{html.escape(JURISDICTION[e['jurisdiction']])}</span>
    <span class="status status-{html.escape(e['status'])}">{html.escape(STATUS[e['status']])}</span>
  </div>
  <h2><a href="#{eid}">{html.escape(e['title'])}</a></h2>
  <p class="label caps">What this means for you</p>
  <p class="summary">{html.escape(e['summary_plain'])}</p>
  <div class="take">
    <p class="label caps">The 916 take</p>
    <p>{html.escape(e['pov'])}</p>
  </div>
  <div class="entry-foot">
    <a class="source" href="{html.escape(e['source_url'])}" rel="noopener">Source: {html.escape(e['source_name'])}</a>
    <span class="tags">{affects_tags}</span>
  </div>
</article>"""


entries_html = "\n".join(entry_html(e) for e in ENTRIES)
last_updated = date.today().strftime("%B %-d, %Y")
count = len(ENTRIES)

juris_buttons = "".join(
    f'<button class="filter" data-group="jurisdiction" data-value="{k}">{v}</button>'
    for k, v in JURISDICTION.items()
)
affects_buttons = "".join(
    f'<button class="filter" data-group="affects" data-value="{k}">{v}</button>'
    for k, v in AFFECTS.items()
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NJ AI Watch: AI Policy and Regulation Tracker for NJ Government and Healthcare | 916 Consulting</title>
<meta name="description" content="A plain language tracker of AI executive orders, laws, and guidance for New Jersey municipalities, counties, and school districts, plus healthcare AI regulation across NJ, NY, CT, and PA. Updated monthly by 916 Consulting.">
<link rel="canonical" href="https://www.916consulting.com/nj-ai-watch/">
<meta property="og:title" content="NJ AI Watch: AI Policy Tracker for NJ Government and Healthcare">
<meta property="og:description" content="What New Jersey administrators and regional healthcare leaders need to know about AI regulation, in plain language, updated monthly.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.916consulting.com/nj-ai-watch/">
<link rel="icon" href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="%230F3540"/><text x="32" y="44" font-family="Georgia,serif" font-size="30" text-anchor="middle" fill="%23FBFCFC">9<tspan fill="%234FAE9B">1</tspan>6</text></svg>'>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --navy: #174A56; --teal: #4FAE9B; --depth: #0F3540;
    --mist: #EEF3F2; --paper: #FBFCFC;
    --text: #174A56; --text-dim: #56737c;
    --line: #dde7e5; --line-strong: #c6d6d3; --card: #ffffff;
    --shadow-card: 0 1px 2px rgba(15,53,64,0.04), 0 8px 24px rgba(15,53,64,0.06);
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--paper); color: var(--text);
    line-height: 1.68; font-size: 16px; -webkit-font-smoothing: antialiased;
  }}
  h1, h2 {{ font-family: "Marcellus", Georgia, serif; font-weight: 400; line-height: 1.16; }}
  .caps {{ font-size: 0.7rem; font-weight: 500; letter-spacing: 0.24em; text-transform: uppercase; }}
  .wrap {{ max-width: 880px; margin: 0 auto; padding: 0 24px; }}
  a {{ color: inherit; }}

  .logo {{ display: inline-flex; align-items: baseline; gap: 12px; text-decoration: none; color: var(--navy); }}
  .logo .numerals {{ font-family: "Marcellus", Georgia, serif; font-size: 1.5rem; line-height: 1; }}
  .logo .one {{ color: var(--teal); }}
  .logo .caption {{ font-size: 0.6rem; font-weight: 500; letter-spacing: 0.5em; text-transform: uppercase; }}

  header.site {{
    position: sticky; top: 0; z-index: 50;
    background: rgba(251,252,252,0.88); backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--line);
  }}
  .nav {{ display: flex; align-items: center; justify-content: space-between; padding: 14px 0; }}
  nav.links {{ display: flex; gap: 24px; align-items: center; }}
  nav.links a {{ color: var(--text-dim); text-decoration: none; font-size: 0.86rem; font-weight: 500; }}
  nav.links a:hover {{ color: var(--teal); }}
  .nav-cta {{ color: #fff !important; background: var(--navy); padding: 8px 16px; border-radius: 6px; font-weight: 600 !important; }}
  .nav-cta:hover {{ background: var(--depth); }}
  @media (max-width: 640px) {{ nav.links a:not(.nav-cta) {{ display: none; }} }}

  .page-head {{ background: linear-gradient(180deg, var(--mist), var(--paper)); border-bottom: 1px solid var(--line); padding: 60px 0 44px; }}
  .eyebrow {{ display: inline-flex; align-items: center; gap: 12px; color: var(--teal); margin-bottom: 16px; }}
  .eyebrow::before {{ content: ""; width: 30px; height: 1px; background: var(--teal); }}
  .page-head h1 {{ font-size: clamp(1.8rem, 4vw, 2.6rem); color: var(--navy); max-width: 24ch; }}
  .page-head .meta {{ margin-top: 18px; color: var(--text-dim); font-size: 0.88rem; }}
  .disclaimer {{
    margin-top: 22px; padding: 14px 18px; max-width: 72ch;
    background: #fff; border: 1px solid var(--line); border-left: 2px solid var(--teal);
    border-radius: 4px; font-size: 0.85rem; color: var(--text-dim);
  }}

  .filters {{ padding: 26px 0 6px; }}
  .filter-row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 10px; }}
  .filter-row .caps {{ color: var(--text-dim); margin-right: 6px; }}
  button.filter {{
    font-family: inherit; font-size: 0.8rem; font-weight: 500;
    color: var(--text-dim); background: #fff;
    border: 1px solid var(--line-strong); border-radius: 999px;
    padding: 6px 14px; cursor: pointer;
  }}
  button.filter:hover {{ border-color: var(--teal); color: var(--teal); }}
  button.filter.on {{ color: var(--navy); border-color: var(--teal); box-shadow: inset 0 0 0 1px var(--teal); }}
  button.filter:focus-visible {{ outline: 2px solid var(--teal); outline-offset: 2px; }}
  .filter-count {{ font-size: 0.8rem; color: var(--text-dim); padding: 4px 0 0; }}

  .entries {{ padding: 18px 0 60px; display: grid; gap: 20px; }}
  .entry {{
    background: var(--card); border: 1px solid var(--line); border-radius: 4px;
    padding: 26px 28px; box-shadow: var(--shadow-card);
  }}
  .entry.hidden {{ display: none; }}
  .entry-meta {{ display: flex; flex-wrap: wrap; gap: 14px; align-items: center; margin-bottom: 10px; }}
  .entry-meta .date {{ color: var(--navy); }}
  .entry-meta .juris {{ color: var(--text-dim); }}
  .status {{
    font-size: 0.64rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--teal); border: 1px solid var(--line-strong);
    border-radius: 999px; padding: 4px 12px; background: var(--paper);
  }}
  .entry h2 {{ font-size: 1.3rem; color: var(--navy); margin-bottom: 14px; }}
  .entry h2 a {{ text-decoration: none; }}
  .entry h2 a:hover {{ color: var(--teal); }}
  .entry .label {{ color: var(--teal); margin-bottom: 4px; font-size: 0.62rem; }}
  .entry .summary {{ color: var(--text); font-size: 0.95rem; margin-bottom: 16px; max-width: 72ch; }}
  .take {{
    border-left: 2px solid var(--teal); background: var(--mist);
    border-radius: 0 4px 4px 0; padding: 12px 18px; margin-bottom: 16px; max-width: 72ch;
  }}
  .take p:last-child {{ color: var(--text-dim); font-size: 0.92rem; }}
  .entry-foot {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; border-top: 1px solid var(--line); padding-top: 14px; }}
  .source {{ font-size: 0.84rem; font-weight: 600; color: var(--navy); text-decoration: none; border-bottom: 1px solid var(--line-strong); }}
  .source:hover {{ color: var(--teal); border-color: var(--teal); }}
  .tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .tag {{ font-size: 0.66rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-dim); background: var(--mist); border-radius: 999px; padding: 3px 10px; }}

  .subscribe {{ background: var(--depth); color: var(--mist); padding: 64px 0; text-align: center; }}
  .subscribe h2 {{ font-size: clamp(1.5rem, 3vw, 2rem); color: #fff; margin-bottom: 10px; }}
  .subscribe p {{ color: #a9c0bd; font-size: 0.94rem; max-width: 50ch; margin: 0 auto 26px; }}
  .subscribe form {{ display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }}
  .subscribe input[type="email"] {{
    font-family: inherit; font-size: 0.92rem; padding: 13px 16px; min-width: 280px;
    border: 1px solid rgba(79,174,155,0.4); border-radius: 6px;
    background: rgba(238,243,242,0.06); color: #fff;
  }}
  .subscribe input[type="email"]::placeholder {{ color: #7fa8a0; }}
  .subscribe button {{
    font-family: inherit; font-size: 0.92rem; font-weight: 600;
    background: var(--teal); color: var(--depth); border: 0; border-radius: 6px;
    padding: 13px 24px; cursor: pointer;
  }}
  .subscribe button:hover {{ filter: brightness(1.08); }}
  .subscribe .fine {{ font-size: 0.76rem; color: #7fa8a0; margin-top: 14px; }}

  .crosslink {{ padding: 56px 0; border-bottom: 1px solid var(--line); }}
  .crosslink .box {{ background: var(--card); border: 1px solid var(--line); border-radius: 4px; box-shadow: var(--shadow-card); padding: 28px 30px; display: flex; flex-wrap: wrap; gap: 18px; justify-content: space-between; align-items: center; }}
  .crosslink h2 {{ font-size: 1.25rem; color: var(--navy); }}
  .crosslink p {{ color: var(--text-dim); font-size: 0.9rem; max-width: 52ch; }}
  .btn-navy {{ display: inline-block; text-decoration: none; background: var(--navy); color: #fff; padding: 12px 22px; border-radius: 6px; font-weight: 600; font-size: 0.9rem; }}
  .btn-navy:hover {{ background: var(--depth); }}

  footer {{ padding: 28px 0; font-size: 0.78rem; color: var(--text-dim); }}
  footer .wrap {{ display: flex; justify-content: space-between; align-items: center; gap: 14px; flex-wrap: wrap; }}
  footer .fine {{ max-width: 60ch; }}
</style>
</head>
<body>

<header class="site">
  <div class="wrap nav">
    <a class="logo" href="../index.html" aria-label="916 Consulting home">
      <span class="numerals">9<span class="one">1</span>6</span>
      <span class="caption">Consulting</span>
    </a>
    <nav class="links">
      <a href="../index.html#ai">AI Oversight</a>
      <a href="../index.html#services">Services</a>
      <a href="#subscribe">Subscribe</a>
      <a class="nav-cta" href="../index.html#contact">Contact</a>
    </nav>
  </div>
</header>

<div class="page-head">
  <div class="wrap">
    <span class="eyebrow caps">NJ AI Watch</span>
    <h1>AI policy and regulation, tracked for New Jersey government and regional healthcare.</h1>
    <p class="meta">Updated monthly at minimum · Last updated {last_updated} · {count} entries</p>
    <div class="disclaimer">
      General information, not legal advice. Every entry links to its primary source.
      Confirm current requirements with your own counsel before acting.
    </div>
  </div>
</div>

<div class="wrap filters">
  <div class="filter-row">
    <span class="caps">Jurisdiction</span>
    {juris_buttons}
  </div>
  <div class="filter-row">
    <span class="caps">Who it affects</span>
    {affects_buttons}
  </div>
  <p class="filter-count" id="filter-count"></p>
</div>

<main class="wrap entries">
{entries_html}
</main>

<section class="crosslink">
  <div class="wrap">
    <div class="box">
      <div>
        <h2>Need help applying any of this?</h2>
        <p>916 Consulting builds AI policies, evaluates vendors, and runs standing AI
        oversight for New Jersey agencies and regional healthcare organizations.</p>
      </div>
      <a class="btn-navy" href="../index.html#contact">Start a Conversation</a>
    </div>
  </div>
</section>

<section class="subscribe" id="subscribe">
  <div class="wrap">
    <h2>Get the monthly NJ AI Watch briefing.</h2>
    <p>One email a month with what changed and what it means for your organization.
    No spam, unsubscribe anytime.</p>
    <form action="https://buttondown.com/api/emails/embed-subscribe/{BUTTONDOWN_USERNAME}" method="post">
      <input type="email" name="email" placeholder="you@youragency.gov" required aria-label="Email address">
      <button type="submit">Subscribe</button>
    </form>
    <p class="fine">Published by 916 Consulting, LLC. Your address is used only for this briefing.</p>
  </div>
</section>

<footer>
  <div class="wrap">
    <a class="logo" href="../index.html" aria-label="916 Consulting home">
      <span class="numerals">9<span class="one">1</span>6</span>
      <span class="caption">Consulting</span>
    </a>
    <span class="fine">Not legal advice. Confirm current requirements with your own counsel.
    © 2026 916 Consulting, LLC · New Jersey</span>
  </div>
</footer>

<script>
  const state = {{ jurisdiction: new Set(), affects: new Set() }};
  const entries = Array.from(document.querySelectorAll('.entry'));
  const countEl = document.getElementById('filter-count');

  function apply() {{
    let shown = 0;
    for (const el of entries) {{
      const j = el.dataset.jurisdiction;
      const a = el.dataset.affects.split(' ');
      const okJ = state.jurisdiction.size === 0 || state.jurisdiction.has(j);
      const okA = state.affects.size === 0 || a.some(x => state.affects.has(x));
      el.classList.toggle('hidden', !(okJ && okA));
      if (okJ && okA) shown++;
    }}
    countEl.textContent = (state.jurisdiction.size || state.affects.size)
      ? 'Showing ' + shown + ' of ' + entries.length + ' entries'
      : '';
  }}

  document.querySelectorAll('button.filter').forEach(btn => {{
    btn.addEventListener('click', () => {{
      const set = state[btn.dataset.group];
      const v = btn.dataset.value;
      if (set.has(v)) {{ set.delete(v); btn.classList.remove('on'); }}
      else {{ set.add(v); btn.classList.add('on'); }}
      apply();
    }});
  }});
</script>

</body>
</html>
"""

out = ROOT / "index.html"
out.write_text(page)
print(f"Built {out} with {count} entries. Last updated stamp: {last_updated}")
