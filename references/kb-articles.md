# Tableau Knowledge Base digest for dashboard builds

Source: official Tableau Knowledge Base articles hosted on help.salesforce.com. Checked 12 Nov 2026.

- Articles read: 111 (108 of the 109 first picked, plus 3 added: 001473875 cache settings, 005132046 WebGL contexts, 001474406 Prep memory).
- Read per theme: LOD and order of operations 14, table calcs 12, totals 6, nulls errors and data types 17, dates and fiscal 12, filters Top N and sets 8, actions and navigation 15, parameters formatting colour and sources 11, charts axes and maps 14, dashboards publishing and performance 6 (some articles sit under more than one theme, so the sum is higher than 111).
- Failed: 1. ID 002113881 returned "page not found".
- Skipped: 88 of the 200 links. Reasons: server admin, TSM, SAML, LDAP, licences, install and Log4j (about 35); Salesforce and Trailhead items such as exam guides, certification, support numbers and Data Cloud (about 20); connectors and drivers (about 10); Tableau Pulse and Tableau Next (about 8); Prep internals that are not about calculations (about 8); Cloud admin errors (about 7).
- Version notes: every entry says "Applies to" only where the article states a version. Most fixes are version independent.
- Raw page text was kept outside the skill folder. Formulas below are verbatim except for white space.

## 1. Level of detail (LOD) and order of operations

### Calculations with FIXED expression return unexpected results when filtered
- ID 001473037 | https://help.salesforce.com/s/articleView?language=en_US&id=001473037&type=1
- Symptom: a dimension filter does not filter a FIXED calculation, or a FIXED result still moves with a filter that is not in its declaration.
- Cause: order of operations is context filters, FIXED, dimension filters, INCLUDE/EXCLUDE, then measure and table calc filters. FIXED is computed per value of the declared dimensions. It does not "ignore" filters: it repeats one value over many rows. If any of those rows survive the filter the whole value shows.
- Fix scenario 1 (FIXED should be filtered): (1) Add the filter to context. (2) Add the filtered field to the FIXED declaration. (3) Switch to INCLUDE or EXCLUDE. INCLUDE/EXCLUDE are not filtered by measure or table calc filters. A FIXED inside another context filter is not filtered by option 1.
- Fix scenario 2 (FIXED should not be filtered but is): use the "replace NULL or missing data with zeros or existing data" options.
```
{ FIXED [Category] : SUM([Sales]) }
{ FIXED [Category], [Region] : SUM([Sales]) }
{ FIXED [State] : SUM([Sales]) }
```
- Note: State with sales only in a filtered-out Category returns no value at all.

### Incorrect data with FIXED LOD filters on a published data source (Server)
- ID 005232695 | https://help.salesforce.com/s/articleView?language=en_US&id=005232695&type=1
- Symptom: on Server, two views using different FIXED LODs as filters show each other's totals when opened one after the other.
- Cause: cache collision when the workbook uses a published data source and the measure aggregation is "Automatic". Not seen with an embedded extract.
- Fix: set the measure aggregation to Sum in Desktop and republish, or replace the FIXED filter with a set.
```
{ FIXED [field A] : MAX(IIF([field B] = 'Value X', 1, 0)) }
MAX(IIF([field B] = 'Value X', 1, 0)) = 1
```
- Note: the second formula is the set condition (By formula), used with IN on Filters. Defect under review at time of writing.

### Using LOD in a CASE or IF statement returns higher than expected results
- ID 001473493 | https://help.salesforce.com/s/articleView?language=en_US&id=001473493&type=1
- Symptom: a CASE or IF that returns an LOD gives inflated totals.
- Cause: because the CASE references a dimension, Tableau does not treat the field as a pure LOD, so it re-aggregates the repeated LOD value in the view.
- Fix: option 1, divide the LOD by SUM([Number of Records]). Option 2, aggregate inside the branch and aggregate the test.
```
CASE [Category]
WHEN "Office Supplies"
THEN { INCLUDE [Customer Name]: MAX([Sales])/ SUM([Number of Records])}
END
```
```
CASE MIN( [Category] )
WHEN "Office Supplies"
THEN SUM( { INCLUDE [Customer Name]:MAX([Sales])} )
END
```

### Unable to convert measure to dimension
- ID 001473640 | https://help.salesforce.com/s/articleView?language=en_US&id=001473640&type=1
- Symptom: a calculated field is a measure and "Convert to Dimension" is greyed out.
- Cause: any aggregation makes the field dynamic. Only non-aggregate calcs (FIXED, row fields, parameters, literals) can be dimensions.
- Fix: wrap in FIXED; remove the aggregation if the grain is already one row; use a Tableau bin; do it in Prep; join instead of blend (secondary fields are always aggregated). Table calcs can never become dimensions. ATTR() cannot go inside FIXED: use MIN() when the fixed grain has one value.
```
IF { FIXED [Region] : SUM( [Sales] ) } < 100
THEN "Low"
ELSE "High"
END
```
```
{ FIXED [Order ID] : MIN( [Category] ) } + " value"
```

### Calculating rank at a level other than the highest level of granularity
- ID 001473147 | https://help.salesforce.com/s/articleView?language=en_US&id=001473147&type=1
- Symptom: RANK or INDEX on a dimension that is not the last one on Rows gives wrong ranks.
- Cause: table calcs cannot ignore a field in the view, so the lowest level always affects them.
- Fix: aggregate to the wanted level with an LOD, then rank it. In Edit Table Calculation choose Specific Dimensions, tick all, put the partition dimension (Region) on top and restart every Region. Ties share a rank with RANK_DENSE: use INDEX with a custom sort for unique ranks.
```
{ EXCLUDE [State] : SUM( [Sales] ) }
RANK_DENSE( SUM( [Sales per Sub-Category] ) )
INDEX()
```

### Unexpected results of new and repeat counts in a view
- ID 001497762 | https://help.salesforce.com/s/articleView?language=en_US&id=001497762&type=1
- Symptom: new and repeat customer counts by date both count the same customer on their first day.
- Cause: different granularity of the data.
- Fix: fix the first purchase date per customer, then label each row.
```
{ FIXED [Customer] : MIN(DATE([Date])) }
```
```
IF DATE([Date]) = [First Purchase Date] THEN "New"
ELSE "Repeat"
END
```

