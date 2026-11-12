# Tableau calcs and viz reference

Mid-build reference for calculated fields, LODs, table calcs, filters, dates, parameters, sets, maps and chart recipes. Formulas are verbatim from the field notes (Harbour Goods retail sample). Field names in [square brackets] are as Tableau shows them after it tidies the CSV headers (order_date becomes Order Date).

Base calc used almost everywhere (no Sales column exists in the source):

```sql
[Quantity] * [Unit Price] * (1 - [Discount])
```

Name it Sales. Margin and Margin % build on it:

```sql
// Margin
[Sales] - [Quantity] * [Unit Cost]
```

```sql
// Margin %
SUM([Margin]) / SUM([Sales])
```

## 1. Shelves and marks mechanics

A worksheet is built from four places. Read any viz from them.

| Place | Job |
|---|---|
| Columns and Rows | Structure: what goes across and what goes down |
| Marks card | How each mark looks: type, Color, Size, Label, Detail, Tooltip (Shape, Path, Angle for some mark types) |
| Filters | Which rows take part at all |
| Pages | Animation shelf |

Show Me only rearranges pills. Ctrl+Z (Command+Z on Mac) undoes it. It knows which charts are possible for the selected fields, not which one answers the question.

### Level of detail of the view

- Every discrete (blue) dimension in the view, on any shelf or on the Marks card, splits the marks further.
- Detail adds marks without changing how they look. It changes the grain of every aggregation in the view.
- Color with a blue field adds marks and splits the view. Color with a green field gives a gradient and adds no marks.
- Dragging a dimension onto Detail is the quick way to stop a line or dot joining separate items (for example Batch on Detail so a reused tank does not join two brews).

### Mark types

Automatic, Bar, Line, Area, Square, Circle, Shape, Text, Map, Pie, Gantt Bar, Polygon, Density.

- Automatic: one dimension plus one measure gives bars. A date plus a measure gives a line. Dimensions on both shelves give text. Automatic never picks Pie.
- When a forced mark type gives nonsense, set it back to Automatic first, then change one thing at a time.
- Dual axis charts have one Marks card section per measure. Set each separately.

### Filters shelf

- A filter removes rows before aggregation. Totals change.
- Hiding a header (right-click > Hide) does not remove rows.
- Dragging a measure to Filters asks Sum, Average and so on, then the range.
- Dragging a continuous measure like Discount to Filters asks how to treat it: pick All values then set the range.
- Apply to other sheets: right-click the pill > Apply to Worksheets > All Using This Data Source. Show it with right-click > Show Filter.

### Useful moves

- Copy a pill instead of moving it: hold Ctrl (Option on Mac) while dragging. Example: SUM(Quantity) from Rows onto Label to put numbers on bars.
- Drag the same measure to Label to show its value on the mark.
- Duplicate a sheet with right-click on the sheet tab > Duplicate.
- Analysis > Totals > Show Row Grand Totals or Add All Subtotals.
- Format a field once for every view: right-click in the Data pane > Default Properties > Number Format.

## 2. Dimensions, measures, discrete, continuous

Two separate ideas. Do not merge them.

| | Discrete (blue) | Continuous (green) |
|---|---|---|
| Dimension | Store Id as headers | A date as a timeline axis |
| Measure | Unit Price turned discrete: 549, 699, 899 as headers | SUM(Quantity) as an axis |

- Dimension: qualitative, groups the data, sits above the line in the Data pane.
- Measure: quantitative, sits below the line.
- Discrete draws a header per value. Continuous draws an axis with no gaps.
- Blue is not "dimension". Green is not "measure". Right-click a field in the Data pane > Convert to Discrete or Convert to Continuous.
- Tableau treats a column ending in "id" as a dimension even if it holds numbers. IDs, postcodes and years are numbers you should never add. Drag them above the line.
- Aggregation: a measure in the view is rolled up (default SUM), so the pill reads SUM(Quantity). Add a dimension and the sum is cut into one value per member. Right-click the pill > Measure (Sum) to change to Average, Median, Count, Minimum, Maximum and others.
- Wrong total? Usually a measure that should be averaged is being summed (Unit Price). Change the aggregation or ask whether the field belongs.
- AVG skips Nulls. COUNT and AVG treat Null differently from SUM.

## 3. Calculated fields

Create with Analysis > Create Calculated Field (or right-click in the Data pane). The status line under the formula says if it is valid.

Two kinds:

- Row-level: runs once per data row (quantity times price).
- Aggregate: runs after rows are rolled up (SUM of one thing divided by SUM of another).
- Every field in a formula must be either inside an aggregation or outside it. `[Discount] / SUM([Gross Sales])` fails with the mixing error.

### ZN: Null to zero

```sql
ZN([Quantity])
```

```sql
ZN([Quantity]) * [Unit Price] * (1 - [Discount])
```

