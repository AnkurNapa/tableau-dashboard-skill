# Migrate Tableau to Power BI: reference

Checked 13 Nov 2026.

A how-to for the work that follows the question set in `intake.md` (Set B). It maps Tableau items to Power BI items, translates formulas and lists what to test. It makes no claim about which product suits a team better.

## Sources

Microsoft Learn (read on the check date):
- https://learn.microsoft.com/en-us/dax/calculate-function-dax (CALCULATE, REMOVEFILTERS, ALL, ALLEXCEPT, KEEPFILTERS, context transition)
- https://learn.microsoft.com/en-us/dax/window-function-dax
- https://learn.microsoft.com/en-us/dax/offset-function-dax
- https://learn.microsoft.com/en-us/dax/rankx-function-dax
- https://learn.microsoft.com/en-us/dax/dateadd-function-dax
- https://learn.microsoft.com/en-us/dax/sameperiodlastyear-function-dax
- https://learn.microsoft.com/en-us/dax/totalytd-function-dax
- https://learn.microsoft.com/en-us/dax/userprincipalname-function-dax
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-visual-calculations-overview
- https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-what-if
- https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security
- https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-overview

Tableau Help (read on the check date):
- https://help.tableau.com/current/pro/desktop/en-us/order_of_operations.htm (text gives only part of the order; the full diagram is an image)
- https://help.tableau.com/current/api/metadata_api/en-us/index.html
- https://help.tableau.com/current/api/metadata_api/en-us/docs/meta_api_start.html

Not read as separate pages: SUMMARIZE, ADDCOLUMNS, INDEX, TOPN, SELECTEDVALUE, COALESCE, Power Query, Direct Lake, Power BI subscriptions, Tableau Pulse, Tableau Data Apps. Anything that rests on those is labelled "derived" or "not verified".

## Labels

- verified: the function syntax or the pattern appears on the cited learn.microsoft.com page. The field names are still placeholders.
- derived: built from verified functions but not printed in that form on an official page. Test on real data before it goes in a client model.
- not verified: written from working knowledge. Check the current docs.

Names such as `Sales[Amount]`, `Customer[CustomerKey]` and `'Date'[Date]` are placeholders. Assume a star schema, a Date table marked as the date table and a measure `[Sales Amount] = SUM(Sales[Amount])`.

## 1. Concept map

Read each row as a starting point, not a one to one rule.

