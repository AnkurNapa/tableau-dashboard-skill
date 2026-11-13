# Vibe coding pitfalls: errors AI makes with Tableau

Searched on 13 Nov 2026: web search plus page reads of vendor help, practitioner blogs, Data School posts, GitHub issues and community threads. Reddit and Tableau Community threads mostly did not render or surface, so no thread is quoted. Where a rule rests on the existing skill or on Tableau behaviour I already trust, it is marked "inference". Nothing here was run in Desktop on 13 Nov.

Confidence labels: **multi** = seen in several sources, **one** = one source, **inference** = my reasoning from the sources or from the skill's own verified notes. Sources are listed as S1 to S24 at the end.

This file adds to `twb-xml.md` section 10, SKILL.md "Top traps" and `kb-articles.md`. It does not repeat them. Where an item overlaps, it says so in a few words.

## 1. twb XML that will not open or opens broken

**1.1 Plausible XML that Tableau rejects.** Symptom: the file looks fine in an editor but Desktop throws an error or refuses to load. Cause: free-form generation of attributes or elements that are not quite right. Fix: paste Tableau's exact error back then diff against a workbook saved by Desktop. Rule: never ship XML an LLM wrote without a test open in Desktop. Confidence: multi (S1 to S4). Source: S2 describes Claude adding invalid attributes that Desktop rejected until the error was fed back.

**1.2 XSD valid does not mean it opens.** Symptom: validator says clean, Tableau still fails. Cause: the schema skips connection attributes, calculation text, function names, object references and tab names (`processContents="skip"`). Fix: use XSD as a first gate only, then a real open. From Tableau Cloud June 2026 and Server 2026.2 the REST Validate Workbook endpoints do syntactic and semantic checks. Rule: three gates, XSD then REST validate then Desktop. Confidence: one authoritative source (S3) plus inference. Tableau support does not cover XML that validates but will not load.

**1.3 Version attributes out of step.** Symptom: workbook opens in newer Desktop only or XSD mismatch. Cause: `version` and `original-version` must match the XSD you validate against (26.1 maps to twb_2026.1.0.xsd). A manifest by version means older Desktop cannot load it. Fix: pick the oldest version you need and keep it consistent. Rule: pin the version once. Confidence: one (S3), consistent with `twb-xml.md` section 10 item 12.

**1.4 Missing `<extract>` block with a packaged Hyper file.** Symptom: Tableau Public refuses the twbx. Cause: Public only opens twbx files with a prebuilt extract and the XML lacked the extract element pointing at it. Fix: reuse a working extract and write the extract element. Rule: for Public, ship twbx plus extract. Confidence: one (S1).

**1.5 Stale twb inside the twbx.** Symptom: an old design loads instead of the new one. Cause: the archive held more than one twb and Tableau picked the stale one. Fix: one twb plus one Data folder. Rule: list the zip contents before handover. Confidence: one (S1).

**1.6 LLM cannot write a Hyper file.** Symptom: model claims to have produced a .hyper. Cause: the format is binary. Fix: build it with the Hyper API or reuse an existing one. Rule: if a tool call did not run the Hyper API, there is no extract. Confidence: one (S1) plus inference.

**1.7 Overloaded inputs.** Symptom: random errors after giving the model a twb, a twbx and the source Excel together. Cause: conflicting context. Fix: give one packaged file as the template. Confidence: one (S1).

**1.8 Extension blocks in the wrong place.** Symptom: "no declaration for worksheet-extension" and undeclared attributes. Cause: a `referenced-extension` block (a Sankey extension in the source) placed or kept where the schema forbids it. Fix: delete that block and reopen. Rule: strip extension metadata unless the extension is genuinely in use. Confidence: one (S5).

**1.9 Deeply nested dashboard layout containers.** Symptom: zones overlap, are misplaced or the file fails. Cause: the layout XML is nested and intricate and models lose track. Fix: generate layout from a simple declarative JSON and convert it by code. Rule: never let a model write zone coordinates by hand. Confidence: one (S6) plus the skill's own item 11 (inference of agreement).

**1.10 Dashboard keyboard order and renamed zones.** Symptom: tab order wrong, zone ids hard to find. Cause: zone ids follow creation order and `enable-sort-zone-taborder` is on. Fix: set it to false and renumber ids. Confidence: one (S7). Low priority.

**1.11 Generic output has no "scrap and rebuild" path.** Symptom: edit after edit makes the file worse. Cause: several changes between tests. Rule: change one thing per test and keep the last good file. Confidence: inference (matches `twb-xml.md` section 11).

