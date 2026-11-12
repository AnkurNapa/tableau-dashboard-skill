# Beverage dashboards catalogue (30 builds)

Source: 30 posts at ankurnapa.github.io/_posts/*tableau*.md (Jan to Oct 2023) plus the Tableau Public list in tableau-field-notes/src/data/vizzes.ts and the page tableau-field-notes/src/pages/beverage.astro.

## How to read this file

- The posts are design write-ups, not workbook exports. They give the business question, the grain, the measure definitions and the chart choices in prose. They give very few complete formulas.
- "Verbatim" means the formula is copied exactly from the post. "Suggested" means the post names the measure but not the formula, so the formula is my inference. Treat Suggested lines as starting points to check against the client's definitions.
- Field names in square brackets are the names the posts use. Sheet counts, filter placement and pixel layout are not in the posts. Where a layout line says "implied", it is read from the prose.
- Generic layout from the post figures: a filter strip across the top, three KPI tiles under it, then one trend sheet and one breakdown sheet. Use this when a post gives nothing more.
- Every post ends with a "Where it breaks" section. The strongest of these are kept below as "Watch", because they tell you what to caption on the dashboard.
- Tableau Pulse, Explain Data and TabPy appear in almost every post. They are add-ons, not part of the build. Mention them only when the client has Tableau Cloud.

## Tableau Public vizzes (published, domain tagged)

| Viz | Domain | Published | Views at 12 Oct 2026 |
|---|---|---|---|
| Wine Intelligence | wine | 2026-05-24 | 356 |
| Craft Beer Intelligence | beer | 2026-05-24 | 314 |
| Craft Distillery | spirits | 2026-05-24 | 182 |
| Wine Operational Intelligence | wine | 2026-05-26 | 37 |
| Beer Fermentation | beer | 2024-11-17 | 229 |
| Hop Buyer Segmentation in India | beer | 2025-12-20 | 99 |
| Pub Brewery Performance Overview (sales trends and inventory) | beer | 2024-11-12 | 98 |
| Craft Beer Reviews | beer | 2025-08-05 | 48 |
| Indian Beer Market | beer | 2024-07-02 | 56 |

All hang under https://public.tableau.com/app/profile/ankur.napa/viz/. Eight non-beverage vizzes (Makeover Monday, Voronoi, L-shaped bars, sales calendar, jump plot and others) show the technique range: custom shapes, calendars and cohort jump plots.

---

# Part 1: The 30 builds

## Brewing production and quality

### D01 Brewery production and yield (2023-01-04)
- Business question: are we drifting, holding or improving on brewhouse yield? Is a yield problem really a capacity problem?
- Grain: one row per batch. Facts hang off a batch key.
- Fields: [Batch ID], [Extract Recovered], [Theoretical Extract], wort volume into fermenter, original gravity, racking loss, packaged volume, fermenter, period.
- Calcs, verbatim: `{ FIXED [Batch ID] : SUM([Extract Recovered]) }` and `{ FIXED [Batch ID] : SUM([Theoretical Extract]) }`, then divide the rolled up sums.
- Calcs, suggested: Brewhouse yield % = SUM of the two fixed fields above divided as a ratio of sums (volume weighted). Loss % = (volume in minus volume out) / volume in at each transfer.
- Sheets: monthly yield trend with target reference line; BAN tiles; tank turns (count distinct batches per fermenter per period) dual axis with capacity utilisation.
- Metric switch: a parameter (yield, hL per brew, tank turns per month, loss %) driving a CASE calculated field, with a parameter action.
- Layout: implied KPI row, trend, tank turns panel.
- KPIs: brewhouse yield, hL per brew, tank turns, loss %.
- Watch: a 2 hL pilot batch must not weigh the same as a 200 hL brew. Uncorrected gravity temperatures and split batches break the maths silently.

### D02 QC control charts (2023-01-21)
- Question: is this sample normal variation or a signal?
- Grain: one row per measurement with parameter name, batch or fill, timestamp and sampling point.
- Calcs, suggested: baseline mean and standard deviation from a fixed baseline window (not live). UCL = mean + 3 sd. LCL = mean minus 3 sd. Warning bands at 2 sd. Out of limits flag = [Value] > [UCL] OR [Value] < [LCL].
- Sheets: continuous time line with reference lines and a shaded reference band; red colour on breaching points.
- Actions: parameter to pick the QC variable (gravity, diacetyl, pH, fill volume); filter and highlight actions from a point to the batch.
- KPIs: out of control point count, parameter mean against limits.
- Watch: never recompute limits live or across a recipe change. An out of control point is a prompt to look, not a fault.

### D03 Live fermentation monitoring, beer (2023-02-04)
- Question: is this tank following its expected path?
- Grain: one row per reading: tank, batch, recipe, timestamp, gravity, temperature, CO2 or pressure.
- Calcs, suggested: per recipe target corridor built from historical good batches (expected gravity and temperature against fermentation hour). Outside band flag compares the current reading with the corridor.
- Sheets: small multiples, one line chart per active tank, gravity curve over a shaded band, temperature on a secondary axis; "attention" indicator; optional TabPy projection as a dashed extension.
- Actions: filter action tank to full history (start, dissolved oxygen at pitch, yeast generation). Parameter to switch recipe or strength band.
- Data: live connection or scheduled .hyper extract; near live, minutes of lag.
- Watch: not a control system. Never wire safety alarms to an extract.

### D04 Wine fermentation (2023-02-14)
- Question: which tank's Brix descent is sluggish before it stalls?
- Grain: one row per tank per reading: tank, Brix, temperature, YAN, malolactic status.
- Calcs, verbatim: `{FIXED [Tank] : MIN([Brix])}` (starting Brix, so percent of sugar consumed is stable).
- Calcs, suggested: percent consumed = 1 minus current Brix / starting Brix. Stuck flag is a table calculation comparing latest Brix with the reading two or three days earlier while Brix is still above dryness.
- Parameters: white ceiling about 12 to 18 C, reds about 25 to 30 C, opening YAN about 150 to 250 mg/L, held as parameters and reference bands.
- Sheets: small multiple grid per tank, Brix descending line coloured by whether the latest temperature is inside the band.
- Actions: parameter action loads the tank detail view with YAN and malolactic status.
- Watch: a flat curve can be a healthy lag phase on native ferments. Six hourly logging misses short spikes.

### D05 Packaging line OEE (2023-02-21)
- Question: where do packaging losses live: stoppages, speed or scrap?
- Grain: one row per production run or shift per line: planned time, run time, rated and actual output, total and reject counts, downtime reason, minutes lost.
- Calcs, stated in prose: Availability = actual run time / planned production time. Performance = actual output / theoretical output at rated speed. Quality = good units / total units. OEE = Availability x Performance x Quality.
- Calcs, suggested: Pareto running total as a table calculation (`RUNNING_SUM(SUM([Minutes Lost])) / TOTAL(SUM([Minutes Lost]))`) on a descending sort.
- Sheets: OEE BAN with gauge against target; three component tiles; Pareto of downtime reasons; OEE trend with target reference line.
- Actions: parameters for line and shift; filter action from a day to that shift's runs and stoppages.
- Watch: dirty downtime coding (everything filed as "other") makes the Pareto one useless bar.

## Quality, sensory and blending

### D06 Wine tasting and blending (2023-04-14)
- Question: which lots in what proportion give the target profile?
- Grain: one row per lot per attribute per taster (long format via Prep). Attributes: fruit, tannin, acidity, oak, balance.
- Calcs: FIXED average per lot per attribute across the panel; INCLUDE to keep per taster variation (disagreement is signal). Blend profile = SUM(lot score x lot proportion) over lots, proportions held in one parameter per candidate lot.
- Sheets: radar or small multiple bars per lot; blend profile against a target shape parameter.
- Watch: blending is non linear. The weighted average is a hypothesis to taste.

### D07 Whisky blending and sensory (2023-09-14)
- Question: how close is a candidate vatting to house style and what does it cost in scarce stock?
- Grain: one row per cask: GC measurements (esters, phenols, vanillin, lactones), panel scores per descriptor, cost or scarcity.
- Calcs: blended profile as a weighted average with per cask proportion parameters; distance from the house target profile.
- Sheets: radar or parallel coordinates of trial against target; cost and scarcity tally.
- Actions: filter and parameter actions to swap casks live.
- Watch: GC numbers do not equal flavour. You can only blend stock that exists.

### D08 Sensory panel results (2023-10-04)
- Question: what does the beer taste like, how much does the panel agree, how true is it to type?
- Grain: one row per panellist per sample per attribute per session.
- Calcs, suggested: panel mean per attribute; standard deviation across panellists (agreement); panellist score minus panel mean (calibration).
- Sheets: attribute profile bars; box plot per attribute; radar of panel mean against style target; panellist deviation over time.
- Actions: parameters for product and session; highlight action from an attribute to individual scores.
- Watch: small samples. Use a control chart mindset to discount tiny moves.

## Cellar, vineyard and rackhouse

### D09 Vineyard yield and harvest (2023-01-14)
- Question: which block do I pick and when?
- Grain: sampling record per block per date: Brix, titratable acidity, pH (target about 3.2 to 3.6 for reds), bunch counts, berry weights.
- Calcs, verbatim: `{FIXED [Block] : AVG([Brix])}`.
- Sheets: block map (colour = Brix, size = estimated yield); ripeness curve (date against Brix, one mark per block) with target Brix by varietal as a parameter reference line; pick sequence table sorted by projected pick date and coloured by tank capacity available.
- Actions: filter action map to curve.
- Data: live source if daily, .hyper if weekly. Prep to standardise block names.
- Watch: weekly sampling cannot catch a three day heat spike. Phenolic ripeness stays a manual note.

### D10 Cellar and barrel ageing (2023-03-14)
- Question: what is in barrel, how old, which barrels need attention?
- Grain: one row per barrel: fill date, oak type, lot, last top up, free and total SO2, volume, vintage.
- Calcs, verbatim: `{FIXED [Lot] : SUM([Volume])}` (litres per lot). An INCLUDE expression averages free SO2 at barrel grain but displays by lot.
- Sheets: barrel matrix (colour = oak type, size = volume); ageing timeline of months in barrel against a target window parameter; top up running total; SO2 red amber green status.
- Actions: click lot to see its barrels; parameter action to flex the ageing target.
- Watch: hand logged data. Barrel to barrel variation hides inside type averages.

### D11 Whisky cask maturation and angel's share (2023-06-14)
- Question: what do we hold, how fast is it evaporating, when is it ready?
- Grain: one row per cask per date observation: cask ID, fill date, cask type, original litres of pure alcohol, current strength, weighing or dip date.
- Calcs, verbatim: `{ FIXED [Cask ID] : MIN([Fill Date]) }` (stable maturation age).
- Calcs, suggested: cumulative loss as a table calculation compounding about 2% a year, partitioned by cask ID and ordered by date. Target age parameter and a loss rate parameter for what-if.
- Sheets: cumulative loss curves; casks reaching target age next quarter; projected volume and strength.
- Watch: sparse weighings make the curve an interpolation. Exponential smoothing misses cask to cask variation.

### D12 Rackhouse microclimate (2023-07-14)
- Question: where do heat and dryness drive faster loss and more variation?
- Grain: one reading per sensor per timestamp, joined to a cask position table (bay, row, height).
- Calcs, verbatim: `{ FIXED [Bay], [Height] : AVG([Temperature]) }`.
- Sheets: heatmap with bay and row on axes, height as small multiple or parameter, colour by temperature, humidity or measured loss; rotation candidates list (casks in the hottest driest cells).
- Actions: highlight action from a hot zone to its casks.
- Data: Prep pivot, then .hyper.
- Watch: few sensors means the heatmap is interpolated, a model not a map.

### D13 Whisky maturing stock valuation (2023-08-14)
- Question: how much capital is locked in casks and when does it unlock?
- Grain: one row per cask: fill date, cask type, strength, current LPA after losses, age band.
- Calcs: `{ FIXED [Cask ID] : ... }` (post gives the shape, not the body) to value each cask once; per litre value driven by age, cask and strength (suggested).
- Sheets: treemap by age band and cask type; litres crossing target age (12, 15 or 18 years) per quarter via a target age parameter; cumulative laid down against matured.
- Actions: row level security so finance sees all and site managers see one warehouse.
- Watch: show values as a range with assumptions on the canvas.

## Production, cost and procurement

### D14 Distillery production and spirit yield (2023-10-14)
- Question: which runs are efficient and which are quietly wasteful?
- Grain: one row per production run (mash plus distillation): cereal tonnes, LPA collected, volume and strength at heads, hearts and tails cuts, energy used.
- Calcs, stated: Spirit yield = LPA / tonnes of cereal. Energy per LPA = energy used / LPA produced. Hearts fraction = hearts / total spirit.
- Sheets: yield by run as a control style chart against target; cut performance; energy per LPA. A LOD holds the per still baseline while the user filters by month.
- Parameter: target yield.
- Watch: a wider hearts cut lifts yield but pulls heavier congeners. Meter accuracy sets the ceiling.

### D15 COGS per hectolitre (2023-05-04)
- Question: which cost lever moved the margin?
- Grain: cost components per period or batch plus hL: ingredient, packaging, energy, direct labour, allocated overhead.
- Calcs, suggested: COGS per hL = SUM(total cost) / SUM(hL), each component its own field and each divided by hL.
- Sheets: waterfall from baseline COGS/hL through each driver delta (table calculation on running total of deltas). What-if parameters for malt, aluminium and energy tariff wired into the cost fields.
- Watch: document the overhead allocation basis on the canvas. Mismatched billing periods (quarterly energy, daily volume) distort the figure.

### D16 Procurement and commodity price (2023-05-21)
- Question: how much spend is still exposed to the market?
- Grain: commodity by period: forecast demand, contracted volume, contract price, spot price.
- Calcs, suggested: Unhedged volume = forecast demand minus contracted volume. Exposure = unhedged volume x (spot minus contract price). Coverage = contracted volume / forecast demand, with a FIXED LOD for contracted volume per commodity.
- Sheets: coverage over time area chart per commodity with spot and contract price on a dual axis; exposure on colour. Scenario parameter per commodity price.
- Watch: Tableau's forecast is not fit for hedging. Contract caps and collars are simplified.

### D17 Inventory and stock age (2023-04-21)
- Question: which lots are old and overstocked?
- Grain: one row per lot: receipt date, on hand, average daily demand.
- Calcs, verbatim: `{ FIXED [Lot ID] : MIN([Receipt Date]) }` (age = DATEDIFF against today).
- Calcs, suggested: Days of cover = on hand / average daily demand. Age band (fresh, watch, ageing, critical) by shelf life per product. FIFO risk flag = lot age over its band threshold while newer lots of the same SKU are still being picked, threshold as a parameter.
- Sheets: heatmap of SKU by age band; scatter with colour = age and size = cover so old and overstocked is visible.
- Watch: receipt date integrity. Returns re-entering stock without a new date.

## Commercial and market

### D18 Depletions and sell through (2023-03-04)
- Question: what did the market pull, not just what we shipped?
- Grain: account by SKU by month: depletion cases, opening inventory, shipment cases.
- Calcs, verbatim: `{ FIXED [Account], [SKU] : SUM([Depletion Cases]) } / { FIXED [Account], [SKU] : SUM([Opening Inv]) + SUM([Shipment Cases]) }` (sell through).
- Calcs, verbatim (YoY): `(ZN(SUM([Depletions])) - LOOKUP(ZN(SUM([Depletions])), -12)) / ABS(LOOKUP(...))`. The post elides the denominator with `...`; complete it as `ABS(LOOKUP(ZN(SUM([Depletions])), -12))`.
- Sheets: dual axis line (shipments faint, depletions bold); highlight table accounts by months coloured by sell through; YoY column.
- Actions: parameter to swap geography (territory, state, distributor); parameter action filters the detail panel.
- Watch: distributor feeds lag 2 to 6 weeks. Small denominators. Unmapped SKUs vanish from FIXED totals.

### D19 Distributor scorecard (2023-03-21)
- Question: who is performing, fairly weighted?
- Grain: distributor by period: distribution breadth, velocity, compliance.
- Calcs, verbatim: `( SUM([Velocity]) - WINDOW_MIN(SUM([Velocity])) ) / ( WINDOW_MAX(SUM([Velocity])) - WINDOW_MIN(SUM([Velocity])) ) * 100` (min max normalise).
- Calcs, verbatim: `[w_dist] * [Dist Score] + [w_vel] * [Vel Score] + [w_comp] * [Comp Score]`. Weights are parameters.
- Sheets: `RANK()` sorted horizontal bars with stacked weighted components; highlight action to linked trend, account list and compliance sheets.
- Watch: Goodhart's law. Segment by market type so a rural wholesaler is not ranked against a metro one. Handle null compliance feeds deliberately.

### D20 Demand forecast and what if (2023-04-04)
- Question: what happens if we run the promotion?
- Grain: one row per SKU per period (weekly depletions or shipped cases).
- Calcs, verbatim: `[Forecast] * (1 + [Promo Uplift])`.
- Build: Analytics pane forecast (exponential smoothing with level, trend and seasonality) with prediction interval shown prominently; parameters for promo uplift, price index and new distribution multiplier; base and adjusted lines side by side; best, likely and worst toggle.
- Caption: "trend + seasonality only; excludes price and promo".
- Watch: under two seasonal cycles the forecast is guessing.

### D21 Taproom sales and footfall (2023-06-04)
- Question: when are we busy, what do people buy, is staffing right?
- Grain: one row per transaction with clean timestamp.
- Measures: sales per hour, transactions per hour, average spend per head, item mix by category. Weather feed joined by date.
- Sheets: hour by day of week heatmap (day across, hour down, colour by measure); footfall against weather; basket mix (food against drink, core against specials, snack attach rate).
- Actions: filter action from a heatmap cell to basket mix. Parameter for temperature or rainfall scenario scaling expected footfall.
- Watch: show counts beside averages. Voids, comps and staff drinks corrupt POS data.

### D22 Wine DTC and varietal sales (2023-05-14)
- Question: which channel and which wine make money?
- Grain: sales line with channel, varietal, region, vintage, revenue, units, margin, club join month.
- Calcs, verbatim: `{FIXED [Varietal], [Vintage] : SUM([Revenue])}`.
- Sheets: DTC against distribution revenue and margin side by side; varietal by vintage breakdown; market map (geographic roles, size = revenue, colour = margin); club retention cohort curve by join month.
- Actions: click a varietal to reflow all views; row level security by territory.
- Watch: channel feeds are not contemporaneous. A 40 member cohort swings on a few cancellations.

### D23 Geospatial sales maps (2023-06-21)
- Question: where should we act?
- Grain: sales by account or region with geography name, volume, growth.
- Build: geographic roles; custom geocoding file for own territories; filled map for aggregate by region, density map for accounts, layered map of accounts over all licensed venues split on and off premise to show white space.
- Actions: filter action from region to a supporting bar chart.
- Watch: check the unknown locations count. Normalise by population or outlets. Standardise names in Prep ("Gtr Manchester" variants).

### D24 New product launch tracker (2023-07-21)
- Question: is it coming back, not just how many did we ship?
- Grain: sale by product by door by customer by date.
- Calcs, verbatim: `{ FIXED [Product] : MIN([First Sale Date]) }` (weeks since launch index: sale date minus this).
- Calcs, suggested: rate of sale = sold units / active doors as a table calculation along the launch week index. Distribution build = running count of distinct doors partitioned by product. First against repeat purchase flag; INCLUDE LOD to count repeat buyers at customer grain.
- Sheets: launch aligned lines (week 0 start), rate of sale per door, trial to repeat ratio. Parameter for cohort (summer against autumn, premium against core) with a parameter action.
- Watch: repeat rate needs six to eight weeks to stabilise. Separate stock metrics (distribution) from flow metrics (rate of sale).

### D25 Promotion lift (2023-07-04)
- Question: what did the promotion add beyond the baseline?
- Grain: product by week with promo flag.
- Calcs, suggested: Baseline by agreed method (trailing average of pre promo weeks, prior year same period or matched control). Incremental volume = actual minus baseline in the promo window. Incremental margin = incremental volume x unit margin.
- Sheets: baseline as a reference band under actual bars on a dual axis; running total of incremental volume; percent difference lift; portfolio view netting cannibalisation. Promo period as a parameter.
- Watch: label the baseline method on the canvas. Pull forward and cannibalisation.

### D26 Brand and marketing performance (2023-08-04)
- Question: where does the next pound of budget go?
- Grain: spend by channel by date (extract 1), sell through (extract 2), social (extract 3).
- Build: data blends on date and channel (joins only at a common grain). Funnel as calculated fields awareness, consideration, trial, repeat, shown as stage conversion rates. Channel ROI = attributed revenue / spend (suggested), with an attribution window parameter of 7, 14 or 30 days.
- Layout: revenue and contribution top, channel ROI middle, engagement as context.
- Watch: label "ROI under a 14 day window". Clean "FB" against "Facebook" in Prep.

### D27 Account churn (2023-08-21)
- Question: which accounts are slipping, against their own rhythm?
- Grain: order line by account.
- Calcs, verbatim: `{ FIXED [Account ID] : MAX([Order Date]) }` (recency = date diff to today).
- Calcs, suggested: frequency = order count over a window; monetary = trailing revenue; at risk flag = recency stretched well past the account's own normal gap between orders.
- Sheets: recency against frequency scatter (size = revenue, colour = churn score from TabPy where used); weekly call list for the high value high risk corner.
- Actions: user filters for row level security per rep.
- Watch: in a three tier market recency measures visibility, not loyalty.

## Corporate

### D28 ESG sustainability (2023-09-04)
- Question: are water, energy and carbon per hL improving and are the numbers defensible?
- Grain: meter readings by site by month, joined to a maintained emission factor table.
- Calcs, verbatim: `SUM([Gas kWh]) * [Gas Emission Factor] + SUM([Electricity kWh]) * [Grid Factor]`.
- Calcs, suggested: water ratio = total water hL / total beer hL. Energy intensity = kWh or MJ per hL.
- Sheets: each metric against annual target reference line with variance colour; Scope 1, 2 and 3 as stacked or small multiples; site comparison small multiples or ranked bar. Show absolute totals as well as intensity.
- Watch: meter boundaries differ by site. Scope 3 error bars. Footnote the factor source.

### D29 EHS safety incidents (2023-09-21)
- Question: where does risk concentrate and are leading indicators healthy?
- Grain: incident (and near miss) by area, type, shift, site, with hours worked.
- Calcs, stated: TRIR style rate = recordable incidents x 200,000 / hours worked, wrapped in a LOD for site grain under a company roll up.
- Sheets: hotspot heatmap area by incident type or shift on a sequential ramp; leading panel (near miss volume, percent corrective actions closed on time, audit completion rate); rate BANs. Parameter for site and period with parameter actions.
- Watch: a falling near miss count is a warning, not a win.

### D30 Executive KPI scorecard (2023-10-21)
- Question: are the six numbers that run the brewery on target?
- KPIs: volume, gross margin, brewhouse yield, OEE, a safety rate, an ESG intensity metric such as water to beer ratio.
- Build: BAN plus sparkline plus RAG per KPI. RAG is a calculated field comparing actual to a target reference. Parameter to switch comparison basis (target, last year, plan). `FIXED` holds the annual target steady against date filters.
- Layout: one page, no scrolling or tabs.
- Watch: Goodhart's law. Review the KPI set at least once a year.

---

# Part 2: Reusable patterns

## P1 Measure first, then chart
Every post opens by fixing the grain and the definitions before any sheet exists. Do the same: write the grain in one line (one row per batch, per cask, per account by SKU by month), list the measures with formulas, get the client to sign them off, then build. Name each component of a composite measure as its own calculated field so the total can be audited.

## P2 Ratios of sums, never averages of ratios
Used in yield (D01), sell through (D18), COGS per hL (D15), spirit yield (D14), rate of sale (D24) and TRIR (D29).
- Pattern: compute numerator and denominator as separate aggregates, then divide.
- Pin each side with FIXED when the ratio must survive a dashboard filter: `{ FIXED [Account], [SKU] : SUM([Depletion Cases]) }`.
- Suppress tiny denominators (a 95% sell through on four cases is noise).

## P3 FIXED LOD to pin a per entity anchor
The same four shapes recur. Copy them.
- First date: `{ FIXED [Cask ID] : MIN([Fill Date]) }`, `{ FIXED [Product] : MIN([First Sale Date]) }`, `{ FIXED [Lot ID] : MIN([Receipt Date]) }`.
- Last date: `{ FIXED [Account ID] : MAX([Order Date]) }`.
- Per entity aggregate: `{FIXED [Block] : AVG([Brix])}`, `{FIXED [Lot] : SUM([Volume])}`, `{ FIXED [Bay], [Height] : AVG([Temperature]) }`.
- Starting value: `{FIXED [Tank] : MIN([Brix])}`.
- Use INCLUDE when the calculation runs at a finer grain than the view (per barrel inside a lot, per customer inside a product).

## P4 OEE
OEE = Availability x Performance x Quality, each a named calculated field (D05).
- Availability = run time / planned time. Performance = actual / rated output. Quality = good / total units.
- Layout: OEE BAN with gauge, three component tiles, downtime Pareto, trend with target reference line.
- Pareto: sort descending, running total table calculation, secondary axis percent.
- Parameters for line and shift. Fix the downtime reason taxonomy before the build.

## P5 Yield family
- Brewhouse yield: actual extract / theoretical extract as a ratio of sums (D01).
- Spirit yield: LPA / tonne of cereal (D14). Energy per LPA. Hearts fraction.
- Vineyard yield: estimate from bunch counts and berry weights (D09).
- Pattern: yield by run against target, shown as a control style chart so drift is obvious.

## P6 COGS per hL and cost waterfall
- Numerator built from named components. Denominator hL. Overhead allocation basis stated on the canvas.
- Waterfall: baseline, then each driver delta, via running total table calculation, bars start where the last ended.
- What if: price parameters (malt, aluminium, energy) wired into the component fields. Linear by design, so say so.

## P7 Control charts and bands
- Baseline mean and sd from a fixed window. UCL and LCL at 3 sd, warning at 2 sd. Flag calculated field, red colour on breach (D02).
- The same band idea carries to fermentation corridors (D03, D04), yield against target (D14) and panellist drift (D08).
- Reference band, not just reference line, so the corridor reads at a glance.

## P8 Year on year and period compare
- Table calculation along the month axis: `(ZN(SUM([Depletions])) - LOOKUP(ZN(SUM([Depletions])), -12)) / ABS(LOOKUP(ZN(SUM([Depletions])), -12))`.
- A parameter to switch the comparison basis (target, last year, plan) as in D30.
- Show count or volume beside any percent change.

## P9 What if parameters
- Promo uplift and price index: `[Forecast] * (1 + [Promo Uplift])` (D20).
- Input price scenarios: malt, aluminium, energy (D15); commodity price per commodity (D16).
- Blend proportions: one parameter per lot or cask (D06, D07).
- Target age and loss rate (D11, D13). Attribution window 7, 14 or 30 days (D26). Score weights (D19).
- Rule: label every what if as an assumption on the canvas. A slider is not a model.

## P10 Metric switch
One parameter plus a CASE calculated field plus a parameter action swaps the measure on one sheet (D01). Also used to swap geography (D18), QC variable (D02) and product or session (D08).

## P11 Small multiples against a target band
Tanks (D03, D04), sites (D28), per still or per lot comparisons. One mini chart per entity, shared axis, band drawn as a reference band, attention colour when outside it.

## P12 Heatmaps for position and time
Hour by weekday (D21), bay by row by height (D12), area by incident type (D29), SKU by age band (D17), account by month (D18). Sequential ramp; click filters to the detail behind the cell.

## P13 Normalise before you compare
Per hL for sites and plants (D28). Min max to 0 to 100 before weighting (D19). Per population or per outlet for maps (D23). Per door for launches (D24). Per 200,000 hours for safety (D29).

## P14 RAG, BAN and sparkline tiles
BAN for the current value, sparkline for trend, RAG calculated field against target (D30). One page only. Amber must mean amber.

## P15 Actions
- Filter action from a mark to detail (tank, barrel lot, region, day, cell).
- Highlight action to tie linked sheets to one entity (D19, D12).
- Parameter action to make a click change a parameter (metric, geography, cohort).
- Row level security via user filters for reps, regions and warehouses (D13, D22, D27).

## P16 Data prep and refresh
- Tableau Prep to standardise names (blocks, tanks, channels, regions), pivot sensor feeds, reshape panel scores to long format.
- Live connection for fast moving sensor data; scheduled .hyper extract for weekly or daily drops.
- Join only at a common grain. Blend on date and channel when grains differ.
- Map SKUs and accounts to a master list or rows vanish from FIXED totals.

## P17 Honest caption rules
Every post's "Where it breaks" turns into a one line caption on the dashboard:
- Forecast: "trend + seasonality only; excludes price and promo".
- Attribution: "ROI under a 14 day window".
- Yield or cost: state the cost allocation or loss definition used.
- Sensory and blending: the dashboard shortlists, the palate decides.
- Maps and rates: state the denominator.
- Safety: read a drop in near misses as a warning.

## P18 Build order for a new beverage dashboard
1. Write the question and the grain.
2. List measures with formulas and get sign off.
3. Build the anchor sheet (trend or heatmap) and the breakdown sheet.
4. Add parameters for targets and what if inputs.
5. Add actions (filter, highlight, parameter).
6. Add the caption rules from P17.
7. Lay out: filter strip, three KPI tiles, trend and breakdown.

## P19 Typical field dictionary by domain

Use these names when scripting a synthetic data set so the formulas above run unchanged.
- Brewing batch: [Batch ID], [Style], [Fermenter], [Extract Recovered], [Theoretical Extract], [Volume HL], [Date].
- Fermentation reading: [Tank], [Recipe], [Timestamp], [Gravity], [Temperature], [Brix], [YAN].
- Packaging run: [Line], [Shift], [Planned Minutes], [Run Minutes], [Units Good], [Units Total], [Downtime Reason], [Minutes Lost].
- Cask: [Cask ID], [Fill Date], [Cask Type], [LPA Fill], [LPA Now], [Strength], [Warehouse], [Bay], [Row], [Height].
- Sales: [Account ID], [Account], [SKU], [Channel], [Distributor], [Depletion Cases], [Shipment Cases], [Opening Inv], [Revenue], [Order Date].
- Cost: [Ingredient Cost], [Packaging Cost], [Energy Cost], [Labour Cost], [Overhead Cost].
- Sustainability and safety: [Gas kWh], [Electricity kWh], [Water HL], [Recordables], [Hours Worked], [Near Misses].
- Keep captions human (Volume (HL)) and field names with underscores when the source is a CSV, as the BREWERY_OPS workbook does.
