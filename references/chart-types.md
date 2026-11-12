# Tableau chart type catalogue

Checked 12 Nov 2026. 53 chart recipes (19 official, 34 derived) plus the 24 Show Me types in table 1.

Sources: help.tableau.com Build Common Chart Types pages (fetched: bar, gantt, pie, treemap, bubbles, line, box plot, highlight, histogram, scatter, text), the Pareto and bullet graph pages, Show Me (buildauto_showme.htm) plus the Tableau maps pages (maps_build.htm and the five maps_howto pages). Pages that returned 404 on 12 Nov: area, bullet, waterfall, dual axis, combination, motion, word cloud (buildexamples_*). Those entries are marked derived, built from the official mechanics on the pages that did load. Show Me field counts come from the hover text in the Show Me pane (the help page does not list them), so treat the counts as a guide and hover in your version.

The chart chooser and one line recipes already live in [calcs-and-viz.md](calcs-and-viz.md) section 11. This file adds the full shelf recipes, calculated fields and traps. Pill key: (d) discrete or blue, (m) continuous or green.

Marking: "official" means the steps come from the cited help.tableau.com page. "derived" means a recipe built from official mechanics (dual axis, table calcs, densification, Path and Detail), not a published Tableau recipe.

## 1. Show Me: the 24 types and the fields each needs

Select the fields first with Ctrl or Cmd click in the Data pane, then open Show Me. Types that cannot be built from the selection are greyed out. Source: https://help.tableau.com/current/pro/desktop/en-us/buildauto_showme.htm

| # | Show Me type | Dimensions | Measures | Other |
|---|---|---|---|---|
| 1 | Text table | 1 or more | 1 or more | |
| 2 | Heat map | 1 or more | 1 or more | |
| 3 | Highlight table | 1 or more | 1 or more | |
| 4 | Symbol map | 0 or 1 | 0 to 2 | 1 geographic field |
| 5 | Filled map | 0 or more | 0 to 1 | 1 geographic field |
| 6 | Pie chart | 1 or more | 1 or 2 | |
| 7 | Horizontal bars | 0 or more | 1 or more | |
| 8 | Stacked bars | 1 or more | 1 or more | |
| 9 | Side by side bars | 1 or more | 1 or more | |
| 10 | Treemap | 1 or more | 1 or 2 | |
| 11 | Circle view | 1 or more | 1 or more | |
| 12 | Side by side circles | 1 or more | 1 or more | |
| 13 | Line (continuous) | 0 or more | 1 or more | 1 date |
| 14 | Line (discrete) | 0 or more | 1 or more | 1 date |
| 15 | Dual line | 0 or more | 2 or more | 1 date |
| 16 | Area (continuous) | 0 or more | 1 or more | 1 date |
| 17 | Area (discrete) | 0 or more | 1 or more | 1 date |
| 18 | Dual combination | 0 or more | 2 or more | 1 date |
| 19 | Scatter plot | 0 or more | 2 to 4 | |
| 20 | Histogram | 0 | 1 | |
| 21 | Box and whisker plot | 0 or more | 1 or more | |
| 22 | Gantt chart | 1 or more | 0 or 1 | 1 date |
| 23 | Bullet graph | 0 or more | 2 or 3 | |
| 24 | Packed bubbles | 1 or more | 1 or 2 | |

Notes: aggregate calculated fields such as a ratio do not count towards the pie or bubble measure total. A histogram needs a single measure and no dimensions (official, buildexamples_histogram.htm). Show Me changes the Marks type and shelves for you, so read the result and fix it, never trust it as final.

## 2. Quick picker

| Analytical question | Best charts | Then try |
|---|---|---|
| Comparison | Bar, Dot plot, Bullet graph | Lollipop, Dumbbell, Highlight table |
| Trend | Line, Area, Sparkline | Slope chart, Bump chart, Calendar heatmap, Control chart |
| Part to whole | Stacked bar, 100 per cent stacked bar, Treemap | Donut, Waffle, Marimekko, Pie (two or three slices) |
| Distribution | Histogram, Box plot | Jitter or strip plot, Density map, Population pyramid (butterfly) |
| Correlation | Scatter plot, Heat map | Packed bubbles (weak), Dual axis (time only) |
| Ranking | Sorted bar, Lollipop | Bump chart, Pareto, Slope chart |
| Flow | Waterfall, Sankey, Funnel | Flow map, Spider map, Gantt, Timeline |
| Geography | Symbol map, Filled map | Density map, Hex map, Spider map |
| Deviation | Diverging bar, Bullet graph, Waterfall | Butterfly, Control chart, Highlight table |
| KPI | BAN tile, KPI with arrows | Sparkline row, Bullet graph |

