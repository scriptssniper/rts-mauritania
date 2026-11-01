# GAMEPLAY — The Undefeated Soil
### Core design document · v0.1 (2026-11-01)
Engine: Godot 4. Sub-genre: point-control RTS, no base-building (World in Conflict loop, Northgard zones). Campaign 1480–1934. History anchors cite repo research docs; every mechanic that is invention, not history, carries a **[FICTION]** tag.

---

## 1. Design Pillars

1. **Asymmetry is economy, not stats.** Both sides field similar small arms [RESEARCH_campaign_history §3: "the gap is logistics and forts, not weapons quality"]. The resistance *takes* what it fields; France *pulls* what it fields across an empire. Every unit both sides deploy is cargo somebody moved across the map.
2. **Mobility vs lattice.** Camel speed and well knowledge vs borj lattice + camel columns. France buys reach by building; the resistance *is* reach.
3. **Water is the clock.** Every unit ticks thirst away from friendly wells. Timers, not health bars, decide desert operations (Nouarmach: 13 killed in action, 11 died of thirst — [RESEARCH_campaign_history §1.3]).
4. **Allegiance is production.** No barracks. Manpower pools live in tribes; tribes switch sides. Losing allegiance = losing the ability to make war [RESEARCH_campaign_history §3: 800+ recognized chiefs, divide-and-rule].

## 2. The Two Economies

| | Resistance | France |
|---|---|---|
| Production model | **Take** — loot, tribute, herds | **Pull** — imperial logistics, subsidies |
| Resource types | Loot crates (arms/ammo/supply), camels, herds, water, baraka (morale) | Military budget, administrative budget, water, convoys |
| Acquisition loop | Rezzou → loot → rearm → bigger rezzou | Budget → convoy → borj → projection → submissions → income |
| Sinks | Raid range extension, war parties, gifts to tribes (allegiance) | Columns, borj construction, subsidies, escort |

The two loops interlock into one **transfer economy**: zero-sum cargo. Every crate looted is a crate France must re-pull from the metropole through two colonies. Both sides see the same ledger ("France: 240 crates in transit; Resistance: 96 captured to date"). Looting isn't flavor — it is the opponent's supply line bleeding.

## 3. Looting System (Resistance core loop)

**Sources:** raided convoys, ambushed columns, overrun borj outposts, tax/raid caravans, tribute payments from wavering tribes.

**Loot categories** (drop as physical crates on raid sites, must be carried off on camels — loot has weight and slows the band):
- **Arms** — Gras rifles (until 1907), then Berthier Mle 1907s (real tech event — smokeless 8mm); bayonets, revolvers; machine-guns only as rare column loot (2 per column, PLAUSIBLE per RESEARCH_armies §1)
- **Ammunition** — the true bottleneck; rifles without cartridges are clubs
- **Provisions & water gear** — extends raid range (each crate = +N hours off-well)
- **Pack camels** — cargo capacity, the loot multiplier
- **Military kit** — uniforms, telegraph wire, tools, medical stores
- **Coin/valuables** — convertible to gifts (allegiance) via zawiya network

**Loot-to-unit pipeline:** a war band's tier = its equipment, not its experience.
- Lance band (traditional) → **Gras band** (10 looted rifles + ammo crate) → **Rifle line** (30+ rifles, sustained volley fire) 
- Tech tree reads as a capture log: "Repeating fire doctrine — unlocked: seized 100 Gras + 3,000 cartridges at Amatil."

**Repurposing rules:** looted gear re-arms levies, captured water gear extends operational radius, telegraph wire becomes camp alarm nets **[FICTION — plausible craft reuse, not documented]**. Looted pack camels join herds.

**Degradation:** looted rifles wear (no armourer network); ammo consumed, never manufactured — every volley fired shrinks the war. Forces raid discipline: the player must keep raiding to keep shooting. Historical mirror: dependence on Moroccan gun-runs and Saint-Louis merchant smuggling [RESEARCH_campaign_history §3, §5.7].

**Cannot be looted:** artillery and machine guns can be *captured* but not *served* (no ammunition pipeline, no trained crews; a captured gun is a static strongpoint piece until its cartridges run dry). Justified: resistance fielded no artillery, ever [RESEARCH_campaign_history §3].

