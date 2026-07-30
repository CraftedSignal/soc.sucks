# soc.sucks — one-pager design

**Date:** 2026-07-30
**Status:** Approved concept, spec for implementation
**Goal:** A single-page website at soc.sucks that any SOC analyst instantly recognizes as their daily life, ending in a CTA that drives traffic to craftedsignal.io.

## Concept

**"The Alert Queue" — the page is a broken SIEM.** The visitor lands inside a parody SIEM triage queue. Every "alert" is a SOC pain point written deadpan in SIEM format. Mid-page the queue gives up and a manifesto takes over. The final section filters the queue to `TRUE POSITIVE (1)`: the CraftedSignal reveal and CTA.

Decisions made during brainstorming:

- **Tone:** Aikido-level spice — sharp, sarcastic, the occasional "bullshit"-tier swear where it lands. Shareable in a work Slack.
- **Branding:** Manifesto-first, brand-last. CraftedSignal appears only in the final reveal.
- **Strategic through-line:** AI auto-triage is part of the problem, not the fix — everyone sells faster ways to close alerts; nobody fixes what generates them. CraftedSignal's differentiation (fix detections upstream) is the payoff of this argument.
- Keep the existing site's joke ("We know it does.") as the opening beat.

## Page structure (five beats, one scroll)

### 1. Hero — the SIEM boots up

- Fake console chrome bar: `UNIFIED SECURITY OPERATIONS CONSOLE v4.7.2 — END OF LIFE`.
- Live-ticking counter: starts at `47,832 OPEN ALERTS`, increments on an irregular interval.
- Huge display type: **"SOC sucks."**
- Subline: *"We know it does. So do you."*
- Scroll cue: `▾ begin triage`.

### 2. The queue — ten alert cards

Each card: severity chip, monospace rule name, metadata line (age / count / assignee / status), deadpan body copy. Copy deck (microcopy may be polished during implementation; tone and meaning are fixed):

1. `CRITICAL` · `Suspicious_PowerShell_v2_FINAL_old` · firing 14× today · assignee: none — *Same rule. Same false positive. Nobody remembers who wrote it. Nobody dares delete it.*
2. `HIGH` · silent for 212 days — *Stopped matching when the log source changed in March. Nothing broke. Nothing fired. Nobody noticed.* (Supporting stat: industry data says only ~5% of deployed detections actually work.)
3. `INFO` · recurring: monthly, before the board meeting — *The slide says 87% MITRE coverage. The heatmap is green. Nobody has ever tested it.*
4. `CRITICAL` · 03:12 AM — *Paged. Escalated. False positive by 03:19. Sleep not recovered. Trust not recovered either.*
5. `MEDIUM` · ticket #4821 · opened 14 months ago — *Tuning request. Status: backlog. Priority: someday.*
6. `HIGH` · deployed straight to production — *Test coverage: "worked in the lab". Rollback plan: prayer.*
7. `LOW` · threshold raised again, fourth time this quarter — *The dashboard is finally green. So is the attacker's path.*
8. `NEW` · via: vendor webinar — **AI-powered auto-triage now enabled.** *The false positives are still being generated. They're just being closed faster now, by something that also doesn't know why they exist.*
9. `MEDIUM` · author: left the company two years ago — *The rule stays. Changing it is archaeology. Deleting it is liability.*
10. `INFO` · audit season — *The auditor asked if the detections work. We showed them a spreadsheet. Everyone nodded.*

Interactive gag: clicking **Dismiss** on a card spawns a duplicate card (*"1 new alert"*) and ticks the hero counter up. Progressive enhancement only — page fully readable without JS.

### 3. The frame break

Near the end of the queue the cards visually degrade (glitch/fade). The page gives up: **"Forget the queue."** Hard contrast switch from dark SIEM to bone-white manifesto.

### 4. The manifesto

Off-white background, massive editorial type, numbered articles. Title: **The soc.sucks manifesto**.

1. An alert nobody reads is a lie.
2. A detection that can't be tested is a guess.
3. Coverage is not a heatmap on a slide. Coverage is what fires when it matters.
4. Noise is not diligence. Volume is not vigilance.
5. Triaging noise faster is not the same as making less noise. The problem was never how fast you close alerts. It's what's creating them. *(thesis)*
6. A rule that breaks silently turns your SIEM into a diary.
7. Burnout is not a staffing problem. It's a signal-quality problem.
8. You were hired to hunt threats. Not to close tabs.

Sign-off: **"SOC doesn't have to suck."**

### 5. The reveal — `TRUE POSITIVE (1)`

Back to the dark queue, but filtered: `filter: TRUE_POSITIVE (1)`. One clean card in a distinct accent (calm green — the only green on the page):

- Title: *Detection: a team building the fix.*
- Meta: `confidence: high · source: verified`
- Body: *"We're not another AI that closes your alerts faster. We fix the detections generating them — tested before they ship, monitored so they never break silently, tuned so the noise never reaches the queue. We're CraftedSignal, and we build the detection engineering control plane."*
- CTA button: **Investigate → craftedsignal.io** linking to `https://craftedsignal.io/?utm_source=soc.sucks&utm_medium=referral&utm_campaign=manifesto`.

Footer: *"soc.sucks — built with love and resentment by CraftedSignal."*

## Visual direction

- Dark near-black SIEM aesthetic; monospace for chrome, rule names, and metadata; real-SIEM severity colors (red / amber / blue chips). Restrained scanline/glitch touches.
- Manifesto section inverts everything: off-white background, huge high-contrast editorial type. The switch is the visual "eye-catcher" moment.
- Typeface pairing: a monospace (e.g. JetBrains Mono) + a heavy display/editorial face for hero and manifesto. Final selection during implementation via the frontend-design skill.
- Fully responsive, mobile-first — primary distribution is Slack/LinkedIn/X on phones.
- `prefers-reduced-motion` respected: no ticking counter animation, no glitch effects.
- Accessibility: semantic HTML, WCAG AA contrast, keyboard-reachable controls.

## Technical

- **One self-contained `index.html`**: inline CSS, small vanilla JS (counter tick, dismiss gag). One Google Fonts link. No build step, no framework, no analytics script (attribution via UTM only).
- **Hosting:** GitHub Pages, existing `CNAME` (soc.sucks). Deploy = push to main.
- **Social:** full OG + Twitter card meta tags; `og-image.png` (1200×630, "SOC sucks. We know it does." + alert-counter motif) referenced by absolute URL `https://soc.sucks/og-image.png`.
- **Favicon:** inline SVG data URI — red alert-badge dot.
- **Meta:** title `SOC sucks. We know it does.`; description written to be quoted when shared.

## Success criteria

- The joke is legible within 3 seconds of landing (chrome + counter + "SOC sucks.").
- A SOC analyst recognizes at least one alert card as their own life before the frame break.
- Share card renders correctly in Slack, LinkedIn, X.
- Single HTML file stays lean (~<100 KB excluding fonts and og-image).
- Works fully without JavaScript; gags are enhancement.
- Outbound CTA carries UTM parameters so craftedsignal.io analytics attribute the traffic.

## Out of scope

- No signup forms, waitlists, or analytics on soc.sucks itself.
- No CMS, build pipeline, or multi-page structure.
- No paid assets; fonts via Google Fonts only.