---

## 3. Core charts

### Bar chart
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_bar.htm
- Use: compare a measure across categories, sorted for ranking.
- Avoid: a truncated axis or a long time series.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Columns: SUM(Sales) (m). Rows: Sub-Category (d). Marks: Bar. Sort descending by Sales. Optional Colour: Ship Mode (d) for stacks. Label: SUM(Sales) via a Cell reference line (Analytics pane, Sum, Label Value, Line None) for stack totals.
- Mistake: a date dropped on Columns gives a year bar with a Line mark first. Change the mark to Bar.

### Stacked bar and 100 per cent stacked bar
Official (stack step): buildexamples_bar.htm
- Use: totals with a rough split. Use 100 per cent for shares.
- Avoid: more than five segments.
- Fields: 2 dimensions (d), 1 measure (m).
- Recipe: Columns: SUM(Sales). Rows: Region. Colour: Segment. Marks: Bar. For 100 per cent: right click SUM(Sales) on Columns, Quick Table Calculation, Percent of Total, Compute Using Segment.
- Mistake: Compute Using left on Table (Across) so each bar shows a share of the grand total.

### Side by side bars
Derived (Show Me type 9)
- Use: compare two or three series per category.
- Avoid: more than three series.
- Fields: 2 dimensions (d), 1 measure (m).
- Recipe: Columns: Segment (d) then SUM(Sales) (m). Rows: Region (d). Colour: Segment. Marks: Bar. Right click the Segment pill on Columns and Show Header off if the legend is enough.
- Mistake: Segment placed inside Rows as well, so each bar sits alone.

### Dot plot
Derived
- Use: many categories or two values per category, zero baseline not vital.
- Avoid: audiences who expect bars.
- Fields: 1 dimension (d), 1 or 2 measures (m).
- Recipe: Rows: Region (d). Columns: SUM(Sales) (m). Marks: Circle. Colour: Segment.
- Mistake: leaving the mark on Automatic gives bars.

### Line chart
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_line.htm
- Use: a measure over continuous time.
- Avoid: unordered categories.
- Fields: 1 date (m or d), 1 measure (m).
- Recipe: Columns: MONTH(Order Date) (m, the second Month in the date menu). Rows: SUM(Sales) (m). Marks: Line. Colour: Region for several lines. Analytics: Forecast or Trend Line if needed.
- Settings: continuous dates draw a linear axis. Discrete dates draw headers.
- Mistake: picking the discrete month (blue) and getting header cells that break the line across years.

### Area chart
Derived (Show Me types 16 and 17)
- Use: total over time with rough contribution.
- Avoid: reading upper layers precisely.
- Fields: 1 date (m), 1 measure (m), 1 dimension (d) for layers.
- Recipe: Columns: MONTH(Order Date) (m). Rows: SUM(Sales) (m). Colour: Segment (d). Marks: Area. Order the layers with Colour sort.
- Mistake: negative values stack above and below zero and look broken. Use lines.

### Pie chart
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_pie.htm
- Use: two or three slices with one clear winner.
- Avoid: more than five slices or similar sizes.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Marks: Pie. Angle: SUM(Profit). Colour: Category (d). Label: Category and SUM(Profit) as percentage of total. Fit: Entire View, then raise Size.
- Settings: Label as Percent of Total uses a Quick Table Calculation on the Label copy only.
- Mistake: negative measure values break the angle. Pies cannot show them.

### Treemap
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_treemap.htm
- Use: part to whole across many nested categories.
- Avoid: comparing similar blocks.
- Fields: 1 to 2 dimensions (d), 1 or 2 measures (m).
- Recipe: Marks: Square. Size: SUM(Sales). Colour: SUM(Profit). Label: Sub-Category. Detail: Category for grouping.
- Mistake: putting a measure anywhere except Size and Colour (it has no effect).