**Uniforms — disguise:** looted kit allows one band per raid to pass as a friendly méhariste patrol at distance until it moves/attacks **[FICTION — standard RTS infiltration fantasy; no documented instance; keep, it's cheap and readable, but never claim it in historical notes]**.

## 4. French Imperial Pull (France core loop)

**Supply lane stages (physical, visible, attackable):**
1. **Metropole** — budget accrues (tier-limited by campaign year)
2. **Saint-Louis** — river steamers up the Senegal; rail head later [RESEARCH_campaign_history §4]
3. **Forward depot** (Rosso/Podor → Moudjeria) — convoy assembly
4. **Convoy** — camel trains, slow, escort-dependent; each borj passed refreshes escort
5. **Borj lattice** — supply radius extension; a borj's zone projects water discipline (slower thirst decay), reinforcement spawn, and treaty projection

**Interception points:** river dockings (safe, but tier-limited), convoy legs (the resistance's hunting ground), borj handoff (garrisoned). The lane is the campaign map's spine.

**Budget duality:**
- **Military budget** → columns, garrisons, escorts, borj construction
- **Administrative budget** → subsidies (coutume replacements), treaty missions, emir restorations. Submissions convert tribes to income + lower unrest but cost real time and diplomats; losing a restored emir to dissidence (the Ayda arc [CHARACTERS.md #10]) is an administrative-budget catastrophe.

**Escalation tiers by campaign year:** 1902–05 diplomacy-cheap/military-poor (Coppolani) → 1907–09 column war (Gouraud) → 1910–13 peak projection → WWI scarcity tier (budget halved, historical 1916 German gun-run event) → 1920s–34 police-war tier (élite méharistes, slow, cheap). Tiers auto-set per mission; skirmish mode exposes them as handicaps.

## 5. Shared Systems

- **Wells:** capture points; controlling side sets open/denied. Denial = filling/scattering (fast) or corpse-poisoning (slow, permanent, atrocity-marked) — **corpse-poisoning [FICTION-flag: not documented in our sources; historical well-warfare denial is] — atrocity mechanics cost allegiance globally**.
- **Thirst clock:** unit stat, ticks up off-well; high thirst = combat penalty → attrition → death (Nouarmach rule). French columns decay slower inside borj radius (water discipline).
- **Herds:** mobile slow economy; graze pasture zones (seasonal); raidable; feed both manpower pools and cargo capacity. Herd loss = famine events in tribes (allegiance hit to their owner).
- **Caravan economy (azalaï):** neutral salt/goods convoys run fixed routes on a calendar [RESEARCH_precolonial §azalaï]; either side can tax (income + caravan reroutes away) or raid (loot + route dies). France taxing = submission pressure; resistance raiding = loot but hurts civilian tribes (allegiance cost).
- **Allegiance meter (per tribe):** −100…+100. Drivers: subsidies, gifts, protection efficacy, atrocity proximity, marabout diplomacy (Sidiya Baba = French-side multiplier; Goudfiya sheikhs = resistance-side), defeat of local rivals. At thresholds: tribute flows, recruitment unlocks, intelligence sharing; hostile: raids, hidden rezzou staging.
- **Seasons:** rainy season (Jun–Sep) — Sahel pasture blooms (herd recovery, cheaper upkeep), columns bog, rezzou season pauses (historical rhythm); dry season — water war peaks; transhumance windows move herd targets **[RESEARCH_armies §7 pending: biome calendar]**.

## 6. Unit Rosters (sketch)

**Resistance:** lance band → Gras band → rifle line; rezzou raiders (fast, loot-bonus, fragile); herd drivers (civilian logistics); marabout retinue (baraka aura — no rout, allegiance diplomacy) [CHARACTERS.md #5]; tribal levies (quality = tribe allegiance); tbal drum unit (capturable objective — sovereign morale field) [RESEARCH_poetry, tbal entry].

**France:** tirailleur foot company; camel-mounted tirailleurs; méhariste company (elite, water-discipline aura; khaki drill + chéchia — era-correct dress per RESEARCH_armies §3); spahis (river-theatre cavalry); 2e escadron de spahis algériens (confirmed in the 1908–09 colonnes volantes — rare veteran cavalry unit, RESEARCH_armies §1); borj garrison; engineer escort; light mountain gun (2×65mm Mle 1906 per column, PLAUSIBLE) + machine-gun section; diplomats/Coppolani-type agents (administrative budget units); telegraph crew (vision link between borjs).

**Neutral:** azalaï caravan, zawiya (safe-passage node), tribal camps (both sides).

## 7. Mission Archetypes — Win/Loss

| Archetype | Plays as | Win | Lose |
|---|---|---|---|
| Rezzou raid | Resistance | loot quota + extraction off-map | band destroyed / thirst death |
| Post siege | Resistance | borj falls or garrison surrenders | relief column arrives unbled |
| Column escort | France | convoy % delivered | convoy burned |
| Submission map | France | tribes above threshold before budget runs | rebellion spreads |
| Counter-rezzou | France | destroy raider band | raiders escape with loot |
| Assassination window | Resistance (scripted) | target killed in 5-min window | window closes |
| Waterless crossing | either | cross the gap with X% alive | — |

## 8. Balance Levers & Failure Modes

- **Looting snowball** (resistance): cap carried ammo per band (camels = soft cap); French tier escalation floods better-armed escorts; ammunition burn rate per volley.
- **French turtling**: administrative income requires submissions, which require projection; borj upkeep drains military budget — lattice is a money fire, not a fort line.
- **Degenerate camping on wells** (either): denial is cheaper than holding; a well denied to *both* sides (scattered) becomes dead ground; season shifts move the fight (pastures).
- **Thirst death-spiral** frustration: bands auto-path via known wells (resistance) / supply radius (France); player error punished, pathing error never.
- Ledger transparency is itself a balance tool: France seeing "240 crates lost" creates counter-raid pressure organically.

## 9. Open Questions

1. Artillery capture — static-only, or draggable as siege bait? (leaning static-only)
2. Multiplayer mirror or async? (default: none — single-player campaign first)
3. How visible is the enemy ledger — full fog-of-war-honest numbers, or intelligence-gated?
4. Disguise band: AI-readable at what range/speed? Needs prototype.
5. Atrocity mechanics (well-poisoning, reprisals): keep as mechanics with allegiance costs, or narrativize only? Tone call.
6. Algerian cavalry roster slot pending [RESEARCH_armies].
7. Season calendar granularity vs map scale — needs biome research (§5) to land.
8. Campaign years vs skirmish: expose escalation tiers as difficulty, or fixed history?