**1.12 Uploading a twb to a hosted model leaks structure.** Symptom: none until it matters. Cause: field names, business logic and connection strings sit in the XML. Rule: strip connection strings and use sample data before sending. Confidence: one (S2).

## 2. Calculated field syntax mistakes

**2.1 Mixing aggregate and row-level values.** Symptom: "Cannot mix aggregate and non-aggregate arguments with this function". Cause: `IF [Category]="x" THEN SUM([Sales]) END`, a pattern that is natural in SQL or Excel. Fix: aggregate everything (use ATTR on the dimension) or make everything row-level or use a FIXED LOD. Rule: before pasting, mark each term row-level or aggregate. Confidence: multi (S8, S9).

**2.2 Missing commas, brackets or ELSE results.** Symptom: "Expected closing parentheses or comma" or "Syntax error". Cause: a truncated formula or ELSE with no value. Fix: complete the clause. Rule: count brackets and give every ELSE a value. Confidence: one (S8).

**2.3 String plus number.** Symptom: "Cannot add string and float values". Cause: a wrong field name or a missed STR. Fix: STR the number or fix the field. Rule: check each field's datatype in the data pane, not from the column name. Confidence: one (S8) plus inference.

**2.4 Functions from other languages.** Symptom: unknown function or parse error. Cause: Excel IFERROR, SUMIFS, VLOOKUP, SQL COALESCE or CASE WHEN ... THEN syntax without END, DAX CALCULATE or DIVIDE. Tableau has IFNULL, ZN, IIF, CASE with END and DIVIDE-free ratios. I did not find a published thread listing invented functions, so this is **inference**. Fix: check every function name against `functions.md`. Rule: grep generated formulas for any function not in the 207 listed.

**2.5 Brackets reference captions that do not exist.** Symptom: a field "not found" or a calculation that refers to a renamed field. Cause: the model guesses captions such as `[Customer]` for Superstore's `[Customer ID]` or `[Customer Name]`. Fix: list real field names from metadata first. Rule: feed the model the column list, never let it guess. Confidence: one (S10) plus inference. Tableau Agent docs say near-duplicate and vague field names make it pick the wrong field (S11).

**2.6 Wrong date function arguments.** Symptom: date parts compared to date values or `DATEDIFF` with the wrong unit string. Cause: models mix SQL `DATEDIFF(a,b)` order with Tableau's `DATEDIFF('day',a,b)`. Confidence: inference. Rule: unit string first, quoted. Pair this with Top traps item 9.

**2.7 Dates stored as text.** Symptom: sorts alphabetically, date functions return NULL. Cause: CSV dates in a non ISO format or a field typed as string. Fix: DATEPARSE with an explicit pattern or ISO in the source. Confidence: one (S11, which lists dates as text as a cause of flawed analysis) plus `twb-xml.md` item 9.

**2.8 NULL silently propagating.** Symptom: blanks in a ratio. Cause: model omits ZN or IFNULL or adds ZN where NULL is the true answer and so hides missing data. Rule: use ZN on purpose and say why. Confidence: inference (Top traps item 6).

**2.9 Vague requests produce wrong calculations.** Symptom: a plausible formula for the wrong metric. Cause: Tableau's own guidance says vague calculation requests can produce an incorrect one. Rule: give numerator, denominator, grain and filters in the prompt. Confidence: one authoritative (S11).

**2.10 First answer wrong, apology when challenged.** Symptom: the model asserts a formula is an error or a behaviour, then reverses. Cause: confident but inconsistent answers across turns. Fix: test in Desktop, not by arguing. Rule: a formula is right when its number reconciles, not when the model agrees. Confidence: one (S10), with several reversals in one article.

## 3. LOD and table calc mistakes

**3.1 Misreading what a FIXED level means.** Symptom: "average sales per customer" that is actually per category. Cause: the model describes the dimension list wrongly. Fix: say aloud what the dimension list is. Confidence: one (S10).

**3.2 Dropping FIXED to "make it row level".** Symptom: `{MIN([Order Date])}` or a bare MIN returns a different thing. Cause: a bare aggregate follows the view and braces with no dimension are not row level. The no-keyword form `{[Customer ID] : MIN(...)}` is valid and acts like FIXED. Rule: keep the keyword. Confidence: one (S10).

**3.3 FIXED ignores dimension filters.** Symptom: a share or total ignores a filter. Cause: FIXED runs before dimension filters. Fix: context filter or INCLUDE or EXCLUDE. Confidence: multi (S12, S13 and the skill). Already Top trap 1.

