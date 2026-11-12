# Data and prep for Tableau dashboards

How to shape data before a chart exists. Read this before building any data source. Sources: Ankur's Tableau field notes (tested on Tableau 2024.2 and later) and the brewery workshop build scripts.

## 1. Data shape rules

Tableau wants tall, clean, typed data. Fix shape first and most calculations disappear.

| Rule | Why |
|---|---|
| One row per event at one declared grain (batch, order line, reading, store and month) | Every SUM and COUNT depends on it. Mixed grains in one table double count |
| Tall beats wide | One column per month cannot be filtered, coloured or put on an axis. Pivot to `period` and `value` |
| One measure meaning per column | Do not store hectolitres and cases in one `Value` column without a unit column |
| Dimensions as text, measures as numbers, dates as real dates | Dates typed as text lose the date hierarchy and continuous axes |
| Keys are stable and unique at their own grain | Joins, relationships and upserts all rely on them |
| Keep a unit column when units mix | `UoM` next to `Value` stops a sum of kg plus bottles |
| Missing is NULL, never 0 or "n/a" | A zero drags averages down. A text value breaks the numeric type |
| No totals or subtotals inside the data | Tableau adds its own. Embedded totals double count |
| Names that read well on a dashboard | `Volume_HL` becomes "Volume (hL)" once, in the published source |

### Long versus wide

Wide (one row per store, one column per week):

| store_id | product_id | wk36 | wk37 | wk38 | wk39 |
|---|---|---|---|---|---|
| ST-003 | P-101 | 20 | 24 | 28 | 18 |

Tall (one row per store, product and week). This is the shape to build on:

| store_id | product_id | week | on_hand |
|---|---|---|---|
| ST-003 | P-101 | wk36 | 20 |
| ST-003 | P-101 | wk37 | 24 |

Wide is fine only for a pure text lookup table or a crosstab that is the final output.

### One flat table or a few related tables

Two shapes work:

- **Flat event table.** One row per event with a `Event_Type` column and shared batch fields repeated. The brewery workshop uses this (`brewery_flat`): stage, QC and inventory events all in one table, with `Detail`, `Value`, `Pass`, `UoM`, `Qty_Planned` and `Cost_ZAR` filled only where they apply. It is simple to publish to Tableau Public as one extract. The cost is sparse columns and batch level fields (`Volume_HL`) repeated on every event row. A SUM of `Volume_HL` over this table counts each batch once per event. Use a FIXED LOD or `COUNTD` or filter to one `Event_Type` first.
- **Star of related tables.** Batches, stage events, QC samples and inventory as separate tables joined by `Batch_ID`. Use relationships (section 2). This is the right default for Server and Cloud models.

Grain check before any build: say in one sentence what one row is. If you cannot, split the table.

### Typing rules that bite

- Prep and Desktop guess types from a sample. Dates in mixed formats arrive as nulls once typed as dates. Keep the column as string, parse it yourself, then retype.
- Number formats: keep currency out of the data. Format in Tableau.
- Money in Hyper: `numeric(10, 2)`, not double, when sums must reconcile to the paisa.
- Booleans as `Pass` and `Fail` text are fine for dashboards because they colour and filter cleanly.

## 2. Relationships, joins and blends

A Tableau data source has two layers.

- **Logical layer.** Tables linked by relationships (noodles). Each table stays at its own grain. Tableau joins only at query time and only for fields the view uses.
- **Physical layer.** Open a logical table (double-click) to join or union physical tables into one flat table. Joins merge rows before any question is asked.

### Choosing

| Use | When | Breaks when |
|---|---|---|
| Relationship | Default. Facts and dimensions, or two facts at different grains | You relate two facts on a non-unique key. Totals look right per store and go wrong when another dimension is added |
| Join (physical) | The result must be one table: extract filter on fields from both sides, a one to one lookup with every record matching, a union of monthly files | One to many. The many side repeats. Sales inflate by the fan-out |
| Union | Same columns across files or tables (monthly exports) | Column names differ. Merge mismatched fields first |
| Blend | Two sources that cannot be related, such as two published data sources | LODs need the linking field in the view. Aggregates only to linking fields. Secondary is left-joined to primary. Workbook Optimizer flags blends |

Tableau's own guidance: relationships first, joins only when you need them.

### Relationship settings

