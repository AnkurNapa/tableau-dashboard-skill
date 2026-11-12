# Tableau formula patterns

Checked 12 Nov 2026. Total patterns: 71 (official 41, derived 30).

A pattern is a complete formula that answers a business question. Individual functions are catalogued in functions.md.

Labels. "official" means the formula text is copied verbatim from a tableau.com or salesforce.com page. "derived" means built from official functions and not printed on an official page in that form. Derived formulas need a test on real data before they go in a client workbook.

Names in square brackets are Superstore style fields. Swap in the real field names.

## Sources read

- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_fixed.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_include.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_exclude.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations_quick.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_string.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_number.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_user.htm
- https://help.tableau.com/current/pro/desktop/en-us/calcs_add_calculated_column.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculating_z_scores.htm
- https://help.tableau.com/current/pro/desktop/en-us/sortgroup_sets_topn.htm
- https://help.tableau.com/current/pro/desktop/en-us/pareto.htm
- https://help.tableau.com/current/pro/desktop/en-us/parameters_swap.htm
- https://help.tableau.com/current/pro/desktop/en-us/dynamic_axis_titles.htm
- https://help.tableau.com/current/pro/desktop/en-us/publish_userfilters_create.htm
- https://help.tableau.com/current/api/vizql-data-service/en-us/docs/vds_table_calcs_examples.html

## Sources that failed

- https://www.tableau.com/blog/LOD-expressions (403, so the Top 15 LOD blog formulas are not copied; the customer ones below are derived)
- https://www.tableau.com/learn/whitepapers/understanding-lod-expressions (403)
- help.tableau.com Top 15 LOD page, LOD examples page and define sort order page (404 at the guessed URLs)
- help.tableau.com calculations_calculatedfields_numberfunctions.htm (404)
- Tableau KB articles on Top N with global percent of total, date calculations for specific ranges, cohort analysis, first to second purchase days and conditional labels. kb.tableau.com redirects to help.salesforce.com, which returned only a script error page, so none of their formulas were read.

Not covered because no official formula could be confirmed: working days between dates (Tableau has no native function and the community formulas fail on weekend start dates), mode, BAN with a native Tableau Pulse style card, Workout Wednesday (no tableau.com hosted post found).

## Level of detail (LOD)

### Total per group, ignoring the view [official]
Question: what are total sales per segment (or region) whatever else sits in the view?
```
{FIXED [Segment] : SUM([Sales])}
```
Context: FIXED runs before dimension filters. Add the filter to context to make it apply.
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm

### Each row against the table average [official]
Question: how does each store's sales compare with the average across all stores?
```
[Sales] - {AVG([Sales])}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm

### Each sale against that customer's average [official]
Question: how does each sale differ from the customer's usual sale?
```
[Sales] - {FIXED [Customer Name] : AVG([Sales])}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm

### Share of total that survives a filter [official]
Question: what share of total sales does each state hold even when other states are filtered out?
```
SUM([Sales]) / ATTR({FIXED : SUM([Sales])})
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm

### Total per year [official]
Question: what are total sales per year?
```
{FIXED YEAR([Order Date]) : SUM(Sales)}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

### Proportion of one answer [official]
Question: what proportion of respondents answered Red per question?
```
{FIXED [Question] : AVG(IF [Answer] = "Red" THEN 1 ELSE 0 END )}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

### Total per customer added to the view [official]
Question: what does each customer buy in total while the view shows coarser marks?
```
{ INCLUDE [Customer Name] : SUM([Sales]) }
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_include.htm

### Average profit per day [official]
Question: what is the average of daily profit when the view is at month level?
```
{INCLUDE DATETRUNC('day', [Order Date]) : AVG(Profit)}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

### Total with a dimension removed [official]
Question: what are sales by month with the region split removed?
```
{EXCLUDE [Region]: SUM([Sales])}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_exclude.htm

### Average monthly sales total [official]
Question: what does a typical month sell?
```
{EXCLUDE [Order Date (Month / Year)] : AVG({FIXED [Order Date (Month / Year)] : SUM([Sales])})}
```
Setup: put Month([Order Date]) on Columns. The field name must match your date field at month and year level.
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_exclude.htm

