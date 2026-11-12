# Dashboard design reference

Rules for designing and laying out a Tableau dashboard. Numbers and settings come from the Tableau Field Notes articles (dashboard design system, accessible dashboards, one KPI one definition, first dashboard, performance recorder, Tableau Agent and Explain Data, first Pulse metric). Items that were marked "general practice" are now checked against help.tableau.com (pages named per section, 12 Nov 2026). Design advice such as BAN card layout remains practice, not Tableau documentation.

Version context: notes written as of October 2026. Custom palette dialog needs Desktop 2025.3 or later. Pulse is Tableau Cloud only. Tableau Agent in Desktop needs 2025.1 or later plus a qualifying Cloud site.

## 1. Layout

### Size
- Use **Fixed size**. In Dashboard pane > **Size** pick a preset or **Custom**.
- Desktop default for a template: **1200 by 800 pixels**.
- Why fixed: Automatic stretches to the reader's window, so the layout reflows on a laptop and leaves gaps on a wide monitor. Fixed also lets the server cache views, so it is faster.
- **Range** sits between Fixed and Automatic (minimum and maximum). Use it only with a reason.
- Automatic size is a Workbook Optimizer flag ("Dashboard size not fixed"). Each screen size renders and caches separately.
- Fixed size on a phone is cramped. Add a phone layout from **Device Preview** (top of the Dashboard pane). Do not shrink the desktop layout.
- Name the tab for the audience, for example `Store manager view`.
- If the dashboard goes on a wall screen (a brewhouse screen, a control room), set the fixed size to that screen.

### Tiled versus floating
- **Tiled** objects snap into a grid and never overlap. Default to tiled for everything.
- **Floating** objects sit on top at a fixed position. They ignore containers and overlap at smaller sizes.
- Holding Shift while dragging makes an object float by accident. Check the **Floating** list in the **Layout** tab Item hierarchy.
- Use floating only for deliberate overlays (a logo, a legend on a map).

### Containers
- A **layout container** is an invisible box. **Horizontal** arranges items side by side. **Vertical** stacks them.
- Start by dragging a **Vertical** container from Objects onto the empty canvas. It fills the space. Put the title and sheets inside it.
- Select the container itself: select a sheet, open its **More Options** arrow in the top corner, choose **Select Layout Container**.
- Same arrow > **Distribute Evenly** shares height (or width) equally between children.
- The **Layout** tab beside **Dashboard** shows the **Item hierarchy** tree: dashboard, tiled area, containers, objects. Use it whenever a drop lands in the wrong place.
- Filter cards and legends are added at the right edge by default. Drag them under the title or delete them if an action does the job.

### Grid and padding (template values)
- 8 pixel grid. Turn on **Dashboard > Show Grid** and set the size in the grid options (label may read **Grid Options**).
- Padding: **16 pixels outside** containers and **8 pixels inside**. Rhythm comes from these two numbers.
- Header container **64 pixels high**: title left, data freshness date right.
- Filter row under the header, always in the same order: **date, region, store**.
- KPI row of **three to five numbers**, then the main chart, then supporting views.
- Footer text object: data source, definition of each KPI and a contact. Also carry the template version.
- Add objects in reading order (title, summary text, filters, main chart, supporting chart). Screen readers follow the order objects were added.

### How many sheets
- Every sheet is a query. Two or three charts load fast. Twelve do not. Split a crowded dashboard into two.
- Check each chart form against a chart chooser before adding a third sheet.
- The slow example in the notes had six worksheets, eight quick filters and a detail table on a live connection.

### Reading order of the page
Design practice: title or finding, KPI row, main chart, supporting views, detail on demand, footer.
- Titles state the finding, not the field name.
- Keep the page to one screen at the fixed size. Push detail to a second dashboard reached by an action or button.

## 2. KPI and BAN cards