| Tableau | Power BI | Note |
|---|---|---|
| Data source (live) | Semantic model in DirectQuery mode, or a live connection to a shared model | Check source support for DirectQuery. Some DAX is not allowed in calculated columns or RLS rules under DirectQuery (see the CALCULATE page). |
| Extract (.hyper) | Import mode, or Direct Lake over OneLake tables | Import keeps a compressed copy in the model. Direct Lake reads Delta tables in OneLake. Direct Lake is not verified here. |
| Extract refresh schedule | Scheduled refresh, or incremental refresh on a date column | Set refresh after the source load finishes. |
| Published data source | Shared semantic model in a workspace | Migrate these first. Reports then connect to one model. |
| Relationships (logical layer) | Model relationships | Set cardinality and filter direction on purpose. See gotchas for many to many. |
| Physical joins and unions | Power Query merge and append, or warehouse views | Do joins upstream where the grain allows. |
| Workbook | Report (.pbix or PBIP project) | A Tableau workbook with many sheets is one report with several pages. |
| Sheet (worksheet) | Visual on a report page | A sheet is one chart. A page holds many visuals. |
| Dashboard | Report page | Layout containers become alignment, groups and the selection pane. |
| Story | Bookmarks plus buttons, or a page navigator | There is no story object. |
| Calculated field (row level) | Calculated column, or a measure when the result must aggregate | Prefer Power Query or the source for row level logic. |
| Calculated field (aggregate) | Measure | Measures react to filter context. |
| LOD expression | CALCULATE with filter modifiers, or an iterator over VALUES | See section 2. |
| Table calculation | Visual calculation, or a window function measure | See section 3. |
| Parameter (value) | What-if parameter (numeric range) or a disconnected table with SELECTEDVALUE | The what-if parameter creates a table and a measure. |
| Parameter (swap measure or dimension) | Field parameter | Lists fields in a slicer. Needs explicit measures. |
| Parameter action | Slicer or field parameter, or a button with a bookmark | No click to set a value action. Plan a redesign. |
| Set | Calculated column flag, a measure with a threshold or a disconnected selection table | Dynamic sets become measures. |
| Set action | Cross filtering, or a slicer on a flag column | Not a direct match. |
| Group | Group in the field list, or a mapping table | A mapping table survives refresh and is easier to audit. |
| Bin | Bin group on a numeric column, or a binned column in Power Query | |
| Hierarchy | Hierarchy in the model (Year, Quarter, Month) | Drill down is a visual feature. |
| Quick filter | Slicer or filter pane entry | |
| Dimension filter | Visual, page or report filter | |
| Context filter | A visual, page or report filter left out of REMOVEFILTERS lists | See section 2. |
| Data source filter | Row filter in Power Query, a source view or an RLS rule | |
| Extract filter | Row filter in Power Query, or a source query | |
| Filter action | Cross filtering and cross highlighting between visuals | Edit interactions to switch it off per visual. |
| Highlight action | Cross highlighting | |
| URL action | Button or visual link with a URL, or a web URL data category on a column | |
| Go to sheet action | Page navigation button, or drillthrough | |
| Dynamic zone visibility | Bookmarks with the selection pane, or a field parameter that swaps visuals | |
| Viz in tooltip | Tooltip page | Field parameters cannot be the linked fields of a tooltip page. |
| Prep flow | Power Query, or Dataflow Gen2 for a shared and scheduled flow | Dataflow Gen2 is Power Query based and can write to several destinations. |
| User filter (RLS) | RLS role with USERPRINCIPALNAME and an entitlement table | See section 5. |
| ISMEMBEROF | Entra security group assigned to an RLS role | Microsoft 365 groups are not supported for RLS membership. |
| Data policy (virtual connection) | RLS on the semantic model, or security at the warehouse or lakehouse | Not a direct match. Decide the layer first. |
| Site | Tenant | Tenant settings carry the admin controls. |
| Project | Workspace, plus an app for distribution | Permissions move from project rules to workspace roles and app audiences. |
| Subscription | Email subscription on a report page | Check licence needs. Not verified here. |
| Data-driven alert | Data alert on a card or gauge, or Activator | Not verified here. |
| Pulse metric | Scorecard goal, or a measure in a report with an alert | Not verified here. Pulse has no one to one item. |
| Data App | Power BI app, embedded report or a Power Apps front end | Not verified here. Scope the interactions the app needs. |

## 2. Order of operations

### Tableau

The working order (from `calcs-and-viz.md`, with the parts confirmed on the Tableau Help page marked):
1. Extract filters.
2. Data source filters (confirmed).
3. Context filters (confirmed).
4. Top N filters and FIXED LODs. The page confirms FIXED runs before dimension filters.
5. Dimension filters (confirmed).
6. INCLUDE and EXCLUDE LODs, then measure filters.
7. Table calculations, which run after dimension filters (confirmed). Table calculation filters come last.

### DAX

A measure is evaluated once for each cell of the visual. The filter context for that cell is built from the row and column fields, slicers, visual, page and report filters, cross filtering and RLS. CALCULATE then edits that context (source: CALCULATE page):
- A filter on a column already in the context overwrites the existing filter on that column.
- KEEPFILTERS adds the new filter without removing the existing one.
- REMOVEFILTERS, ALL and ALLEXCEPT remove filters from the columns or tables named.
- With no filter arguments CALCULATE still turns a row context into a filter context.

RLS filters are applied by the engine for the viewer. Treat them as outside the reach of REMOVEFILTERS (the RLS page says only matching rows are visible).

### Why FIXED maps to CALCULATE with REMOVEFILTERS or ALLEXCEPT

A FIXED LOD is computed at a stated grain before dimension filters run. In DAX the matching move is to take the filter context the visual built and strip it back to the dimensions named in the LOD.
- `{FIXED [Customer] : SUM([Sales])}` keeps only the customer. Use ALLEXCEPT on the customer table, naming the customer key.
- `{FIXED : SUM([Sales])}` has no dimension. Use REMOVEFILTERS() with no argument, or REMOVEFILTERS on named tables.