### Earliest order date in the whole table [official]
Question: when does the data start?
```
{MIN([Order Date])}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

### Last order date in each month [derived]
Question: which day closes each month, so I can show the month-end value?
```
{FIXED DATETRUNC('month', [Order Date]) : MAX([Order Date])}
```
Use: compare to the row date for a flag, `[Order Date] = [Month End Order Date]`, then put the flag on Filters as True.
Built from the FIXED and DATETRUNC examples at https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

## Table calculations

Every dimension in the view is either addressing (the direction of travel) or partitioning (where the calculation restarts). Set it through Compute Using or Edit Table Calculation. Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations.htm

### Running total [official]
Question: how much has accumulated up to each period?
```
RUNNING_SUM(SUM([Profit]))
```
Addressing: the date field (Table down or a specific dimension). Restart per year by leaving Year as a partition.
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

### Record to date and record-breaking days [official]
Question: how many days did the price set a new high?
```
RUNNING_MAX(AVG([Close]))
```
```
IF AVG([Close]) = [Record to Date]
THEN 1
ELSE 0
END
```
```
RUNNING_SUM([Count Days Record Broken])
```
Name the first field Record to Date and the second Count Days Record Broken. Addressing is the date.
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

### Running product [official]
Question: what is the compounded result of period factors?
```
SUM([Profit]) * PREVIOUS_VALUE(1)
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

### Moving average over three periods [derived]
Question: what is the smoothed trend over the current and two prior periods?
```
WINDOW_AVG(SUM([Profit]), -2, 0)
```
Addressing: the date field. The official page prints this formula with a missing bracket, so the corrected form is shown.
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

### Rolling 75th percentile [official]
Question: what is the upper quartile of recent periods?
```
WINDOW_PERCENTILE(SUM([Profit]), 0.75, -2, 0)
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

### Percent of total [derived]
Question: what share of the partition does each mark hold?
```
SUM([Sales]) / TOTAL(SUM([Sales]))
```
Addressing: the dimension being compared. Table down gives share of the whole table, Pane down gives share within each pane. The quick table calculation does the same without a formula.
Source: built from https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations_quick.htm

### Change against the previous period [derived]
Question: how much did this period move against the one before?
```
(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))
```
Addressing: the date field. Use -12 on a monthly view for the same month last year. The quick calculations Percent difference and Year over year growth give the same result.
Source: built from LOOKUP at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

### Label only the latest mark [derived]
Question: how do I show a value label on the last point of a line?
```
IF LAST() = 0 THEN SUM([Sales]) END
```
Addressing: the date field. Put it on Label.
Source: LAST() example at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

## Time intelligence

### Year-over-year percent change with two helper fields [official]
Question: how did sales change from 2013 to 2014?
```
IF YEAR([Order Date]) = 2013 THEN [Sales] ELSE 0 END
```
```
IF YEAR([Order Date]) = 2014 THEN [Sales] ELSE 0 END
```
```
(SUM([2014]) - SUM([2013])) / SUM([2013])
```
Name the helper fields 2013 and 2014. Replace the years with parameters for a flexible version.
Source: https://help.tableau.com/current/pro/desktop/en-us/calcs_add_calculated_column.htm

### Push dates out [official]
Question: what is a due date if every task slips by one week?
```
DATEADD('week', 1, [due date])
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm

### Months between two dates [official]
Question: how many months did a member stay?
```
DATEDIFF('month', [date joined band], [date left band])
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm

### Weekday as a number [official]
Question: how do I turn the weekday name into a sortable number?
```
CASE LEFT(DATENAME('weekday',[Order Date]),3)
WHEN 'Sun' THEN 0
WHEN 'Mon' THEN 1
WHEN 'Tue' THEN 2
WHEN 'Wed' THEN 3
WHEN 'Thu' THEN 4
WHEN 'Fri' THEN 5
WHEN 'Sat' THEN 6
END
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm

### Current month against prior month with a picked month [derived]
Question: how does the chosen month compare with the month before?
```
IF DATETRUNC('month', [Order Date]) = DATETRUNC('month', [Selected Month]) THEN [Sales] END
```
```
IF DATETRUNC('month', [Order Date]) = DATEADD('month', -1, DATETRUNC('month', [Selected Month])) THEN [Sales] END
```
Setup: Selected Month is a date parameter. Name the fields Current Sales and Prior Sales, then use the BAN pattern in the dynamic UI section.
Source: built from DATETRUNC and DATEADD at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm

### Last N days from today [derived]
Question: what were sales in the last N days?
```
IF [Order Date] > DATEADD('day', -[N Days], TODAY()) AND [Order Date] <= TODAY() THEN [Sales] END
```
Setup: N Days is an integer parameter. Swap TODAY() for a date parameter to move the anchor.
Source: built from DATEADD and TODAY at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm

