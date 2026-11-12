# Tableau calculation function reference

Source of truth is the official Tableau help, checked 12 Nov 2026:

- https://help.tableau.com/current/pro/desktop/en-us/functions_all_categories.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_all_alphabetical.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_spatial.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_additional.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_typeconversion.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_functions_tablecalculation.htm
- https://help.tableau.com/current/pro/desktop/en-us/functions_operators.htm
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm

Count: 207 entries (the 200 names on the alphabetical page plus 7 spatial functions that only the category page lists: DIFFERENCE, INTERSECTION, NO_CUTOUTS, PARSE_WKT, SYMDIFFERENCE, UNION, VALIDATE). MAX and MIN appear once, under Aggregate. They also work row by row with two arguments.

Concepts for LOD expressions, table calculation addressing, order of operations and dates live in [calcs-and-viz.md](calcs-and-viz.md). This file is the lookup table: syntax, meaning, one example and the trap to avoid. Field names in examples are placeholders such as [Sales].

Data source support varies by function. Where the help page lists limits they are named in the Note column. When a function fails on a live connection, create an extract or use the table calculation equivalent.

## Contents

1. Number
2. String
3. Date
4. Type conversion
5. Logical and null handling
6. Aggregate
7. User
8. Table calculation
9. Level of detail (LOD)
10. Spatial
11. Pass-through (RAWSQL)
12. Regular expression
13. Predictive modelling and analytics extensions
14. Additional (Hive, Impala, BigQuery)
15. Operators and precedence

## 1. Number

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| ABS | ABS(number) | Absolute value | ABS(-7) = 7 | None |
| ACOS | ACOS(number) | Arccosine in radians | ACOS(-1) = 3.14159 | Input must be -1 to 1 |
| ASIN | ASIN(number) | Arcsine in radians | ASIN(1) = 1.5708 | Input must be -1 to 1 |
| ATAN | ATAN(number) | Arctangent in radians | ATAN(1) = 0.7854 | Result lies between -PI/2 and PI/2 |
| ATAN2 | ATAN2(y, x) | Arctangent of y/x in radians | ATAN2(2, 1) = 1.1071 | Argument order is y first, then x |
| CEILING | CEILING(number) | Rounds up to the next integer | CEILING(3.1) = 4 | Not supported on every source (listed: Excel, text, SQL Server, Redshift, BigQuery, Hive, Salesforce and others) |
| COS | COS(number) | Cosine of an angle in radians | COS(PI()) = -1 | Angle in radians, not degrees |
| COT | COT(number) | Cotangent of an angle in radians | COT(PI()/4) = 1 | Undefined at 0 |
| DEGREES | DEGREES(number) | Radians to degrees | DEGREES(PI()) = 180 | None |
| DIV | DIV(integer1, integer2) | Integer part of a division | DIV(11, 2) = 5 | Use this for integer division. 11/2 returns 5.5 |
| EXP | EXP(number) | e raised to a power | EXP(2) = 7.389 | Large inputs overflow |
| FLOOR | FLOOR(number) | Rounds down to the next integer | FLOOR(-3.1) = -4 | Same source limits as CEILING except Redshift. Rounds toward minus infinity |
| HEXBINX | HEXBINX([Lon], [Lat]) | X coordinate of the nearest hexagonal bin | HEXBINX([Longitude], [Latitude]) | Bin side length is 1. Pair with HEXBINY. Used for hex maps |
| HEXBINY | HEXBINY([Lon], [Lat]) | Y coordinate of the nearest hexagonal bin | HEXBINY([Longitude], [Latitude]) | Plot both on Columns and Rows with a measure on Size or Colour |
| LN | LN(number) | Natural logarithm | LN(EXP(3)) = 3 | Null if the argument is zero or negative |
| LOG | LOG(number, [base]) | Logarithm in a given base | LOG(1000) = 3 | Base defaults to 10. Null for zero or negative input |
| PI | PI() | The constant pi | PI() = 3.14159 | Needs the brackets |
| POWER | POWER(number, power) | Raises a number to a power | POWER(5, 2) = 25 | Same as the ^ operator |
| RADIANS | RADIANS(number) | Degrees to radians | RADIANS(180) = 3.14159 | None |
| ROUND | ROUND(number, [decimals]) | Rounds to the given digits | ROUND(2.345, 2) = 2.35 | Floating point oddities appear. For display use number formatting instead. Negative decimals round left of the point on some sources |
| SIGN | SIGN(number) | Returns -1, 0 or 1 | SIGN(-12) = -1 | None |
| SIN | SIN(number) | Sine of an angle in radians | SIN(PI()/2) = 1 | Angle in radians |
| SQRT | SQRT(number) | Square root | SQRT(25) = 5 | Negative input gives null |
| SQUARE | SQUARE(number) | Square of a number | SQUARE(5) = 25 | None |
| TAN | TAN(number) | Tangent of an angle in radians | TAN(PI()/4) = 1 | Angle in radians |