### Packed bubble chart
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_bubbles.htm
- Use: a fast rough view of size across many items.
- Avoid: any exact comparison (use a bar).
- Fields: 1 or more dimensions (d), 1 or 2 measures (m).
- Recipe: Marks: Circle. Size: SUM(Sales). Colour: SUM(Profit). Detail: Category. Label: Region.
- Mistake: no Detail field gives one single bubble.

### Text table
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_text.htm
- Use: exact values in a crosstab.
- Avoid: finding patterns (use a highlight table).
- Fields: 2 dimensions (d), 1 measure (m).
- Recipe: Columns: YEAR(Order Date) (d). Rows: Sub-Category (d). Text: SUM(Sales). For shares: Add Table Calculation on the Text pill, Percent of Total, Pane (Down).
- Mistake: Marks card set to Bar after a Show Me click. Switch back to Text.

### Highlight table
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_highlight.htm
- Use: a crosstab where colour finds the big and small cells.
- Avoid: precise comparison of close values.
- Fields: 2 dimensions (d), 1 measure (m).
- Recipe: Columns: Segment. Rows: Region then Sub-Category. Marks: Square. Colour: SUM(Profit), Red-Black Diverging with Use Full Color Range. Text: SUM(Profit). Optional Size: SUM(Sales) for a heat map.
- Mistake: a sequential palette on a measure that crosses zero.

### Heat map
Derived from the highlight table recipe (Show Me type 2)
- Use: two dimensions, many cells, colour carries density.
- Avoid: exact values.
- Fields: 2 dimensions (d), 1 measure (m).
- Recipe: Columns: DATEPART('hour',[Order Time]) (d). Rows: DATENAME('weekday',[Order Date]) (d). Marks: Square. Colour: COUNT([Order ID]). Size: Fit Entire View.
- Mistake: weekday names sort alphabetically. Sort manually from Monday.

### Circle view and side by side circles
Derived (Show Me types 11 and 12)
- Use: strip of values per category with no bar ink.
- Avoid: values that overlap a lot.
- Fields: 1 or more dimensions (d), 1 measure (m).
- Recipe: Columns: Category (d) then SUM(Sales). Rows: Region. Marks: Circle. Detail: Customer Name for one circle per customer.
- Mistake: forgetting Detail, so every circle collapses into one.

### Histogram
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_histogram.htm
- Use: the shape of one measure.
- Avoid: an unchecked bin size.
- Fields: 1 measure.
- Recipe: Drag Quantity to Columns, Show Me, Histogram. Tableau builds a continuous bin on Columns and CNT(Quantity) on Rows. Colour: Segment. Right click the bin in the Data pane, Edit, to change size.
- Settings: percentages need a Percent of Total on the Label copy with Compute Using Cell.
- Mistake: the default bin size. Try three sizes.

### Box plot
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_boxplot.htm
- Use: spread and outliers across a few groups.
- Avoid: lay audiences with no dots shown.
- Fields: 1 or 2 dimensions (d), 1 measure (m), one dimension at row level for Detail.
- Recipe: Columns: Segment then Region. Rows: AVG(Discount). Show Me, Box and Whisker. Drag Region back to Columns. Analysis, Aggregate Measures off. Marks: Circle. Detail: Customer Name. Edit Reference Line to change fill.
- Mistake: Aggregate Measures left on, so each box is a flat line.

### Scatter plot
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_scatter.htm
- Use: two measures against each other, one mark per item.
- Avoid: proof of cause or thousands of marks (use density).
- Fields: 2 measures (m), 1 dimension (d) for Detail.
- Recipe: Columns: SUM(Sales). Rows: SUM(Profit). Colour: Category. Detail: Region. Analytics: Trend Line.
- Mistake: no Detail, so a single mark sits at the grand total.

### Gantt chart
Official: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_gantt.htm
- Use: start, duration and overlap.
- Avoid: totals (bar length is a duration).
- Fields: 1 date (m), 1 dimension (d), 1 duration measure (m).
- Recipe: Columns: WEEK(Order Date) (m). Rows: Sub-Category then Ship Mode. Marks: Gantt Bar. Size: AVG(OrderUntilShip). Colour: Ship Mode.
```
OrderUntilShip = DATEDIFF('day',[Order Date],[Ship Date])
```
- Mistake: Size left as SUM, so duration balloons.