**3.4 Top N against context.** Symptom: fewer rows than expected or a Top N that ranks the whole set. Cause: Top and Bottom filters run before ordinary dimension filters. The MCP query tool even returns a MISSING_CONTEXT_ON_DIMENSION_FILTER warning for it. Fix: `context: true` on the filter to rank within the subset. Confidence: one authoritative (S14).

**3.5 Granularity: SUM of a line-item measure.** Symptom: a regional revenue of 2.3 million against 1.8 million in Finance. Cause: order totals repeated per line item. Fix: FIXED at order level then roll up, plus a hidden reconciliation sheet. Rule: variance above 1 per cent blocks publishing. Confidence: one (S15) plus the skill's trap 3.

**3.6 Distinct counts do not add up.** Symptom: grand total or subtotal of COUNTD differs from the sum of parts. Cause: COUNTD is not additive across groups. Fix: a FIXED COUNTD at the right level, then a window sum and validate. Confidence: multi (S16, S17).

**3.7 Table calc addressing.** Symptom: running totals or percent of total jump when a dimension is added. Cause: default "compute using" changes with the view. Fix: Specific Dimensions. Confidence: multi (S18, the skill). Top trap 5.

**3.8 Quartile and rank by an AI formula "90 per cent right".** Symptom: one item under the wrong bucket. Cause: sort or addressing, not syntax. Confidence: one weak source (S19), mostly inference.

**3.9 Totals with a table calc or EXCLUDE.** Symptom: asterisk or odd grand total. Top trap 8. No new source.

## 4. Data model mistakes

**4.1 Joining facts of different grain.** Symptom: totals multiply. Cause: the model reaches for JOIN as in SQL. Fix: relationships. Confidence: multi (S15, S20 and the skill).

**4.2 Blended data that Tableau Agent cannot see.** Symptom: answers miss the secondary source. Cause: the agent works only with the primary data source. Fix: bring both into one published source with relationships. Confidence: one authoritative (S11).

**4.3 Leading zeros lost on string keys.** Symptom: "01003" becomes "1003" and joins or maps fail. Cause: the CSV was saved from Excel or typed as a number by inference. Fix: declare the column string in the relation and keep the CSV as text. Rule: set every ID column to string by hand. Confidence: multi (S21), the loss often occurs before Tableau sees the file.

**4.4 Wrong role or default aggregation.** Symptom: ZIP codes as measures, unit prices summed. Cause: field properties. Fix: set role and default aggregation in the source. Confidence: one authoritative (S11).

**4.5 Hidden and duplicate fields.** Symptom: the wrong near-duplicate field used. Fix: hide unneeded fields and give descriptions. Confidence: one authoritative (S11).

**4.6 Relation columns and types do not match the CSV.** Overlaps `twb-xml.md` section 10 items 7 and 9. No new source.

## 5. Dashboard layout and actions

**5.1 Zone coordinates written by a model.** See 1.9. Confidence: one plus inference.

**5.2 Actions naming a sheet that is off by one character.** `twb-xml.md` item 11. Inference only; no new report.

**5.3 Over-generated charts.** Symptom: more fields and helper Boolean calculations than asked for. Cause: the model adds extras. Rule: diff the calculation list against the request. Confidence: one (S2).

**5.4 Tableau Agent does not build dashboards.** The FAQ says it does not build dashboards or model data (S22). Rule: do not promise a dashboard from Agent. Confidence: one authoritative.

## 6. Performance

**6.1 COUNTD and row-level LODs on large data.** Symptom: slow dashboards. Cause: heavy distinct counts, nested LODs. Confidence: inference. I found no source with numbers. Rule: record performance before handover (skill step 6).

**6.2 Result caps in the query tools.** The MCP query tool has a limit argument and optional server caps, flagged by a truncation field. A truncated result presented as a total is wrong. Confidence: one authoritative (S14). Rule: read the truncation flag every time.

## 7. REST, TSC, MCP and Hyper API code

**7.1 400011 when publishing a workbook whose data source "is not found".** Symptom: "Datasource not found for workbook" although it exists on the site. Cause: the XML still pointed to the old server and site through `repository-location` and the `connection` attributes. Deleting them was not enough. Fix: set them to the target server and site values. Maintainers said hand-edited XML is not generally supported and the issue was closed in Jan 2026. Confidence: one thread (S23), several reporters in it.

**7.2 400011 on large extracts or on a workbook referencing a .tds.** Fix: publish the data source first or publish a twbx. Confidence: one (S24) summarised via a search snippet, so treat as unverified.

**7.3 401002 after a long run.** Cause: the sign-in token expired during a long script. Fix: sign in again just before the publish call. Confidence: one search summary of the REST docs, plus inference.