### Dynamic date range around an anchor [derived]
Question: which orders fall in the N days up to a chosen anchor date?
```
DATEDIFF('day', [Order Date], [Anchor Date]) >= 0 AND DATEDIFF('day', [Order Date], [Anchor Date]) < [N Days]
```
Setup: Anchor Date is a date parameter. Put the Boolean on Filters as True.
Source: built from DATEDIFF at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm

### Year to date against the same days last year [derived]
Question: how does year to date compare with the same stretch last year?
```
IF DATEPART('dayofyear', [Order Date]) <= DATEPART('dayofyear', TODAY()) THEN [Sales] END
```
Put Year([Order Date]) on Columns. A leap year shifts the cut by one day after February.
Source: built from DATEPART at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm

## Customer analytics

### First purchase date [official]
Question: when did each customer first buy?
```
{FIXED [Customer Name] : MIN([Order Date])}
```
Name it First Purchase Date.
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_fixed.htm

### Days since first purchase [official]
Question: how many days after their first order did each order happen?
```
DATETRUNC('day', [Order Date])-DATETRUNC('day', [First Purchase Date])
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_fixed.htm

### New or returning customer by month [derived]
Question: is the order from a new customer or a returning one in that month?
```
IF DATETRUNC('month', [Order Date]) = DATETRUNC('month', {FIXED [Customer Name] : MIN([Order Date])}) THEN "New" ELSE "Returning" END
```
Put it on Color and COUNTD([Customer Name]) on Rows.
Source: built from the first purchase LOD at https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_fixed.htm

### Cohort month and months since joining [derived]
Question: which cohort does a customer belong to and how old is the order?
```
DATETRUNC('month', {FIXED [Customer Name] : MIN([Order Date])})
```
```
DATEDIFF('month', {FIXED [Customer Name] : MIN([Order Date])}, [Order Date])
```
Name them Cohort Month and Months Since First. Put Cohort Month on Rows and Months Since First on Columns.
Source: built from the first purchase LOD and DATEDIFF at the pages named above.

### Retention rate [derived]
Question: what share of each cohort is still buying in month N?
```
COUNTD([Customer Name]) / MIN({FIXED [Cohort Month] : COUNTD([Customer Name])})
```
Use with the cohort fields above. The denominator is the cohort size and does not change with Months Since First.
Source: built from COUNTD and FIXED at https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

### Order frequency per customer [derived]
Question: how many orders has each customer placed?
```
{FIXED [Customer Name] : COUNTD([Order ID])}
```
Use it as a dimension (right click, Convert to Dimension) for a histogram of customers by order count.
Source: built from COUNTD at https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

### Lifetime value to date [derived]
Question: how much has each customer spent in total?
```
{FIXED [Customer Name] : SUM([Sales])}
```
This is revenue to date, not a forecast. Subtract cost fields for margin based value.
Source: built from the FIXED example at https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm

## Statistics

### Z-score [official]
Question: how many standard deviations is each state from the mean?
```
WINDOW_AVG(SUM([Sales]))
```
```
WINDOW_STDEVP(SUM([Sales]))
```
```
(SUM([Sales]) - [Average Sales]) / [STDEVP Sales]
```
Name them Average Sales and STDEVP Sales. Set Compute Using on the Z-score field to the dimension such as State. A value beyond 1.96 or below -1.96 is usually treated as an outlier.
Source: https://help.tableau.com/current/pro/desktop/en-us/calculating_z_scores.htm

### Outlier flag in one field [derived]
Question: which marks sit outside the usual range?
```
IF ABS((SUM([Sales]) - WINDOW_AVG(SUM([Sales]))) / WINDOW_STDEVP(SUM([Sales]))) > 1.96 THEN "Outlier" ELSE "Normal" END
```
Addressing: the dimension being tested.
Source: built from the Z-score page above.

### Percentile [official]
Question: what is the 90th percentile of a score?
```
PERCENTILE([Score], 0.9)
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

### Percentile of order totals by country [official]
Question: what is the 90th percentile of order size once lines are rolled up to orders?
```
{INCLUDE [Order ID] : SUM([Sales])}
```
Wrap it as PERCENTILE([Order Sales], .90) where Order Sales is the field above, with Country in the view.
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

### Median order value [derived]
Question: what is the typical order, not the average one?
```
MEDIAN({INCLUDE [Order ID] : SUM([Sales])})
```
Source: built from MEDIAN and INCLUDE at the aggregate page above.

### Weighted average [derived]
Question: what is the price averaged by units sold?
```
SUM([Price] * [Quantity]) / SUM([Quantity])
```
Source: built from SUM at https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