Two traps (derived):
- ALLEXCEPT works on one table. Filters on other tables still reach the fact table through relationships. To clear a Product slicer from a customer level calculation, add REMOVEFILTERS(Product) as well.
- A FIXED LOD in Tableau still obeys context filters. A blanket REMOVEFILTERS removes those too.

### How context filters map

A Tableau context filter exists to run before FIXED and Top N. In Power BI keep the same filter as an ordinary filter and leave its column out of the REMOVEFILTERS or ALLEXCEPT list. Build the list from the dimension filters that must not reach the calculation. If a filter must apply to everything and never be removed (for example a legal entity), move it to Power Query, a source view or an RLS rule.

Top N needs the same care. A Top N set ranks before dimension filters in Tableau. In DAX the rank runs over whatever is left in context, so put REMOVEFILTERS or ALLSELECTED inside the rank on purpose (section 3).

## 3. Formula translations

Each block shows the Tableau formula first, then the DAX measure.

### COUNTD (derived)
```
COUNTD([Customer ID])
```
```dax
Customers = DISTINCTCOUNT(Sales[CustomerKey])
```

### Ratio of sums (derived)
```
SUM([Profit]) / SUM([Sales])
```
```dax
Margin % = DIVIDE(SUM(Sales[Profit]), SUM(Sales[Amount]))
```
DIVIDE returns BLANK on a zero denominator. See the gotchas on integer division and blanks.

### FIXED, one dimension (verified)
Source: the Customer Segment example on https://learn.microsoft.com/en-us/dax/calculate-function-dax uses ALLEXCEPT with context transition.
```
{FIXED [Customer ID] : SUM([Sales])}
```
```dax
Sales per Customer (fixed) =
CALCULATE(
    SUM(Sales[Amount]),
    ALLEXCEPT(Customer, Customer[CustomerKey]),
    REMOVEFILTERS(Product),
    REMOVEFILTERS('Date')
)
```
The ALLEXCEPT pattern is verified. The two extra REMOVEFILTERS lines are derived and depend on which dimension filters must not reach the number.

### FIXED, no dimension (verified)
Source: the Revenue % Total Channel example on the CALCULATE page uses REMOVEFILTERS inside CALCULATE.
```
{FIXED : SUM([Sales])}
```
```dax
Sales All Rows =
CALCULATE(SUM(Sales[Amount]), REMOVEFILTERS())
```
REMOVEFILTERS with no argument is derived from the documented forms (all filters, a column list or a table).

### INCLUDE (derived)
```
{INCLUDE [Customer ID] : SUM([Sales])}
```
Averaged in the view:
```dax
Avg Sales per Customer =
AVERAGEX(VALUES(Customer[CustomerKey]), [Sales Amount])
```

### EXCLUDE (derived)
```
{EXCLUDE [Category] : SUM([Sales])}
```
```dax
Sales Excl Category =
CALCULATE([Sales Amount], REMOVEFILTERS(Product[Category]))
```

### Percent of total (verified)
Source: Revenue % Total Channel on the CALCULATE page.
```
SUM([Sales]) / TOTAL(SUM([Sales]))
```
```dax
Sales % of Total =
DIVIDE(
    [Sales Amount],
    CALCULATE([Sales Amount], REMOVEFILTERS(Product[Category]))
)
```
TOTAL respects the filters in the view. To respect slicers but ignore the row fields, use ALLSELECTED instead of REMOVEFILTERS (see TOTAL below).

### Running total (verified)
Source: Example 2 on https://learn.microsoft.com/en-us/dax/window-function-dax and RUNNINGSUM on the visual calculations page.
```
RUNNING_SUM(SUM([Sales]))
```
Measure, restarting each fiscal year:
```dax
Running Sales =
SUMX(
    WINDOW(
        1, ABS, 0, REL,
        ALLSELECTED('Date'[Fiscal Year], 'Date'[Month Number Of Year]),
        PARTITIONBY('Date'[Fiscal Year])
    ),
    [Sales Amount]
)
```
Visual calculation:
```dax
Running sum = RUNNINGSUM([Sales Amount])
```
Add HIGHESTPARENT as the second argument to restart at the top level of the visual hierarchy.