### Bullet graph
Official page: https://help.tableau.com/current/pro/desktop/en-us/qs_bullet_graphs.htm (page text fetched via search only)
- Use: actual against a target with bands.
- Avoid: first time audiences without a legend line.
- Fields: 1 dimension (d), 2 measures (m).
- Recipe: Rows: Category. Columns: SUM(Sales). Detail: SUM(Quota). Marks: Bar. Analytics: Reference Line on the axis, Per Cell, Value SUM(Quota), plus Distribution bands at 60 per cent and 80 per cent of Average.
- Mistake: the target on Detail but no reference line, so nothing shows.

### Pareto chart
Official: https://help.tableau.com/current/pro/desktop/en-us/pareto.htm (page text fetched via search only)
- Use: find the vital few.
- Avoid: roughly equal categories.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Columns: Sub-Category sorted descending by SUM(Sales). Rows: SUM(Sales) twice. Marks: first Bar, second Line. Dual Axis, synchronise. Second SUM(Sales): Quick Table Calculation, Running Total, then add a secondary calculation Percent of Total.
```
RUNNING_SUM(SUM([Sales])) / TOTAL(SUM([Sales]))
```
- Settings: Compute Using Table (Across) for both layers. Hide the left axis title.
- Mistake: Percent of Total applied before Running Total, so the order is wrong.

### Waterfall chart
Derived (page returned 404). Uses the Gantt mechanic from the Gantt page.
- Use: start to end value with steps.
- Avoid: dozens of steps.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Columns: Sub-Category (d). Rows: SUM(Profit) with Quick Table Calculation Running Total. Marks: Gantt Bar. Size: calculated field below. Colour: Profit above or below zero.
```
-SUM([Profit])
```
- Settings: Running Total Compute Using Table (Across). Add a Total with Analytics, Totals, Show Column Grand Totals for the end bar.
- Mistake: Size left on SUM(Profit), so negative bars draw upwards.

### Dual axis chart
Derived (page returned 404)
- Use: two measures with different units on one time axis.
- Avoid: implying correlation.
- Fields: 1 date (m), 2 measures (m).
- Recipe: Columns: MONTH(Order Date). Rows: SUM(Sales) then SUM(Profit). Right click the second pill, Dual Axis. Marks per layer: Bar then Line. Right click the right axis, Synchronize Axis, only if both share a unit.
- Mistake: stretched independent axes make lines cross where you choose.

### Combination chart
Derived (page returned 404)
- Use: volume and rate together.
- Avoid: more than two layers.
- Fields: 1 date (m), 2 measures (m).
- Recipe: as Dual axis, with Bar for the volume layer and Line with circles for the rate layer. Put Colour only on the line layer.
- Mistake: Marks card has an All layer that overrides both. Change layers one at a time.

### Motion chart (pages)
Derived (page returned 404)
- Use: change of a scatter or bubble across time.
- Avoid: reports and print.
- Fields: 2 measures (m), 1 date (d), 1 dimension (d).
- Recipe: Columns: AVG(Sales). Rows: AVG(Profit). Detail: Customer Name. Pages: YEAR(Order Date). Tick Show History, Trails.
- Mistake: Pages on a continuous date, which has no play control.

### Word cloud
Derived (page returned 404; the text mark behaviour is from the Show Me and marks help)
- Use: rough word frequency for text.
- Avoid: precise comparison.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Marks: Text. Text: Word (d). Size: SUM(Count). Colour: SUM(Count). Fit Entire View.
- Mistake: words not split into rows first. Split the text field in prep.

---

## 4. Maps

### Symbol map
Official: https://help.tableau.com/current/pro/desktop/en-us/maps_howto_symbol.htm
- Use: an amount at a place.
- Avoid: dense overlapping points.
- Fields: Latitude and Longitude (m generated or measure), 1 ID dimension (d).
- Recipe: double click Latitude and Longitude. Detail: ID. Size: a measure. Colour: a measure. Opacity 70 per cent. Sort ID by the measure descending so large marks sit under small ones.
- Mistake: no Detail, so one point at the centre.

### Filled map
Official: https://help.tableau.com/current/pro/desktop/en-us/maps_howto_choropleth.htm
- Use: a rate or ratio by region.
- Avoid: raw totals in regions of unequal size.
- Fields: 1 geographic dimension (d), 1 measure (m).
- Recipe: double click State. Marks: Map (filled). Drill to County with the plus icon. Colour: a rate. Right click the Colour pill, Attribute. Border: None.
- Mistake: Filled maps are not available for cities or airports (official note in buildexamples_maps.htm).