### Profit margin with a zero guard [official]
Question: what is the margin, with no error when sales are zero?
```
IIF(SUM([Sales]) !=0, SUM([Profit])/SUM([Sales]), 0)
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

### Correlation across all rows [official]
Question: how strongly do sales and profit move together?
```
{CORR(Sales, Profit)}
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm

## Ranking and top N

### Rank with a choice of tie handling [derived]
Question: where does each item stand when ties share or split a rank?
```
RANK(SUM([Sales]))
```
```
RANK_DENSE(SUM([Sales]))
```
```
RANK_UNIQUE(SUM([Sales]))
```
RANK leaves gaps after ties. RANK_DENSE does not. RANK_UNIQUE gives every row its own number. Addressing: the dimension being ranked.
Source: ranking methods shown at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm

### Top N from a parameter [derived]
Question: show only the top N items, where the user picks N.
```
RANK(SUM([Sales])) <= [Top N]
```
Setup: Top N is an integer parameter. Put the Boolean on Filters as True. Table calculation filters run last, so other filters do not reshuffle the underlying data.
Source: built from RANK. Parameter use in Top filters: https://help.tableau.com/current/pro/desktop/en-us/sortgroup_sets_topn.htm

### Top N and Others label [official]
Question: how do I label the top N customers and group the rest?
```
IF [Top N Customers by Sales]
THEN "Top " + str([Top Customers 2]) + " Customers"
ELSE "Others"
END
```
Setup: an integer parameter named Top Customers 2, plus a set named Top N Customers by Sales (Top tab, By Field, Sales, Sum) linked to the parameter.
Source: https://help.tableau.com/current/pro/desktop/en-us/sortgroup_sets_topn.htm

### Roll the rest into Others with expand and collapse [official]
Question: how do I show the top N by name and one Others row for everything else?
```
IF [Expand or Collapse]="Collapse" THEN
  IF [Top N Customers by Sales]
  THEN [Customer Name]
  ELSE "Others" END
ELSE [Customer Name] END
```
Setup: a string parameter named Expand or Collapse with the values Expand and Collapse. Replace Customer Name on Rows with this field.
Source: https://help.tableau.com/current/pro/desktop/en-us/sortgroup_sets_topn.htm

### Pareto 80/20 cumulative share [derived]
Question: which few items make up 80 percent of sales?
```
RUNNING_SUM(SUM([Sales])) / TOTAL(SUM([Sales]))
```
Setup: sort the dimension descending by Sales. Put Sales on Rows twice for a dual axis. Make the second a line with this field. The official recipe uses Running Total then a secondary Percent of Total, which gives the same result. Add a reference line at 0.8.
Source: recipe at https://help.tableau.com/current/pro/desktop/en-us/pareto.htm

### Top percent instead of top count [derived]
Question: show the top 20 percent of items by sales.
```
RANK_PERCENTILE(SUM([Sales])) >= 0.8
```
Put the Boolean on Filters as True. Addressing: the dimension being ranked.
Source: built from RANK_PERCENTILE, listed at https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations_quick.htm as the Percentile quick calculation.

## Strings

### Join first and last name [official]
Question: how do I make one name field?
```
[First name] + " " + [Last name]
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calcs_add_calculated_column.htm

### Split a code by a delimiter [official]
Question: how do I pull the second token from a hyphenated code?
```
SPLIT ("a-b-c-d", "-", 2)
```
Use a negative index to count from the right, as in SPLIT ("a|b|c|d", "|", -2). Swap the literal for a field.
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_string.htm

### Trim and proper case a name [derived]
Question: how do I clean untidy names?
```
PROPER(TRIM([Name]))
```
Source: built from TRIM and PROPER at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_string.htm

### Replace text [official]
Question: how do I swap a fragment in a text field?
```
REPLACE("Version 3.8", "3.8", "4x")
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_string.htm

### Flag rows that contain a code [derived]
Question: which products carry a given code?
```
CONTAINS([Product ID], "XYZ")
```
The help page prints a mismatched bracket in this example, so the corrected spelling is shown.
Source: https://help.tableau.com/current/pro/desktop/en-us/calcs_add_calculated_column.htm

### Extract the number from a text field [derived]
Question: how do I get the first run of digits out of text?
```
INT(REGEXP_EXTRACT([Text], '(\d+)'))
```
Source: built from REGEXP_EXTRACT and INT. Function reference: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_string.htm

### Take the last piece of an ID [derived]
Question: how do I read the state code from IDs like 123_WA?
```
SPLIT([Store ID], "_", -1)
```
Source: built from the SPLIT example above.

## Nulls

