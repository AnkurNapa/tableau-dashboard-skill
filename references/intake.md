# Intake: ask before you build

Never start a dashboard or a migration from a one-line request. Run the matching question set first with the AskUserQuestion tool: at most four questions per call, two to four options each, the recommended option first. Skip any question the request or the files already answer. Say which answer you took from where. Write the answers to `brief.md` in the working folder, read it back to the person in five lines, then build.

## Set A: new Tableau dashboard

Round 1, purpose
1. Who opens it and how often? (Executive weekly, manager daily, analyst ad hoc, public audience)
2. What decision should it change? Ask for one sentence. Push back on "see everything".
3. Which three to five KPIs matter most? For each: numerator, denominator, grain, filters, target. One KPI, one definition.
4. What comparison makes a number good or bad? (Target, prior period, prior year, peer group)

Round 2, data
1. Where does the data live? (Snowflake, Databricks, another database, a published data source, files, an API). For Snowflake or Databricks also ask: auth method, warehouse or SQL warehouse name, live or extract. See `connectors.md`.
2. What is the grain of each table? How do the tables relate?
3. How fresh must it be? (Live, hourly, daily, weekly)
4. Who may see which rows? (Everyone, by region, by account, by user attribute)

Round 3, delivery
1. Where will it run? (Tableau Cloud, Tableau Server, Tableau Public, Desktop only, a Tableau Data App)
2. Which device and size? (Desktop 1200 by 800, laptop, phone layout too)
3. Which palette? (House, accessible Okabe Ito, Field Notes, beverage, the client brand: ask for hex values)
4. What do you want back? (Build kit with data plus shelf recipe, scripted .twb from a template, Data App, design review of an existing workbook)

Round 4, only when needed
- Accessibility level required, language, number formats (lakh and crore or millions), fiscal year start, existing workbooks to match, deadline.

Then: write the KPI table, the sheet list (one question per sheet, chart picked from `chart-types.md`) and the layout sketch into `brief.md` before any calculation.

## Set B: migrate Tableau to Power BI

Round 1, scope
1. How many workbooks, data sources and Prep flows? Is there an inventory, or should one be built with the Metadata API?
2. Why migrate? What must not get worse? (Licence cost, a Fabric strategy, one tool, performance)
3. Target platform? (Power BI Pro, Premium Per User, Fabric capacity: which SKU)
4. Deadline and whether both tools run side by side for a period.

Round 2, data
1. Live connections or extracts? Which sources?
2. Published data sources shared by many workbooks? These become shared semantic models first.
3. Prep flows or custom SQL to move? (Power Query, Dataflow Gen2, warehouse views)
4. Row level security in use? (User filters, entitlement tables, data policies, ISMEMBEROF)

Round 3, workbooks
1. Which calculations are hardest? Ask for a sample of LOD expressions, table calcs, parameters and sets.
2. Which interactivity matters? (Filter actions, parameter actions, set actions, dynamic zone visibility, viz in tooltip)
3. Pixel match or redesign? A redesign is cheaper and usually better.
4. Subscriptions, alerts, Pulse metrics or embedding to replace?

Round 4, people
- Who signs off each report, who builds, how users will be trained, how success is measured (usage, refresh time, numbers that reconcile).

Then: rank workbooks by usage and complexity, migrate a thin slice first (one shared model plus its most used report), reconcile every KPI to the Tableau number before moving on. Mapping and DAX patterns: `migrate-to-power-bi.md`.

## Rules

- Ask in rounds, not one long form. Stop asking once the brief is clear.
- Offer a default for every question so a busy person can accept and move on.
- Never invent a KPI definition. If nobody can define it, list it as an open question in `brief.md`.
- Log any question that would have prevented a mistake into `lessons.md`, then add it to this file.