## 2. String

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| ASCII | ASCII(string) | Code of the first character | ASCII("A") = 65 | Only the first character counts |
| CHAR | CHAR(number) | Character for an ASCII code | CHAR(65) = "A" | Use CHAR(10) for a line break in tooltips and labels |
| CONTAINS | CONTAINS(string, substring) | True if the substring is present | CONTAINS("Calculation", "alcu") = true | Case sensitivity depends on the data source. Wrap both sides in LOWER to be safe |
| ENDSWITH | ENDSWITH(string, substring) | True if the string ends with the substring | ENDSWITH("Tableau", "au") = true | Trailing spaces are ignored |
| FIND | FIND(string, substring, [start]) | Position of the substring | FIND("Calculation", "alcu") = 2 | Returns 0 when not found. Positions start at 1. Start position is optional |
| FINDNTH | FINDNTH(string, substring, occurrence) | Position of the nth occurrence | FINDNTH("Calculation", "a", 2) = 7 | Not available on every data source. Extract if it fails |
| LEFT | LEFT(string, number) | Leftmost characters | LEFT("Matador", 4) = "Mata" | None |
| LEN | LEN(string) | Number of characters | LEN("Matador") = 7 | Null in gives null out |
| LOWER | LOWER(string) | Converts to lowercase | LOWER("ProductVersion") = "productversion" | None |
| LTRIM | LTRIM(string) | Removes leading spaces | LTRIM(" Matador") = "Matador" | Spaces only, not tabs |
| MID | MID(string, start, [length]) | Substring from a start position | MID("Calculation", 2, 5) = "alcul" | Start is 1 based. Without length it runs to the end |
| PROPER | PROPER(string) | Capitalises the first letter of each word | PROPER("PRODUCT name") = "Product Name" | Limited to some flat files and extracts |
| REPLACE | REPLACE(string, substring, replacement) | Replaces matching text | REPLACE("Version 3.8", "3.8", "4.0") = "Version 4.0" | Returns the string unchanged if no match. Literal match only. Use REGEXP_REPLACE for patterns |
| RIGHT | RIGHT(string, number) | Rightmost characters | RIGHT("Calculation", 4) = "tion" | None |
| RTRIM | RTRIM(string) | Removes trailing spaces | RTRIM("Market   ") = "Market" | Spaces only |
| SPACE | SPACE(number) | String of repeated spaces | "A" + SPACE(3) + "B" | Useful for padding labels |
| SPLIT | SPLIT(string, delimiter, token number) | Returns one token from a delimited string | SPLIT("a-b-c", "-", 2) = "b" | Negative token counts from the right. Only supported on some sources. On others use the Split UI command or an extract. Token number must be a constant |
| STARTSWITH | STARTSWITH(string, substring) | True if the string starts with the substring | STARTSWITH("Matador", "Ma") = true | Leading spaces are ignored |
| TRIM | TRIM(string) | Removes leading and trailing spaces | TRIM(" Market ") = "Market" | Spaces only |
| UPPER | UPPER(string) | Converts to uppercase | UPPER("Calculation") = "CALCULATION" | None |

Regular expression string functions are in section 12. String concatenation uses the + operator and any null makes the whole result null. Wrap parts in IFNULL or ZN-style guards.

## 3. Date