### Moving average (verified shape, derived measure)
Source: Example 1 on the WINDOW page and MOVINGAVERAGE on the visual calculations page.
```
WINDOW_AVG(SUM([Sales]), -2, 0)
```
Visual calculation:
```dax
Moving avg = MOVINGAVERAGE([Sales Amount], 3)
```
Measure (derived from the WINDOW example):
```dax
Sales 3 Month Avg =
AVERAGEX(
    WINDOW(
        -2, REL, 0, REL,
        ALLSELECTED('Date'[Month Start]),
        ORDERBY('Date'[Month Start])
    ),
    [Sales Amount]
)
```
The window counts rows that exist in the axis, not calendar months. A month with no rows is skipped, as the WINDOW page notes.

### Rank (verified)
Source: https://learn.microsoft.com/en-us/dax/rankx-function-dax
```
RANK(SUM([Sales]))
RANK_DENSE(SUM([Sales]))
```
```dax
Sales Rank =
RANKX(ALLSELECTED(Product[Product]), [Sales Amount], , 0, Skip)

Sales Rank Dense =
RANKX(ALLSELECTED(Product[Product]), [Sales Amount], , 0, Dense)
```
Order 0 ranks high to low. Skip is the default and matches the Tableau competition rank. Dense matches RANK_DENSE. RANKX treats BLANK as zero.

### Difference from previous (verified)
Source: Example 4 on https://learn.microsoft.com/en-us/dax/offset-function-dax and PREVIOUS on the visual calculations page.
```
SUM([Sales]) - LOOKUP(SUM([Sales]), -1)
```
Visual calculation:
```dax
Vs previous = [Sales Amount] - PREVIOUS([Sales Amount])
```
Measure (derived from Example 2 of the OFFSET page):
```dax
Sales vs Previous Month =
[Sales Amount]
    - CALCULATE([Sales Amount], OFFSET(-1, , ORDERBY('Date'[Month Start])))
```
Time intelligence discourages DATEADD and similar functions inside visual calculations, so use OFFSET or PREVIOUS there.

### Year over year (verified)
Source: SAMEPERIODLASTYEAR page.
```
(ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)) / ABS(LOOKUP(ZN(SUM([Sales])), -1))
```
```dax
Sales PY =
CALCULATE([Sales Amount], SAMEPERIODLASTYEAR('Date'[Date]))

Sales YoY % =
DIVIDE([Sales Amount] - [Sales PY], [Sales PY])
```
Needs a contiguous Date table. DATEADD errors when the dates in context are not a contiguous interval (DATEADD page).

### Year to date (verified)
Source: TOTALYTD page.
```
RUNNING_SUM(SUM([Sales]))   // reset each year
```
```dax
Sales YTD = TOTALYTD([Sales Amount], 'Date'[Date])

Sales YTD Fiscal =
TOTALYTD([Sales Amount], 'Date'[Date], "3/31")
```
The third form passes a year end date as a string. The year part is ignored (TOTALYTD page).

### Prior year, by month shift (verified)
Source: DATEADD page.
```
DATEADD('year', -1, [Order Date])
```
```dax
Sales PY via DATEADD =
CALCULATE([Sales Amount], DATEADD('Date'[Date], -1, YEAR))
```
The interval is a keyword, not a quoted string. Shifts from the last two days of a month use extension semantics (DATEADD page).

### First purchase date (derived)
Tableau (see `formula-patterns.md`):
```
{FIXED [Customer ID] : MIN([Order Date])}
```
Calculated column on Customer (context transition, described on the CALCULATE page):
```dax
First Purchase Date =
CALCULATE(MIN(Sales[OrderDate]))
```
Measure:
```dax
First Purchase (measure) =
MINX(VALUES(Customer[CustomerKey]), CALCULATE(MIN(Sales[OrderDate])))
```