### Conditionally show or hide parameter controls, filters, web objects or legends
- ID 001473228 | https://help.salesforce.com/s/articleView?language=en_US&id=001473228&type=1
- Symptom: when a dashboard hides a sheet by parameter or until a filter action fires, its filters, legends and parameter controls still show.
- Fix: Dynamic Zone Visibility (Desktop 2022.3 and later): put the sheet and its controls in one container and set "Control visibility using zones" to a Boolean field. For "show after click", build a set and a Change Set Values action, then use the Boolean below. Older fallback: show only relevant values and hide filter titles (not for dropdowns, leaves white space).
```
{ FIXED : MAX([Region Set])}
```

### Hide some dimension member subtotals when there is only one
- ID 001473542 | https://help.salesforce.com/s/articleView?language=en_US&id=001473542&type=1
- Symptom: subtotals cannot be switched off per member when a member has one row.
- Fix: right-click the single sub-header and Hide, or swap two sheets (subtotals on and off) with this Boolean on the Filters shelf of both (True on one, False on the other).
```
ATTR( {EXCLUDE [dimensions], [in], [view]: COUNTD([subtotal dimension])} ) > 1
```

### Tableau Prep: FIXED not supported in older versions
- ID 001456881 | https://help.salesforce.com/s/articleView?language=en_US&id=001456881&type=1
- Fix: Aggregate on Order ID with SUM(Sales), then inner join back on Order ID and remove the duplicate key.
```
{FIXED [Order ID]: SUM([Sales])}
```

### Long flow time from many FIXED calcs in one Prep cleaning step
- ID 004464651 | https://help.salesforce.com/s/articleView?language=en_US&id=004464651&type=1
- Symptom: a cleaning step with about 50 FIXED LODs never completes.
- Fix: delete unneeded ones; split them across parallel cleaning steps and inner join on a unique Row Id.

### FIXED in Prep gives wrong values with ROW_NUMBER (and output changes each run)
- IDs 001497700 and 001498512 | https://help.salesforce.com/s/articleView?language=en_US&id=001497700&type=1 and https://help.salesforce.com/s/articleView?language=en_US&id=001498512&type=1
- Cause: ROW_NUMBER over a non-unique PARTITION or ORDERBY has no guaranteed order, so numbers change between runs.
- Fix: use Source Row Number (Prep 2023.1 and later); add more fields to ORDERBY; drop RowNumber from the FIXED; output after the Clean step so the number becomes static.
```
{ FIXED [RowNumber],[Month]: MAX([Value])}
```

### Lookup table calculation in Prep
- ID 001471487 | https://help.salesforce.com/s/articleView?language=en_US&id=001471487&type=1
- Applies to: LOOKUP exists in Prep 2023.2 and later. Earlier: shifted self-join.
```
{ ORDERBY [Order Date] ASC : ROW_NUMBER() }
[Row Number] + 1
```
- Note: after the join set the default aggregation of the shifted field to Average, or SUM duplicates by orders per day.

### Calculations show "Undefined" in the data preview
- ID 001471451 | https://help.salesforce.com/s/articleView?language=en_US&id=001471451&type=1
- Cause and fix: by design. LOD and table calcs only mean something at the view level of detail. No action needed.

## 2. Table calculations

### Table calculation becomes invalid or unexpected after adding or removing a dimension
- ID 001471540 | https://help.salesforce.com/s/articleView?language=en_US&id=001471540&type=1
- Symptom: error "The table calculation for {calculation} requires a field that is missing. Please add the missing field to the view."
- Cause: every non-aggregated dimension in the view either partitions or addresses a table calc. Changing dimensions changes its level of detail.
- Fix: Edit Table Calculation and untick the red dimension, or add the extra dimension as Measure > Minimum (aggregated dimensions do not partition), or change the Compute Using settings.

### Table calc results change after converting a live connection to an extract
- ID 001474595 | https://help.salesforce.com/s/articleView?language=en_US&id=001474595&type=1
- Cause: row order is not guaranteed across live to extract. Relative directions such as Table (across) can change.
- Fix: put a unique row id on Detail and compute using Specific Dimensions, never Table (across) on a scatter.

### Edit Table Calculation missing from the menu
- ID 001497805 | https://help.salesforce.com/s/articleView?language=en_US&id=001497805&type=1
- Cause: Show Forecast is on. Fix: Analysis > Forecast > untick Show Forecast, or Clear Sheet.

### Calculating the difference between two values of one measure
- ID 001473029 | https://help.salesforce.com/s/articleView?language=en_US&id=001473029&type=1
- Fix: duplicate the sheet, use LOOKUP with an offset, then keep only the last column with a filter.
```
SUM([Sales]) - LOOKUP(ZN(SUM([Sales])), -2)
LAST() = 0
```
- Alternative: isolate each year in its own calculated field and subtract: `SUM([2015 Sales]) - SUM([2013 Sales])`.

### Year-over-year growth compares the wrong parts when years are incomplete
- ID 001473562 | https://help.salesforce.com/s/articleView?language=en_US&id=001473562&type=1
- Cause: table calcs use the index of values in the view, not the date part. A year starting in March lines up with a year starting in January.
- Fix: edit the quick table calc in the shelf, change both -1 offsets to -4 (quarters) and set "At the level" to Quarter of Date.

### Table calc filter "Apply to totals" fails with INDEX or RANK
- ID 001470631 | https://help.salesforce.com/s/articleView?language=en_US&id=001470631&type=1
- Cause: in the grand total with a down direction, INDEX() and RANK() are always the first or only value (SIZE() returns 1).
- Fix: build total and crosstab as separate sheets and combine them on a dashboard.

### Display rank based on the grand total in a crosstab
- ID 001496845 | https://help.salesforce.com/s/articleView?language=en_US&id=001496845&type=1
- Cause: rank fields must be discrete. Discrete fields cannot show totals.
- Fix: compute the total as a field, make both discrete, rank it, place Rank far left on Rows and Grand Total right-most, then set Edit Table Calculation.
```
TOTAL(SUM([Sales]))
RANK([Grand Total])
```

### Group by top N records
- ID 001463501 | https://help.salesforce.com/s/articleView?language=en_US&id=001463501&type=1
- Fix: Customer ID as dimension, parameter "Group by N records", then:
```
RANK(SUM([Sales]))
"Group" + STR(FLOAT(INT([Sales_RANK]/[Group by N records]-0.01))+1)
```
- Note: put GroupID left of Customer ID on Rows and sort Customer ID by Sales.