- Edit with **Performance Options** on the noodle. Defaults: **Cardinality** Many to Many and **Referential Integrity** Some records match.
- Change them only when you know the data. Example: One store per many orders with all records matching.
- Wrong settings give wrong numbers fast. If a key is missing on one side and you set One and All, rows vanish silently.
- With Some records match, a target for a store with no orders is kept on the target side. A physical inner join drops it.

### The double counting demonstration (verbatim numbers)

Orders (55 rows, 153,065.80 sales) joined physically to targets (72 rows, 12 per store) on `store_id` gives 660 rows. SUM(Sales) reads 1,836,789.60, exactly twelve times the truth. Related at the store level, the same two tables return 153,065.80 and 153,650 targets.

Sales calculation used throughout:

```sql
[Quantity] * [Unit Price] * (1 - [Discount])
```

### Fix a fan-out without leaving a join

Only if a join is unavoidable. Use FIXED LOD on the one side:

```sql
{FIXED [Store Id] : MAX([Target Sales])}
```

Better: relate instead.

## 3. Multi-fact models (2024.2 and later)

Two fact tables that share dimensions: give the model more than one base table.

1. Remove the second fact from the canvas.
2. Drag it back onto the **New Base Table** drop area. Accept the warning.
3. Hover the new table, drag its plus icon onto the shared dimension (stores). Stores now has two incoming relationships and becomes a **shared table**.

Brewery example: brew logs at batch grain and a sales plan at beer and month grain. Relate both to a shared beer table and a shared month table. Brewed against planned then lines up per beer per month. Never join them.

Limits to design around:

- Row-level calculations, combined fields and set definitions can only use fields from the same upstream base table.
- Tableau Pulse may not work on multi-fact sources. Swapping dimensions with a parameter can fail silently.
- Extracts of multi-fact sources need 2024.2.1 or later.
- If the facts share no dimension table (category stored as text on one side, reached through products on the other), build a shared table first. That is modelling, not a setting.
- Relationships cannot be defined between two published data sources. Model inside one source or blend.

## 4. Prep flow patterns

Prep Builder comes with the Creator licence on Windows and Mac. Creators can also build flows in the browser on Tableau Cloud and Server 2020.4 or later. Flow shape: Input, steps, profile, changes, Output.

### Where a fix lives

| Problem | Fix in |
|---|---|
| Store ID typed in lower case by one till | Prep, then tell the till owner |
| One column per month | Prep (Pivot) |
| One-off grouping for one chart | Desktop |
| Ratio that must respect dashboard filters | Desktop |
| Product hierarchy every team uses | Warehouse or source |
| Export that drops rows | Upstream. Prep cannot clean rows that never arrived |

Rule: clean as far upstream as you have authority and no further downstream than the people who need the fix.

### When Prep beats calculations

- Cleaning done once and written to a table instead of repeated in each workbook.
- Pivots (Desktop pivot is limited and repeated per workbook).
- Dedup, union and join with row counts you can check at each step.
- Fixed LOD, rank and aggregate results that are expensive at view time.
- A visible Changes pane as the audit record.

Desktop wins for anything that depends on the reader's filters: ratios of sums, percent of total, table calculations, parameter driven logic. Prep calculates row by row and in fixed groups before any filter exists.

### Clean

- Trim and case: **Clean > Trim Spaces**, **Clean > Make Uppercase** on the key field.
- Clean values before looking for duplicates. Otherwise Prep calls two copies of one order different.
- Do not hide an unknown key (a store `ST-099` not in the registry). Keep it, label it, let someone chase it.
- The profile is drawn from a sample by default. On large tables a bad value may never show in the profile but is still in the data.

### Parse mixed date formats

Keep `order_date` as string at the Input step. Then create `order_day`:

```sql
IFNULL(
  IFNULL(
    DATEPARSE("yyyy-MM-dd", [order_date]),
    DATEPARSE("dd/MM/yyyy", [order_date])
  ),
  DATEPARSE("dd MMM yyyy", [order_date])
)
```

Each DATEPARSE returns null when text does not fit, so the IFNULL chain tries them in turn. Capital `MM` is month. Lower case `mm` is minutes and gives dates stuck on January. After the card shows no null bar, delete the original and rename `order_day` to `order_date`. Ambiguous formats such as `06/07/2026` cannot be solved by code. Ask the owner of the export.

### Union