From the notes: a KPI row of three to five numbers sits under the header and filter row, above the main chart. Design practice for the cards themselves (layout advice, not documented by Tableau; the container and object behaviour is verified against https://help.tableau.com/current/pro/desktop/en-us/dashboards_create.htm, 12 Nov 2026):
- One big number (BAN, "big alone number"), a short label, a comparison (prior period or target) and a direction cue.
- Each card is its own small worksheet in a horizontal container, so the row distributes evenly.
- Put the cards in a Horizontal or Vertical layout container, not the top-level tiled area. A hidden tiled object leaves blank space at top level, but siblings in a layout container fill the gap.
- Make a card a link: add a Navigation object over or beside it (see section 5), or a Go to Sheet action from the card sheet.
- Use the neutral colour for the comparison and the primary colour for the actual.
- Direction needs more than colour: add an arrow shape or a word ("Above target", "Below target").
- Every KPI uses the certified field. No card restates the formula in its own calculated field.
- Every KPI links to its definition (footer text or a link in the card tooltip).
- Give each card a text title and caption sentence so a screen reader has something to read. A number alone in a mark label is not enough.
- Label the period on the card ("Q3 2026"). Say whether it is a steady-state or partial figure.
- Do not show a ratio over a partial or loss period without saying so.

## 3. Colour and fonts

### Palette (all pass WCAG 2.2 contrast on white)
| Token | Hex | Ratio on white | Use |
|---|---|---|---|
| Primary | #1F4E79 | 8.66 | The measure that matters, actual |
| Accent | #B35C00 | 4.72 | Highlight, selected, the one thing to look at |
| Category 3 | #0F6E6E | 6.04 | Third series |
| Category 4 | #6A3D9A | 7.64 | Fourth series |
| Category 5 | #8C564B | 5.92 | Fifth series |
| Neutral | #5A5A5A | 6.90 | Everything else, comparison, prior period |
| Text | #333333 | 12.63 | Titles, labels |
| Text secondary | #767676 | 4.54 | Axis labels, captions |

- Categorical colours pass 3 to 1 non-text contrast against white. Text colours pass 4.5 to 1.
- **Five categorical colours is a ceiling.** A sixth series means group, filter or use small multiples.
- Rule: primary for actual, neutral for comparison, accent for one thing only.
- Sequential palette: #D9E2EC to #1F4E79. The light end is only 1.31 to 1 on white. Label low values or add a mark border.
- Off-white backgrounds lower every ratio. On #F7F7F5 the Tableau 10 blue falls from 4.55 to 4.24 and fails for small text. Prefer white or recheck every colour.
- Colour means the same thing across every dashboard in the estate (actual is always the primary colour).
- Pick colours for meaning first, then check contrast. Avoid eight subtle blues.

### Installing a palette
- Desktop 2025.3 and later: **Edit Colors** dialog > **Create Custom Palette** at the end of the palette list.
- Desktop 2025.2 and earlier: add to `Preferences.tps` in **My Tableau Repository**, then restart Desktop.

```xml
<?xml version='1.0'?>
<workbook>
  <preferences>
    <color-palette name="Harbour Goods categorical" type="regular">
      <color>#1F4E79</color>
      <color>#B35C00</color>
      <color>#0F6E6E</color>
      <color>#6A3D9A</color>
      <color>#8C564B</color>
    </color-palette>
    <color-palette name="Harbour Goods sequential" type="ordered-sequential">
      <color>#D9E2EC</color>
      <color>#1F4E79</color>
    </color-palette>
  </preferences>
</workbook>
```
- `type` values: `regular`, `ordered-sequential`, `ordered-diverging`.
- Ship the file to every author machine with the IT software settings tool. A palette on one laptop is a preference, not a system.

### Colours that fail (Tableau 10 defaults on white)
| Colour | Ratio on white | Verdict |
|---|---|---|
| #4E79A7 blue | 4.55 | Passes text and bars |
| #F28E2B orange | 2.42 | Fails both |
| #E15759 red | 3.68 | Bars only |
| #59A14F green | 3.16 | Bars only |
| #EDC948 yellow | 1.61 | Fails both |
| #999999 grey | 2.85 | Fails text |

Replace grey axis text with #767676 (4.54).

### Type scale
Set once in **Format > Workbook**. Workbook-level changes overwrite worksheet-level changes (wanted for a system, surprising in an old workbook).
| Role | Size | Weight |
|---|---|---|
| Dashboard title | 18 pt | Bold |
| Worksheet title | 12 pt | Bold |
| Body, labels, tooltips | 10 pt | Regular |
| Captions, axis | 9 pt | Regular, #767676 |

- One font family only. Pick one that audience machines and the server both have. A font missing on the server falls back silently, so check a published view, not Desktop.
- Four sizes are enough. The audit in the notes found 9 sizes and 31 colours in a messy estate, 4 and 9 after a quarter on the system.

## 4. Dashboard actions

Open with **Dashboard > Actions > Add Action**. Types: Filter, Highlight, Go to URL, Go to Sheet, Change Parameter, Change Set Values. Verified against help.tableau.com action pages (https://help.tableau.com/current/pro/desktop/en-us/actions_dashboards.htm, actions_highlight_advanced.htm, actions_parameters.htm, actions_sets.htm), 12 Nov 2026. From a worksheet the same dialog is **Worksheet > Actions**.

| Action | Use when | Notes |
|---|---|---|
| **Filter** | Selecting a mark on an overview should restrict other sheets (store bar filters the monthly line) | Tick only the sheets that should respond |
| **Highlight** | Keep all marks visible but draw the eye to related ones | Good for small multiples; no filtering cost. Hover suits it. Match on All Fields, Dates and Times (one date field per sheet) or Selected Fields |
| **Go to URL** | Link to a definition page, a ticket, an external record | URL must start with http:// or https://. Insert field values such as `<Country>`. URL Target can be a Web Page object on the dashboard |
| **Go to Sheet** | Drill from summary to a detail sheet or another dashboard | Run on Select or Menu (Tableau names them the best choices for navigation). Select can be limited to single select |
| **Change Parameter** | Selection drives a parameter (a calculation reads it) | Parameter must be used in the view. Pick Target Parameter and Source Field. Choose an Aggregation for multi mark selections |
| **Change Set Values** | Selection builds a set used for in/out comparison | Set must be used in the view. Not usable in Stories |

### Building the filter action (steps from the notes)
1. **Dashboard > Actions > Add Action > Filter**.
2. Name it for the flow, for example `Store to month`.
3. **Source Sheets**: tick only the sheet that is clicked (`Sales by store`).
4. Run action on **Select**. Tick **Single-select only** for one item at a time.
5. **Target Sheets**: tick only the sheets that should respond (`Sales by month`).
6. When the selection is cleared: **Show all values**.
7. Leave **All Fields** on. **OK**, then **OK** again.
- Shortcut: select the sheet on the dashboard, **More Options** arrow > **Use as Filter**. It makes an action with "generated" in the name. Build by hand once to learn what it hides.
- Test: select a bar, the target redraws. Select the same bar again (or empty space), the target returns to all. Check in **Presentation Mode** (F7 on Windows).

### Trigger and clear settings for the other types
- **Run action on**: Hover (pointer rests on a mark), Select (click, works for every type) or Menu (right-click, Control-click on Mac, a selected mark, then the menu entry). Hover and Menu also add an entry to the tooltip.
- **Highlight**: Dashboard > Actions > Add Action > Highlight > name > source sheets > run on > target sheets > Target Highlighting: **All Fields**, **Dates and Times** or **Selected Fields** > OK twice.
- **Change Parameter**: Add Action > Change Parameter > name > source > run on > Target Parameter and Source Field (set Aggregation for several marks) > when the selection is cleared choose **Keep current value** or **Set value to** a chosen value. With Aggregation None and different values across marks the action does not run.
- **Change Set Values**: Add Action > Change Set Values > name > source > run on > Target Set (data source, then set) > on run choose **Assign values to set**, **Add values to set** or **Remove values from set** > when cleared choose **Keep set values**, **Add all values to set** or **Remove all values from set**.
- **Go to URL**: Add Action > Go to URL > name > Source Sheets > run on > URL (http:// or https://) > URL Target **Web Page Object** or the browser.
- **Filter shortcut**: on the view's shortcut menu choose **Use as Filter**. On a secondary sheet that must not react, choose **Ignore Actions**.
- Rename Web Page objects when a dashboard has several, so each action targets the right one.

### Action failure modes
- Every sheet ticked as target: selecting a bar filters the bar chart itself and the other bars vanish.
- **Leave the filter** on clear: the line stays filtered after deselect and readers think data is missing. Use **Show all values**.
- Hover or select actions are not accessible. Nothing a reader needs may exist only behind an action.
- Put detail on a separate sheet reached by an action instead of on the main view (this also fixes slow marks).

## 5. Navigation

Navigation object steps verified against https://help.tableau.com/current/pro/desktop/en-us/dashboards_create.htm, 12 Nov 2026. Layout advice stays practice, with notes constraints:
- Build navigation with the **Navigation** object (buttons to other dashboards) or **Go to Sheet** actions. Avoid long scrolling pages.
- Navigation object: in the Dashboard pane, Objects section, drag **Navigation** onto the dashboard. Open the object's pop-up menu in its upper corner > **Edit Button**. Pick the sheet in **Navigate to** (it must be outside the current dashboard). Set **Button Style** to image or text. Optional **Tooltip** text.
- While authoring, Alt-click (Windows) or Option-click (Mac) the button to follow it. In a published dashboard one click works.
- The **Download** object works the same way with an **Export to** format menu.
- Tableau documents alt text for Image objects only. For a button, rely on the visible text style and the tooltip. Test with a screen reader.
- Keep the header container the same on every dashboard (title left, freshness date right) so a manager moving from the South dashboard to the West one does not relearn it.
- Keep filters in the same order everywhere: date, region, store.
- Custom navigation buttons or images must have a pointer target of **at least 24 by 24 CSS pixels** (WCAG 2.2 criterion 2.5.8) or enough spacing.
- Give image objects alt text (Tableau lists it for Image objects) and prefer text style buttons.
- On the published page: hide the **Custom Views**, **Subscriptions** and **Alerts** toolbar buttons and turn off Web Edit for audiences that need accessibility conformance.
- Skip to Content jumps past the Tableau toolbar. Test tab order on the published view.
- The embed page is part of the dashboard. A conformant view inside an inaccessible page still fails.

## 6. Tooltips and viz in tooltip

The notes give one hard rule: **tooltips are not accessible**, so values must also appear as mark labels or text. Viz in Tooltip details verified against https://help.tableau.com/current/pro/desktop/en-us/viz_in_tooltip.htm, 12 Nov 2026. The rest is practice:
- Tooltips add depth. They never carry the only copy of a value.
- Keep the tooltip to what a reader needs: name, value, comparison, one line of context.
- **Viz in Tooltip** embeds a sheet in the tooltip. Steps: build the tooltip sheet on its own worksheet with a clear name (for example "Tooltip: Profit by Sub-Category"). On the source sheet click **Tooltip** on the Marks card, then **Insert > Sheets** and pick it. Tableau writes the markup. Optionally right-click the tooltip sheet tab and **Hide** it, then **Unhide All Sheets** from the source tab later.
- Filtering: the default is `filter="<All Fields>"`, which matches every dimension in the source view at its most detailed level (the Filters shelf is ignored). To limit it, edit the filter value in the Tooltip editor and list fields separated by commas. Date fields need the date level, for example `<MONTH(Order Date)>`.
- Size: `maxwidth` and `maxheight` in the markup, default 300 by 300 pixels. Needing over 600 means the tooltip sheet is too big.
- Limits: worksheets only (not dashboards or stories). The embed is a static image. It cannot nest another Viz in Tooltip. Not available for totals and grand totals from 2023.3. One tooltip sheet serves one source sheet at a time. Show Me can reset tooltip edits. Selected Fields filtering does not work across data sources.
- Keep embedded sheets small and few. Each one is another query per hover.
- Set tooltips to 10 pt body text per the type scale.
- Turn off tooltips on marks that have none to show.
- Leave **View Data** on. It gives screen reader users a table of underlying values.

## 6b. Dynamic zone visibility and show/hide containers

Verified against https://help.tableau.com/current/pro/desktop/en-us/dynamic_zone_visibility.htm and https://help.tableau.com/current/pro/desktop/en-us/dashboards_create.htm, 12 Nov 2026.

### Dynamic zone visibility (show or hide a zone from data)
- Layout tab of the selected zone > tick **Control visibility using value** > pick the field or parameter.
- The field or parameter must be Boolean, return a single value and not depend on the viz structure (a fixed LOD fits). If it is not listed, one of those fails.
- Worked pattern (reveal a detail chart after a mark click): create a Boolean parameter. Create a calculation that returns `True` and put it on Detail on the source sheet. Add a Change Parameter action from that sheet to the parameter with the calculation as Source Field. Set the clear behaviour to **Set value to** False. Select the zone to reveal, open Layout and tick Control visibility using value with that parameter. The source zone can also use **Use as Filter**.
- Does not work for sheets used in Stories.
- Put the controlled zones in a layout container so neighbours resize into the gap.

### Show/Hide button (user toggles a zone)
1. Select the object (a container works best). Open its pop-up menu in the upper corner > **Add Show/Hide Button**.
2. Open the button menu > **Edit Button**.
3. **Dashboard Item to Show/Hide**: the target. An object can be the target of only one button, so choose None where another button already owns it.
4. **Button Style**: image or text. **Button Appearance**: set **Item Shown** and **Item Hidden** separately. Add tooltip text.
5. Authoring: Alt-click (Windows) or Option-click (Mac) the button to toggle.
- Floating objects reveal whatever is underneath when hidden. Tiled objects at top level leave blank space. Inside a Horizontal or Vertical layout container the others fill the space.
- Typical uses: a filter panel that slides away, a definitions drawer, a detail table off the main page.
- Hidden content is still on the page for the server to load, so it does not replace moving heavy detail to another dashboard.
- Accessibility: make the button text say what it toggles. Check tab order on the published view.

## 7. Accessibility (WCAG 2.2 AA)

Tableau says dashboards can be built to conform. Conformance is a result of choices, not a default.

### Contrast
- **1.4.3 Contrast (Minimum)**: **4.5 to 1** normal text, **3 to 1** large text.
- **1.4.11 Non-text Contrast**: **3 to 1** for bars, lines and other graphical objects against neighbouring colours.
- Measure the hex codes with a contrast checker (WCAG relative luminance formula). Do not eyeball.
- Axis text: use #767676 (4.54), never #999999 (2.85).

### Colour and colour blindness
- **1.4.1 Use of Color**: colour cannot be the only signal. Red and green status columns fail outright.
- Replace red and green with a text label ("Above target", "Below target") or a shape plus label. Colour may stay as a second signal.
- Check every legend: is there a label, shape or position that carries the same meaning?
- Start from Tableau's colour-blind palette. Pick colours that differ in lightness, not only hue.
- Test every palette with a colour vision deficiency simulator before shipping.
- Red-green colour vision deficiency affects roughly one man in twelve.

### Marks
- Keep each sheet **under 1,000 marks**. Mark count is in the Desktop status bar.
- Views over 1,000 marks are rendered on the server. Server-rendered views are not supported for WCAG conformance.
- Replace row-level detail tables with a summary (store by category). Put detail on its own sheet under 1,000 marks with a filter.

### Keyboard and focus
- Tab and Shift+Tab move between components. Enter or Space activates.
- **2.1.1 Keyboard**, **2.4.3 Focus Order**, **2.4.7 Focus Visible** apply.
- **2.4.11 Focus Not Obscured (Minimum)** (new in 2.2): a focused control must not hide behind a sticky banner on the embed page.
- Publish to Server or Cloud, then use the view with the keyboard only. Note every control you cannot reach and every place focus disappears.
- **2.5.8 Target Size (Minimum)**: pointer targets at least **24 by 24 CSS pixels** or enough spacing.

### Filters
- Supported for conformance: **single-value** and **multiple-value** filters, as a list or drop-down.
- A **range slider is not supported**. Swap a date slider for a single-value drop-down of months.

### Text, alt text and reading order
- Every view gets a title that says what it shows and a caption stating the finding in a sentence.
- Rename legend and filter headings to say what they control ("Colour key for product category"), not the field name.
- Plain words. No all capitals. No "image of" at the start of an alt text.
- Recent versions generate alt text per view and let you edit it. Read it and add context a reader needs.
- Add mark labels so values sit on the bars, not only in tooltips.
- Reading order follows the order objects were added. Rebuild adding them in reading order. Editing the dashboard XML is the only alternative and is not worth the risk on a shared workbook.
- Listen with NVDA, JAWS or VoiceOver and write the order down.

### Where accessibility stops
- Interactivity inside a view (selecting marks, reading tooltips) is not accessible. A story that depends on hover cannot conform.
- Conformant views do not support web editing. Give editors a separate route.
- Tableau's guidance names Server and Cloud. Do not promise WCAG conformance for a Tableau Public embed.
- Dense charts (every order, every postcode) cross 1,000 marks. Aggregate first.
- Keep evidence with the workbook: the before and after table, the palette hex codes and the screen reader reading order.

## 8. KPI definition discipline

Define each KPI once, as close to the data as possible. Everything else reads it.
- Put the calculation in one **certified published data source**. Workbooks connect to it and never write their own formula.
- Build the **Pulse metric definition** on the same source and the same field.
- One named person signs off any change.

### Where the definition lives
| Option | Single source of truth | Works in Pulse | Fails when |
|---|---|---|---|
| Calculated field in each workbook | No | Only if rebuilt in the source | The second workbook is built |
| Calculated field in a certified published data source | Yes, within Tableau | Yes | Someone connects to the raw file |
| Column in a database view or table | Yes, every tool | Yes, via published source | The view is bypassed |
| External semantic layer (Tableau Next semantic models, warehouse metrics layer) | Yes, across tools | Check per product | The organisation cannot own it |

Default: row 2, with the most important KPIs pushed down to row 3 over time.

### Rules
- **One name, one formula.** "Sales" alone is banned. Net Sales and Gross Sales are two KPIs with two names.
- **Clean once.** Duplicates, negative quantities and unknown stores are excluded upstream, not with a filter in each workbook.
- **Describe in the field.** Description holds formula in words, grain, exclusions and owner. It shows in the Data pane and the Metadata API exposes it.
- **Certify the source.** Catalog (where licensed) adds data quality warnings and lineage.
- Label past reported figures with the definition they used. Version every change with a date.
- Dashboard footers link to the definitions page.

### Why it matters (worked example)
Three "Q3 sales" numbers for the same quarter, all correct for their own definition:
| Called "Q3 sales" in | What it is | Value |
|---|---|---|
| Finance workbook | Quantity times unit price, before discount | 159,897.00 |
| Regional dashboard | After discount, cleaned orders | 153,065.80 |
| Spreadsheet export | After discount, raw file with bad rows | 156,269.85 |
Gap one: 6,831.20 of discount. Gap two: bad rows.

### Detect drift (Metadata API, Cloud or Server)
```graphql
query NetSalesEverywhere {
  calculatedFields(filter: { name: "Net Sales" }) {
    name
    formula
    datasource { name }
    downstreamWorkbooks { name projectName }
  }
}
```
Any result whose data source is not the certified one, or whose formula differs, is drift. Run it monthly and send the list to the KPI owner. Check field names against the Metadata API reference for your version first.

### Questions to ask before building
1. Which ten numbers appear in board or leadership packs? Those are the KPIs.
2. Who decides the definition when two teams disagree? A name, not a department.
3. Before or after discounts, returns, tax and cancellations?
4. At what grain is it true (order, day, store, month)? Can it be summed across stores or only recomputed?
5. Where do bad rows go today?
6. Which other tools show the number? Which wins when they disagree?
7. How is a definition change announced? What happens to last quarter's figure?

### Anti-patterns
- The heroic workbook everyone copies.
- Same name, different formula.
- Fixing data in the view (a filter in one workbook only).
- Pulse on a side copy or a speed extract.
- Multi-fact sources in Pulse without testing (Pulse may not work on multi-fact relationship sources).
- Definition by meeting, never written into the field description.

## 9. Performance checklist

Do not guess. Record first, fix the biggest bar, record again.

### Performance recorder
Desktop:
1. Open the workbook. Close other workbooks.
2. **Help > Settings and Performance > Start Performance Recording**.
3. Do what a slow user does: open the dashboard, change two filters, select a mark.
4. **Help > Settings and Performance > Stop Performance Recording**.

A workbook opens with the **Performance Summary** dashboard: **Timeline** (events in order), **Events** (sorted by duration) and **Query** (SQL of the selected event).

Event types: **Executing query**, **Compiling query**, **Computing layouts**, **Connecting to data source**, **Generating extract**, **Geocoding**, **Blending data**. On Server also **Server rendering**.

Server: an administrator enables **Record workbook performance metrics** in site **Settings**. Add `:record_performance=yes&` to the view URL just before `:iid=`, refresh and use the view. Server timings include rendering and network. Record where the users are.

### Workbook Optimizer
**Server > Run Optimizer**. Sorts into **Take action**, **Needs review**, **Passed**. Useful flags: **Number of filters**, **Filter uses "Only Relevant Values"**, **Number of views in a dashboard**, **Live data connections**, **Number of LOD calculations**, **Uses data blending**, **Dashboard size not fixed**. Optimizer reads the design. The recorder measures it. Use both. A live connection can be right: mark the flag ignored with a reason.

### Read the recording (sort Events by elapsed time)
1. Top bar is a query? Read the SQL. Look for a query returning every order row, a filter on a string calculation or a long LOD subquery chain.
2. Many small queries in a row? Eight quick filters on **Only Relevant Values** each fire a query when another changes. Twenty fast queries can cost more than one slow one.
3. Top bar is **Computing layouts**? That is marks. A detail table or a map with thousands of points spends its time drawing.

### Fixes in priority order (largest bar first)
1. **Show fewer marks.** Summary by store and category. Detail on a separate sheet reached by an action. Under 1,000 marks.
2. **Tame the filters.** **Only Relevant Values** to **All Values in Database** where users cope. Cut eight filters to the three people use. Filter on the raw field, not a calculated string.
3. **Move work out of the query.** Row-level string and date calculations go into the source or a Tableau Prep flow. Materialise them in an extract.
4. **Extract the live connection.** If minute freshness is not needed, publish an extract on a schedule. Use **Aggregate data for visible dimensions** when order-level rows are never needed. Add extract filters for history nobody reads.
5. **Simplify LODs.** A FIXED expression at order grain rebuilt on every filter change is a hidden cost. Compute upstream if the grain is fixed.
6. **Fix the dashboard size.** Fixed size lets the server reuse cached views.
7. **Use context filters carefully.** A context filter that cuts data hard and rarely changes can speed up Top N or FIXED. One that changes on every click slows things because the context rebuilds.

### Prove it
Record again with identical steps. Compare total time and the top three events. Keep both recordings in the workbook change log. Illustrative shape of a good result:
| Event | Before | After | Change |
|---|---|---|---|
| Executing query, detail table | 9.8 s | 0.6 s | Summary, detail on demand |
| Executing query, quick filters (8) | 6.1 s | 0.9 s | Three filters, All Values in Database |
| Computing layouts | 3.4 s | 0.5 s | About 40,000 marks down to under 200 |
| Total to first view | 21.0 s | 2.6 s | Extract with aggregated data |
Those numbers are illustrative, not measured.

### Traps
- Desktop is not Server. Record where the users are.
- The first run is cold. Record cold and warm and label each.
- If **Executing query** still dominates after trimming, the fix is an index, a summary table or another source. Take the SQL to the database team.
- Change one thing at a time. Five changes and one recording cannot show which fix worked.
- Brewery pattern: forty thousand sensor points per tank crawl. Aggregate to the hour for the overview and keep minute data for the selected tank.

## 10. Pulse metrics and Explain Data in a dashboard

### Pulse (Tableau Cloud only)
- A **metric definition** holds one measure, one aggregation, one time dimension and the filters people may change. People follow metrics, not definitions.
- Pulse reads one published data source. Use an extract or a database connection. A live file connection publishes but never refreshes.
- Pulse is off by default. An administrator turns it on: **Settings > Tableau Pulse > Deployment > Turn on Tableau Pulse**. AI summaries are a separate switch: **Settings > General > AI in Tableau > Tableau Pulse: Summarizes key metric insights**. The summary needs two or more followed metrics.
- Site role to create a definition: Creator, Site Administrator Explorer or Explorer (can publish). Viewers can follow only.
- Definition steps: **Tableau Pulse > New Metric Definition**, choose the source, **Connect**, then:
  - Name and description (formula in words, exclusions).
  - **Measure** and **Aggregation** (Sum).
  - **Temporality**: Over time. **Time dimension**: Order Date.
  - **Adjustable metric filters**: at least one. These become the dimensions Pulse analyses, so pick the ones a manager would ask about.
  - **Insights** tab: set **Value going up is** to favourable or unfavourable correctly.
  - **Save Definition**.
- Use the **Certified definition** toggle on the one you stand behind (needs Create Metric Definitions permission on the data source).
- Time range: Pulse uses today's date. Data that stops in September shows nothing for "month to date" in October. Set the range to the last full quarter.
- Calendar mismatch: Pulse uses calendar periods unless a custom calendar is set. A finance close on other dates will not match.
- Check the first number against Desktop on the same file before trusting it. Example check, Q3 2026 all stores 153,065.80 against Q2 227,738.10 (-32.8%).
- Where it fits a dashboard: Pulse holds one number steady with a digest (email or Slack). A dashboard holds the diagnosis. Use the KPI row for the headline and link to the Pulse metric for the follow.
- Pulse only explains movement across the dimensions you listed as adjustable filters.

### Tableau Agent
- Turns a sentence into a view or calculation. Generative: it guesses date level, aggregation and what "top" means. It does not ask clarifying questions.
- State date range, aggregation and sort measure every time. Write down the expected number before you read the bars.
- Creating a calculation and using it in a view are two separate requests.
- It does not do: joins or relationships, data type or role changes, groups, sets or parameters, reference lines, dashboard building, filter controls or actions, cubes. With a blend it uses the primary source only.
- Check the Filters shelf, not just the bars. Use **Recreate** to step back, **Retry with Tableau Agent** for a fresh attempt.
- Keep SUM() out of the inside of a row-level formula (multiplying three sums is not the sum of products).
- Tableau Agent in dashboards is beta (from 2026.1, Cloud only). Do not design a process around a beta.
- Cloud: prompts go through the Einstein Trust Layer. Server: you connect your own LLM provider and own PII masking.

### Explain Data
- Statistical models around one mark. It proposes what might sit behind a value. It cannot identify causes.
- Open with the **Data Guide** icon in the toolbar or the tooltip menu (lightbulb in Tableau Public).
- Needs the measure aggregated with SUM, AVG, COUNT, COUNTD or an AGG calculation, a single primary data source, no blends and no cubes.
- On small numbers (a few dozen records per mark) treat every explanation as coincidence. Example: Pune fell 68,235.25 to 29,266.75 on 16 and 11 orders. Every explanation was true and none was a cause.
- Treat each explanation as a question for the owner, not an answer for the board.
- Needs **Run Explain Data** capability on the workbook. An administrator can turn it off for the site.
- Fit in a dashboard: a drill-down aid for authors and analysts. Do not put it on the page as the explanation of record.

## 11. Pre-handover checklist

Layout
- [ ] Fixed size set (1200 by 800 for desktop) and a phone layout added in Device Preview if phones matter.
- [ ] Everything tiled. Floating list in the Item hierarchy contains only deliberate overlays.
- [ ] 8 pixel grid, 16 outer and 8 inner padding, 64 pixel header.
- [ ] Filters in order date, region, store. KPI row of three to five numbers.
- [ ] Footer with data source, KPI definitions, contact and template version.
- [ ] Objects added in reading order.

Colour and type
- [ ] Palette from the system. Maximum five categorical colours. Primary for actual, neutral for comparison, accent for one thing.
- [ ] Text and axis colours pass 4.5 to 1. Bars pass 3 to 1. Axis text is #767676 or darker.
- [ ] Four type sizes (18, 12, 10, 9 pt) set in Format > Workbook. One font family that exists on the server.

Actions and navigation
- [ ] Each filter action has one source and only the intended targets. Clear behaviour is Show all values.
- [ ] Nothing needed exists only behind hover or select.
- [ ] Navigation buttons are at least 24 by 24 CSS pixels and have text alternatives.
- [ ] Tested in Presentation Mode and on the published view.

Accessibility
- [ ] No status by colour alone. Text label or shape present.
- [ ] Every sheet under 1,000 marks. Values labelled on marks.
- [ ] Every view has a title and a caption stating the finding. Legend and filter headings renamed.
- [ ] Alt text read and edited. View Data left on.
- [ ] No range slider. Single or multiple value filters only.
- [ ] Keyboard-only pass on the published view. Reading order heard with a screen reader.
- [ ] Web Edit off and Custom Views, Subscriptions and Alerts buttons hidden for the audience.

KPIs
- [ ] Every KPI has one name, one formula and one owner on record.
- [ ] Defined in a certified published data source. Field description holds formula, grain, exclusions and owner.
- [ ] Pulse definition (if used) is on the same source and field, with favourable direction set correctly.
- [ ] Headline number checked against an independent build from the same data.
- [ ] Footer links to the definitions page.

Performance
- [ ] Performance recording taken before and after. Both kept in the change log.
- [ ] Workbook Optimizer run. Every flag fixed or ignored with a reason.
- [ ] Few filters, All Values in Database where possible. Extract or aggregated data where freshness allows.
- [ ] Two or three charts per dashboard where possible. Detail on a separate sheet.
- [ ] Checked cold and warm on the server where users are.

Release
- [ ] Published view opened on the target screen. Fonts render as designed.
- [ ] Evidence stored with the workbook: contrast table, palette hex codes, reading order, recordings.