### Cohort month and retained customers (derived)
```
DATETRUNC('month', {FIXED [Customer ID] : MIN([Order Date])})
```
Calculated column on Customer:
```dax
Cohort Month =
DATE(YEAR([First Purchase Date]), MONTH([First Purchase Date]), 1)
```
Customers from a cohort who ordered in the selected month:
```dax
Retained Customers =
CALCULATE(
    DISTINCTCOUNT(Sales[CustomerKey]),
    KEEPFILTERS(FILTER(VALUES(Customer[CustomerKey]), Customer[Cohort Month] < MIN('Date'[Month Start])))
)
```
Test cohort counts against the Tableau view before trusting the percentages.

### IF, CASE, IIF, ZN, IFNULL (derived)
```
IF [Sales] > 100 THEN "High" ELSEIF [Sales] > 50 THEN "Mid" ELSE "Low" END
CASE [Region] WHEN "East" THEN 1 WHEN "West" THEN 2 ELSE 0 END
IIF([Profit] > 0, "Gain", "Loss")
ZN(SUM([Sales]))
IFNULL(SUM([Sales]), 0)
```
```dax
Band =
VAR s = [Sales Amount]
RETURN
    IF(s > 100, "High", IF(s > 50, "Mid", "Low"))

Region Code =
SWITCH(SELECTEDVALUE(Customer[Region]), "East", 1, "West", 2, 0)

Gain Loss = IF([Profit] > 0, "Gain", "Loss")

Sales ZN = COALESCE([Sales Amount], 0)
```
For a multi-branch test with conditions use SWITCH(TRUE(), cond1, result1, cond2, result2, default).

### Common string and date functions (derived)
| Tableau | DAX |
|---|---|
| `LEFT([x], 3)`, `MID([x], 2, 3)`, `RIGHT([x], 3)` | `LEFT(x, 3)`, `MID(x, 2, 3)`, `RIGHT(x, 3)` |
| `UPPER`, `LOWER`, `TRIM`, `LEN` | `UPPER`, `LOWER`, `TRIM`, `LEN` |
| `CONTAINS([x], "a")` | `CONTAINSSTRING(x, "a")` |
| `FIND([x], "a")` (1 based, 0 if absent) | `SEARCH("a", x, 1, 0)` |
| `REPLACE([x], "a", "b")` | `SUBSTITUTE(x, "a", "b")` |
| `[a] + " " + [b]` | `a & " " & b` |
| `STR([n])`, `FLOAT`, `INT` | `FORMAT(n, "0")`, `CONVERT`, `INT` |
| `YEAR`, `MONTH`, `DAY`, `TODAY()` | `YEAR`, `MONTH`, `DAY`, `TODAY()` |
| `DATETRUNC('month', [d])` | `DATE(YEAR(d), MONTH(d), 1)` or `STARTOFMONTH` over a date column |
| `DATEDIFF('day', [a], [b])` | `DATEDIFF(a, b, DAY)` |
| `DATEADD('month', 1, [d])` | `EDATE(d, 1)` for a single date. Use DATEADD only for date column shifts in time intelligence. |

### ATTR (derived)
```
ATTR([Region])
```
```dax
Region (single) =
SELECTEDVALUE(Customer[Region], "Multiple values")
```
Tableau shows an asterisk when the field has more than one value. SELECTEDVALUE returns the alternate result when the filter context holds zero or many values, so you choose the label.

### WINDOW_SUM (verified shape)
Source: WINDOW page.
```
WINDOW_SUM(SUM([Sales]), -2, 0)
```
```dax
Sales Last 3 Months =
SUMX(
    WINDOW(
        -2, REL, 0, REL,
        ALLSELECTED('Date'[Month Start]),
        ORDERBY('Date'[Month Start])
    ),
    [Sales Amount]
)
```
Tableau WINDOW_SUM(expr, FIRST(), 0) maps to `WINDOW(1, ABS, 0, REL, ...)`.

### LOOKUP (verified shape)
Source: OFFSET page.
```
LOOKUP(SUM([Sales]), -1)
```
```dax
Sales Previous Month =
CALCULATE([Sales Amount], OFFSET(-1, , ORDERBY('Date'[Month Start])))
```
OFFSET returns an empty table when the shift lands outside the partition, so the first row is BLANK. Add PARTITIONBY to restart per year or per product.