- Drag one Input onto another until **Union** appears.
- Mismatched fields (`qty` against `quantity`): select both, right-click, **Merge Fields**. Fix types in each input first or the merged field shows a Change Data Type icon.
- For a folder of same-shape files use **Union multiple tables** on the Input step **Tables** tab.
- Keep the added **Table Names** field for tracing, but leave it out of the duplicate check.

### Identify duplicates

1. Clean step, select every field except **Table Names**.
2. **Identify Duplicate Rows** adds **Is Duplicate Row?** with Unique and Duplicate.
3. Select Unique, **Keep Only**.

Include Table Names and an order in two overlapping exports survives twice. Duplicates differing in one field (a corrected quantity) are not caught. Pick only the key field and decide which copy wins.

### Join

- Check the join clause and read **Summary of Join Results** before changing anything.
- A default inner join silently drops unmatched rows. Use a Left join plus a label:

```sql
IFNULL([region], "Unmapped")
```

- Net amount in the flow:

```sql
[quantity] * [unit_price] * (1 - [discount])
```

- Remove duplicated key columns (`store_id-1`) after the join.

### Pivot (columns to rows)

1. Plus on the step, **Pivot**, direction **Columns to Rows**.
2. Tick **Use wildcard search to pivot**, type `wk`, press Enter.
3. Rename the names field to `week` and the values field to `on_hand`.

The wildcard picks up next month's `wk40` to `wk43` with no edit. Dragging four named fields would ignore every new week. A wildcard such as `wk` also matches `wk_notes`, so tighten the pattern. Rows to Columns mode cannot be undone by dragging fields back. Use Undo. Date fields must be strings before they become column names.

### Aggregate

Drag group fields to **Grouped Fields** and measures to **Aggregated Fields** (SUM default, switch to AVG and so on). Every field not dragged in is gone after this step. Branch the flow first if you need the detail later.

Aggregate before you join: a daily summary per store joined to 50 store rows is cheap. Joining stores to millions of order lines and then aggregating is not.

### LOD in Prep

Only FIXED is available. No INCLUDE or EXCLUDE. No nesting. No combining an LOD with other arithmetic in one field. So build two fields:

```sql
{FIXED [store_id], [week] : SUM([on_hand])}
```

Name it `store_week_units`. Then:

```sql
[on_hand] / [store_week_units]
```

Name that `share_of_store_week`. The one-field form `[on_hand] / {FIXED [store_id], [week] : SUM([on_hand])}` is rejected. A Prep LOD is computed once when the flow runs and ignores dashboard filters. A share that must respond to a category filter belongs in Desktop.

### Rank in Prep

```sql
{PARTITION [store_id] : {ORDERBY [avg_on_hand] : RANK()}}
```

- Descending by default. Largest gets rank 1. Add `ASC` after the field to reverse.
- RANK gives ties the same number and skips the next. RANK_DENSE does not skip. ROW_NUMBER exists in the calculation editor but not the visual one.
- Top three per group: **Filter > Calculation**, then `[stock_rank] <= 3`. With ties you get more than three rows. That is correct.

Worked check (54 stores-by-product rows, 4 weeks): input 54, after Pivot 216, after Aggregate 54, after rank filter 18.

### Output

- **Save output to** File as **Tableau Data Extract (.hyper)**, or Published data source, or a database table.
- Write options: Hyper and published sources support **Create table** and **Append to table** only. CSV supports Create table only. Excel, Amazon S3, CRM Analytics and Databricks outputs do not support incremental refresh.
- Running a flow twice with Append doubles every row.
- Save the flow as `.tfl`. Use **Export Packaged Flow** (.tflx) to carry the input files.
- Do not name a field `Number of Records`. It causes a permission error in Prep.

### Prep at scale

Measure first: Performance of Flow Runs admin view, Backgrounder Task Delays, or the REST API:

```bash
curl -s "https://<your-pod>.online.tableau.com/api/<api-version>/sites/<site-id>/flows/runs?filter=flowId:eq:<flow-id>" \
  -H "X-Tableau-Auth: <token>" -H "Accept: application/json"
```

Fix in this order:

1. Untick unused fields in each Input step. A later Clean step removes them after they were read.
2. Filter rows in the Input step so the condition reaches the database:

```sql
[order_date] >= DATEADD('month', -24, TODAY())
```

3. Aggregate before you join.
4. Use custom SQL or a database view for heavy joins. The database joins large tables better than a flow.
5. Replace copies of one flow with a flow parameter.

The data sample setting only speeds editing. A scheduled run always processes the full data.