### Density map
Official: https://help.tableau.com/current/pro/desktop/en-us/maps_howto_heatmap.htm
- Use: clusters in many points.
- Avoid: few marks.
- Fields: Latitude, Longitude, 1 ID (d).
- Recipe: Columns: Longitude. Rows: Latitude. Detail: ID (Add all members). Marks: Density. Adjust intensity and colour.
- Mistake: the density mark needs Detail, otherwise one point.

### Flow (path) map
Official: https://help.tableau.com/current/pro/desktop/en-us/maps_howto_flow.htm
- Use: movement across time (storms or vehicle tracks).
- Avoid: no order field.
- Fields: Latitude, Longitude, order date or number, 1 path ID (d).
- Recipe: Columns: Longitude. Rows: Latitude. Detail: Storm Name. Marks: Line. Path: Date as Exact Date. Size: AVG(Wind). Colour: Storm Name.
- Mistake: Path left on a date with year level, so points join out of order.

### Spider (origin to destination) map
Official: https://help.tableau.com/current/pro/desktop/en-us/maps_howto_origin_destination.htm
- Use: one origin to several destinations.
- Avoid: thousands of paths with no filter.
- Fields: Latitude, Longitude, Path ID (d), Point Order.
- Recipe: Columns: Longitude (Dimension). Rows: Latitude (Dimension). Marks: Line. Detail: Path ID. Path: Point Order (Dimension). Colour: Path ID. Or with origin and destination on one row, use MAKELINE (derived, see below).
```
MAKELINE(MAKEPOINT([Origin Lat],[Origin Lon]),MAKEPOINT([Dest Lat],[Dest Lon]))
```
- Mistake: leaving Latitude and Longitude as Measures, so paths aggregate.

### Hex map
Derived (spatial bin functions, no help page fetched)
- Use: point counts in even hexagonal cells.
- Avoid: precision at small scale.
- Fields: Latitude, Longitude (m).
- Recipe: create a group of hex calcs. Columns: HEXBINX. Rows: HEXBINY. Marks: Shape, hexagon. Colour: COUNT([ID]). Size by zoom level.
```
HEXBINX([Longitude],[Latitude])
HEXBINY([Longitude],[Latitude])
```
- Mistake: leaving Latitude and Longitude on the shelf at the same time.

---

## 5. Advanced charts (all derived)

### Donut chart
- Use: share of one total with a label in the hole.
- Avoid: more than three slices.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Rows: MIN(0) twice. Marks (first): Pie, Angle SUM(Sales), Colour Category. Dual Axis. Marks (second): Circle, Colour white, Size smaller than the pie. Hide the axes. Label the circle with a KPI.
```
MIN(0)
```
- Mistake: Synchronize Axis left off, so the hole is off centre.

### Slope chart
- Use: change between two points.
- Avoid: more than two dates.
- Fields: 1 date (d), 1 measure (m), 1 dimension (d).
- Recipe: Columns: YEAR(Order Date) (d), filter to two years. Rows: SUM(Sales). Detail: Region. Marks: Line with circles. Label ends only.
- Mistake: three or more dates make it a plain line.

### Bump chart
- Use: rank change over time.
- Avoid: values that matter more than rank.
- Fields: 1 date (d), 1 dimension (d), 1 measure (m).
- Recipe: Columns: MONTH(Order Date) (d). Rows: calculated rank below. Colour: Category. Marks: Line and Circle, Dual Axis. Reverse the Rows axis. Label the first and last points.
```
RANK(SUM([Sales]))
```
- Settings: Compute Using Category.
- Mistake: Compute Using Table (Across), which ranks months not categories.

### Dumbbell chart
- Use: two values per category and the gap.
- Avoid: more than two values.
- Fields: 1 dimension (d), 2 measures (m).
- Recipe: Rows: Region (d). Columns: Measure Values. Filter Measure Names to the two values. Marks: Circle, Colour Measure Names. Add a second Measure Values to Columns, Dual Axis. On the second layer set Marks: Line, Path Measure Names, Detail Region. Synchronise.
- Mistake: Path set to Region, so lines do not join the pair.