### TOTAL (derived)
```
TOTAL(SUM([Sales]))
```
```dax
Sales Total in View =
CALCULATE([Sales Amount], ALLSELECTED())
```
ALLSELECTED keeps slicer and filter selections and drops the filters from the visual's row and column fields.

### Top N with Others (derived)
Create a disconnected table `TopN` (a numeric range or GENERATESERIES) and a slicer on it.
```
IF [Rank] <= [Top N] THEN [Product] ELSE "Others" END
```
```dax
Top N Selected = SELECTEDVALUE(TopN[N], 5)

Sales Top N =
VAR n = [Top N Selected]
VAR r = RANKX(ALLSELECTED(Product[Product]), [Sales Amount], , 0, Dense)
RETURN
    IF(r <= n, [Sales Amount])

Sales Others =
VAR n = [Top N Selected]
VAR topRows = TOPN(n, ALLSELECTED(Product[Product]), [Sales Amount])
RETURN
    CALCULATE([Sales Amount], ALLSELECTED(Product[Product]))
        - SUMX(topRows, [Sales Amount])
```
Show Top N in a chart and Others in a card or a total line. A single chart with an Others bar needs a helper column or table. See the gotcha on sort by calculation.

## 4. Interactivity

| Tableau | Power BI route | Steps and limits |
|---|---|---|
| Filter action | Cross filtering | On by default between visuals on a page. Use Edit interactions to turn it off for chosen pairs. |
| Highlight action | Cross highlighting | Same menu. Chosen per visual. |
| Go to sheet or dashboard | Page navigation button, or drillthrough | Drillthrough passes the selected values as filters to a target page. Field parameters cannot be the linked field of a drillthrough or tooltip page (field parameters page). |
| Parameter action | Slicer on a field parameter or a what-if parameter | No click to set action. A slicer, a button with a bookmark or a visual that cross filters a disconnected table are the options. |
| Set action | Cross filter a flag column, or a slicer | Plan a different interaction. |
| Dynamic zone visibility | Bookmarks plus the selection pane, or a field parameter that swaps the measure or axis | Bookmarks capture visibility, filter and slicer state as options. Test each bookmark after layout changes. |
| Viz in tooltip | Tooltip page | A small page sized as a tooltip, linked from the visual. |
| Swap measure with a parameter | Field parameter | Created from Modeling, New parameter, Fields. The DAX is a table of (name, NAMEOF reference, order) rows. Use explicit measures only. |
| Parameter as a number input | What-if parameter | Created from Modeling, New parameter, Numeric range. It makes a table and a measure. At most 1,000 unique values. Designed for measures in visuals. |
| Quick filters | Slicers | Sync slicers across pages with the sync pane. |
| Table calculation along a pane | Visual calculation | Edit mode on the visual. Not available on slicers or custom visuals. Cannot be pinned to dashboards or used with Publish to web. |

Field parameter DAX (verified from https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters):
```dax
Parameter = {
    ("Customer", NAMEOF('Customer'[Customer]), 0),
    ("Category", NAMEOF('Product'[Category]), 1),
    ("Color", NAMEOF('Product'[Color]), 2),
    ("Product", NAMEOF('Product'[Product]), 3)
}
```
What-if parameter measure (verified from https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-what-if):
```dax
Sales after Discount =
SUM(Sales[SalesAmount]) - (SUM(Sales[SalesAmount]) * 'Discount percentage'[Discount percentage Value])
```

Visual calculation limits to tell report authors (visual calculations page): no sorting or filtering on the calculated field; no reuse by copy and paste across visuals; no data categories. Exports leave the results out.

## 5. Data and security

### Connection mode

| Tableau | Power BI | Check |
|---|---|---|
| Extract | Import, or Direct Lake when the data already sits in OneLake Delta tables | Model size against the capacity limit. Refresh window. Direct Lake is not verified here. |
| Live connection | DirectQuery | Source speed per visual. Some DAX is blocked in calculated columns and RLS under DirectQuery. |
| Live to a published data source | Live connection to a shared semantic model | Add a local model if you need field parameters (field parameters page). |
| Extract plus incremental refresh | Incremental refresh on a date column | Not verified here. |