Flow parameters (Prep Builder 2021.4.1, Cloud and Server 2021.4.0 or later): create `p_region` as String with a list of allowed values. Insert it from the editor's parameter list in the filter:

```sql
[region] = [p_region]
```

Put the parameter in the Output name. Publish once and schedule one task per value. An administrator must enable flow parameters in site or server settings. Avoid **All** as allowed values for any parameter used in custom SQL (injection risk). Parameters cannot add or remove steps. System parameters for run date and time arrive in Prep Builder 2023.2.

A `.tfl` is a zip of JSON files. Keep it in Git, publish by script (Tableau Server Client or REST) so the file matches a commit. Download the published copy before editing because web edits leave nothing in your laptop copy.

## 5. Extracts and the Hyper API

The Hyper API is the extract engine as a library. Use it when a dashboard source is a script output (CSV, ERP export, simulator) rather than a database.

Install:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install tableauhyperapi tableauserverclient
```

The package ships its own `hyperd` for Windows, macOS and Linux. Pin the tested version in `requirements.txt` (versions look like `0.0.26479`).

### Table definition API

```python
from tableauhyperapi import (
    Connection, CreateMode, HyperProcess, NOT_NULLABLE, NULLABLE, SqlType,
    TableDefinition, TableName, Telemetry, escape_string_literal,
)

ORDERS = TableDefinition(
    table_name=TableName("Extract", "Extract"),
    columns=[
        TableDefinition.Column("order_id", SqlType.text(), NOT_NULLABLE),
        TableDefinition.Column("order_date", SqlType.date(), NOT_NULLABLE),
        TableDefinition.Column("store_id", SqlType.text(), NOT_NULLABLE),
        TableDefinition.Column("product_id", SqlType.text(), NOT_NULLABLE),
        TableDefinition.Column("quantity", SqlType.int(), NOT_NULLABLE),
        TableDefinition.Column("unit_price", SqlType.numeric(10, 2), NOT_NULLABLE),
        TableDefinition.Column("discount", SqlType.numeric(4, 2), NULLABLE),
    ],
)
```

- Always explicit types. `numeric(10, 2)` for money, `date` for dates. Let Hyper guess and you get text.
- `NOT_NULLABLE` on keys and quantities makes bad rows fail the load instead of slipping through as nulls.
- `"Extract"."Extract"` is the schema and table name Tableau uses in its own single-table extracts. Use it by default.
- Other SqlType constructors seen in the workshop build: `SqlType.double()`, `SqlType.big_int()`, `SqlType.text()`, `SqlType.date()`.

### Pattern A: Inserter from a CSV (the brewery workshop build)

From `build_hyper.py`. Use when each value needs Python parsing. It bakes `brewery_flat.csv` into `brewery_flat.hyper` so a `.twbx` can go to Tableau Public (which needs extracts, not live connections):

```python
import csv
from pathlib import Path
from tableauhyperapi import (
    HyperProcess, Telemetry, Connection, CreateMode,
    TableDefinition, SqlType, Inserter, TableName, Nullability, Date,
)

HERE = Path(__file__).parent
CSV_PATH = HERE / "data" / "brewery_flat.csv"
HYPER_PATH = HERE / "data" / "brewery_flat.hyper"

COLUMNS = [
    ("Batch_ID", SqlType.text(), "text"),
    ("Style", SqlType.text(), "text"),
    ("Brewer", SqlType.text(), "text"),
    ("Status", SqlType.text(), "text"),
    ("Volume_HL", SqlType.double(), "float"),
    ("Date", SqlType.date(), "date"),
    ("Stage", SqlType.text(), "text"),
    ("Stage_Order", SqlType.big_int(), "int"),
    ("Equipment", SqlType.text(), "text"),
    ("Operator", SqlType.text(), "text"),
    ("Duration_Hr", SqlType.double(), "float"),
    ("Event_Type", SqlType.text(), "text"),
    ("Detail", SqlType.text(), "text"),
    ("Value", SqlType.double(), "float"),
    ("Pass", SqlType.text(), "text"),
    ("UoM", SqlType.text(), "text"),
    ("Qty_Planned", SqlType.double(), "float"),
    ("Cost_ZAR", SqlType.double(), "float"),
]