### Lollipop chart
- Use: a ranked list where bars are a wall of ink.
- Avoid: close values.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Rows: Customer Name (d). Columns: SUM(Sales) twice. Dual Axis. First layer: Bar with Size small. Second: Circle. Synchronize. Sort descending.
- Mistake: forgetting to synchronise, so the circle drifts off the bar.

### Funnel chart
- Use: stage by stage drop off.
- Avoid: stages not in order.
- Fields: 1 dimension (d) in stage order, 1 measure (m).
- Recipe: Rows: Stage (d), sorted by stage number. Columns: SUM(Value), then a second copy with the calculated field below. Marks: Bar for both. Hide the axes and colour on one measure. Label the values.
```
-SUM([Value])
```
- Mistake: sorting by value rather than the stage order.

### Radial bar chart
- Use: compact ranking in a circle.
- Avoid: precise reads.
- Fields: 1 dimension (d), 1 measure (m), densified points.
- Recipe: Build 100 points per bar with a scaffold table or bins. Rows: Y calc. Columns: X calc. Marks: Line (polygon on request). Path: point order. Detail: Category. Hide the axes. Fit square.
```
[X] = ([Radius]+[Bar Index])*COS([Theta])
[Y] = ([Radius]+[Bar Index])*SIN([Theta])
[Theta] = [Point Order]/100*[Pct of Max]*3*PI()/2
```
- Mistake: unequal axis ranges squash the circle. Use a Fixed axis with equal span on both.

### Sankey diagram
- Use: volume moving between stages.
- Avoid: a flow with few links (use a stacked bar).
- Fields: source (d), target (d), value (m), plus densified bins.
- Recipe: Densify with a bin field t from 0 to 48. Columns: [t] (m). Rows: [Curve]. Marks: Line, Path [t], Detail Link. Colour: Source. Size: SUM(Value) via a second sheet for bar nodes, then dashboard float.
```
[t] = ([Bin]-24)/4
[Sigmoid] = 1/(1+EXP(1-[t]))
[Curve] = [Y Source]+([Y Target]-[Y Source])*[Sigmoid]
```
- Mistake: forgetting to densify, so lines are straight.

### Small multiples (trellis)
- Use: one chart per category on equal scales.
- Avoid: more than 12 panels.
- Fields: 1 or 2 dimensions (d), 1 or more measures.
- Recipe: Rows: Region (d). Columns: Category (d). Fixed axes. Marks: Line. Or a wrapped grid with the calcs below.
```
[Col] = (INDEX()-1)%4
[Row] = INT((INDEX()-1)/4)
```
- Settings: both calcs Compute Using Region.
- Mistake: independent axes make the panels look similar when they are not.

### Sparkline
- Use: many small trends.
- Avoid: when readers need a value.
- Fields: 1 date (m), 1 measure (m), 1 dimension (d).
- Recipe: Rows: Region (d). Columns: WEEK(Order Date) (m). Rows: SUM(Sales). Marks: Line. Hide axes. Fit Entire View.
- Mistake: shared axes flatten smaller rows.

### Calendar heatmap
- Use: a daily pattern across weeks.
- Avoid: long periods without a sort.
- Fields: 1 date (d), 1 measure (m).
- Recipe: Columns: WEEK(Order Date) (d). Rows: DATENAME('weekday',[Order Date]) (d). Marks: Square. Colour: SUM(Sales). Small multiple by MONTH.
- Mistake: week number not aligned to the month.

### Waffle chart
- Use: one share out of 100.
- Avoid: several shares.
- Fields: scaffold 100 rows.
- Recipe: Columns: [X]. Rows: [Y]. Marks: Square. Colour: [Status]. Detail: [Id]. Hide axes.
```
[X] = ([Id]-1)%10
[Y] = INT(([Id]-1)/10)
[Status] = IF [Id] <= ROUND([Share]*100) THEN 'On' ELSE 'Off' END
```
- Mistake: forgetting to Rows reverse so the grid fills top down.

### Control chart (process chart)
- Use: watch a process against limits.
- Avoid: small samples.
- Fields: 1 date (m), 1 measure (m).
- Recipe: Columns: DAY(Date). Rows: SUM(Value). Marks: Line. Reference Lines from the calcs below.
```
Mean = WINDOW_AVG(SUM([Value]))
UCL = WINDOW_AVG(SUM([Value]))+3*WINDOW_STDEV(SUM([Value]))
LCL = WINDOW_AVG(SUM([Value]))-3*WINDOW_STDEV(SUM([Value]))
```
- Settings: Compute Using Table (Across).
- Mistake: control limits from the displayed range, not a baseline period.