### Prep to Power Query or Dataflow Gen2

- A Prep flow that serves one report becomes Power Query steps in that model.
- A Prep flow that feeds many reports or runs on a schedule becomes a Dataflow Gen2 item or a warehouse or lakehouse pipeline. Dataflow Gen2 uses Power Query and can write to destinations such as a Fabric Lakehouse, a Fabric Warehouse or an Azure SQL database. It needs a Fabric or Premium capacity (Dataflow Gen2 page).
- Map steps one by one: Input to Get Data, Clean to column transforms, Aggregate to Group By, Join to Merge, Union to Append, Pivot to Pivot or Unpivot, Output to the dataflow destination.
- Check row counts after every step against the Prep output.

### Row level security

Tableau patterns and their targets:
- User filter on a manager field: a role filtering a mapping table on `[UserEmail] = USERPRINCIPALNAME()`.
- Entitlement table joined on user: the same mapping table, related to the dimension it limits.
- ISMEMBEROF: an Entra security group assigned to a role.
- USERNAME() or a user attribute: USERPRINCIPALNAME() returns the sign-in name (verified on the USERPRINCIPALNAME and RLS pages).

Entitlement table (derived):
```
Entitlement(UserEmail, Region)
```
Role "Regional" on the `Entitlement` table:
```dax
[UserEmail] = USERPRINCIPALNAME()
```
Then a relationship from `Entitlement[Region]` to `Customer[Region]` that filters the customer table. For a many user to many region case the relationship must carry the filter to the dimension. For the case where the filter must flow the other way, turn on Apply security filter in both directions on that one relationship (RLS page). Test performance after enabling it.

Facts to keep from the RLS page:
- Roles are defined in Power BI Desktop (Modeling, Manage roles), members are added in the service.
- RLS applies to workspace Viewers only. Admin, Member and Contributor roles bypass it.
- A user in several roles sees the union of those roles.
- Microsoft 365 groups cannot be role members. Distribution, mail-enabled and Entra security groups can.
- Service principals cannot be added to a role.
- Direct Lake models support RLS. If a query falls back to DirectQuery the filters still apply.
- RLS cannot hide a column. Use object level security for that.

### Testing roles

1. In the service, open the model, choose Security, then Test as role for each role and for a named person.
2. Show `USERPRINCIPALNAME()` in a card on a test page to see the exact value users get.
3. Test with an actual Viewer account. Test as role uses your own identity for dynamic rules, so it cannot show what an external guest sees.
4. Test as role does not work for DirectQuery models with single sign-on.
5. Compare row counts per user against the Tableau user filter result for at least one user per role.

## 6. Runbook

### 1. Inventory with the Metadata API

The endpoint is `/api/metadata/graphql` on the Tableau host (verified on the Metadata API start page). On Tableau Server the metadata service must be enabled first. Field names below are derived from the schema as used in `cookbook.md` and `dashboard-design.md`. Check them against the reference for your version.
```graphql
query WorkbookInventory {
  workbooks {
    name
    projectName
    owner { username }
    sheets { name }
    upstreamDatasources { name }
    embeddedDatasources { name }
    upstreamDatabases { name connectionType }
  }
}
```
Calculated field audit for one data source (same caveat):
```graphql
query CalcInventory {
  calculatedFields {
    name
    formula
    datasource { name }
    downstreamWorkbooks { name }
  }
}
```
Usage counts are not in the Metadata API as far as these pages show. Take view counts from the REST API usage statistics or Admin Insights. Not verified here.

### 2. Rank

Score each workbook on two axes and write them into `brief.md`.
- Usage: views in the last 90 days, distinct viewers.
- Complexity: number of calculated fields, count of LODs and table calcs, parameters and actions, data sources and Prep flows, RLS present or not.

Migrate high usage and low complexity first to build the pattern. Retire workbooks with no use rather than moving them. Ask the owner before dropping one.

### 3. Thin slice

One shared semantic model with its Date table, its measures and its RLS roles, plus the most used report built on it. Ship that slice to a small group before any second workbook starts.