def parse_row(row):
    out = []
    for col_name, _, kind in COLUMNS:
        raw = row.get(col_name, "")
        if raw == "" or raw is None:
            out.append(None)
        elif kind == "float":
            out.append(float(raw))
        elif kind == "int":
            out.append(int(raw))
        elif kind == "date":
            y, m, d = raw.split("-")
            out.append(Date(int(y), int(m), int(d)))
        else:
            out.append(str(raw))
    return out


def main():
    if HYPER_PATH.exists():
        HYPER_PATH.unlink()

    table_def = TableDefinition(
        table_name=TableName("Extract", "Extract"),
        columns=[
            TableDefinition.Column(name, sql_t, Nullability.NULLABLE)
            for name, sql_t, _ in COLUMNS
        ],
    )

    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(
            endpoint=hyper.endpoint,
            database=str(HYPER_PATH),
            create_mode=CreateMode.CREATE_AND_REPLACE,
        ) as conn:
            conn.catalog.create_schema("Extract")
            conn.catalog.create_table(table_def)

            with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                rows = [parse_row(r) for r in reader]

            with Inserter(conn, table_def) as ins:
                ins.add_rows(rows)
                ins.execute()

            row_count = conn.execute_scalar_query(
                f'SELECT COUNT(*) FROM {TableName("Extract", "Extract")}'
            )
            print(f"Wrote {row_count} rows to {HYPER_PATH}")
            print(f"Size: {HYPER_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
```

Notes on the pattern: empty string becomes `None` (NULL). Dates must be `tableauhyperapi.Date` objects, not strings. Ints and floats must be cast in Python. `Inserter` is a context manager and nothing is written until `ins.execute()`. Delete the old file first or use `CREATE_AND_REPLACE`.

### Pattern B: COPY from CSV, build to a temp file, swap

Fastest load because `COPY` runs inside the Hyper process. Typed columns reject dirty rows:

```python
import sys
from pathlib import Path

CSV = Path(sys.argv[1] if len(sys.argv) > 1 else "harbour-goods-orders-clean.csv")
HYPER = Path("harbour-goods-orders.hyper")
BUILD = HYPER.with_name("harbour-goods-orders.building.hyper")

with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(
        endpoint=hyper.endpoint,
        database=BUILD,
        create_mode=CreateMode.CREATE_AND_REPLACE,
    ) as conn:
        conn.catalog.create_schema(ORDERS.table_name.schema_name)
        conn.catalog.create_table(ORDERS)
        loaded = conn.execute_command(
            f"COPY {ORDERS.table_name} FROM {escape_string_literal(str(CSV))} "
            "WITH (format => 'csv', header => true)"
        )
        units, net = conn.execute_list_query(
            f"SELECT SUM(quantity), SUM(quantity * unit_price * (1 - discount)) "
            f"FROM {ORDERS.table_name}"
        )[0]
        print(f"loaded {loaded} rows, {units} units, net {net}")

# Swap in the new file only after the load succeeded.
BUILD.replace(HYPER)
```

`CREATE_AND_REPLACE` wipes the target, so build into a second file and swap. Yesterday's extract then survives a bad night. Print row count and a control total after every build and compare to the source.

### Pattern C: upsert into an existing extract

Open with `CreateMode.NONE`, stage, delete matching keys, insert:

```python
with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, HYPER, CreateMode.NONE) as conn:
        # Stage the new file in a temporary table with the same columns.
        conn.execute_command(
            f"CREATE TEMPORARY TABLE staging AS SELECT * FROM {ORDERS} LIMIT 0"
        )
        conn.execute_command(
            f"COPY staging FROM {escape_string_literal(str(UPDATE_CSV))} "
            "WITH (format => 'csv', header => true)"
        )
        # Replace any order that arrives again, then add the rest.
        replaced = conn.execute_command(
            f"DELETE FROM {ORDERS} WHERE order_id IN (SELECT order_id FROM staging)"
        )
        added = conn.execute_command(f"INSERT INTO {ORDERS} SELECT * FROM staging")
```

Here `ORDERS = TableName("Extract", "Extract")`. Delete then insert by key is idempotent: run it twice and totals do not move. It is not atomic. Copy the file, update the copy and swap it in for anything that matters. It needs a unique and stable key.

### Publish a Hyper file

A published `.hyper` has no live source for Cloud to refresh. Republish it with Tableau Server Client in Overwrite mode:

```python
import os

import tableauserverclient as TSC

HYPER_FILE = "harbour-goods-orders.hyper"
DATASOURCE_NAME = "Harbour Goods Orders Extract"
PROJECT = "Harbour Sales"