### Replace null with zero [official]
Question: how do I stop null grades breaking a calculation?
```
ZN([Test Grade])
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm

### Replace null with text [official]
Question: how do I show a placeholder where a value is missing?
```
IFNULL([Assigned Room], "TBD")
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm

### Test for null [official]
Question: which rows have no value?
```
ISNULL([Assigned Room])
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm

### Null safe growth [derived]
Question: how do I show growth only when the prior period has data?
```
IF ZN(LOOKUP(SUM([Sales]), -1)) = 0 THEN NULL ELSE (SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1)) END
```
Addressing: the date field.
Source: built from ZN and LOOKUP at the pages named above.

## Dynamic UI: parameters, titles, colours

### Measure swap with a parameter [official]
Question: how does the user pick which measure the chart shows?
```
CASE [Choose a Measure]
WHEN "Sales" THEN SUM([Sales])
WHEN "Profit" THEN AVG([Profit])
WHEN "Quantity" THEN COUNT([Quantity])
WHEN "Shipping Cost" THEN MEDIAN([Shipping Cost])
END
```
Setup: a string list parameter with the four names. Reference each parameter value, not the Display As text.
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm

### Swap two measures on both axes [official]
Question: how do I let users change the X and Y measures?
```
CASE [Placeholder 1 Selector]WHEN "Discount" THEN SUM([Discount])WHEN "Profit" THEN AVG([Profit])WHEN "Quantity" THEN SUM([Quantity])WHEN "Sales" THEN AVG([Sales])END
```
Duplicate it as Placeholder 2 with the Placeholder 2 Selector. Aggregate every measure or none. For axis titles, double click the axis, choose Parameter under Axis Titles and pick the selector.
Source: https://help.tableau.com/current/pro/desktop/en-us/parameters_swap.htm and https://help.tableau.com/current/pro/desktop/en-us/dynamic_axis_titles.htm

### Dynamic sheet title text [derived]
Question: how does the title follow the selection?
```
[Choose a Measure] + " by region, " + STR(YEAR(TODAY()))
```
Setup: put the field on Text in a sheet and hide the header, or insert it from the title editor Insert menu. Dynamic axis titles from a parameter need Tableau 2023.1 or later.
Source: built from STR and YEAR. Axis titles: https://help.tableau.com/current/pro/desktop/en-us/dynamic_axis_titles.htm

### Profit buckets for colour [derived]
Question: how do I colour marks as profit, break even or loss?
```
IF SUM([Profit]) > 0 THEN "Profitable" ELSEIF SUM([Profit]) = 0 THEN "Break even" ELSE "Loss" END
```
Put it on Color. The logical functions page shows the same bucketing idea.
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm

### Category by threshold [official]
Question: how do I band a score into labels?
```
IF [GPA] <3 THEN "Needs Improvement" ELSEIF [GPA] <3.5 THEN "Sufficient" ELSE "Excellent" END
```
Source: https://help.tableau.com/current/pro/desktop/en-us/calcs_add_calculated_column.htm

### KPI arrow [derived]
Question: how do I show an up or down arrow for change?
```
IF SIGN([Change]) = 1 THEN "▲" ELSEIF SIGN([Change]) = -1 THEN "▼" ELSE "▬" END
```
Setup: Change is the percent change field. Put the arrow on Text and colour it with a second field that returns "Up" or "Down".
Source: built from SIGN at https://help.tableau.com/current/pro/desktop/en-us/functions_functions_number.htm

### BAN against prior period [derived]
Question: what is the headline figure and its change against the prior period?
```
SUM([Current Sales])
```
```
(SUM([Current Sales]) - SUM([Prior Sales])) / ABS(SUM([Prior Sales]))
```
Use the Current Sales and Prior Sales fields from the time intelligence section. Place both on Text in one sheet.
Source: built from the fields above.

## Security

### User filter by manager [official]
Question: how do managers see only their own rows?
```
USERNAME() = [Manager]
```
Setup: join a reference table that maps Manager to Region. Put the Boolean on Filters as True. Test with Filter as User. Apply it as a data source filter for stronger control.
Source: https://help.tableau.com/current/pro/desktop/en-us/publish_userfilters_create.htm

### Manager or national group [official]
Question: how do regional managers see their region while national managers see everything?
```
[Regional Manager] = USERNAME() OR ISMEMBEROF("National Managers")
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_user.htm

### Region from a user attribute [official]
Question: how do I restrict rows by an attribute set on the user?
```
[Region] = USERATTRIBUTE("Region")
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_user.htm

### Attribute holds many values [official]
Question: how do I allow a user several regions?
```
USERATTRIBUTEINCLUDES('Region', [Region])
```
Source: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_user.htm
