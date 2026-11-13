# Tableau skill lessons

Read this before every build. Add an entry the moment a mistake is found, whoever caught it. Newest at the top. When an entry repeats, mark it REPEAT and move its rule into "Top traps" in SKILL.md.

Format: date, task, what went wrong, how it was caught, rule.

## Log

- 2026-11-13, NIQ beer suite: a dashboard window without <viewpoints> made Desktop 2026.3 refuse the workbook ("element 'active' is not allowed for content model '((cards,viewpoint?,simple-id)|(viewpoints,active,device-preview,simple-id))'"). Caught by Ankur seeing the dialog. Rule: every dashboard window writes <viewpoints> (empty for a text only dashboard) before <active>.
- 2026-11-13, NIQ beer suite: a calc whose key equalled a raw column name was written twice in one datasource; Desktop warned "Ignoring calculated field, field is already defined by data source". Caught by Ankur on open. Rule: calc names and captions never equal a source column; check duplicates per datasource before opening.
- 2026-11-13, NIQ beer suite: opened a generated file before validating it, so an error dialog reached the user's screen. Rule: validate with the official XSD (github.com/tableau/tableau-document-schemas, strip the _.fcp feature flag prefixes first) plus a comparison with the sample workbooks in the Desktop bundle; then open one fixed file only.
- 2026-11-13, NIQ beer suite: screencapture of the Desktop window failed ("could not create image from window") because the terminal has no Screen Recording permission. Rule: check capture permission with a tiny region before planning Desktop screenshots.

- 2026-11-12, building this skill: python3 -I hid the user site packages, so pymupdf looked missing when reading a PDF. Caught by the import error. Rule: for --user packages, cd to a clean scratch folder and run python3 without -I.
- 2026-11-12, building this skill: tableau.com (blog, whitepapers, release pages) returns 403 to WebFetch and to the gstack headless browser. Caught on the first fetch. Rule: do not retry tableau.com by script; ask Ankur to save the page as PDF from his browser.
- 2026-11-12, building this skill: kb.tableau.com redirects to help.salesforce.com, which WebFetch cannot render. Caught by an empty script error page. Rule: read KB articles with the gstack browser. Search URL facet for articles only: `#q=<query>&f:@objecttype=[KBKnowledgeArticle]&f:@sflanguage=[en_US]`, go to about:blank first, then wait for network idle plus 3 s.
- 2026-11-12, building this skill: several help.tableau.com buildexamples_*.htm pages (area, bullet, waterfall, Pareto, dual axis) return 404. Caught by the chart agent. Rule: search help.tableau.com for the topic instead of guessing the page name.
- 2026-11-12, building this skill: the first twb-xml.md guessed zone coordinates, floating zone placement and the version marker. Caught by checking eight real Desktop saves. Rule: never write .twb XML from inference; copy the structure from a real saved file.
- 2026-11-12, building this skill: formulas in the cookbook (chapters 5 and 10) are screenshots, so the text extract misses them. Caught by the distiller. Rule: entries marked "typical form" or "derived" are not tested; test them in Tableau before a client sees them.
