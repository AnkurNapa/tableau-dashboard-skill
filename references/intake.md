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

## Office hours: the blunt round (Gary Tan style)

Run this before Set A when the request is vague ("a sales dashboard", "show everything"), when someone wants a dashboard reviewed or when a live dashboard has low use. Warm to the person, brutal to the dashboard. The job is to find the one thing that will make it go unused and say it plainly. Evidence beats opinion and usage beats both: push every claim down to who opens it, when and what they did next.

Ask in order. Do not move on until the answer is specific. "Sales leadership" is not an answer. "Priya, the South region head, every Monday at 9 before the pipeline call" is an answer.

1. **Who opens it on Monday morning?** One named person and the meeting it feeds. A dashboard for everyone is a dashboard for nobody.
2. **What do they use today instead?** An Excel export, a PowerPoint slide, a WhatsApp number from an analyst. That is the real competitor. If the current answer works, ask why replace it.
3. **What will they do differently after looking?** One decision, in one sentence. If nobody can name it, the dashboard is a report and a scheduled email may beat it.
4. **Which number would make them pick up the phone?** One KPI with numerator, denominator, grain and threshold. If two teams define it differently, settle that first: a dashboard cannot fix a definition fight.
5. **Can you prove the number is right?** Name the source of truth it must match (finance close, the ERP, a Nielsen or NIQ read) and the tolerance. No reconciliation, no launch.
6. **What is the smallest version that gets used this week?** One sheet, one KPI against its comparison, shared as an image or a Tableau Public link. Not eight pages next quarter.
7. **What are you avoiding?** Usually dirty data, an undefined KPI, row level security nobody has specified or a stakeholder who has not agreed to use it.

### Tableau and analytics pressure points

Check these every time:

- **Building before anyone asked.** Twelve sheets and a slick layout for a question nobody owns. Ask who requested it and what they said when they saw the first version.
- **Ratios that do not add up.** A share, %ACV, penetration or margin averaged across rows instead of a ratio of sums. Ask how the total row is computed before anything else.
- **Filters that lie.** A context filter, an LOD or a table calc that ignores the slicer the reader thinks is applied. Ask what happens to each KPI when the region filter changes.
- **Extract freshness nobody checks.** A daily extract that failed on Tuesday still looks fine on Friday. Ask where the refresh time is shown on the page.
- **Panel and sample data read as census.** Small cells, unweighted buyers, a launch brand under-read by the panel. Ask for the minimum sample shown and how coverage is checked.
- **Pretty before true.** A colour palette and custom shapes before one number reconciles. Grade the demand and the accuracy, not the artefact.
- **Usage nobody measures.** On Server or Cloud the admin views show views per user. If nobody opened it in 30 days, kill it or narrow it.

### Output shape

Produce these parts, in this order, then go to Set A with what survived:

1. **Verdict** in one line: build, narrow or kill, plus the single reason.
2. **The real problem**, one paragraph, naming what is being avoided.
3. **KPI audit**: a table of each KPI against its definition, its source of truth and whether it reconciles (yes, no or nobody knows).
4. **This week**: three actions at most, each done in a day, each producing evidence (a named user saw it and acted, a number matched finance) rather than more sheets.
5. **The number to watch**: weekly views by the named user or the decision it changed. Say which value would mean it is working.

Skip flattery and skip repeating the request back. If the brief is solid, say so in one line and spend the rest on the weakest link. Write the verdict and the KPI audit into `brief.md`.