### Crosstab export problems with table calcs
- IDs 001472035 and 001474307
- 001472035 (https://help.salesforce.com/s/articleView?language=en_US&id=001472035&type=1): Export > Crosstab to Excel drops the alias of a table calc column when Measure Names is on Color. Remove Measure Names from Color or use absolute addressing.
- 001474307 (https://help.salesforce.com/s/articleView?language=en_US&id=001474307&type=1): CSV row order differs from the view when a table calc field plus a field on a Marks card is used. Use Copy > Crosstab or set the sort manually.

### View blank or frozen after removing dimensions used in table calcs (Table Extensions)
- ID 005237279 | https://help.salesforce.com/s/articleView?language=en_US&id=005237279&type=1
- Symptom: edit screen freezes, or the view opens blank with no error.
- Cause: Table Extensions need the dimensions named in Compute Using.
- Fix: right-click the measure, find the missing dimension and drag it back (for example Order Date to Detail).

### Prep: ROW_NUMBER and LOOKUP
- See section 1 (IDs 001497700, 001498512, 001471487).

## 3. Totals and subtotals

### Grand totals showing unexpected numbers with certain calculations
- ID 001473383 | https://help.salesforce.com/s/articleView?language=en_US&id=001473383&type=1
- Symptom: grand total of a COUNTD or ratio is not the sum of the rows (3 instead of 4).
- Cause: Total using Automatic recomputes the aggregation over the whole data, not over the displayed cells.
- Fix: Analysis > Totals > Total All Using > SUM, or compute at the row level with an LOD and sum it.
```
Sum({Include : COUNTD([Fruit])})
```

### Grand totals and subtotals do not show expected numbers with table calculations
- ID 001473705 | https://help.salesforce.com/s/articleView?language=en_US&id=001473705&type=1
- Symptom: "Total using" is greyed out and the total does not match the cells.
- Cause: table calcs only support Automatic totals. If the calc uses a non-additive aggregation (division, MIN, AVG) the total is not the sum of the view.
- Fix: rewrite with LOD functions so Total using is available, or add a copy of each Rows dimension to Detail and wrap the calc so only the first row sums the window.
```
IF FIRST() = 0
THEN WINDOW_SUM([Difference Between Average Sales])
END
```

### Showing a different calculation for subtotals and grand totals
- ID 001453768 | https://help.salesforce.com/s/articleView?language=en_US&id=001453768&type=1
- Fix: use WINDOW_COUNT of the dimension to detect which level is being drawn. The result depends on data, view and filters, so test it.
```
IF WINDOW_COUNT(ATTR([Category]))=0 THEN SUM([Quantity])
ELSEIF WINDOW_COUNT(ATTR([Category]))=3 THEN SUM([Profit])
ELSE SUM([Sales])
END
```

### Unable to turn on grand totals for discrete measures
- ID 001473781 | https://help.salesforce.com/s/articleView?language=en_US&id=001473781&type=1
- Symptom: blank total, or error "Cannot turn on Grand Totals for discrete measures."
- Cause: totals only work on continuous aggregated measures. The view needs at least one header. Continuous dimensions cannot be totalled.
- Fix: blank total, rebuild with Measure Names and Measure Values. Error, wrap in FIXED, convert to Dimension and use on Rows.
```
{ FIXED [Segment] : [Profit Ratio] }
```

### Actions using grand totals do not filter target sheets
- ID 001473771 | https://help.salesforce.com/s/articleView?language=en_US&id=001473771&type=1
- Cause: clicking a total selects all values of the totalled field. Filter action with "exclude all" gives no values. Parameter actions keep the last value. Set actions with "remove" keep the last value.
- Fix: feed a parameter from a field that is not totalled, then filter on CONTAINS.
```
IF MIN([Category]) != MAX([Category])
THEN 'all'
ELSEIF MIN([Sub-Category]) != MAX([Sub-Category])
THEN MIN([Category])
ELSE MIN([Sub-Category])
END
```
```
CONTAINS([Click History Parameter], [Sub-Category])
OR CONTAINS([Click History Parameter], [Category])
OR CONTAINS([Click History Parameter], 'all')
OR [Click History Parameter] = 'none'
```
- Set the action aggregation to Concatenate and clearing to "Set value to" none.

### Table calc filter "Apply to totals" with INDEX or RANK
- See section 2 (ID 001470631).

## 4. Nulls, errors and data types

### Calculated field returns null results
- ID 001474028 | https://help.salesforce.com/s/articleView?language=en_US&id=001474028&type=1
- Seven causes, each a gold trap.
- 1. Any expression with NULL is NULL. Wrap in ZN(): `ZN( [Sales] ) + ZN( [Profit] )` and `ZN( SUM( [Sales] )) + ZN( SUM( [Profit] ))`.
- 2. Conditions with NULL are NULL. Use `ISNULL( [Region] )` not `[Region] = NULL`. IFNULL replaces with a value.
- 3. IF or CASE with no ELSE returns NULL when nothing is True (Tableau adds ELSE NULL).
- 4. Two mutually exclusive IFs subtracted are always NULL. Wrap each in an aggregate, a FIXED or a WINDOW function (the aggregate wrap fails if the tested dimension is in the view).
```
SUM( IF [Region] = "Central" THEN [Sales] END )
-
SUM( IF [Region] = "West" THEN [Sales] END )
```
```
{ FIXED : SUM( IF [Region] = "Central" THEN [Sales] END ) }
-
{ FIXED : SUM( IF [Region] = "West" THEN [Sales] END ) }
```
```
WINDOW_SUM( SUM( IF [Region] = "Central" THEN [Sales] END ))
-
WINDOW_SUM( SUM( IF [Region] = "West" THEN [Sales] END ))
```
- 5. A string with non-numeric characters converts to NULL.
```
FLOAT( RIGHT( [Price], LEN( [Price] ) - 1 ))
```
```
FLOAT(IF ISNULL( FLOAT( LEFT( [Price],1 )))THEN RIGHT( [Price], LEN( [Price] ) - 1 )ELSE [Price]END)
```
- 6. Division by zero returns NULL.
- 7. DATE() or DATEPARSE() return NULL when the format does not match the data or locale: DATEPARSE('m-d-yyyy', ...) on "1/13/2018" fails.

### Decimal numbers interpreted as NULL
- ID 001473274 | https://help.salesforce.com/s/articleView?language=en_US&id=001473274&type=1
- Cause: file uses dot as decimal separator but Tableau locale expects comma, or the reverse.
- Fix: data source page, arrow on the text file, Text file properties, set Locale to English. Text files only.

### CSV currency values show as NULL
- ID 004754263 | https://help.salesforce.com/s/articleView?language=en_US&id=004754263&type=1
- Fix: format the column as Currency in Excel, save, then reconnect as a new connection.

### Converting string to date or datetime gives NULL
- ID 001473665 | https://help.salesforce.com/s/articleView?language=en_US&id=001473665&type=1
- Cause: on a live connection the database does the conversion and databases differ.
- Fix: convert in the database; use an extract; or wrap with DATE() in Custom SQL.

### Oracle errors ORA-01843 (not a valid month) and ORA-01861 (literal does not match)
- IDs 001473616 and 001498372 | https://help.salesforce.com/s/articleView?language=en_US&id=001473616&type=1 and https://help.salesforce.com/s/articleView?language=en_US&id=001498372&type=1
- Cause: DATE() on a string whose format differs from Oracle's.
- Fix: match the string format, extract, or switch to DATEPARSE.
```
DATE( STR ([Year]) + "-" + STR([Month]) + "-1" )
DATEPARSE("yyyy-MM-dd", (STR ([Year]) + "-" + STR([Month]) + "-1" ))
```

### Unable to use a string field in ISMEMBEROF()
- ID 001473496 | https://help.salesforce.com/s/articleView?language=en_US&id=001473496&type=1
- Error: "Argument 1 to ISMEMBEROF must be a(n) string literal". Fix: create a parameter from the field and pass the parameter.

### MEDIAN() sometimes returns nan
- ID 001473196 | https://help.salesforce.com/s/articleView?language=en_US&id=001473196&type=1
- Fix: Data > source > Extract > Remove, then Extract Data again.

### Calculation results differ between Desktop and Server after publishing
- ID 001537663 | https://help.salesforce.com/s/articleView?language=en_US&id=001537663&type=1
- Cause: numbers with more than 16 digits after the decimal point.
- Fix: round to fewer than 15 digits in Default Number Format, for example 0.0000.

### Calculations containing user functions cannot reference physical tables
- ID 001920436 | https://help.salesforce.com/s/articleView?language=en_US&id=001920436&type=1
- Error: "Calculations containing user functions cannot reference fields from Physical Tables". Cause: user functions cannot span logical tables. Fix: change the Relationship to a Join.

### Blend error: unsupported aggregation with a cube primary
- ID 001472350 | https://help.salesforce.com/s/articleView?language=en_US&id=001472350&type=1
- Cause: cube measure default aggregation is AVG (quasi-additive). Supported: SUM, MIN, MAX, COUNT. Fix: change it in the cube.

### Cube warning: measure incompatible with dimensions in the view
- ID 001473534 | https://help.salesforce.com/s/articleView?language=en_US&id=001473534&type=1
- Cause: cubes hold pre-aggregated values, so some field combinations do not exist. Fix: work with the DBA.

### Unexpected aggregation (duplicated values) with row-level IF and relationships
- ID 005318709 | https://help.salesforce.com/s/articleView?language=en_US&id=005318709&type=1
- Symptom: SUM(IF [Code1] = 1 THEN [Measure] END) shows 60 instead of 20 across two related tables.
- Cause: a row-level IF forces a hidden row-level join to the dimension table, so the measure repeats once per matching row.
- Fix: make it an aggregate calculation.
```
IF ATTR([Code1]) = 1
THEN SUM([Measure])
END
```

### LOD returns NULL or missing data with relationships and a data source filter
- ID 005321784 | https://help.salesforce.com/s/articleView?language=en_US&id=005321784&type=1
- Symptom: FIXED on table B returns NULLs when a data source or context filter is on table A.
- Cause: the filter runs before FIXED, so Tableau builds an inner join between the tables.
- Fix: use a normal dimension filter (runs after FIXED), use physical joins with an explicit left join, or put the filter on the same table as the LOD target.

### Prep: TabPy results wrong with unsorted rows
- ID 005237277 | https://help.salesforce.com/s/articleView?language=en_US&id=005237277&type=1
- Cause: Prep does not guarantee row order sent to TabPy. Fix: sort inside the Python script, for example with df.sort_values().

### Database function errors (REGEXP on SQL Server, ASCII on Redshift)
- ID 001472791 | https://help.salesforce.com/s/articleView?language=en_US&id=001472791&type=1: "Unknown Function". SQL Server has no regex. Use RAWSQL pass-through.
- ID 001472879 | https://help.salesforce.com/s/articleView?language=en_US&id=001472879&type=1: "ASCII is not available for non-aggregates from this data source". Redshift treats ASCII as leader-node only. Use an extract.

## 5. Dates and fiscal years

### Using date functions with fiscal years
- ID 001473696 | https://help.salesforce.com/s/articleView?language=en_US&id=001473696&type=1
- Symptom: DATEPART('month', #2/1/2022#) returns 2 even when February is the first fiscal month.
- Cause: date functions use the calendar year by design.
- Fix: shift the date with DATEADD by months, then use the date function. Standard fiscal naming uses the calendar year of the last month, so shift into the next calendar year. Months to add by fiscal start: Feb 11, Mar 10, Apr 9, May 8, Jun 7, Jul 6, Aug 5, Sep 4, Oct 3, Nov 2, Dec 1.
```
DATEPART('year', DATEADD('month', 11, [Order Date]) )
DATE( "2/1/" + STR( YEAR( DATEADD( 'month', 11, [Order Date] ))))
DATEDIFF('week',[First fiscal day],[Order Date]) +1
```
- Note: DATETRUNC on a shifted date returns a shifted date (#1/1/2023# for Feb 2022). Do not show it to end users.

### Fiscal year number is higher than expected
- ID 001473880 | https://help.salesforce.com/s/articleView?language=en_US&id=001473880&type=1
- Cause: Tableau names the fiscal year after the calendar year of its last month, so April 2014 start shows FY2015.
- Fix: subtract a year, then set the fiscal start on the new field. Use a custom Month/Year date.
```
DATEADD('year', -1, [Order Date])
```

### Custom fiscal year or week start lost after publishing with a published data source
- ID 001474064 | https://help.salesforce.com/s/articleView?language=en_US&id=001474064&type=1
- Cause: publishing syncs to the data source properties by design.
- Fix: duplicate the date field and set Default Properties > Fiscal Year Start on the copy, or create a local copy of the data source, set it, then republish the data source.

### Date calculations, filters and time stamps wrong after publishing
- ID 001473770 | https://help.salesforce.com/s/articleView?language=en_US&id=001473770&type=1
- Cause: NOW(), TODAY(), relative date filters and timestamps use the Server or Cloud time zone.
- Fix: for extracts set Site Time Zone for Extracts (Settings > General). Otherwise shift hours in a calculation. Replace relative date filters with calcs set to True.
```
DATEADD('hour',<number of hours>,[<datetime field>])
[DateTimeField] >= {FIXED: MAX(DATETRUNC('hour',[DateTimeField]))}
[DateTimeField] >= DATEADD('hour', 3, NOW())
```
- Note: the number of hours moves with daylight saving.

### DATE() calculations return different values when the workbook locale changes
- ID 005224425 | https://help.salesforce.com/s/articleView?language=en_US&id=005224425&type=1
- Cause: DATE() is locale dependent. 12/31/2024 reads as month first in US, day first in UK and Australia.
- Fix: use MAKEDATE or DATEPARSE with an explicit format. Set the workbook locale to one value before publishing.
```
IF [Purchase Date] > MAKEDATE(2024,12,31) THEN [Purchase Date] ELSE [Dispatch Date] END
DATE(IF [Purchase Date]>DATEPARSE("dd/MM/yyyy","31/12/2024") THEN [Purchase Date] ELSE [Dispatch Date]END)
```

### Counting weekdays between dates
- ID 001458004 | https://help.salesforce.com/s/articleView?language=en_US&id=001458004&type=1
- Fix: shift weekend start dates forward and weekend end dates back, then subtract two days per week.
```
IF DATEPART('weekday', [Order Date]) = 1
THEN DATEADD('day', 1, [Order Date])
ELSEIF DATEPART('weekday', [Order Date]) = 7
THEN DATEADD('day', 2, [Order Date])
ELSE [Order Date]
END
```
```
IF DATEPART('weekday', [Ship Date]) = 1
THEN DATEADD('day', -2, [Ship Date])
ELSEIF DATEPART('weekday', [Ship Date]) = 7
THEN DATEADD('day', -1, [Ship Date])
ELSE [Ship Date]
END
```
```
MIN(
DATEDIFF('day', [Order Date (shifted to weekday)], [Ship Date (shifted to weekday)])
+ 1
- 2 * DATEDIFF('week', [Order Date (shifted to weekday)], [Ship Date (shifted to weekday)])
)
```
- Month version: start `DATETRUNC('month', [Order Date])`, end `DATEADD('day', -1, DATEADD('month', 1, DATETRUNC('month', [Order Date])))`. Holidays: join a Holidays table with Order Date <= Holiday Date and Ship Date >= Holiday Date.

### Rolling 12-month value with DATEDIFF
- ID 001458304 | https://help.salesforce.com/s/articleView?language=en_US&id=001458304&type=1
```
IF (DATEDIFF('month',[Order Date],TODAY()))<=12 THEN [Sales] ELSE null END
```

### Datetime ticks to a date
- ID 001456974 | https://help.salesforce.com/s/articleView?language=en_US&id=001456974&type=1
```
DATETIME(([<Time>]* POWER(10, -7) / 60 / 60 / 24)-693593)
```

### Overridable dynamic default selection in a filter
- ID 001473758 | https://help.salesforce.com/s/articleView?language=en_US&id=001473758&type=1
- Cause: filters have only a static default (value at save or publish). A dynamic default is not built in.
- Fix: dynamic parameters (Desktop 2020.1 and later), relative date filter, Latest Date preset (discrete date lists only), or a type-in parameter:
```
IF [Enter 'Yesterday' or a Date] = "Yesterday"
THEN TODAY() - 1
ELSE DATE( [Enter 'Yesterday' or a Date] )
END
```
```
[Date Conversion] = [Order Date]
```

### Date parameter set to 12/31/9999 shows 12/31/7999
- ID 005115600 | https://help.salesforce.com/s/articleView?language=en_US&id=005115600&type=1
- Desktop only. Fix: set the range maximum to 12/31/9999, or use a String parameter in year-month-day order and convert with DATE() or DATEPARSE().

### Date axis labels overlap on Server and Cloud when Major tick is fixed
- ID 005316933 | https://help.salesforce.com/s/articleView?language=en_US&id=005316933&type=1
- Cause: continuous date axis, client rendering and a fixed major tick (known limitation W-21599868).
- Fix: append ?:render=false to the view URL, or set Major Tick Marks to Automatic and republish.

## 6. Filters, Top N and sets

### Showing all values when a Top N filter returns fewer than N or ignores other filters
- IDs 001473578 and 001497317 | https://help.salesforce.com/s/articleView?language=en_US&id=001473578&type=1 and https://help.salesforce.com/s/articleView?language=en_US&id=001497317&type=1
- Symptom: Top 5 Sub-Category by Sales shows the same five whatever Region is picked, or the sort is wrong with a dimension filter.
- Cause: Top N is computed before ordinary dimension filters.
- Fix: right-click the other filter and Add to Context. Or use INDEX() as a table calc filter.

### Error "The filter limit must be greater than zero" with a Top N parameter
- ID 001534475 | https://help.salesforce.com/s/articleView?language=en_US&id=001534475&type=1
- Cause: parameter allows a value below 1. Fix: restrict the parameter to values of 1 or more.

### Filter Top N items with a button
- ID 001453844 | https://help.salesforce.com/s/articleView?language=en_US&id=001453844&type=1
- Fix: a sheet acting as a button (marks coloured white) with a filter action to the target sheet.

### Specifying sort order of items in quick filters
- ID 001472873 | https://help.salesforce.com/s/articleView?language=en_US&id=001472873&type=1
- Cause: sorting a quick filter list by a measure is not supported (a view sort does not sort the list). Fix: put a concatenated field on the filter.
```
STR([rank]) +' - ' + [category]
```

### Filtering a single axis of a dual-axis chart
- ID 001474101 | https://help.salesforce.com/s/articleView?language=en_US&id=001474101&type=1
- Cause: everything on Filters applies to the whole view.
- Fix: (1) a calculation that ignores filters (FIXED or a parameter). A FIXED fails when all rows of a category are filtered out. With a parameter each axis has one NULL mark. (2) blend a second copy of the data source. (3) self-union and add an axis name to the filter field. (4) overlay two sheets with a transparent top sheet.
```
IF [Table Name] = "{table name}"
THEN [Axis Measure]
END
```

### Unable to create a combined set
- ID 001497995 | https://help.salesforce.com/s/articleView?language=en_US&id=001497995&type=1
- Cause: Create Combined Set only appears for sets built on the same dimension or measure. Fix: build both on the same field, or put both sets on Filters and use IN and OUT combinations.

### Applying an action filter to worksheets in different dashboards
- ID 001473760 | https://help.salesforce.com/s/articleView?language=en_US&id=001473760&type=1
- Fix: right-click the action pill on Filters and choose Apply to Worksheets > All Using This Data Source or Selected Worksheets.

## 7. Actions and navigation

### Multiple action filters cancel each other out
- ID 001471140 | https://help.salesforce.com/s/articleView?language=en_US&id=001471140&type=1
- Cause: when sheets are sorted by a table calc or measure to the left of the selected field and text values are clicked, the filter changes the sort and clears the previous selection.
- Fix: move the sorting field right of the filtered fields; use Sort > By Field instead of a field in the view; or select marks (bars) instead of text.

### Filter actions or Go to Sheet missing or not working in published dashboards
- ID 001473315 | https://help.salesforce.com/s/articleView?language=en_US&id=001473315&type=1
- Cause: "Show sheets as tabs" is off. Fix: tick it in the publish dialog, or Details page > Tabbed views > Show Tabs.

### Dashboard URL menu actions not appearing
- ID 001473077 | https://help.salesforce.com/s/articleView?language=en_US&id=001473077&type=1
- Cause: menu actions render in tooltips. Fix: Worksheet > Tooltip > Show Tooltips, then republish.

### Parameter action fails on Server when the value has a line break
- ID 001470981 | https://help.salesforce.com/s/articleView?language=en_US&id=001470981&type=1
- Fix: upgrade to Server 2024.2.12, 2025.1.0 or later. Or remove the line break, hide the parameter card, or set Allowable values to a List fed from the source field.

### Dashboard actions do not filter as expected on navigation
- ID 005167227 | https://help.salesforce.com/s/articleView?language=en_US&id=005167227&type=1
- Go To Sheet keeps dashboard filters. Go To URL loads the destination default or the user's custom view. Use Go To URL for landing pages.

### Fields from blended sources unavailable for URL actions
- ID 001473840 | https://help.salesforce.com/s/articleView?language=en_US&id=001473840&type=1
- Fix: a new sheet with the needed source as primary, a filter action from the original sheet. Put the URL action on the new sheet.

### Display dynamic images on a dashboard
- ID 001473811 | https://help.salesforce.com/s/articleView?language=en_US&id=001473811&type=1
- Not built in. Use a URL action or custom shapes.

### Change the default highlight colour
- ID 001473643 | https://help.salesforce.com/s/articleView?language=en_US&id=001473643&type=1
- Not built in. Workaround: a parameter action plus a colour calculation.
```
IF [Select a Sub-Category]="" then "Blue"
ELSEIF [Select a Sub-Category]= [Sub-Category]
then "Orange"
else "Gray"
END
```
- Note: add a dimension "1" to Detail and set Highlight to it to disable default highlighting. Set colours in the Color card, not in the calc.

### Subscription with parameters shows unexpected data
- ID 005229020 | https://help.salesforce.com/s/articleView?language=en_US&id=005229020&type=1
- Cause: the data source behind "Value when workbook opens" is not blended with the view primary source, so the value fails to load for subscription renders.
- Fix: force a blend and add the source field to Filters with all values included. Republish and re-run.

### Filtering a Server URL with a parameter fails for PNG or PDF download
- ID 001534552 | https://help.salesforce.com/s/articleView?language=en_US&id=001534552&type=1
- Cause: known issue W-14041482 when vizqlserver.data_refresh=0 (cache always). Fix: add &:refresh=y to the URL, or reset the key with `tsm configuration set -k vizqlserver.data_refresh -d` then `tsm pending-changes apply`.

### Duplicate parameters corrupt workbook after web edit (Cloud 2025.1)
- ID 004633784 | https://help.salesforce.com/s/articleView?language=en_US&id=004633784&type=1
- Cause: web edit defect from about 28 Feb 2025. Deleting the duplicates and republishing keeps them.
- Fix: check the .twb for "duplicate: ParameterName". Restore a revision from before 28 Feb 2025, open it in Desktop 2024.x and republish.

### Error CDEAC1A9 opening a workbook with a list parameter (Desktop 2024.2 and later)
- ID 005314186 | https://help.salesforce.com/s/articleView?language=en_US&id=005314186&type=1
- Fix: update Desktop to the latest maintenance release or 2024.2.7 or later.

### User filter with USERNAME() feeding a parameter can expose other users' data
- ID 004634124 | https://help.salesforce.com/s/articleView?language=en_US&id=004634124&type=1
- Cause: USERNAME() as a parameter initial value is cached across users.
- Fix: do not put the user function in a parameter. Reference the calculated field directly. Publish with a user group selected and confirm the thumbnail reads "User Specific View".
```
IF [Calculation field from (1)] <> 'PROD' THEN
[Any field] = [Calculation field from (1)]
ELSE
TRUE
END
```

## 8. Parameters, formatting and colour

### Change formatting for different values based on parameter selection
- ID 001473686 | https://help.salesforce.com/s/articleView?language=en_US&id=001473686&type=1
- Symptom: a measure-swap parameter shows one number format for every choice.
- Cause: the swap calc is one field, so it has one format.
- Fix: (1) one field per option that returns NULL otherwise, each with its own default format, all on Label. (2) format as text inside a CASE. (3) two sheets swapped on a dashboard (best for date levels).
```
IF [<Measure Swapping Parameter>] = 'Sales' THEN [Sales] ELSE NULL END
IF [<Measure Swapping Parameter>] = 'Discount' THEN [Discount] ELSE NULL END
```

### STR() ignores the default date and number formatting
- ID 001473689 | https://help.salesforce.com/s/articleView?language=en_US&id=001473689&type=1
- Fix: build the format with string functions.
```
IF ABS(SUM([Profit])) > 999
THEN
IF SUM([Profit]) < 0 THEN "-" ELSE "" END
+ "$"
+ LEFT(STR(FLOOR(ABS(SUM([Profit])))),LEN(STR(FLOOR(ABS(SUM([Profit])))))-3)
+ ","
+ RIGHT(STR(FLOOR(ABS(SUM([Profit])))), 3)
ELSE
IF SUM([Profit]) < 0 THEN "-" ELSE "" END
+ "$"
+ LEFT(STR(ABS(SUM([Profit]))), 3)
END
```

### Make fields in a text table selectable
- ID 004576658 | https://help.salesforce.com/s/articleView?language=en_US&id=004576658&type=1
- Fix: a String list parameter plus one CASE field per slot, or pivot the source and filter on Pivot Field Names.
```
CASE [Display Field 1]
WHEN "1" THEN [Field1]
WHEN "2" THEN [Field2]
END
```

### Stable colours for dynamic groups and colours after filtering
- IDs 001472894 and 001472984 | https://help.salesforce.com/s/articleView?language=en_US&id=001472894&type=1 and https://help.salesforce.com/s/articleView?language=en_US&id=001472984&type=1
- Cause: Tableau does not map similar members to the same colour. Dynamic colour after a filter is not built in.
- Fix: assign colours for every parameter value, or colour by a stable calc (a rank, not the name that includes the parameter). Use a larger palette, a sequential palette or a rank calc.

### Custom colour palette does not save with an ad-hoc calculation
- ID 001473255 | https://help.salesforce.com/s/articleView?language=en_US&id=001473255&type=1
- Cause: a Boolean calc generates True and False at open, so saved colours do not map.
- Fix: return explicit strings, or save the calc as a field.
```
IF SUM([Dollars HUB])/SUM([Dollars SB eligible])*100>MAX([Target PCT])
THEN 'True'
ELSE 'False'
END
```

### Colours change after replacing a data source (and what else is lost)
- IDs 001473911 and 005131425 | https://help.salesforce.com/s/articleView?language=en_US&id=001473911&type=1 and https://help.salesforce.com/s/articleView?language=en_US&id=005131425&type=1
- Lost or reset on replace: colour, shape, sort, number and date format, aggregation, total using, comment, fiscal year start, image and geographic role, aliases, folders, hierarchies, data source filter, date properties. Used calcs, sets, bins and groups regenerate. Unused ones do not.
- Fix: copy calcs, groups and sets to the new source first, then replace. If both are published use Edit Server and Site Path. If same connector use Edit Connection.

### Calculated field duplicated with an error after switching Server
- ID 001475008 | https://help.salesforce.com/s/articleView?language=en_US&id=001475008&type=1
- Cause: the same field was recreated by hand on each server, so remote field names differ.
- Fix: republish the source from one environment to the other, or Replace References.

### Sort order of a calculated field changes after REST API replace
- ID 001474732 | https://help.salesforce.com/s/articleView?language=en_US&id=001474732&type=1
- Known issue W-12862805, now fixed. Fix: edit the connection in a downloaded .tdsx and republish, use tabcmd with -o, or reset the manual sort.

### Incorrect sort with quick sort buttons when a dummy axis is used
- ID 001473058 | https://help.salesforce.com/s/articleView?language=en_US&id=001473058&type=1
- Cause: ATTR(1) dual axis is really a scatter, so the quick sort sorts by that axis. Fix: right-click the dimension, choose Sort, then pick the field and aggregation.

### Trailing full width spaces not trimmed on Server
- ID 001497276 | https://help.salesforce.com/s/articleView?language=en_US&id=001497276&type=1
- Fix: ?:render=false, clean the data, or:
```
REGEXP_REPLACE([<name>], '　+$', '')
```
- Note: the character before the plus sign is a full width space (U+3000).

## 9. Charts, axes and maps

### Unable to synchronise axis when using Measure Values as an axis
- ID 001473031 | https://help.salesforce.com/s/articleView?language=en_US&id=001473031&type=1
- Cause: Measure Values are float. Float and integer cannot synchronise.
- Fix: right-click the measure, Change Data Type > Number (Decimal).

### Wrong axis value in a dual-axis line
- ID 001473291 | https://help.salesforce.com/s/articleView?language=en_US&id=001473291&type=1
- Fix: untick and retick Dual Axis on the second measure and synchronise. If the first axis is all NULL, wrap it in ZN().

### Dual-axis chart with several measures on both axes
- ID 001473860 | https://help.salesforce.com/s/articleView?language=en_US&id=001473860&type=1
- Not supported. Workaround: pivot the measures into one measure. Pivot cannot be applied to calculated fields and other measures need revising (divide by the number pivoted).

### Dynamically synchronise axes across worksheets
- ID 001473822 | https://help.salesforce.com/s/articleView?language=en_US&id=001473822&type=1
- Not built in. Use fixed axes, or fix the limits with LODs and a reference band on both sheets (no label, no line, no fill). Add context filters to both sheets.
```
{ FIXED [Sub-Category] : SUM([Sales]) }
IF MAX([Sales per Sub-Category]) >= MAX([Profit per Sub-Category]) THEN MAX([Sales per Sub-Category])
ELSE MAX([Profit per Sub-Category])
END
IF MIN([Sales per Sub-Category]) >= MIN([Profit per Sub-Category]) THEN MIN([Profit per Sub-Category])
ELSE MIN([Sales per Sub-Category])
END
```

### Add a reference line to a discrete header
- ID 001473994 | https://help.salesforce.com/s/articleView?language=en_US&id=001473994&type=1
- Fix: make the bin a continuous field (same formula Tableau uses for bins), or fake the line with a dual-axis bar fixed 0 to 1.
```
(FLOOR([Sales]/1655)*1655)
IF [Sub-Category]= "Chairs & Chairmats" OR [Sub-Category]= "Rubber Bands" THEN 1 END
```

### Doughnut chart
- ID 001473877 | https://help.salesforce.com/s/articleView?language=en_US&id=001473877&type=1
- Fix: pie plus a dual-axis dummy circle coloured as the background, smaller, with headers hidden.
```
MIN(1)
```

### Exterior pie labels with arrows
- ID 001453803 | https://help.salesforce.com/s/articleView?language=en_US&id=001453803&type=1
- Fix: annotate the marks (Annotate > Mark), drag them out, Format > Line > Arrow, turn off normal mark labels.

### Dotted specific lines in a multi-line chart
- ID 005135002 | https://help.salesforce.com/s/articleView?language=en_US&id=005135002&type=1
- Fix: isolate the lines in a calc, add as a second measure, set Path to dashed on its Marks card, make it dual axis and synchronise, then set Measure Name colours for the originals to white.
```
IF [Sub-Category] = "Art" OR [Sub-Category] = "Chairs" THEN [Profit] END
```

### Waterfall of cumulative month-over-month differences
- ID 005135048 | https://help.salesforce.com/s/articleView?language=en_US&id=005135048&type=1
- Fix: Gantt Bar mark, size from the negated difference, running sum on Rows.
```
ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)
-[1. Month-over-month]
RUNNING_SUM([1. Month-over-month])
```
- Note: set the running sum nested calc to Table (across).

### Basket analysis chart
- ID 001458592 | https://help.salesforce.com/s/articleView?language=en_US&id=001458592&type=1
- Fix: relate Orders to a second copy of Orders on Order ID, Sub-Category on Columns and Sub-Category (Orders1) on Rows, COUNTD of Order ID on Text and Color, Square marks. Add this filter set to True.
```
ATTR([Sub-Category (Orders1)])>=ATTR([Sub-Category])
```

### Adjust space between panes in a bar chart
- ID 001458700 | https://help.salesforce.com/s/articleView?language=en_US&id=001458700&type=1
- Not built in. Make Quarter continuous and widen the bar, or set the Column Divider format.

### Combining generated and data source latitude and longitude on a dual-axis map
- ID 001474040 | https://help.salesforce.com/s/articleView?language=en_US&id=001474040&type=1
- Applies to: fixed in Desktop 2018.1 and later. Earlier: custom geocoding or a background image.

### Vertical line in an area chart when zoomed above 100%
- ID 005036600 | https://help.salesforce.com/s/articleView?language=en_US&id=005036600&type=1
- Cause: browser rendering. Enable hardware acceleration in Chrome on Mac.

### Blank space on the x-axis of Gantt charts on Server
- ID 005208538 | https://help.salesforce.com/s/articleView?language=en_US&id=005208538&type=1
- Applies to: Server 2024.2.x, 2024.3.x, 2025.1.x. Fix: upgrade to 2025.3 or later.

## 10. Dashboards, publishing and performance

### Truncated text (#######) in fixed-size dashboards on Cloud
- ID 005133006 | https://help.salesforce.com/s/articleView?language=en_US&id=005133006&type=1
- Cause: Cloud renders strictly in the browser so text that overflows its space shows as #######.
- Fix: smaller or lighter font, bigger containers, space around dynamic text, check in Cloud preview. Automatic sizing removes the problem.

### Too many active WebGL contexts with many embedded views
- ID 005132046 | https://help.salesforce.com/s/articleView?language=en_US&id=005132046&type=1
- Cause: each embedded view uses one WebGL context and the browser caps them. Fix: fewer embedded views per page and lighter pages.

### Different cache settings for different workbooks
- ID 001473875 | https://help.salesforce.com/s/articleView?language=en_US&id=001473875&type=1
- Not per workbook. Set Balanced or Refresh more often for all, or append ?:refresh=y to a view URL, or click Refresh Data.

### Intermittent blank totals in crosstab export (Server 2025.1)
- ID 005225352 | https://help.salesforce.com/s/articleView?language=en_US&id=005225352&type=1
- Fix: upgrade to 2025.3 or later, or disable the external cache: `tsm configuration set -k vizqlserver.native_api.external_cache_disable -v true` and `tsm configuration set -k dataserver.native_api.external_cache_disable -v true`, each followed by `tsm pending-changes apply`.

### Asterisk in grand total with EXCLUDE on a dimension not in view
- ID 005239069 | https://help.salesforce.com/s/articleView?language=en_US&id=005239069&type=1
- Applies to: Desktop before 2025.1. Fix: upgrade, or remove dimensions from the EXCLUDE that are not in the view.
```
{EXCLUDE [Dimension_Name1],[Dimension_Name2],[Dimension_Name3] : SUM([Measure])}
```

### Prep: flow memory error on Cloud
- ID 001474406 | https://help.salesforce.com/s/articleView?language=en_US&id=001474406&type=1
- Fix: drop unused columns, avoid Custom SQL, join in the database, aggregate before joins, split into linked flows, or run in Prep Builder or on the command line.

## Top 20 traps

1. FIXED ignores dimension filters unless they are in context or in the declaration. It also still shows a value if any row of that value survives a filter (001473037).
2. Top N is evaluated before ordinary dimension filters. Add the other filters to context or the Top N will not move (001473578, 001497317).
3. Any aggregation makes a calculated field a measure. Only non-aggregate calcs (FIXED, row fields, parameters) become dimensions (001473640).
4. A table calc depends on every dimension in the view. Adding or removing a dimension breaks it or changes the answer. Use Specific Dimensions and a unique id, never Table (across) on a scatter (001471540, 001474595).
5. Table calcs and non-additive aggregations (COUNTD, ratios, AVG) give wrong grand totals. Use Total All Using SUM, or an LOD rewrite (001473383, 001473705).
6. Any expression containing NULL is NULL. Use ZN, IFNULL and ISNULL. Never write `= NULL`. IF and CASE with no ELSE return NULL (001474028).
7. Two IF calcs that are never true on the same row return NULL when subtracted. Wrap each in an aggregate, FIXED or WINDOW function (001474028).
8. An LOD inside CASE or IF is re-aggregated and inflated. Divide by SUM([Number of Records]) or aggregate inside the branch (001473493).
9. Date functions ignore the fiscal year start and fiscal years are named after the calendar year of the last month. Shift with DATEADD (001473696, 001473880).
10. DATE() is locale dependent and database dependent. Use MAKEDATE or DATEPARSE with an explicit format (005224425, 001498372, 001473665).
11. NOW(), TODAY() and relative date filters use the Server or Cloud time zone after publishing. Set the site time zone for extracts (001473770).
12. Navigation and filter actions need "Show sheets as tabs" when published. Menu actions need tooltips switched on (001473315, 001473077).
13. Actions fired from a grand total select every member of the totalled field. Feed a parameter from a field that is not totalled (001473771).
14. Quick table calcs for year over year match by index, not by date part. Incomplete years compare the wrong periods (001473562).
15. A parameter or measure swap is one field with one number format. Build one field per option or format as text (001473686).
16. Replacing a data source resets colour, sort, formats, fiscal start, aliases and more. Copy the calcs first (005131425, 001473911).
17. A published data source overrides workbook field properties on publish, such as a custom fiscal year (001474064).
18. Relationships plus a row-level IF duplicate measures. A data source filter turns an LOD into an inner join. Write aggregate calcs and filter after FIXED (005318709, 005321784).
19. A calculation using USERNAME() inside a parameter default can show other users' data. Reference the calc directly and publish with a user group (004634124).
20. Prep ROW_NUMBER and TabPy depend on row order, which is not guaranteed. Sort explicitly or output the result so it becomes static (001498512, 005237277).