Date functions ignore the fiscal year start set on a field. Date parts accepted by date_part arguments: 'year', 'quarter', 'month', 'dayofyear', 'day', 'weekday', 'week', 'hour', 'minute', 'second', 'iso-year', 'iso-quarter', 'iso-week', 'iso-weekday'. The optional start_of_week argument takes 'monday' to 'sunday' and defaults to the data source setting.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| DATEADD | DATEADD(date_part, interval, date) | Adds an interval of date parts | DATEADD('month', 3, #2026-01-15#) = 2026-04-15 | Interval can be negative. Result keeps the type of the input |
| DATEDIFF | DATEDIFF(date_part, date1, date2, [start_of_week]) | Number of date part boundaries crossed from date1 to date2 | DATEDIFF('day', #2026-01-01#, #2026-03-01#) = 59 | Counts boundaries, not elapsed time. 31 Dec to 1 Jan is 1 year apart. Order is start then end |
| DATENAME | DATENAME(date_part, date, [start_of_week]) | Date part as a string | DATENAME('month', #2026-03-15#) = "March" | Returns text, so it sorts alphabetically. Use DATEPART to sort |
| DATEPARSE | DATEPARSE(date_format, date_string) | Parses a string to a date with an exact format | DATEPARSE('dd/MM/yyyy', [Text Date]) | Not on every source. Listed: non-legacy Excel and text, Hive variants, Google Sheets, MySQL, Oracle, PostgreSQL and extracts. Not supported on Hive variants in some versions. Format letters are case sensitive. Some formats fail on some connections. Extract the data if the live source refuses |
| DATEPART | DATEPART(date_part, date, [start_of_week]) | Date part as an integer | DATEPART('month', #2026-03-15#) = 3 | Use for numeric sort and arithmetic |
| DATETRUNC | DATETRUNC(date_part, date, [start_of_week]) | Rounds a date down to a level | DATETRUNC('month', #2026-03-15#) = 2026-03-01 | Returns a date, so axes stay continuous. Best for month and quarter grouping |
| DAY | DAY(date) | Day of the month, 1 to 31 | DAY(#2026-03-15#) = 15 | None |
| ISDATE | ISDATE(string) | True if the string is a valid date | ISDATE("2026-03-15") = true | Takes a string, not a date field. Validity follows the system locale |
| ISOQUARTER | ISOQUARTER(date) | ISO 8601 quarter | ISOQUARTER(#2026-01-01#) | Quarters follow ISO weeks, not the calendar |
| ISOWEEK | ISOWEEK(date) | ISO 8601 week number | ISOWEEK(#2026-01-01#) | Early January can fall in week 52 or 53 of the prior ISO year |
| ISOWEEKDAY | ISOWEEKDAY(date) | ISO 8601 weekday, Monday is 1 | ISOWEEKDAY(#2026-03-15#) = 7 | Sunday is 7 |
| ISOYEAR | ISOYEAR(date) | ISO 8601 year | ISOYEAR(#2026-01-01#) | Can differ from YEAR near 1 January |
| MAKEDATE | MAKEDATE(year, month, day) | Builds a date from numbers | MAKEDATE(2026, 3, 15) | Available for extracts. Check other sources. Out of range values roll over (month 13 becomes January next year) |
| MAKEDATETIME | MAKEDATETIME(date, time) | Combines a date and a time | MAKEDATETIME([Date], [Time]) | MySQL compatible connections only (MySQL and Amazon Aurora). Elsewhere build with DATETIME and string parts |
| MAKETIME | MAKETIME(hour, minute, second) | Builds a time as a datetime | MAKETIME(14, 52, 40) | Date part is 1/1/1899. Extracts and some other sources only |
| MONTH | MONTH(date) | Month as an integer | MONTH(#2026-03-15#) = 3 | None |
| NOW | NOW() | Current local date and time | NOW() | Needs the brackets. Recalculates on each refresh. Not stable in extracts |
| QUARTER | QUARTER(date) | Calendar quarter as an integer | QUARTER(#2026-03-15#) = 1 | Ignores a fiscal year start |
| TODAY | TODAY() | Current local date | [Order Date] >= TODAY() - 30 | Server time zone applies on Tableau Server |
| WEEK | WEEK(date) | Week as an integer | WEEK(#2026-03-15#) = 11 | Depends on the week start setting |
| YEAR | YEAR(date) | Year as an integer | YEAR(#2026-03-15#) = 2026 | Ignores a fiscal year start |

DATE and DATETIME are in section 4. ISDATE is also listed under logical functions on the help page.

## 4. Type conversion

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| DATE | DATE(expression) | Converts a string, number or datetime to a date | DATE("2026-09-22") | Fails silently to null on formats it does not recognise. Use DATEPARSE with a format then |
| DATETIME | DATETIME(expression) | Converts a string, number or date to a datetime | DATETIME("April 15, 2005 07:59:00") | Same recognition limits as DATE |
| FLOAT | FLOAT(expression) | Casts to a decimal number | FLOAT(3) = 3.000 | Use INT for whole numbers |
| INT | INT(expression) | Casts to an integer | INT(-9.7) = -9 | Expressions truncate toward zero. A string is first read as a float then rounded. INT("9.7") gives 10. Use ROUND, CEILING or FLOOR for control |
| STR | STR(expression) | Casts to a string | STR([Postal Code]) | Stops codes being summed. A boolean converts to "1" or "0" and unknown to null |

Booleans cast to integer, float or string (true is 1, false is 0) but not to a date.

## 5. Logical and null handling

Keywords and functions in one table. Use ELSEIF as one word. Every IF and CASE ends with END.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| IF | IF test THEN value [ELSEIF test THEN value] [ELSE value] END | Returns the value of the first true test | IF [Profit] > 0 THEN "Gain" ELSE "Loss" END | Without ELSE a failed test returns null |
| THEN | part of IF or CASE | Result when a test is true | see IF | Required after each test |
| ELSEIF | ELSEIF test THEN value | Extra test inside IF | IF [x] > 10 THEN "H" ELSEIF [x] > 5 THEN "M" ELSE "L" END | Tests run top down. Order matters |
| ELSE | ELSE value | Default when no test is true | see IF | Optional. Omit and unmatched rows are null |
| END | END | Closes IF or CASE | see IF | Missing END is the most common syntax error |
| CASE | CASE expression WHEN value THEN result [ELSE result] END | Returns the result of the first matching WHEN | CASE [Region] WHEN "East" THEN 1 WHEN "West" THEN 2 ELSE 0 END | Matches equality only. For ranges use IF |
| WHEN | WHEN value THEN result | A value to match inside CASE | see CASE | Also accepts WHEN IN with a list or set |
| IIF | IIF(test, then, else, [unknown]) | Inline IF | IIF([Profit] > 0, "Gain", "Loss", "Unknown") | The optional fourth value covers a null test. Without it null in gives null out |
| IFNULL | IFNULL(expr1, expr2) | Expr1 unless it is null then expr2 | IFNULL([Discount], 0) | Types must match. Use ZN for numbers. IFNULL also works for text and dates |
| ISNULL | ISNULL(expression) | True if the expression is null | ISNULL([Ship Date]) | An empty string is not null. Test with [Field] = "" too |
| ZN | ZN(expression) | Expression, or 0 if null | ZN(SUM([Sales])) | Numbers only. ZN is shorthand for IFNULL(x, 0). Wrap the aggregate, not the field, when the whole view row is missing |
| AND | expr1 AND expr2 | True if both are true | [Sales] > 100 AND [Profit] > 0 | Short circuit evaluation. Null AND false is false |
| OR | expr1 OR expr2 | True if either is true | [Region] = "East" OR [Region] = "West" | Short circuit evaluation |
| NOT | NOT expression | Logical negation | NOT ISNULL([Ship Date]) | NOT of null is null |
| IN | expr1 IN expr2 | True if a value is in a set or list | [Region] IN ("East", "West") | Right side is a literal list, a set or a multiple value parameter. List syntax is round brackets with commas |

Null logic: a comparison with null returns null. IF treats null as not true, so use ISNULL or IFNULL explicitly.

## 6. Aggregate

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| ATTR | ATTR(expression) | The value if it is the same on every row else * | ATTR([Region]) | Shows * when several values exist. Compare to a string only after wrapping, for example IF ATTR([Segment]) = "A" THEN ... END. Not allowed inside LOD aggregates |
| AVG | AVG(expression) | Average of non-null values | AVG([Sales]) | Numbers only. Nulls are skipped so the count is smaller than rows. Average of averages is not the overall average |
| COLLECT | COLLECT(spatial) | Combines spatial values | COLLECT([Geometry]) | Spatial fields only. Used to merge shapes in a view |
| CORR | CORR(expr1, expr2) | Pearson correlation, -1 to 1 | CORR([Sales], [Profit]) | Limited sources: extracts, Oracle, PostgreSQL, Teradata, Vertica, BigQuery, Presto and some others. Use WINDOW_CORR or an extract elsewhere |
| COUNT | COUNT(expression) | Count of non-null values | COUNT([Order ID]) | Does not count nulls. For rows including nulls use COUNT of a never null key |
| COUNTD | COUNTD(expression) | Count of distinct non-null values | COUNTD([Customer ID]) | Slow on large data. Not additive across a view, so totals do not equal the sum of rows |
| COVAR | COVAR(expr1, expr2) | Sample covariance | COVAR([Sales], [Profit]) | Same source limits as CORR. Use WINDOW_COVAR or an extract |
| COVARP | COVARP(expr1, expr2) | Population covariance | COVARP([Sales], [Profit]) | Same source limits as CORR |
| MAX | MAX(expression) or MAX(expr1, expr2) | Maximum, or the larger of two values | MAX([Order Date]) or MAX([a], [b]) | One argument aggregates. Two arguments compare row by row. Works on strings and dates. Null in the two argument form gives null |
| MEDIAN | MEDIAN(expression) | Median of a numeric field | MEDIAN([Sales]) | Not on Access, Redshift, Cloudera Hadoop, Vertica, DB2, Netezza, SQL Server, MySQL, SAP HANA or Teradata. Extract the data |
| MIN | MIN(expression) or MIN(expr1, expr2) | Minimum, or the smaller of two values | MIN([Order Date]) or MIN([a], [b]) | Same behaviour as MAX |
| PERCENTILE | PERCENTILE(expression, number) | Value at a percentile | PERCENTILE([Sales], 0.95) | Number is a constant from 0 to 1. Limited sources: non-legacy Excel and text, extracts, Oracle 10+, Sybase IQ 15.1+, Cloudera Hive, Hortonworks Hive, EXASolution 4.2+. Extract elsewhere |
| STDEV | STDEV(expression) | Sample standard deviation | STDEV([Sales]) | n-1 denominator |
| STDEVP | STDEVP(expression) | Population standard deviation | STDEVP([Sales]) | n denominator |
| SUM | SUM(expression) | Sum of non-null values | SUM([Sales]) | Numbers only. All null gives null, so wrap with ZN where a zero is wanted |
| VAR | VAR(expression) | Sample variance | VAR([Sales]) | n-1 denominator |
| VARP | VARP(expression) | Population variance | VARP([Sales]) | n denominator |

Rule: you cannot mix aggregated and non-aggregated terms in one calculation. SUM([Sales]) / [Quantity] is an error. Use SUM([Sales]) / SUM([Quantity]). Division of integers by / returns a decimal in Tableau, so use DIV for integer division.

## 7. User

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| FULLNAME | FULLNAME() | Full name of the signed in user | FULLNAME() | Returns the local OS user in Desktop |
| ISFULLNAME | ISFULLNAME("User Full Name") | True if the user full name matches | ISFULLNAME("Ankur Napa") | Argument must be a literal string |
| ISMEMBEROF | ISMEMBEROF("Group Name") | True if the user belongs to the group | ISMEMBEROF("Managers") | Null if not signed in. Accepts Active Directory domains. Group changes apply in a new session. Basis of row level security |
| ISUSERNAME | ISUSERNAME("username") | True if the username matches | ISUSERNAME("jsmith") | Literal string only |
| USERDOMAIN | USERDOMAIN() | Domain of the current user | USERDOMAIN() | Meaningful for Active Directory on Server |
| USERNAME | USERNAME() | Username of the current user | [Manager] = USERNAME() | Basis of user filters. Set the filter on the data source, not a worksheet, for security |
| USERATTRIBUTE | USERATTRIBUTE('attribute_name') | First value of a user attribute from a JWT or SAML response | USERATTRIBUTE('Region') | Null when the attribute is absent. Embedded and SSO scenarios |
| USERATTRIBUTEINCLUDES | USERATTRIBUTEINCLUDES('attribute_name', 'expected_value') | True if any value of the attribute matches | USERATTRIBUTEINCLUDES('Region', 'EMEA') | Use for multi value attributes |

## 8. Table calculation

Table calculations run on the aggregated view. Default Compute Using is Table (Across), which is often the wrong direction. Always set Compute Using or addressing explicitly. Concepts and patterns are in [calcs-and-viz.md](calcs-and-viz.md).

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| FIRST | FIRST() | Offset from the current row to the first row | FIRST() = -2 on row 3 | Returns an offset, not a value. Zero or negative |
| INDEX | INDEX() | Position of the current row, from 1 | INDEX() <= 5 | Position only. It is not a value rank. Use as a filter for top N after sorting |
| LAST | LAST() | Offset from the current row to the last row | LAST() = 4 on row 3 of 7 | Returns an offset. LAST() = 0 flags the last row |
| LOOKUP | LOOKUP(expression, [offset]) | Value at a relative row offset | LOOKUP(SUM([Sales]), -1) | Null where the target row does not exist. Use FIRST()+n or LAST()-n for fixed positions |
| PREVIOUS_VALUE | PREVIOUS_VALUE(expression) | This calculation in the previous row | SUM([Profit]) + PREVIOUS_VALUE(0) | First row returns the argument. Seed with 1 for products |
| RANK | RANK(expression, ['asc' or 'desc']) | Standard competition rank | RANK(SUM([Sales])) | Default is descending. Ties share a rank and the next is skipped (1, 2, 2, 4). Nulls are not ranked |
| RANK_DENSE | RANK_DENSE(expression, ['asc' or 'desc']) | Dense rank | RANK_DENSE(SUM([Sales])) | Default descending. No gaps (1, 2, 2, 3) |
| RANK_MODIFIED | RANK_MODIFIED(expression, ['asc' or 'desc']) | Modified competition rank | RANK_MODIFIED(SUM([Sales])) | Default descending. Ties take the higher number (1, 3, 3, 4) |
| RANK_PERCENTILE | RANK_PERCENTILE(expression, ['asc' or 'desc']) | Percentile rank, 0 to 1 | RANK_PERCENTILE(SUM([Sales])) | Default is ascending, unlike the other ranks |
| RANK_UNIQUE | RANK_UNIQUE(expression, ['asc' or 'desc']) | Unique rank | RANK_UNIQUE(SUM([Sales])) | Default descending. Ties get different ranks by view order |
| RUNNING_AVG | RUNNING_AVG(expression) | Running average to the current row | RUNNING_AVG(SUM([Sales])) | Restarts per partition |
| RUNNING_COUNT | RUNNING_COUNT(expression) | Running count | RUNNING_COUNT(SUM([Sales])) | Counts non-null marks |
| RUNNING_MAX | RUNNING_MAX(expression) | Running maximum | RUNNING_MAX(SUM([Sales])) | None |
| RUNNING_MIN | RUNNING_MIN(expression) | Running minimum | RUNNING_MIN(SUM([Sales])) | None |
| RUNNING_SUM | RUNNING_SUM(expression) | Running total | RUNNING_SUM(SUM([Sales])) | Direction follows Compute Using. Date axis must be in the addressing |
| SIZE | SIZE() | Number of rows in the partition | SIZE() | Counts rows, not values. Needs a table calc context |
| TOTAL | TOTAL(expression) | Total of the expression across the partition | SUM([Sales]) / TOTAL(SUM([Sales])) | Default addressing is Table (Across). Percent of total fails when the direction is wrong. For fixed totals use a LOD instead |
| WINDOW_AVG | WINDOW_AVG(expression, [start, end]) | Average over a window | WINDOW_AVG(SUM([Profit]), -2, 0) | Offsets are relative to the current row. Omit them for the whole partition. Use FIRST()+n or LAST()-n for edges |
| WINDOW_CORR | WINDOW_CORR(expr1, expr2, [start, end]) | Pearson correlation over a window | WINDOW_CORR(SUM([Profit]), SUM([Sales]), -5, 0) | Works on any source |
| WINDOW_COUNT | WINDOW_COUNT(expression, [start, end]) | Count over a window | WINDOW_COUNT(SUM([Profit]), -2, 0) | None |
| WINDOW_COVAR | WINDOW_COVAR(expr1, expr2, [start, end]) | Sample covariance over a window | WINDOW_COVAR(SUM([Profit]), SUM([Sales]), -2, 0) | n-1 denominator |
| WINDOW_COVARP | WINDOW_COVARP(expr1, expr2, [start, end]) | Population covariance over a window | WINDOW_COVARP(SUM([Profit]), SUM([Sales]), -2, 0) | Equals the sample value scaled by (n-1)/n |
| WINDOW_MAX | WINDOW_MAX(expression, [start, end]) | Maximum over a window | WINDOW_MAX(SUM([Sales])) | None |
| WINDOW_MEDIAN | WINDOW_MEDIAN(expression, [start, end]) | Median over a window | WINDOW_MEDIAN(SUM([Sales]), -2, 0) | Works on any source, unlike MEDIAN |
| WINDOW_MIN | WINDOW_MIN(expression, [start, end]) | Minimum over a window | WINDOW_MIN(SUM([Sales])) | None |
| WINDOW_PERCENTILE | WINDOW_PERCENTILE(expression, number, [start, end]) | Percentile over a window | WINDOW_PERCENTILE(SUM([Profit]), 0.75, -2, 0) | Number is 0 to 1. Works on any source, unlike PERCENTILE |
| WINDOW_STDEV | WINDOW_STDEV(expression, [start, end]) | Sample standard deviation over a window | WINDOW_STDEV(SUM([Profit]), -2, 0) | n-1 denominator |
| WINDOW_STDEVP | WINDOW_STDEVP(expression, [start, end]) | Population standard deviation over a window | WINDOW_STDEVP(SUM([Profit]), -2, 0) | n denominator |
| WINDOW_SUM | WINDOW_SUM(expression, [start, end]) | Sum over a window | WINDOW_SUM(SUM([Profit]), FIRST()+1, 0) | Moving sums need explicit offsets |
| WINDOW_VAR | WINDOW_VAR(expression, [start, end]) | Sample variance over a window | WINDOW_VAR(SUM([Profit]), -2, 0) | n-1 denominator |
| WINDOW_VARP | WINDOW_VARP(expression, [start, end]) | Population variance over a window | WINDOW_VARP(SUM([Profit]), -2, 0) | n denominator |

Table calc traps: they cannot be used inside LOD aggregates or as dimensions, they run after most filters (a filter on a table calc hides marks but does not change partitions). A null in the addressing field breaks the order. The same name can sit on Rows and Columns with different Compute Using.

## 9. Level of detail (LOD)

Syntax: `{ FIXED | INCLUDE | EXCLUDE dim1, dim2 : aggregate }`. The no dimension form `{ MIN([Order Date]) }` is the same as `{ FIXED : MIN([Order Date]) }` and returns one value for the whole table. Concepts and the filter trap are in [calcs-and-viz.md](calcs-and-viz.md).

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| FIXED | { FIXED [dim] : aggregate } | Computes at the named dimensions, ignoring the view | { FIXED [Region] : SUM([Sales]) } | Ignores view filters except context filters, data source filters and extract filters. Add a filter to context to affect it |
| INCLUDE | { INCLUDE [dim] : aggregate } | Adds dimensions to the view level of detail | { INCLUDE [Customer Name] : SUM([Sales]) } | Wrap in AVG or MAX in the view to roll up again |
| EXCLUDE | { EXCLUDE [dim] : aggregate } | Removes dimensions from the view level of detail | { EXCLUDE [Region] : SUM([Sales]) } | Cannot be used where there are no dimensions to remove. Removing a computed date part only matches a field with the same definition |

Limits: no table calculations inside the aggregate. ATTR is not supported inside the aggregate. A FIXED result with no aggregate in the view needs ATTR or an aggregate to be used on a mark.

## 10. Spatial

Units in quoted unit arguments: meters or metres or m, kilometers or kilometres or km, miles or mi, feet or ft.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| AREA | AREA(polygon, 'units') | Surface area of a polygon | AREA([Geometry], 'km') | Units must be quoted |
| BUFFER | BUFFER(point or linestring or polygon, distance, 'units') | Shape around a geometry | BUFFER(MAKEPOINT(47.59, -122.32), 3, 'km') | Point gives a circle. Polygon grows with a positive distance or shrinks with a negative one |
| COLLECT | COLLECT(spatial) | Aggregate that combines spatial values | COLLECT([Geometry]) | Also listed under aggregate. Spatial fields only |
| DIFFERENCE | DIFFERENCE(spatial, spatial) | First shape with the overlap of the second removed | DIFFERENCE([Polygon1], [Polygon2]) | Polygons and multipolygons only. Not on the alphabetical page |
| DISTANCE | DISTANCE(point1, point2, 'units') | Distance between two points | DISTANCE([Origin], [Destination], 'km') | Live connections only. It keeps working after conversion to an extract |
| INTERSECTION | INTERSECTION(spatial, spatial) | Overlapping part of two shapes | INTERSECTION([A], [B]) | Polygons and multipolygons only. Not on the alphabetical page |
| INTERSECTS | INTERSECTS(geometry1, geometry2) | True if two geometries overlap | INTERSECTS([Point], [Polygon]) | Supports point and polygon, line and polygon, polygon and polygon |
| LENGTH | LENGTH(geometry, 'units') | Geodetic length of linestrings | LENGTH([Route], 'miles') | NaN if there are no linestrings |
| MAKELINE | MAKELINE(point1, point2) | Line between two points | MAKELINE(MAKEPOINT([Lat1], [Lon1]), MAKEPOINT([Lat2], [Lon2])) | Origin to destination maps. Long lines draw as geodesic curves |
| MAKEPOINT | MAKEPOINT(latitude, longitude, [SRID]) | Point from coordinates | MAKEPOINT([Latitude], [Longitude]) | Latitude first. The generated Latitude and Longitude fields cannot be used. WGS84 degrees assumed without an SRID. SRID is an EPSG code |
| NO_CUTOUTS | NO_CUTOUTS(spatial) | Fixes polygons with reversed boundaries | NO_CUTOUTS([Geometry]) | Returns the original if no fix is needed. Not on the alphabetical page |
| OUTLINE | OUTLINE(polygon) | Converts a polygon to linestrings | OUTLINE([Geometry]) | Lets you style the border apart from the fill |
| PARSE_WKT | PARSE_WKT(string) | Well known text to a spatial value | PARSE_WKT([WKT]) | Coordinates assumed WGS84. Not on the alphabetical page |
| SHAPETYPE | SHAPETYPE(geometry) | Structure of a geometry as text | SHAPETYPE([Geometry]) = "Polygon" | Returns text such as Point, Polygon, MultiPolygon or Mixed |
| SYMDIFFERENCE | SYMDIFFERENCE(spatial, spatial) | Non-overlapping parts of both | SYMDIFFERENCE([A], [B]) | Not on the alphabetical page |
| UNION | UNION(spatial) or UNION(spatial1, spatial2) | Merges geometries | UNION(VALIDATE([Geometry])) | One argument aggregates across rows. Touching polygons dissolve. Points and lines collect without dissolving. Not on the alphabetical page |
| VALIDATE | VALIDATE(geometry) | Geometry if valid else null | VALIDATE([Geometry]) | Catches self intersecting perimeters. Not on the alphabetical page |

## 11. Pass-through (RAWSQL)

These send SQL straight to the database. The expression is a quoted string with %1, %2 placeholders for the arguments. They may not work on federated, published or extract data sources. The AGG versions take aggregate expressions and run at the view level. There is no RAWSQLAGG_SPATIAL.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| RAWSQL_BOOL | RAWSQL_BOOL("sql_expr", [arg1], ...) | Boolean from SQL | RAWSQL_BOOL("%1 > 0", [Profit]) | Database specific SQL. Not portable |
| RAWSQL_DATE | RAWSQL_DATE("sql_expr", [arg1], ...) | Date from SQL | RAWSQL_DATE("CAST(%1 AS DATE)", [Text Date]) | Not portable |
| RAWSQL_DATETIME | RAWSQL_DATETIME("sql_expr", [arg1], ...) | Datetime from SQL | RAWSQL_DATETIME("CAST(%1 AS TIMESTAMP)", [Text]) | Not portable |
| RAWSQL_INT | RAWSQL_INT("sql_expr", [arg1], ...) | Integer from SQL | RAWSQL_INT("LENGTH(%1)", [Name]) | Not portable |
| RAWSQL_REAL | RAWSQL_REAL("sql_expr", [arg1], ...) | Number from SQL | RAWSQL_REAL("SQRT(%1)", [Sales]) | Not portable |
| RAWSQL_SPATIAL | RAWSQL_SPATIAL("sql_expr", [arg1], ...) | Spatial from SQL | RAWSQL_SPATIAL("ST_GeomFromText(%1)", [WKT]) | Live connections to spatial databases |
| RAWSQL_STR | RAWSQL_STR("sql_expr", [arg1], ...) | String from SQL | RAWSQL_STR("UPPER(%1)", [Name]) | Not portable |
| RAWSQLAGG_BOOL | RAWSQLAGG_BOOL("sql_expr", [arg1], ...) | Boolean from an aggregate SQL expression | RAWSQLAGG_BOOL("SUM(%1) > 0", [Profit]) | Arguments must be aggregates in the view |
| RAWSQLAGG_DATE | RAWSQLAGG_DATE("sql_expr", [arg1], ...) | Date from an aggregate SQL expression | RAWSQLAGG_DATE("MAX(%1)", [Order Date]) | Same |
| RAWSQLAGG_DATETIME | RAWSQLAGG_DATETIME("sql_expr", [arg1], ...) | Datetime from an aggregate SQL expression | RAWSQLAGG_DATETIME("MAX(%1)", [Stamp]) | Same |
| RAWSQLAGG_INT | RAWSQLAGG_INT("sql_expr", [arg1], ...) | Integer from an aggregate SQL expression | RAWSQLAGG_INT("COUNT(%1)", [ID]) | Same |
| RAWSQLAGG_REAL | RAWSQLAGG_REAL("sql_expr", [arg1], ...) | Number from an aggregate SQL expression | RAWSQLAGG_REAL("PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY %1)", [Sales]) | Common route to a median or percentile the source lacks |
| RAWSQLAGG_STR | RAWSQLAGG_STR("sql_expr", [arg1], ...) | String from an aggregate SQL expression | RAWSQLAGG_STR("STRING_AGG(%1, ',')", [Region]) | Common route to string aggregation |

## 12. Regular expression

Tableau extracts use ICU regex syntax. Other sources use their own engine, so check that database. Patterns in extracts must be constants, not fields. These functions do not work on every source.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| REGEXP_EXTRACT | REGEXP_EXTRACT(string, pattern) | Returns the part that matches | REGEXP_EXTRACT('abc 123', '[a-z]+\\s+(\\d+)') = '123' | Supported on text files, Hive, BigQuery, PostgreSQL, extracts, Excel, Salesforce, Vertica, Greenplum, Teradata 14.1+, Snowflake and Oracle. With a group the group is returned |
| REGEXP_EXTRACT_NTH | REGEXP_EXTRACT_NTH(string, pattern, index) | Returns the nth capturing group | REGEXP_EXTRACT_NTH('abc 123', '([a-z]+)\\s+(\\d+)', 2) = '123' | Index 0 returns the whole match. Narrower support than REGEXP_EXTRACT: text files, PostgreSQL, extracts, Excel, Salesforce, Vertica, Greenplum, Teradata 14.1+ and Oracle. Not Hive, BigQuery, Impala or Snowflake |
| REGEXP_MATCH | REGEXP_MATCH(string, pattern) | True if any substring matches | REGEXP_MATCH([Email], '^[^@]+@[^@]+$') | Unanchored by default. Add ^ and $ for a full match. Also supported on Impala 2.3.0+ |
| REGEXP_REPLACE | REGEXP_REPLACE(string, pattern, replacement) | Replaces matches | REGEXP_REPLACE('abc 123', '\\s', '-') = 'abc-123' | Same sources as REGEXP_EXTRACT. In extracts both pattern and replacement must be constants |

## 13. Predictive modelling and analytics extensions

Model functions are table calculations that fit a model on the fly. Script and model extension functions call an external service (TabPy, Rserve, Einstein Discovery or similar) that an admin has configured. Use aggregated arguments and set Compute Using.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| MODEL_PERCENTILE | MODEL_PERCENTILE(target_expression, predictor_expression, ...) | Probability (0 to 1) that the expected value is at or below the observed value | MODEL_PERCENTILE(SUM([Sales]), COUNT([Orders])) | Target first. The CDF of the prediction. Low or high values flag outliers |
| MODEL_QUANTILE | MODEL_QUANTILE(quantile, target_expression, predictor_expression, ...) | Predicted value at a quantile | MODEL_QUANTILE(0.5, SUM([Sales]), COUNT([Orders])) | Quantile first, which is the opposite order to MODEL_PERCENTILE. Quantile is a constant from 0 to 1 |
| MODEL_EXTENSION_BOOL | MODEL_EXTENSION_BOOL(model_name, arguments, expression) | Boolean from a deployed model | MODEL_EXTENSION_BOOL("churn", "inputSales", SUM([Sales])) | Needs an external service connection. Argument types and order must match the expressions |
| MODEL_EXTENSION_INT | MODEL_EXTENSION_INT(model_name, arguments, expression) | Integer from a deployed model | MODEL_EXTENSION_INT("bucket", "inputSales", SUM([Sales])) | Same |
| MODEL_EXTENSION_REAL | MODEL_EXTENSION_REAL(model_name, arguments, expression) | Number from a deployed model | MODEL_EXTENSION_REAL("profitRatio", "inputSales", "inputCosts", SUM([Sales]), SUM([Costs])) | Same |
| MODEL_EXTENSION_STR | MODEL_EXTENSION_STR(model_name, arguments, expression) | String from a deployed model | MODEL_EXTENSION_STR("label", "inputSales", SUM([Sales])) | The help text also writes this as MODEL_EXTENSION_STRING. Check the name your version accepts |
| SCRIPT_BOOL | SCRIPT_BOOL(script, expr1, ...) | Boolean from an R or Python script | SCRIPT_BOOL("return map(lambda x: x > 0, _arg1)", SUM([Profit])) | R uses .arg1 with a leading dot. Python uses _arg1 with a leading underscore |
| SCRIPT_INT | SCRIPT_INT(script, expr1, ...) | Integer from a script | SCRIPT_INT("return [int(x) for x in _arg1]", SUM([Profit])) | The script must return one column with as many rows as it received |
| SCRIPT_REAL | SCRIPT_REAL(script, expr1, ...) | Number from a script | SCRIPT_REAL("return map(lambda x: x * 0.5, _arg1)", SUM([Profit])) | Runs per partition. Needs Rserve or TabPy configured |
| SCRIPT_STR | SCRIPT_STR(script, expr1, ...) | String from a script | SCRIPT_STR("return [str(x) for x in _arg1]", SUM([Profit])) | The help text also writes SCRIPT_STRING. Check the name your version accepts |

## 14. Additional (Hive, Impala, BigQuery)

Source specific functions. They work only on the named connection. PARSE_URL and PARSE_URL_QUERY also work on Cloudera Impala.

| Function | Syntax | Does | Example | Note |
|---|---|---|---|---|
| GET_JSON_OBJECT | GET_JSON_OBJECT(JSON string, JSON path) | JSON value at a path | GET_JSON_OBJECT([Json], '$.name') | Hadoop Hive |
| PARSE_URL | PARSE_URL(string, url_part) | URL component | PARSE_URL('http://www.tableau.com', 'HOST') = 'www.tableau.com' | Hive and Impala. Parts: HOST, PATH, QUERY, REF, PROTOCOL, AUTHORITY, FILE, USERINFO |
| PARSE_URL_QUERY | PARSE_URL_QUERY(string, key) | Value of a query parameter | PARSE_URL_QUERY('http://www.tableau.com?page=1&cat=4', 'page') = '1' | Hive and Impala |
| XPATH_BOOLEAN | XPATH_BOOLEAN(XML string, XPath) | True if the XPath matches or is true | XPATH_BOOLEAN([Xml], 'values/value[@id="1"] = 5') | Hive |
| XPATH_DOUBLE | XPATH_DOUBLE(XML string, XPath) | Floating point result | XPATH_DOUBLE([Xml], 'sum(value/*)') = 6.5 | Hive |
| XPATH_FLOAT | XPATH_FLOAT(XML string, XPath) | Floating point result | XPATH_FLOAT([Xml], 'sum(value/*)') = 6.5 | Hive |
| XPATH_INT | XPATH_INT(XML string, XPath) | Integer result | XPATH_INT([Xml], 'sum(value/*)') = 6 | Hive. Zero if not numeric |
| XPATH_LONG | XPATH_LONG(XML string, XPath) | Long integer result | XPATH_LONG([Xml], 'sum(value/*)') = 6 | Hive. Zero if not numeric |
| XPATH_SHORT | XPATH_SHORT(XML string, XPath) | Short integer result | XPATH_SHORT([Xml], 'sum(value/*)') = 6 | Hive. Zero if not numeric |
| XPATH_STRING | XPATH_STRING(XML string, XPath) | Text of the first matching node | XPATH_STRING([Xml], 'sites/url[@domain="com"]') | Hive |
| DOMAIN | DOMAIN(string_url) | Domain of a URL | DOMAIN('http://www.google.com:80/index.html') = 'google.com' | Google BigQuery |
| GROUP_CONCAT | GROUP_CONCAT(expression) | Joins values into one comma separated string | GROUP_CONCAT([Region]) = "Central,East,West" | Google BigQuery. Acts like SUM for strings |
| HOST | HOST(string_url) | Host name including any port | HOST('http://www.google.com:80/index.html') = 'www.google.com:80' | Google BigQuery |
| LOG2 | LOG2(number) | Base 2 logarithm | LOG2(16) = 4 | Google BigQuery |
| LTRIM_THIS | LTRIM_THIS(string, string) | Removes a leading occurrence of the second string | LTRIM_THIS('[-Sales-]', '[-') = 'Sales-]' | Google BigQuery. Compare LTRIM, which removes spaces only |
| RTRIM_THIS | RTRIM_THIS(string, string) | Removes a trailing occurrence of the second string | RTRIM_THIS('[-Market-]', '-]') = '[-Market' | Google BigQuery |
| TIMESTAMP_TO_USEC | TIMESTAMP_TO_USEC(expression) | Timestamp to UNIX microseconds | TIMESTAMP_TO_USEC(#2012-10-01 01:02:03#) = 1349053323000000 | Google BigQuery |
| TLD | TLD(string_url) | Top level domain plus any country domain | TLD('http://www.google.co.uk:80/index.html') = '.co.uk' | Google BigQuery |
| USEC_TO_TIMESTAMP | USEC_TO_TIMESTAMP(expression) | UNIX microseconds to timestamp | USEC_TO_TIMESTAMP(1349053323000000) | Google BigQuery |

## 15. Operators and precedence

Highest first. Operators on one level run left to right. Brackets override the order and the innermost run first.

| Level | Operator | Does | Note |
|---|---|---|---|
| 1 | - (negate) | Unary minus | -(7+3) = -10 |
| 2 | ^ | Power | 6^3 = 216. Same as POWER |
| 3 | * / % | Multiply, divide, remainder | % works on integers only. 9 % 2 = 1. / on two integers returns a decimal, so use DIV for integer division |
| 4 | + - | Add or concatenate, subtract | + joins strings and adds days to dates. Minus on dates subtracts days. Any null in a + gives null |
| 5 | == = > < >= <= != <> | Comparison | Returns true, false or null. = and == are the same. != and <> are the same |
| 6 | NOT | Negation | Runs after comparisons |
| 7 | AND | Logical and | Before OR. Add brackets when mixing AND with OR |
| 8 | OR | Logical or | Lowest |

Common slip: [a] = 1 OR [b] = 2 AND [c] = 3 runs the AND first. Bracket it.