auth = TSC.PersonalAccessTokenAuth(
    os.environ["TABLEAU_PAT_NAME"],
    os.environ["TABLEAU_PAT_SECRET"],
    site_id=os.environ["TABLEAU_SITE"],
)
server = TSC.Server(os.environ["TABLEAU_SERVER"], use_server_version=True)

with server.auth.sign_in(auth):
    projects = [p for p in server.projects.filter(name=PROJECT) if p.parent_id is None]
    if not projects:
        raise SystemExit(f"Project {PROJECT} not found")
    ds = server.datasources.publish(
        TSC.DatasourceItem(projects[0].id, name=DATASOURCE_NAME),
        HYPER_FILE,
        mode=TSC.Server.PublishMode.Overwrite,
    )
    print(f"Published {ds.name} ({ds.id})")
```

Nightly job: build or update, check totals, publish. For Tableau Public the extract goes inside a `.twbx` and is not published through TSC.

## 6. Extract refresh and incremental refresh

### In Desktop

**Data > the source > Extract Data**. Keep **All rows**, tick **Incremental refresh** and pick the column under **Identify new rows using column**. Use a rising ID or a load timestamp. Set this up before publishing.

- Incremental adds rows with a value above the stored maximum. It never sees edits or deletes in old rows.
- A date column fails when yesterday's rows arrive late. They are not later than the stored maximum. Use a sequence or load timestamp.
- Use a date range refresh if old rows can change.
- Pair nightly incremental with a weekly full refresh.
- A schema change forces a full refresh.

### Backgrounder load

A backgrounder runs one job at a time. Sixty refreshes at 02:00 on two backgrounders leave 58 waiting. Users see yesterday's numbers at 07:00. Fix in this order:

1. Spread the schedules (every 15 or 30 minutes across the window). On Server a lower priority number runs first. Give the business-critical source the best priority.
2. Make big sources incremental.
3. Remove schedules for content nobody opens (stale for 90 days).
4. Add capacity last. Server only:

```bash
tsm topology set-process -n node2 -pr backgrounder -c 4
tsm pending-changes apply
```

```bash
tsm topology set-node-role -n node2 -r extract-refreshes
tsm pending-changes apply
```

The node role needs Advanced Management and restarts the server. Cloud: capacity is capped by edition (up to 15 concurrent extract jobs on Standard).

Measure queue wait on Server (timestamps are UTC, so 02:00 in Bengaluru is 20:30 the previous day):

```sql
SELECT date_trunc('hour', created_at) AS hour_queued,
       COUNT(*) AS jobs,
       ROUND(AVG(EXTRACT(EPOCH FROM (started_at - created_at)) / 60)::numeric, 1) AS avg_wait_min,
       ROUND(MAX(EXTRACT(EPOCH FROM (started_at - created_at)) / 60)::numeric, 1) AS max_wait_min,
       ROUND(SUM(EXTRACT(EPOCH FROM (completed_at - started_at)) / 60)::numeric, 1) AS run_min,
       SUM(CASE WHEN finish_code = 1 THEN 1 ELSE 0 END) AS failed