```sql
ZN([Quantity]) * [Unit Price]
```

The last one is Gross Sales (price before discount). Put ZN at the edge so a Null in the middle of a longer formula cannot turn the whole result Null silently. ZN changes AVG: Quantity averaged is 1.763 over 59 rows, Quantity (filled) is 1.733 over 60 rows. Know which you mean.

### IF

Tests in order, stops at the first true. Needs END. Returns a string, so the field lands above the line.

```sql
IF [Discount] = 0 THEN "No discount"
ELSEIF [Discount] <= 0.05 THEN "Up to 5%"
ELSE "Over 5%"
END
```

### CASE

Exact matches on one field. Always write ELSE.

```sql
CASE [Store Id]
WHEN "ST-003" THEN "South"
WHEN "ST-007" THEN "South"
WHEN "ST-011" THEN "West"
WHEN "ST-014" THEN "West"
WHEN "ST-019" THEN "North"
WHEN "ST-022" THEN "East"
ELSE "Unknown store"
END
```

Fine for six items. For sixty, join a lookup file instead.

### Aggregate ratio

```sql
1 - SUM([Sales]) / SUM([Gross Sales])
```

Averaging a ratio row by row weights a one-item order the same as a big order. Whole file: Discount Rate 4.2 per cent against AVG(Discount) 3.1 per cent. Make ratios aggregates. Brewery equivalent: efficiency as SUM(extract recovered) / SUM(extract available).

### Other formulas from the notes

```sql
// Average Order Value (Claude's first answer, wrong when rows repeat an order)
SUM([Net Sales]) / COUNT([Order Id])
```

Use COUNTD([Order Id]) when the grain is order line. A duplicate row still inflates SUM, so dedupe in the source or Prep.

```sql
// Selected measure (parameter swap)
CASE [Choose measure]
WHEN 'Sales' THEN SUM([Sales])
WHEN 'Units' THEN SUM([Quantity])
WHEN 'Margin' THEN SUM([Margin])
END
```

```sql
// Waterfall step size
-SUM([Sales])
```

### Calc gotchas

- Strings match exactly. "st-003" does not match "ST-003". Use UPPER() on both sides for untidy sources.
- Decimals: prefer `<=` ranges to `=` on a decimal like 0.05.
- IF or CASE with no ELSE returns Null for unmatched rows. Nulls hide in a Null header.
- An aggregate calc on Filters filters the rolled-up result per mark, not the rows.

## 4. LOD expressions

Syntax: `{FIXED [dim1], [dim2] : AGG([measure])}` or `{INCLUDE [dim] : ...}` or `{EXCLUDE [dim] : ...}`. A FIXED with no dimension (`{ FIXED : SUM(...) }`) is table-scoped and gives one value for the whole source.

| Type | Grain | Filter behaviour |
|---|---|---|
| FIXED | Named dimensions only, ignores the view | Runs before ordinary dimension filters. Respects context, data source and extract filters |
| INCLUDE | View grain plus the named dimension | Runs after dimension filters |
| EXCLUDE | View grain minus the named dimension | Runs after dimension filters |

- FIXED returns a value per underlying row. INCLUDE and EXCLUDE return measures computed per mark.
- Requires Tableau 2024.2 or later for the notes' build, but LODs exist from 9.0. Cubes and a few older connectors do not support LODs at all.

### When to use

- Share of a stable denominator (store total, company total) that must not move with a dimension filter: FIXED.
- Share of whatever is currently filtered in: EXCLUDE.
- "Average of a total at a finer grain" (typical product per region): INCLUDE.
- Anything that must be stable whatever the view or used in a filter before aggregation: LOD, not table calc.

### Examples (verbatim)

```sql
{FIXED [Store Id] : SUM([Sales])}
```

Named Store Sales (FIXED). In the view with Store Id and Category it shows 163,488 for ST-003 Electronics, which is four times the real 40,872 because four order rows each carry the store total and SUM adds them. Change the pill to Measure (Sum) > Minimum. Or use MIN in the next calc:

```sql
// Category share of store (FIXED)
SUM([Sales]) / MIN([Store Sales (FIXED)])
```

```sql
// Category share of store (EXCLUDE)
SUM([Sales]) / SUM({EXCLUDE [Category] : SUM([Sales])})
```

```sql
// Average sales per product
AVG({INCLUDE [Product Id] : SUM([Sales])})
```

```sql
// Share of Company Sales: aggregate
SUM([Net Sales]) / MIN({ FIXED : SUM([Net Sales]) })
```

### FIXED vs dimension filter trap

