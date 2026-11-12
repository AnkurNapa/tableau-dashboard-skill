---
name: tableau-dashboard
description: Use when asked to build, design, review or fix a Tableau dashboard, workbook, .twb or .twbx, a Tableau Public viz, a Tableau calculated field, LOD or table calc, a Prep flow or Hyper extract for Tableau, or to publish, embed or automate Tableau (REST, TSC, Metadata API, Embedding API, extensions, Tableau MCP). Also for any Tableau function or formula, which chart type to use and how to build it, a Tableau number that looks wrong (totals, filters, nulls, LOD drift), data apps with dynamic zone visibility, brewery, winery or distillery dashboards in Tableau, or "the same as my Tableau Field Notes".
---

# Tableau dashboard

Distilled from Ankur's Tableau Field Notes (63 articles in ~/Documents/tableau-field-notes/src/content/articles), his 30 beverage Tableau builds (ankurnapa.github.io/_posts/*tableau*), the BREWERY_OPS workshop kit and the brewing KPI dashboard extension. Added on 12 Nov 2026: help.tableau.com (functions, charts, actions), 106 official KB articles from help.salesforce.com, eight real Desktop .twb saves from GitHub and the Tableau Cookbook for Experienced Professionals (PDF in ~/Downloads).

Each reference labels its content "official", "verified" or "derived". Test anything derived, or marked "typical form", before it goes into a client workbook. Ankur is a Tableau Ambassador: any public post carries "I'm a Tableau Ambassador (unpaid). Views are my own." and no Tableau vs Power BI comparisons.

## Before you start

Read `references/lessons.md` (short). Then open only the one reference the step needs from the table below, not all of them.

## Top traps (check every calc and every sheet against these)

1. FIXED LODs and Top N run before dimension filters. Add the filter to context or the number drifts.
2. Ratios are SUM over SUM. AVG of a ratio is wrong.
3. SUM of a FIXED field at a finer view multiplies it. Wrap it in MIN or MAX.
4. A join across facts of different grains multiplies totals. Use relationships.
5. Table calcs change when a dimension enters or leaves the view. Set Specific Dimensions.
6. Any expression with a NULL is NULL. IF or CASE with no ELSE returns NULL. Use ZN or IFNULL on purpose.
7. An aggregated field is a measure and cannot become a dimension. Use an LOD to make a dimension.
8. Grand totals with table calcs or EXCLUDE can show unexpected values or an asterisk. Check `kb-articles.md` before trusting them.
9. A date part (blue) is a label and a date value (green) is a timeline. Never compare a full year with a part year.
10. Anything labelled "derived" or "typical form" is untested. Say so on handover.

## Read the reference that fits the step

| Step | Reference |
|------|-----------|
| Shape the data, relationships, Prep, Hyper extracts, RLS | `references/data-and-prep.md` |
| Calculated fields, LOD, table calcs, order of operations, dates, parameters, sets, maps, chart chooser | `references/calcs-and-viz.md` |
| Any function: syntax, example, source limits (207 functions from help.tableau.com) | `references/functions.md` |
| Ready formulas for business questions: YoY, % of total, cohorts, top N, Pareto, dynamic titles (71 patterns) | `references/formula-patterns.md` |
| Every chart type: Show Me needs, shelf recipe, calcs, common mistake (53 charts) | `references/chart-types.md` |
| A number looks wrong: official KB fixes for unexpected results, totals, filters, nulls (106 articles, Top 20 traps) | `references/kb-articles.md` |
| Tableau Data Apps (2026.3 beta): agent-built web apps hosted in Tableau via Tableau MCP, scaffold, queryAsync, publish | `references/data-apps.md` |
| Layout, colour, type, KPI cards, actions, accessibility, performance, handover checklist | `references/dashboard-design.md` |
| Brewery, winery or distillery questions, KPI formulas, 30 worked builds | `references/beverage-dashboards.md` |
| Writing a .twb or .twbx by script | `references/twb-xml.md` |
| Publish, permissions, REST, TSC, Metadata API, embedding, extensions, TabPy, MCP | `references/publish-and-automate.md` |

## Build flow

1. **Question first.** Write the three to five business questions and one definition per KPI (numerator, denominator, grain, filters). One KPI, one definition: put it in a published data source, never in two workbooks.
2. **Data.** One fact table per grain, long format. Relate facts of different grains, never join them (a join at the wrong grain multiplied totals 12 times in the sample). Build the extract with the Hyper API (`pip3 install --user tableauhyperapi`) to a temp file, then swap.
3. **Calcs.** Ratios are SUM over SUM, never AVG of a ratio. A FIXED LOD runs before dimension filters: add the filter to context or the share drifts. Wrap a FIXED field in MIN or MAX in a view, or SUM multiplies it. Set table calc addressing with Specific Dimensions.
4. **Sheets.** Pick each chart from the chart chooser table. Under 1,000 marks a sheet. Colour carries one meaning only.
5. **Dashboard.** Fixed 1200 by 800, tiled containers, 8 px grid, a header of 64 px, BAN row, then the main chart, then detail. Filter actions over quick filters. Five categorical colours at most, text contrast 4.5 to 1.
6. **Ship.** Run the performance recorder, then the handover checklist in `dashboard-design.md`. Publish through TSC or the REST API with a PAT read from the environment, never typed into a script.

## Colour palettes

`palettes/Preferences.tps` holds 13 custom palettes: house, accessible (Okabe Ito, red amber green, greys), Field Notes and beverage (beer SRM, wine, whisky, brewhouse stages). Copy it to `~/Documents/My Tableau Repository/Preferences.tps` (merge if one already has palettes) and restart Tableau. One file per family sits beside it. To change a palette, edit `scripts/make_palettes.py` and run `python3 scripts/make_palettes.py palettes`; never hand edit the .tps files.

## Tooling on this Mac

Tableau Desktop is not installed (last ran 26 Sep 2026), so nothing here can open a workbook to prove it works. Choose a route and tell Ankur which:
- **Build kit (default).** Clean data as CSV or .hyper, calc fields typed out, a sheet by sheet shelf recipe like the BREWERY_OPS README. Ankur builds it in Desktop or Tableau Public web authoring in minutes.
- **Scripted .twb.** Follow `twb-xml.md` (verified against eight real Desktop saves). Template first: edit a real saved workbook rather than writing XML from nothing, since no maintained from-scratch generator exists. It is unverified until it opens in Desktop: say so on handover and never claim it works.
- **Dashboard extension.** For custom visuals inside Tableau, copy `~/Documents/obsidian/tableau-brewing-extension` (trex manifest plus extension.js).

## After every build: learn

1. Note each mistake made or caught (a wrong number, a broken shelf, a guessed formula, a fetch that failed, a copy slip). Add it to the top of `references/lessons.md` and to `~/.claude/mistakes-log.md`.
2. If it matches an existing lesson, mark that lesson REPEAT and add its rule to Top traps above. Keep Top traps to 12 or fewer: merge before adding.
3. If a reference file was wrong, fix that file in place and label the fix with the date.
4. A new technique that worked goes into the matching reference, labelled "verified" with the date and the dataset it was tried on.

## Copy

Titles, captions, tooltips and READMEs are copy. They go through the humanizer rules: no dashes, no ", and", British spelling. Scan the files on their own before any commit.