**7.4 TSC is not a repair tool.** Rule: validate the workbook with the REST validate endpoints before publish (S3).

**7.5 Document API limits.** The library cannot add extracts to workbooks or data sources and does not update field information. A script that promises either is wrong. Confidence: one (library documentation mirror, S25).

**7.6 MCP prerequisites.** Published data sources only, VizQL Data Service on, the API Access permission on the data source, the Metadata API on. Missing any gives empty data source lists or errors. Embedded data sources need Tableau 2026.3 and an admin switch. Confidence: one authoritative (S14, S26).

**7.7 VDS cannot do everything.** No spatial, R or Python, pass-through, fiscal date calculations or COUNT(table). No calculations that use sets, combined fields or reference a group. No cube sources. One filter per field. No hour or minute date aggregations. A query cap of 100 per hour per Creator licence. Rule: do not ask an agent for these through MCP. Confidence: one authoritative (S27).

**7.8 Agents guess filter values.** An agent searched for "EU" when the data held "European Union (EU)" and filled gaps with plausible guesses. The MCP tool validates string filter values by default, so do not turn that off. Confidence: one (S28) plus one authoritative (S14).

**7.9 Field captions versus underlying names.** On Tableau 2025.3 and later set `interpretFieldCaptionsAsFieldNames` when captions repeat across logical tables. On older versions the option is rejected even when validation is off. Confidence: one authoritative (S14).

**7.10 Hyper API and NaN or NULL dates.** Symptom: ValueError "invalid value nan" or export that hangs. Cause: pandas NaN or NULL in a date or timestamp column. Fix: fill a dummy value or convert to string and pass `datetime.date`, not numpy datetime64. Pin pantab to 3.x in production as 4.0 changed its API. Confidence: multi (S29, S30).

**7.11 Flow files are zip plus JSON.** A .tfl is an archive containing JSON. A model that writes JSON must repack it. Confidence: one (S31). One test found a model's conversion of a 750,000 row flow wrong on about 155,000 rows at first pass, 8 rows at second and exact at third (S32). Rule: reconcile the row counts and values against Prep's own output.

**7.12 Wrong results caused by source errors the AI cannot see.** Same article: the source data itself had errors. Rule: profile the data before blaming the flow. Confidence: one (S32).

## 8. Hallucinated features and menu paths

**8.1 Features that do not exist in a given edition.** No source found. Inference: models describe Desktop menu paths for web authoring and the reverse and name Tableau Next or Pulse features as if all editions had them. Rule: confirm every menu path against `help.tableau.com` for the user's version.

**8.2 Vendor error rates.** A Salesforce engineering interview put an early intent classifier error at about 20 per cent (S33). Vendor reported. Rule: the Agent is a draft writer, not a checker.

**8.3 Agent business preferences are not a calculation engine.** Multi-step or raw maths inside preferences is misapplied and the file is capped at 50 preferences and about 8,000 characters (S11).

## Top 15 checklist before handing over an AI-written workbook

1. Open it in Desktop. XSD valid and REST valid are not enough (S3).
2. Every function name is in `functions.md`; none from Excel, SQL or DAX.
3. Every field in brackets exists in the metadata list, spelled exactly.
4. No formula mixes an aggregate with a row-level field without ATTR or an LOD.
5. Every ID and code column is string, leading zeros intact.
6. Date columns are real dates (ISO or DATEPARSE); date parts are not compared with date values.
7. Ratios are SUM over SUM; a weighted average is SUM(value*weight) over SUM(weight).
8. Every FIXED LOD has its filters in context or the share is checked with the filter on.
9. A FIXED field summed at a finer grain is wrapped in MIN or MAX.
10. COUNTD is never summed across groups; grand totals reconcile to a one line query.
11. Facts of different grain are related, never joined.
12. Table calcs use Specific Dimensions and the view was tested with a dimension added and removed.
13. Totals reconcile to the source within 1 per cent, with a hidden check sheet.
14. Layout comes from a script or Desktop, not hand written coordinates; one twb in the twbx; version attributes consistent.
15. Anything run through REST, TSC, MCP or Hyper API shows its real response: token fresh, data source references on the target site, no truncated results, no NaN in dates.

## Rules for scripting a twb from CSVs with LOD expressions for distinct weighted buyers

This section is inference built on the sources above and `twb-xml.md`. It has not been run.