### BAN KPI tile
- Use: one number with a comparison.
- Avoid: alone with no context.
- Fields: 1 or 2 measures (m).
- Recipe: Marks: Text. Text: SUM(Sales) and the % vs target. Colour: [Above Target] (d). Fit Entire View.
```
[Above Target] = SUM([Sales]) >= SUM([Target])
```
- Mistake: colour on the value itself, which hurts reading.

### KPI with arrows
- Use: the direction of change.
- Avoid: no comparison base.
- Fields: 2 measures (m).
- Recipe: Marks: Text. Text: the calc below. Colour: same calc.
```
IF SUM([Sales]) >= SUM([Sales PY]) THEN "▲" ELSE "▼" END
```
- Mistake: colour only. Add arrows for readers who cannot see colour.

### Jitter (strip) plot
- Use: all points in a category.
- Avoid: large counts.
- Fields: 1 dimension (d), 1 measure (m), 1 ID (d).
- Recipe: Columns: Category (d) then the jitter calc. Rows: SUM(Sales). Detail: Row ID. Marks: Circle at 50 per cent opacity.
```
[Jitter] = ([Row ID] % 11) / 11
```
- Mistake: RANDOM() changes at every refresh. Use the fixed formula.

### Diverging bar chart
- Use: positive and negative on a centred line.
- Avoid: no clear centre.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Rows: Question. Columns: [Signed]. Colour: Sentiment. Marks: Bar. Sort by net.
```
IF [Sentiment]="Negative" THEN -[Pct] ELSE [Pct] END
```
- Mistake: stacking order puts negative values in the wrong sequence.

### Marimekko chart
- Use: share and size of two categories together.
- Avoid: many columns.
- Fields: 2 dimensions (d), 1 measure (m).
- Recipe: Columns: [Start]. Rows: SUM(Sales) as Percent of Total with Compute Using Segment. Size: SUM(Sales). Colour: Segment. Detail: Region. Marks: Bar.
```
RUNNING_SUM(SUM([Sales]))-SUM([Sales])
```
- Settings: Compute Using Region for Start.
- Mistake: Marks on Automatic, so Size does nothing.

### Butterfly (tornado) chart
- Use: two sides back to back.
- Avoid: more than two groups.
- Fields: 1 dimension (d), 2 measures (m).
- Recipe: Rows: Age Band. Columns: [Left], SUM([Female]). Marks: Bar. Reverse the left axis or use the calc below. Hide axes.
```
[Left] = -SUM([Male])
```
- Mistake: unsynchronised axes distort one side.

### Timeline
- Use: events on a time line.
- Avoid: dense events.
- Fields: 1 date (m), 1 dimension (d).
- Recipe: Columns: Exact Date (m). Rows: Lane (d). Marks: Circle. Label: Event. Optional Gantt bars for ranges.
- Mistake: discrete date, so spacing is not to scale.

### Gantt variants
- Use: progress, capacity or milestones.
- Avoid: a blur of tasks.
- Fields: start (m), end (m), task (d).
- Recipe: Columns: DAY(Start). Rows: Task. Marks: Gantt Bar. Size: duration calc. For progress add a second layer, Dual Axis, with Size the completed days.
```
[Duration] = DATEDIFF('day',[Start],[End])
[Done Days] = [Duration]*[Pct Complete]
```
- Mistake: Size on SUM(Start), so the bar is wrong.

### Rounded bars
- Use: softer ranking bars.
- Avoid: formal reports.
- Fields: 1 dimension (d), 1 measure (m).
- Recipe: Rows: Category. Columns: SUM(Sales) and MIN(0) and SUM(Sales). Dual axis. Layers: Bar thin, Circle at 0, Circle at the value. Synchronize. Match Size of circles to bar thickness.
- Mistake: unsynchronised axes put circles off the bar ends.

### Population pyramid
Derived (not in the fetched pages)
- Use: two groups across age bands.
- Avoid: no shared bands.
- Fields: 1 dimension (d), 2 measures (m).
- Recipe: see Butterfly. Colour: Sex. Sort age bands in order.
- Mistake: bands sorted alphabetically.