### 4. Reconciliation checklist

For each KPI, one row in a sheet:
- [ ] Same filter state in both tools (same dates, same slicers, same user).
- [ ] Totals match at grand total, at each level of the main hierarchy and for the latest and earliest period.
- [ ] Row counts match at the fact table and at each dimension.
- [ ] Distinct counts match (COUNTD against DISTINCTCOUNT).
- [ ] Ratios match with the same denominator definition.
- [ ] Blank and null handling checked on at least one empty period and one empty member.
- [ ] Time intelligence checked at a year end, a month end and a leap day.
- [ ] Ranks checked at a tie.
- [ ] Each RLS role checked with one named user against the old user filter.
- [ ] Refresh time and visual load time recorded against the targets in `brief.md`.
- [ ] Owner signs the sheet.

Record any gap with its cause (definition, data, logic) in `lessons.md`.

### 5. Cut over

1. Freeze changes to the Tableau workbook.
2. Run both tools side by side for the agreed period. Show the reconciliation sheet to the owner.
3. Move subscriptions, alerts and embeds. Update links and bookmarks.
4. Train the audience on the slicer and drill patterns, which differ from Tableau.
5. Announce a date after which the Tableau view is read only.

### 6. Decommission

1. Mark the workbook as migrated, with the report link, in its description.
2. Set it to read only for a fixed period, then hide it.
3. Archive the .twbx and the Prep flows with the reconciliation sheet.
4. Remove extract refreshes and schedules to free capacity.
5. Review access, licences and the project structure for the retired content.

## 7. Gotchas

- Blanks and nulls. Tableau shows Null and counts it only where asked. DAX BLANK is not zero in a visual, but RANKX treats BLANK as zero and arithmetic treats BLANK as zero in sums. Decide per measure whether an empty cell stays empty. Use COALESCE only where a zero is meant.
- Integer division. Test division with whole numbers in both tools. Use DIVIDE with an explicit alternate result so a zero denominator never shows an error. Check the data type of the result column (fixed decimal against decimal) before comparing ratios.
- The ATTR asterisk. Tableau shows `*` for several values. SELECTEDVALUE returns BLANK unless you give an alternate. Pick a label such as "Multiple values".
- Blending. A Tableau blend links on shared fields at view level and aggregates the secondary source first. In Power BI model the link as a relationship, with a bridge dimension if both sides have different grains. Expect different results where blend fields were not unique.
- Dual axis. Power BI has combo charts for line plus column. A dual axis with two different mark types on the same scale may need a secondary axis setting. Synchronise the axes on purpose or the shapes will mislead.
- Maps. Tableau geocodes with built in roles. Power BI map visuals read latitude and longitude or location text and may geocode differently. Compare a sample of places. Store coordinates in the model when exactness matters.
- Sort by calculation. A visual sorts by a field or a measure shown in it. Sorting a column by a measure that is not in the visual needs a helper column or a sort by column setting in the model. A rank used for sorting needs the ranked field on the visual.
- Date hierarchies. Tableau builds date levels on any date field. Power BI auto date/time builds hidden tables that can bloat a model. Use one marked Date table and your own hierarchy. With field parameters, auto date/time hierarchies lose the hierarchy behaviour, so use explicit levels (field parameters page).
- Time intelligence needs a contiguous Date table. DATEADD errors when the dates in context are not contiguous (DATEADD page).
- Many to many. Tableau relationships handle many to many at query time. Power BI supports many to many relationships too but filter direction and ambiguity need design. Prefer a bridge table with single direction filters and test totals both ways.
- Context transition. A measure inside an iterator triggers context transition. A calculated column using an aggregate needs CALCULATE (CALCULATE page).
- RLS and USERELATIONSHIP. USERELATIONSHIP in DAX can cause errors when RLS is on (RLS page). Redesign those measures.
- Totals. A Tableau grand total recomputes the formula at that level. A DAX measure also evaluates at the total level, so a ratio or distinct count can differ from the sum of rows. Check totals on every KPI.
- Viz level filters. A Tableau filter can sit on a measure after aggregation. In Power BI use a visual level filter on a measure, or build the logic into the measure.