- Declare the buyer ID as string in the relation. A buyer key that loses leading zeros will split one buyer into two or merge two (S21).
- Distinct buyers is COUNTD at a stated grain. Write `{FIXED [Region] : COUNTD([Buyer ID])}` and say which level it is. Never SUM a COUNTD across regions to get a company total (S16, S17).
- Weighted metrics are SUM(x*w) over SUM(w) computed at the view. If an LOD supplies the weight, wrap it in MIN or MAX when the view is finer than the LOD (S15 and Top trap 3).
- Add the filters that should change the buyer count to context or the FIXED COUNTD ignores them (S12, S13).
- If one buyer buys in several rows or tables, relate the tables on buyer ID and keep one grain per table (S15).
- A Hyper extract made from the CSVs is built by the Hyper API with `datetime.date` and no NaN in date columns (S29, S30). A twb that points at CSVs needs the columns and types to match the header exactly.
- Reconcile the buyer count with `SELECT COUNT(DISTINCT buyer_id)` on the same CSVs before handing over.
- Projected buyers is not a weighted average. It is the sum of each distinct buyer's weight: `SUM({FIXED [Buyer ID] : MIN([Weight])})` over the buyers in the view. Or use SUM of the weight field on a household table related to the purchase table, so each household counts once. Lead's note (13 Nov 2026), not yet run in Desktop.
- Penetration needs a base that product filters cannot touch: total weight of all households in the geography, from the household table or an EXCLUDE or FIXED on geography only. Check it with a brand filter on: the base must not move.

## Sources

- S1 https://ddd.bearblog.dev/llm-gen-tableau/
- S2 https://sqlsekou.substack.com/p/hacking-tableau-workbooks-with-ai
- S3 https://github.com/tableau/tableau-document-schemas
- S4 https://dev.to/twilize4332/the-ai-agent-that-builds-tableau-dashboards-for-you-meet-twilize-5gnf
- S5 https://thedataschool.co.uk/sean-fei/fixing-corrupted-tableau-workbooks-error-codes-in-xml/
- S6 https://datacooper.pages.dev/blog/maybe-say-goodbye-to-endless-dragging-and-dropping-or-a-new-way
- S7 https://thedataschool.co.uk/holly-andersen/fixing-tableau-dashboard-tab-order-with-xml/
- S8 https://www.thedataschool.co.uk/a/clare-fox/why-doesnt-that-work-four-common-calculated-field-errors-in-tableau/
- S9 https://www.theinformationlab.co.uk/community/blog/fixing-tableau-errors-cannot-mix-aggregate-and-non-aggregate-arguments
- S10 https://interworks.com/blog/2023/06/26/ten-questions-for-chatgpt-about-tableau-and-level-of-detail-expressions/
- S11 https://help.tableau.com/current/online/en-us/web_author_einstein_best_practice.htm
- S12 https://trailhead.salesforce.com/trailblazer-community/feed/0D5KX00000jASz30AG
- S13 https://interworks.com/?p=24447
- S14 https://tableau.github.io/tableau-mcp/docs/tools/data-qna/query-datasource
- S15 https://codewithbehnam.github.io/blog/2025/when-tableau-lied-to-me/
- S16 https://www.thedataschool.co.uk/salome-grasland/untitled-183
- S17 https://www.thebricks.com/resources/guide-how-to-avoid-double-counting-in-tableau
- S18 https://www.thedataschool.co.uk/benjamin-wortmann/how-lods-works
- S19 https://trailhead.salesforce.com/trailblazer-community/feed/0D5KX00000pNtAu0AK
- S20 https://www.thebricks.com/resources/guide-why-is-tableau-doubling-my-numbers
- S21 https://www.thebricks.com/resources/guide-how-to-truncate-a-zip-code-in-tableau
- S22 https://help.tableau.com/v0.0/online/en-us/web_author_einstein_faq.htm
- S23 https://github.com/tableau/server-client-python/issues/1621
- S24 https://lightrun.com/answers/tableau-server-client-python-400011-bad-request-when-publishing-hyper-datasource
- S25 https://docsearch.algolia.com/mcp/docs/repo/tableau/document-api-python
- S26 https://tableau.github.io/tableau-mcp/docs/getting-started
- S27 https://help.tableau.com/current/api/vizql-data-service/en-us/docs/vds_limitations.html
- S28 https://thedataschool.co.uk/charles-yi/creating-an-ai-wrapper-around-vizql-data-service-vds/
- S29 https://community.dataiku.com/discussion/comment/38049/
- S30 https://pantab.readthedocs.io/en/stable/changelog.html
- S31 https://datablog.pages.dev/posts/tfl-json
- S32 https://howtospeakdata.substack.com/p/convert-tableau-prep-files-to-python
- S33 https://engineering.salesforce.com/einstein-copilot-for-tableau-building-the-next-generation-of-ai-driven-analytics/