FROM background_jobs
WHERE job_name IN ('Refresh Extracts', 'Increment Extracts')
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY 1
ORDER BY 1;
```

Run `SELECT DISTINCT job_name FROM background_jobs` first to confirm names. On Cloud use the Admin Insights Job Performance data source or the REST API (`/jobs?filter=jobType:eq:refresh_extracts`).

Time limits: Cloud cancels one refresh at two hours (fixed). Server uses `backgrounder.querylimit` (7200 seconds default) plus `backgrounder.extra_timeout_in_seconds` (1800 default).

### Prep Conductor schedules

Scheduling flows needs Prep Conductor, part of Data Management. Without it you can publish and run flows by hand on the web only. Or run `tableau-prep-cli --incrementalRefresh -t flow.tfl` from a scheduler you own.

Flow incremental setup: Input step **Settings** tab, **Enable incremental refresh**, **Input field** `order_seq` (whole number, date or datetime, one field only), matching **Output field** with the same name and type. First run is always a full refresh. Output write options: full **Create table**, incremental **Append to table**. If the count jumps by the whole table on an incremental run, the incremental write option is Create table or the input field is wrong. Set **Embedded Password** on database connections before publishing. Packaged local files are not refreshed and Tableau Cloud has no direct file connections, so schedule against a database.

Typical tasks: incremental at 02:00 daily and full at 03:00 on Sunday. Use a **Linked Task** (up to 20 flows) when one flow feeds another.

## 7. Published and certified data sources

A published data source is one model on the server, reused by every workbook. Build joins, calculations, names and formats once.

Build checklist:

1. Relate tables (relationships, not inner joins, so unmatched keys survive).
2. Add shared calculations:

```sql
// Net Sales
[Quantity] * [Unit Price] * (1 - [Discount])
```

```sql
// Gross Margin
[Net Sales] - [Quantity] * [Unit Cost]
```

3. Set default number formats (**Default Properties > Number Format**) and a **Comment** on each key measure.
4. Hide duplicate key fields. Group fields into folders such as Order, Store, Product, Measures.
5. Extract (**Extract > Edit**, keep **Logical Tables**, **All rows**).
6. **Server > Publish Data Source**. Tick **Update workbook to use the published data source**. For databases set **Embed password**. Schedules cannot run on Prompt user.
7. Schedule: Cloud via **Explore > All Data Sources > Actions > Refresh Extracts > Schedule a Refresh**. Server via the **Extract Refreshes** tab (admins define schedules). Press **Refresh Now** once to prove the server can reach the data.
8. Certify: **... > Data Labels > Certification** (Server 2023.1 and earlier: **Edit Certification**). Tick **Certified** and add a note naming the owner and refresh time. Allowed for site admins, project owners and project leaders. No Data Management needed for data sources.

Verification: connect a second workbook with **Data > New Data Source > Tableau Server**. Same totals with no local calculated fields. A different total (155,415.80 against 156,269.85 in the sample) means a relationship became an inner join.

Rules:

- The server must see the file. A laptop path or a mapped drive letter fails. Use a UNC share on Server, or Bridge or a cloud store on Cloud.
- Certification is a promise. Put a named team in the note and review quarterly.
- Move good workbook calculations into the source. Do not let authors keep rebuilding Net Sales.
- Use a service account for embedded credentials. Passwords and OAuth tokens expire with the person.

## 8. Virtual connections and data policies

Four governance layers, each with its own question:

| Layer | Answers | Needs Data Management |
|---|---|---|
| Virtual connection | Who holds the database credentials | Yes |
| Data policy on it | Who sees which rows, once, for every workbook, source and flow input | Yes |
| Certification | Which source to use | No (for a published data source) |
| Tableau Catalog | What breaks if a column changes (lineage) | Yes |

Data Management is no longer sold as a stand-alone add-on. You have it from an earlier purchase, the Tableau+ bundle or Tableau Cloud+ on Cloud, or Tableau Server+ or Tableau Enterprise on Server. Check before designing.

Virtual connection steps for a policy:

1. Create the virtual connection and add the fact table and the entitlement table.
2. **Data Policies** tab. Drag the fact table to **Add as Policy Table**.
3. Drag the entitlement table to **Add as Entitlement Table** (or **Use as entitlement table**).
4. Map the fact `store_id` column to the entitlement `store_id` column.
5. Write the condition (see section 9).
6. **Preview as User**, then publish. Turn off visibility of the entitlement table on the **Tables** tab. Hidden tables still filter and cannot be used in a viz.

Certification of virtual connections needs Data Management. Certifying databases, tables and files needs Data Management and Catalog. On Server enable the Metadata API before Catalog.

Where shaping happens: warehouse views or dbt for logic many tools need. A scheduled Prep flow for logic only Tableau users need. Published source calculations for light definitions.

Never let a flow output land in an open project. Data policies filter what a flow reads, not what it writes. Put outputs in a locked project.

## 9. Row level security patterns

Pick one, in this order of preference when Data Management is available:

| Approach | Rule lives in | Weakness |
|---|---|---|
| Data policy on a virtual connection | The connection, once | Needs Data Management. Flow outputs escape it |
| User filter in a published data source | Each published source | Repeated per source. A new source without it leaks |
| Database security (views, native RLS) | The warehouse | Needs per-user database identity. Hard with extracts |
| One extract per audience from Prep | One output each | Copies multiply |

### Entitlement table (deep)

One row per user per store. Columns: `user_name`, `store_id`, `role`. Feed it from the HR or identity system, not a hand-kept sheet.

### Published data source pattern

1. Add the entitlement file as a second physical table. **Inner** join on `Store Id` = `Store Id`. Orders with no entitlement row (unknown store) drop out on purpose. Nobody is entitled to an unknown store.
2. Create `RLS Store Access`:

```sql
USERNAME() = [User Name]
```

If cases mix, compare lower case:

```sql
LOWER(USERNAME()) = LOWER([User Name])
```

3. **Data > source > Edit Data Source Filters > Add**, choose `RLS Store Access`, tick **True**. Desktop then shows nothing, which is correct. Fail closed.
4. Hide `User Name`, `Role` and `RLS Store Access`.
5. Extract and publish. The data source filter travels with it.
6. On the source **Permissions**: give groups **View** and **Connect**. Deny **Download Data Source** because a downloaded extract holds every row.

The inner join multiplies rows (59 orders become 413 with seven users per store). The filter returns each user to one row per order.

Expected check (sample): store manager ST-014 sees 13 rows and 32,714.75. A user not in the table sees 0 rows. Head office sees 59 of 60 rows because ST-099 has no entitlement. Decide now whether unknown stores belong to a head office entitlement or to a data quality report.

### Data policy conditions

```sql
USERNAME() = [user_name]
```

```sql
ISMEMBEROF("Harbour Finance")
OR [username] = USERNAME()
```

```sql
ISMEMBEROF('Managers') OR USERNAME() = [employee_name]
```

```sql
FULLNAME() = [EmployeeName]
```

```sql
[Region] = "North"
```

The group form lets a group see every row while everyone else sees their own.

### Function notes

- `USERNAME()` returns the signed-in Tableau user on the server. In Desktop it returns the local or network login.
- On Tableau Cloud the username is the email address. On Server it depends on the identity store. Confirm what `USERNAME()` returns matches what the entitlement table holds.
- `ISMEMBEROF("Group")` tests Tableau group membership. Use it for an override group.
- `USERATTRIBUTE()` returns values only when the attribute arrives in a JWT, SAML response or OIDC claim. It returns NULL in Desktop authoring and does not work through Tableau Bridge.
- Row explosion: for thousands of users prefer a sparse entitlement design (one row per user per region or group) or a data policy.

### Test

Sign in as real users. Preview as User in Desktop is a help, not proof. The author is usually in the override group, so tests as the author always pass.

## 10. Gotchas

- Join a fact to a target table at a different grain and totals multiply (12 times in the sample). Relate them.
- Dates typed as date at the Input step turn mixed-format values into nulls. Keep string, parse, retype.
- Clean values before duplicate checks. Leave Table Names out of the duplicate fields.
- An inner join drops unmatched rows silently. Left join and label as `Unmapped`.
- The Aggregate step deletes every field you did not group or aggregate. Branch first.
- Prep LOD is FIXED only, never nested, never combined with other arithmetic in one field.
- Prep calculations ignore dashboard filters. Ratios that must respond to filters go in Desktop.
- Append on a Hyper output run twice doubles the rows. Make loads idempotent with delete then insert by key.
- Hyper `CREATE_AND_REPLACE` wipes the target. Build to a temp file and swap.
- Hyper typing: loosen types to make an error go away and you hide dirty data. Clean upstream.
- A published `.hyper` cannot refresh itself. Republish with TSC in Overwrite mode.
- Incremental refresh misses edits and deletes. Add a weekly full refresh.
- Date-based incremental misses late-arriving rows. Use a sequence or load timestamp.
- Server cannot read your laptop path. Use a UNC share, Bridge or a database.
- Embedded passwords expire. Use a service account.
- Backgrounder queues, not slow jobs, cause stale 07:00 dashboards. Spread schedules first.
- Cloud cancels any extract refresh at two hours with no setting to change it.
- Multi-fact: calculations, sets and combined fields cannot cross base tables. Extracts need 2024.2.1 or later.
- Relationships cannot join two published data sources. Blend or model inside one source.
- A flat event table repeats batch level fields on every event row. SUM of `Volume_HL` overcounts. Use a FIXED LOD or filter by `Event_Type`.
- Workbook user filters protect nothing if the viewer can edit or download. Put RLS on the published source or a data policy.
- Data policies do not filter flow outputs. Lock the output project.
- Deny **Download Data Source** on any secured extract.
- Usernames drift. A rename makes a manager see nothing overnight.
- `USERATTRIBUTE()` is NULL in Desktop and through Bridge.
- Data Management changes the design. Check the licence before drawing the architecture.