- With Category filtered to Kitchen as an ordinary dimension filter: the EXCLUDE share jumps to 100 per cent on every row (the filter ran first so the denominator is Kitchen only). The FIXED share stays put (still divides by the whole store).
- Right-click the Category filter > Add to Context (pill turns grey). Context runs before FIXED, so FIXED now reads 100 per cent too.
- Company share example: drop ST-099 with a normal filter and the six remaining shares sum to 99.45 per cent (ST-099's 854.05 stays in the FIXED denominator). Add the Store Id filter to context and they sum to 100 per cent.
- Choose by question: "share of each store that is Kitchen" wants FIXED. "Share of this filtered view" wants EXCLUDE.
- A dashboard filter action is a dimension filter, so a FIXED number on the target sheet will not move.

### LOD gotchas

- SUM on a FIXED field coarser than the view multiplies it. Wrap in MIN, MAX or AVG. Or move the division into the LOD.
- INCLUDE averages only members that exist. A product with no orders in a region is absent, not zero. Pad with a list if zeros should count.
- Each FIXED can add a subquery. Many of them slow the workbook.

## 5. Table calculations

A table calc runs on the numbers already in the view, after the query and after dimension and measure filters. The pill shows a small triangle.

Quick table calcs (right-click a green measure pill > Quick Table Calculation): Running Total, Difference, Percent Difference, Percent of Total, Rank, Percentile, Moving Average, YTD Total, Compound Growth Rate, Year Over Year Growth, YTD Growth.

Typed examples:

```sql
// Running Net Sales: table calculation
RUNNING_SUM(SUM([Net Sales]))
```

```sql
LOOKUP(MIN([Region]), 0)
```

The second is the table calc filter trick (see section 6).

### Addressing and partitioning

- Partitioning fields define the groups the calc restarts in.
- Addressing fields define the direction it moves within each group.
- Compute Using assigns the jobs. Unticked fields in Specific Dimensions become partitions.
- Open it: right-click the pill > Edit Table Calculation.

| Compute Using | Meaning |
|---|---|
| Table (across) | Moves along columns. Rows are partitions |
| Table (down) | Moves down rows. Columns are partitions |
| Table (across then down) | Whole table is one partition |
| Specific Dimensions | You tick the addressing fields. Survives swapping rows and columns |

- When more than one field is ticked, At the level and Restarting every appear. Restarting every names a ticked field that acts as a partition (useful when Year and Month are split).
- Use Specific Dimensions for anything published. Table (across) is tied to the layout and silently changes meaning if someone pivots the view.

### Patterns with settings

- Running total that resets per region: Region on Rows, month on Columns, SUM(Sales) > Running Total, Compute Using Table (across). Table (down) gives a plausible but wrong cumulative down regions (the July column ends at total July sales).
- Percent of Total, three questions from one pill: Table (across) gives each row sums to 100 per cent. Table (down) gives each column sums to 100 per cent. Table (across then down) or both ticked gives all cells sum to 100 per cent. Title the view to say which.
- Rank within group: Specific Dimensions, tick Store Id only, leave Region unticked. Region becomes the partition so every region has a 1. Tick both for a company-wide rank.
- Percent Difference: defaults to Table (across). The first period is blank (correct, no previous period).
- Year Over Year Growth: put YEAR(Order Date) on Columns and QUARTER(Order Date) on Rows (both discrete) with SUM(Sales) on Text. The first year is blank. Table (down) compares Q2 with Q1 in the same year and calls it year on year.
- Percent of total of a filtered view: quick Percent of Total recomputes after filters, so filtered-out stores vanish from the denominator. To keep shares of the whole company use a FIXED LOD or a table calc filter.
- Pareto: Sales on Rows twice, second pill > Quick Table Calculation > Running Total, Edit Table Calculation > Add secondary calculation > Percent of Total. Both Table (across).

### Table calc gotchas

- Wrong direction raises no error. Check one number by hand.
- Filtering out a period removes its row, so Percent Difference for the next period goes blank. Use a table calc filter.
- Missing marks: a category with no sales is not in the table, so running totals and YoY step past it. Show Empty Rows (Analysis > Table Layout) or pad the data.
- Running totals, ranks and waterfalls follow the sort. Changing the sort changes the result.
- Last running total point should equal the grand total. If not, the calc restarts somewhere.

## 6. Order of operations

Fixed pipeline, not the order you dragged filters.

1. Extract filters
2. Data source filters
3. Context filters
4. Top N filters and FIXED LODs (applied independently of dimension filters, so Top N ranks before the dimension filter can narrow it)
5. Ordinary dimension filters (filter actions and sets act here too)
6. INCLUDE and EXCLUDE LODs, then measure filters on the aggregated value
7. Table calculations and table calc filters, last

Exact slots for blending, totals and forecasts: read the official diagram before an exam. Treat the list above as the working model.

### The classic traps

- Top N plus a Category filter: "Top 3 stores" with Category = Kitchen as a dimension filter ranks all categories first, so Chennai (more Kitchen than Bengaluru or Pune) is missing. Fix: right-click the Category pill > Add to Context.
- FIXED LOD ignoring a dimension filter: same fix, Add to Context (see section 4).
- Top N sets are computed before ordinary dimension filters. A region filter leaves the company top three. Put the region filter in context.
- Percent of total under a dimension filter: the filter ran first so the table calc saw only the filtered rows. Fix with a table calc filter.

### Table calc filter

```sql
LOOKUP(MIN([Region]), 0)
```

Name it Region (table calc filter), drag it to Filters, keep West. LOOKUP makes it a table calc so the filter runs last. Percent of total is computed across all six stores, then four are hidden. It only hides. All rows are still queried.

### Context filter costs

- A context filter turns grey. On a live connection Tableau may build a temporary table.
- Use context for filters that cut the data a lot and rarely change. Do not put every quick filter in context.

### Other order facts

- Measure filter (Sum of Sales at least 20000) runs on the aggregated value after dimension filters.
- Grand totals are computed after measure filters, so a filtered grand total is the total of what is left.
- Data source filters apply to every sheet and FIXED respects them. Extract filters drop rows from the extract entirely.

## 7. Dates

Right-click a date pill: two groups of options.

| Group | Name | Colour | Behaviour |
|---|---|---|---|
| Upper | Date part (Year, Quarter, Month, Day) | Blue, discrete | A label. "January" means every January added together |
| Lower | Date value or truncation | Green, continuous | Keeps the year. Draws a timeline |

Rules:

- Trend: lower group (continuous), for example MONTH(Order Date) green on Columns. Format the axis: right-click the axis > Format > Axis tab > Scale, custom date format such as `mmm yy`.
- Compare the same month across years: upper group Month (blue) on Columns, YEAR(Order Date) on Color, line mark. Date part is right here because the year is split out by colour.
- Dates arrive blue as YEAR(Order Date) by default. Convert deliberately.
- Never compare a full year with a part year. Sales by year with 12 months against 9 months says the business shrank. Filter to matching windows.
- Date range filter: drag the date to Filters > Range of Dates > Next, set start and end, then right-click the pill > Apply to Worksheets > All Using This Data Source.
- Relative dates (Last 12 months) move with today. Good for a live dashboard. A fixed range keeps a walkthrough stable.

### Date functions and patterns

Verified against help.tableau.com, https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm, 12 Nov 2026. The field notes themselves show only the UI route plus DATEPARSE. The function syntax below is checked against that page. The business patterns (YTD, PYTD, MTD, rolling 12 months) are built from those functions: Tableau documents the functions, not the patterns, so test each on a known date.

Syntax (from the page):
- `DATEADD(date_part, interval, date)`
- `DATEDIFF(date_part, date1, date2, [start_of_week])`
- `DATEPARSE(date_format, date_string)` (the format must match exactly. Connector support varies)
- `DATEPART(date_part, date, [start_of_week])` returns an integer. `DATENAME` returns a string.
- `DATETRUNC(date_part, date, [start_of_week])`
- `MAKEDATE(year, month, day)` takes numbers. Out of range values roll over, so MAKEDATE(2020,4,31) gives 1 May 2020. Use DATE or DATEPARSE for strings.
- `ISOWEEK(date)`, `ISOQUARTER(date)`, `ISOYEAR(date)`
- `TODAY()` and `NOW()` take no arguments. On live connections NOW() may use the database server time zone.
- date_part values: year, quarter, month, dayofyear, day, weekday, week, hour, minute, second, iso-year, iso-quarter, iso-week, iso-weekday. ISO weeks always start on Monday.

```sql
// Month value from a date (continuous when used as a dimension)
DATETRUNC('month', [Order Date])
```

```sql
// Days between two dates
DATEDIFF('day', [Start Date], [End Date])
```

```sql
// Parse an unusual text date
DATEPARSE('dd/MM/yyyy', [Order Date Text])
```

```sql
// Build a date from numeric parts, first of the month for a year and month pair
MAKEDATE([Year], [Month], 1)
```

```sql
// ISO week number and ISO week start (always Monday)
ISOWEEK([Order Date])
DATETRUNC('iso-week', [Order Date])
```

```sql
// Same date one year earlier (for a comparison column)
DATEADD('year', -1, [Order Date])
```

```sql
// Year to date, current year
IF YEAR([Order Date]) = YEAR(TODAY()) AND [Order Date] <= TODAY() THEN [Sales] END
```

```sql
// Prior year to date, same window (a leap year shifts the day of year by one)
IF YEAR([Order Date]) = YEAR(TODAY()) - 1 AND DATEPART('dayofyear', [Order Date]) <= DATEPART('dayofyear', TODAY()) THEN [Sales] END
```

```sql
// Month to date
IF DATETRUNC('month', [Order Date]) = DATETRUNC('month', TODAY()) AND [Order Date] <= TODAY() THEN [Sales] END
```

```sql
// Same period last year, month to date (Boolean filter; use DATEADD to move today back a year)
[Order Date] >= DATETRUNC('month', DATEADD('year', -1, TODAY()))
AND [Order Date] <= DATEADD('year', -1, TODAY())
```

```sql
// Rolling 12 full months, excluding the current part month (Boolean filter set to True)
[Order Date] >= DATEADD('month', -12, DATETRUNC('month', TODAY()))
AND [Order Date] < DATETRUNC('month', TODAY())
```

```sql
// Days since last order, per row
DATEDIFF('day', [Order Date], TODAY())
```

```sql
// Fiscal year start April, as a calculation when the fiscal property is not available (non relational sources)
DATETRUNC('year', DATEADD('month', -3, [Order Date]))
```

Tips from the page: DATETRUNC does not hide the time part, so format the field to show only the date. Passing 'monday' as start_of_week changes week arithmetic, for example DATEDIFF('week', #2013-09-22#, #2013-09-24#, 'monday') is 1 while 'sunday' gives 0.

For year-on-year without calcs use the quick table calc Year Over Year Growth (section 5) or YTD Total and YTD Growth.

### Fiscal year and weeks

Verified against help.tableau.com, https://help.tableau.com/current/pro/desktop/en-us/dates_fiscal.htm and https://help.tableau.com/current/pro/desktop/en-us/dates_calendar.htm, 12 Nov 2026.
- Fiscal year for one field: right-click (Control-click on Mac) the date dimension in the Data pane > Default Properties > Fiscal Year Start > pick the month. Each date dimension is set separately.
- Fiscal year for the whole data source: right-click the data source in the Data pane > Date Properties > Fiscal year start. The same dialog holds the week start day.
- Fiscal start changes Year, Quarter and Week Number only. Month, Day and Weekday stay calendar. With an April start, 1 June 2004 is FY 2005, Q1.
- Fiscal dates apply to relational sources only. Only the date levels present in the view show the fiscal calendar.
- ISO 8601 weeks always start on Monday whatever the week start setting. Use the iso-week, iso-year, iso-quarter and iso-weekday date parts for them.

### Date gotchas

- Dates stored as text (Abc icon) sort alphabetically and cannot make a timeline. Change the type on the data source page or use DATEPARSE().
- 03/04/2026 can mean 3 April or 4 March. Tableau reads it with the computer locale. Check one known date.
- An impossible date (31 September) becomes a Null. A small indicator at the bottom right says "1 null". Its value is parked under Null.
- A continuous axis draws a straight line across a month with no orders. A discrete axis leaves a gap. Neither shows zero.

## 8. Parameters and parameter actions

A parameter is a single workbook value. It does nothing until a calc, filter, reference line or Top N reads it. Order: build the parameter, build the calc that reads it, then show the control.

Create: Data pane drop-down arrow > Create Parameter. Show: right-click the parameter > Show Parameter.

| Parameter | Settings |
|---|---|
| Choose measure | String, Allowable values List: Sales, Units, Margin |
| Sales target | Float, Allowable values All, current 30000, format number no decimals |
| Price change % | Integer, Range, min -10, max 10, step 1, current 0 (show as slider) |
| Selected store | String, Allowable values All, current ST-003 |

### Recipes (verbatim)

Measure swap: Store Id on Rows, Selected measure on Columns. See the CASE in section 3. Title it dynamically: Worksheet > Show Title, then Insert in the title editor gives `<Parameters.Choose measure> by store`.

Target reference line: right-click the axis > Add Reference Line, Value set to the parameter, Label Value.

```sql
[Selected measure] >= [Sales target]
```

Drag it to Color. Hide the target control when another measure is chosen or give each measure its own target.

What-if price change:

```sql
// Projected sales
SUM([Sales]) * (1 + [Price change %] / 100)
```

```sql
// Projected margin
[Projected sales] - SUM([Quantity] * [Unit Cost])
```

Highlight the selected store:

```sql
[Store Id] = [Selected store]
```

### Parameter action (select a mark to set the value)

1. Build the dashboard with the store chart on it.
2. Dashboard > Actions > Add Action > Change Parameter.
3. Source sheet: the store sheet. Run action on Select.
4. Target parameter: Selected store. Source field: Store Id. Aggregation: None.
5. When selection clears: Keep current value.

Any sheet that uses Selected store (for example a product breakdown filtered with `[Store Id] = [Selected store]`) follows.

### Self-refreshing parameters

Since 2020.1 the Create Parameter dialog can fill its list from a field and set the current value from a field when the workbook opens. Labels may read "When workbook opens" or similar.

### Parameter gotchas

- A parameter or control not used in the view, a calc or a reference line does nothing, including a parameter action.
- Aggregation None with two marks of different ids selected makes the action skip. Pick an aggregation or design for one mark.
- Swapping dimensions with a parameter can fail silently in a multi-fact relationship model.
- Parameters are global and per session. On Server or Cloud a viewer's change never alters the published default.
- A what-if is not a forecast (no price elasticity in the data). Say so in a caption.
- Title a swap with the parameter. A swapped chart with a fixed title misleads.

## 9. Sets and set actions

A set splits one dimension into In and Out. Create: right-click the dimension > Create > Set. It appears under its own heading with a Venn icon. It lives on one dimension only.

### Set types

- Top N: Top tab > By field > Top, 3, Sales, Sum (name it Top 3 stores).
- Condition: Condition tab > By formula:

```sql
COUNTD([Order Id]) >= 10
```

- Manual: General tab, tick members. Leave all unticked for an empty set.
- Combined: select two sets in the Data pane > right-click > Create Combined Set. Options: all members in both sets, shared members or one set less shared.

### Using a set

- On Rows it shows In and Out. Add a Quick Table Calculation > Percent of Total for the share.
- Add Store Id after it on Rows to list members in each group.
- On Filters it keeps In by default.
- On Color it highlights members.

### Drill-down with a set action

1. Make a set on Store Id called Expanded store with nothing ticked.
2. Create the calc:

```sql
IF [Expanded store] THEN [Category] END
```

Name it Category drill.
3. Sheet: Store Id then Category drill on Rows, Sales on Text. Every store shows one row with a Null category.
4. Dashboard > Actions > Add Action > Change Set Values.
5. Source: the store sheet. Run on Select. Target set: Expanded store.
6. Running the action: Assign values to set. Clearing the selection: Remove all values from set.

Select a store and its row opens into categories. Select empty space and it closes. The calc reads the set. The action only changes membership.

### Set gotchas

- Top N sets ignore ordinary dimension filters (they run first). Put the other filter in context.
- A set action does nothing unless a shelf, calc or the Marks card uses the set.
- Add values to set and Remove values from set rewrite the set's General tab. That differs from the tooltip Add to and Remove from options, which apply after the set's condition.
- Set actions do not work in stories.
- A set of store and category pairs needs a set on a combined field. Two sets plus a combined set usually read better.

## 10. Maps

A field is mappable when it has a geographic role: City, State/Province, Country/Region, Postcode and a few more. Double-click a role field and Tableau draws a map using Longitude (generated) on Columns and Latitude (generated) on Rows.

### Setup

1. Relate the location table to the facts on the shared key (Store Id = Store Id).
2. Roles: a globe icon beside the field means a role is set. Otherwise click the Abc icon > Geographic Role > City, State/Province or Country/Region.
3. Latitude and Longitude roles work only on number fields.
4. City role covers world cities with population 15,000 or more.

### Symbol map (totals)

1. Double-click City. City lands on Detail.
2. Sales on Size. Store name on Label.
3. Marks dropdown: Circle.

### Filled map (rates or shares)

1. Double-click State.
2. Marks dropdown: Map.
3. A rate or share (sales per head, discount rate, growth) on Color.

### Fixing unknown places

- An indicator at the bottom right shows the unknown count. Select it > Edit Locations (or Map > Edit Locations).
- Under Geographic Roles set Country/Region to From field and pick Country. That resolves most ambiguous cities (Delhi in India against several in the United States).
- In Match Values to Locations, fix Unrecognized rows by typing a name Tableau knows or by Enter Latitude and Longitude. Bengaluru against Bangalore is the typical case.
- Delhi in a filled map may need matching to Tableau's name for the territory.
- A key with no row in the location file (ST-099) has no city. Filter it out or fix the source.

### Lat/long fallback (most reliable)

Longitude to Columns, Latitude to Rows, Store Id on Detail. No name matching at all. Use for any site list.

### Map gotchas

- Filled maps of totals mislead: the region with more stores shades darkest. Use symbol maps for totals.
- Big areas shout. A large area with a small value dominates.
- Map tiles load from the internet. Offline gives points on a blank background.
- Thousands of overlapping circles: switch Marks to Density.
- Custom territories (sales zones) are not in the place list. Group states or bring a spatial file.

## 11. Chart chooser

Pill key: (d) discrete or blue, (m) continuous or green.

### By question

| Question | Chart |
|---|---|
| Compare categories | Bar, Dot plot, Highlight table, Bullet graph |
| Change over time | Line, Area, Sparkline, Slope chart, Gantt, Dual-axis |
| Part to whole | Stacked bar, Treemap, Waterfall, Area |
| Distribution | Histogram, Box plot, Dot plot |
| Relationship | Scatter, Heat map, Dual-axis |
| Ranking | Bar, Lollipop, Pareto, Slope chart |
| Deviation from target | Bullet, KPI tile (BAN), Waterfall, Highlight table |
| Geography | Symbol map, Filled map |
| Flow | Waterfall, Gantt, Sankey (no native mark) |

### Shelf recipes

| Chart | Use when | Recipe | Avoid when |
|---|---|---|---|
| Bar | Compare a measure across categories, sort for ranking | Rows: Sub-Category (d). Columns: SUM(Sales) (m). Marks: Bar | Long time series or an axis that cannot start at zero |
| Dot plot | Many categories or two values per category | Rows: Region (d). Columns: SUM(Sales) (m). Marks: Circle. Colour: Segment (d) | Audience expects bars and zero baseline matters |
| Highlight table | Crosstab with colour to find big and small cells | Columns: Region (d). Rows: Category (d). Marks: Square. Colour: SUM(Profit) (m) | Precise comparison of close values |
| Bullet graph | Actual against target with poor, fair, good bands | Rows: Brewery (d). Columns: SUM(Yield) (m). Detail: SUM(Target) (m). Marks: Bar, reference line and bands on Target | Audience new to it, without a one-line legend |
| Line | Continuous measure over continuous time | Columns: MONTH(Order Date) (m). Rows: SUM(Sales) (m). Marks: Line | Unordered categories |
| Area | Total over time with rough part contribution | Columns: MONTH(Order Date) (m). Rows: SUM(Sales) (m). Colour: Segment (d). Marks: Area | Precise comparison of upper layers |
| Sparkline | Many small trends for shape and direction | Rows: Measure Names (d), Measure Values (m). Columns: WEEK(Date) (m). Marks: Line, independent axes, axes hidden | People need to read a number (add the BAN) |
| Slope chart | Change between exactly two points in time | Columns: YEAR(Order Date) (d). Rows: SUM(Sales) (m). Detail: Region (d). Marks: Line, filter to two years | More than two dates (use a line) |
| Gantt chart | Start, end and overlap (tank occupancy, schedules) | Columns: DAY(Start Date) (m). Rows: Tank (d). Size: SUM(Days in Tank) (m). Marks: Gantt Bar | Totals (bar length is a duration) |
| Dual-axis combination | Two measures with different units over the same time | Columns: MONTH(Order Date) (m). Rows: SUM(Volume) (m), AVG(Price) (m). Marks: Bar and Line, Dual Axis | Implying a correlation |
| Stacked bar | Totals plus rough split (100 per cent stacked for shares) | Rows: Region (d). Columns: SUM(Sales) (m). Colour: Pack Type (d). Marks: Bar | More than four or five segments |
| Treemap | Part to whole across many nested categories | Marks: Square. Size: SUM(Sales) (m). Colour: SUM(Profit) (m). Label: Sub-Category (d) | Comparing similar-sized blocks |
| Waterfall | Start value to end value (price to margin, plan to actual) | Columns: Cost Driver (d). Rows: RUNNING_SUM(SUM(Change)) (m). Size: -SUM(Change) (m). Marks: Gantt Bar | Dozens of steps (group small ones into Other) |
| Histogram | Shape of one measure | Columns: Days to FG (bin) (d). Rows: CNT(Batch) (m). Marks: Bar | Before trying two or three bin sizes |
| Box plot | Spread and outliers across a few groups | Columns: Yeast Strain (d). Rows: AVG(Days to FG) (m). Detail: Batch (d). Marks: Circle, Analytics: Box Plot | Lay audience without the dots shown |
| Scatter plot | Two measures against each other, one mark per item | Columns: AVG(Ferment Temp) (m). Rows: AVG(Diacetyl) (m). Detail: Batch (d). Marks: Circle | Proof of cause or thousands of marks (use density) |
| Heat map | Where two dimensions meet most often | Columns: DATEPART(hour) (d). Rows: WEEKDAY(Date) (d). Colour: CNT(Orders) (m). Marks: Square | Exact values matter (add labels or use a highlight table) |
| Lollipop | Ranked list where long bars are a wall of ink | Rows: Account (d). Columns: SUM(Sales) (m), SUM(Sales) (m). Marks: Thin Bar and Circle, Dual Axis, synchronised | Values close together |
| Pareto | Find the vital few making most of the total | Columns: Stop Reason (d). Rows: SUM(Minutes) (m), Running % of total (m). Marks: Bar and Line, Dual Axis, sorted descending | Categories roughly equal |
| KPI tile (BAN) | One number with target and direction | Marks: Text. Text: SUM(Volume) (m), % vs Target (m). Colour: Above Target (d) | Standing alone with no comparison |
| Symbol map | An amount at a place, size carries the number | Columns: Longitude (generated) (m). Rows: Latitude (generated) (m). Detail: City (d). Size: SUM(Sales) (m). Marks: Circle | Dense places that pile up (filter or aggregate first) |
| Filled map | A rate or ratio by region | Columns: Longitude (generated) (m). Rows: Latitude (generated) (m). Detail: State (d). Colour: AVG(Sales per Head) (m). Marks: Map | Raw totals |
| Sankey | Volume moving between stages | No Sankey mark. Needs densified data and nested table calcs (Columns: t (bin), Rows: sigmoid curve calc, Marks: Line) or a community template or extension | Try a waterfall or a flow table first |

### Charts to avoid

| Chart | Why | Use instead |
|---|---|---|
| Pie beyond a few slices | Angles are hard to compare. Two or three slices with one winner is fine | Sorted bar or 100 per cent stacked bar |
| 3D charts | Tableau does not draw them. Perspective distorts and hides values | The flat version |
| Dual-axis traps | Independent axes can be stretched so any two lines cross where you like | Synchronise when units match, label both or stack two small charts |
| Packed bubbles | Circle area is the weakest common encoding and the layout has no order | Bar or treemap |

### Build recipes for the harder charts

Dual axis, bars plus line (sales and margin percentage):

1. MONTH(Order Date) continuous on Columns.
2. SUM(Sales) on Rows, then Margin % on Rows to its right.
3. Right-click the Margin % pill > Dual Axis.
4. Marks card: SUM(Sales) Bar, AGG(Margin %) Line.
5. Do NOT synchronise axes when units differ (rupees against a percentage). Synchronise only for the same unit. Start the right axis near the data and label it.

Bullet chart (actual against target):

1. Store Id on Rows, Sales on Columns, Target Sales on Detail.
2. Right-click the Sales axis > Add Reference Line > Per Cell, value SUM(Target Sales), aggregation Sum. Short dark stroke.
3. Second reference item: Distribution, Per Cell, percentages of SUM(Target Sales): 60 and 80. Shade light grey. Tick Fill Below for three bands.
4. Narrow the bars with Size.
5. Relate the target table to stores on Store Id, not to orders. Otherwise SUM(Target Sales) inflates.

Pareto (products making 80 per cent of sales):

1. Name on Columns, Sales on Rows. Sort Name by Field, Descending, Sales, Sum.
2. Sales on Rows again > Quick Table Calculation > Running Total > Edit Table Calculation > Add secondary calculation > Percent of Total. Both Table (across).
3. Right-click the second pill > Dual Axis. First Bar, second Line.
4. Constant reference line at 0.8 on the right axis.

Waterfall (categories to total):

1. Category on Columns, Sales on Rows. Sort Category descending by Sales.
2. SUM(Sales) > Quick Table Calculation > Running Total.
3. Marks: Gantt Bar.
4. Create `-SUM([Sales])` and drag it to Size.
5. Analysis > Totals > Show Row Grand Totals for the final bar.
6. Colour by Category or a sign calc when steps can be negative.

Lollipop: two copies of the measure on Columns, dual axis, one Thin Bar and one Circle, synchronise axes.

Slope chart: filter the date to exactly two values or the lines turn into a line chart.

## 12. Gotchas

Data and setup

- Check the data first. Row counts and COUNTD against COUNT expose duplicates. Look for blanks, negatives, unknown keys and impossible dates before building.
- A duplicate row inflates SUM. COUNTD(Order Id) gives 59 orders against 60 rows. Fix at source or in Prep, not in a calc.
- A Null quantity: SUM skips it, AVG skips it, COUNT counts the row. Use ZN() at the edge when zero is the right answer.
- Join the target table to the dimension both facts share (stores), not to the fact (orders). Otherwise targets are counted per order row.
- Verify every build against a number computed another way. Last running total point equals the grand total. Percent of total sums to 100.

Filters and order

- Dimension filters do not touch FIXED LODs or Top N. Add to Context.
- Context filters cost performance. Use sparingly.
- A table calc cannot see filtered-out marks. Use a table calc filter (`LOOKUP(MIN([Dim]), 0)`) to hide without changing the base.
- Filter actions are dimension filters, so FIXED numbers on target sheets do not react.
- Sets (Top N) run before dimension filters.

Calcs

- Aggregate and non-aggregate arguments cannot mix in one formula.
- Average ratios are wrong. Divide the sums.
- SUM of a FIXED LOD multiplies it. Use MIN or MAX.
- Table calc direction is silent. Table (across) and (down) move with the layout. Use Specific Dimensions for published views.
- Sort order changes running totals, ranks and waterfalls.
- Always write ELSE in IF and CASE.

Dates

- Date part (blue) is a label, date value (green) is a timeline. A month part adds Januaries of different years.
- Full year against part year lies. Filter to equal windows.
- Set Fiscal Year Start in Default Properties before building finance views.
- Text dates cannot draw a timeline. Fix the type.

Charts and design

- Never synchronise a dual axis across different units.
- Filled maps for rates, symbol maps for totals.
- Red and green only fails colour vision deficiency. Use labels or a blue and orange pair.
- A big number without a comparison tells nobody whether to worry. Pair every BAN with target and direction.
- Parameters and set actions do nothing unless the field is used in the view or a calc.
- Title views that use parameters or table calc direction so the reader knows the question being answered.
