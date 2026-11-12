# Tableau Data Apps: build reference

Checked 13 Nov 2026. Beta product, so details change. Labels: official (Tableau or Salesforce page or repo), unofficial (third party), unconfirmed (no source or sources disagree).

## Sources

| Short name | URL | Status |
| --- | --- | --- |
| Dev docs landing | https://tableau.github.io/extensions-api/docs/dataapps/ | official |
| Dev docs, one-file text of all Data Apps pages (Get Started, Overview, Details, Manage, Security, Samples) | https://tableau.github.io/extensions-api/llms-dataapps.txt | official |
| Sample README | https://github.com/tableau/extensions-api/blob/main/Samples/DataApp/README.md | official |
| Tableau plugin and authoring skill | https://github.com/tableau/tableau-plugin/tree/main/src/plugin/skills/tableau-data-app-authoring | official |
| Tableau MCP repo (scaffold-data-app PR 930) | https://github.com/tableau/tableau-mcp/pull/930 | official |
| Salesforce blog, 3 Nov 2026 | https://www.salesforce.com/blog/tableau-data-apps-from-prompt-to-trusted-agentic-analytics/ | official |
| Tableau Next Data Apps Beta Guide (PDF, linked from the blog, not read) | https://resources.docs.salesforce.com/rel1/doc/en-us/static/pdf/Tableau_Next_Data_Apps_Beta_Guide_Draft_10-28.pdf | official, unread |
| Vizney explainer | https://www.vizney.com/what-is-tableau-data-apps/ | unofficial |
| Datastudios post | https://www.datastudios.org/post/tableau-data-apps-beta-claude-chatgpt-mcp-governed-analytics-apps | unofficial, seen only in a search summary |
| Tableau release pages (new-features, coming-soon) | https://www.tableau.com/products/new-features | official, blocked: WebFetch returned 403 and the gstack headless browser returned no Data Apps text |

Developer docs were found. The official docs say the beta is "available only on Tableau Cloud". The Salesforce blog also names Tableau Server and Tableau Next as targets. Treat Server and Next as unconfirmed for the beta.

## 1. What a Data App is

Official (docs overview, https://tableau.github.io/extensions-api/llms-dataapps.txt): a data app is a code-built interactive application. It is a Dashboard Extension or Viz Extension whose web resources (HTML, JavaScript, CSS, images) are packaged inside a workbook (.twbx) and hosted by Tableau. Code runs in the viewer's browser and queries Tableau at runtime. A workbook can hold more than one data app. Tableau hosts only the front end. It gives no runtime for server-side code.

| | Dashboard | Embedded viz (Embedding API) | Dashboard extension | Viz extension | Data App |
| --- | --- | --- | --- | --- | --- |
| Built with | Drag and drop in Tableau | Your own web page that embeds a Tableau view | Web app in a dashboard zone | Custom mark type on a worksheet Marks card | Code (usually AI agent written) bundled with the workbook |
| Where the code is hosted | None | Your own server | Your own server (or the site safe list) | Your own server, or packaged | Inside the workbook, served by Tableau |
| Data access | Native VizQL | Tableau view, inherits permissions | Extensions API on the dashboard | Marks card summary data | queryAsync(), readMetadata(), fetch() against connected sources |
| Interface | Tableau chart catalogue | Tableau view in your page | Custom, inside one zone | Custom chart in one worksheet | Custom, full app experience (tabs, controls, custom charts) |
| Needs a separate web server | No | Yes | Yes unless packaged | Yes unless packaged | No |
| Status | GA | GA | GA (Cloud, Server, Desktop 2018.2+) | GA (2024.1+) | Beta |

Sources for the table: data apps rows official (https://tableau.github.io/extensions-api/llms-dataapps.txt); extension version floors official (same file, Installation section); embedded viz row official (same file, "How is this different from the Tableau Embedding API?"). The "Marks card summary data" detail for viz extensions is from general Extensions API knowledge and is unconfirmed for this release.

Official: a packaged Dashboard Extension still appears on a dashboard and a packaged Viz Extension still appears on a worksheet. Bundling does not change where the interface shows.

## 2. Availability, versions, licences, settings

- Beta announced 3 Nov 2026. Official (Salesforce blog).
- Cloud only during the beta. Official (dev docs landing).
- Sample needs Tableau 2026.3.1 or later. Official (sample README).
- Extensions API minimum in the example manifest is 1.11. This is an API version, not a product version. Official (Data App Details).
- Beta on Tableau Cloud and Tableau Next. Official (blog). Server is named as a publish target for apps built in Tableau Studio. Unconfirmed: the dev docs say Cloud only.
- GA on Tableau Cloud and Server in Nov 2026 and Tableau Next in Dec 2026: from the task brief. Unconfirmed. One search summary of a Tableau release page said Beta Oct 2026 on Cloud and GA for Server in Nov 2026. I found no source for a Tableau Next GA date.
- Licence: no published licence rule beyond site roles. Unconfirmed whether a particular edition (Standard, Enterprise, Tableau+) is needed.
- Site admin: Settings, then Packages tab, then Settings view. Set "Allow Packages on this Site" (per site). Official (Manage Data Apps).
- Other site controls, all official (Manage Data Apps):
  - "Allow Packaged Extensions to trigger popups".
  - "Extension Package Allowed Origins": each origin must be HTTPS. A package declaring a source outside the list will not run.
  - "Tableau REST API Access": "Allow all REST API access (all paths and methods)" or an explicit list of HTTP method plus relative path. Placeholders `{api-version}` and `{site-id}` work in paths.
  - Packages view: table of packages with Enabled, Version, Author and a per-package Disable action.
- Roles to create: Creator or Explorer (can publish); Publish and Overwrite on the project; View, Connect and API Access on each data source; admin allowance for any REST paths used. Official (Overview).
- Roles to view: View, Full Data Query and API Access on the workbook; View, Connect and API Access on each published data source. Official (Overview).

## 3. Architecture

Official unless marked.

- Package layout (verbatim from Data App Details):

```text
Regional Sales/
├── Regional Sales.twb
└── Packages/
    └── com.example.regional-sales/
        ├── manifest.json
        ├── extensions/
        │   └── data-app.trex
        └── content/
            ├── index.html
            └── src/
                ├── app.js
                ├── styles.css
                └── tableau.extensions.1.latest.js
```

- The .twbx is a ZIP with the .twb and Packages/ at its root. Only files under `content/` are served at runtime (plugin build guide, official).
- Data path: app in the viewer's browser, then Extensions API `queryAsync()`, then Tableau. Vizney (unofficial) says the request goes to `/api/v1/vizql-data-service/query-datasource` on the same host. The sample README (official) says the sample queries through the Extensions API and VizQL Data Service. The plugin guide (official) says results come back as `{ data: [...] }`.
- Data sources: published data sources (live or extract) wired into the .twb as a `sqlproxy` connection, or a data file embedded in the workbook. The scaffold ships an empty `<datasources/>`, so wiring is a required step. Official (plugin skill).
- Semantic layer: the blog (official) says the semantic layer and Hyper engine resolve metric logic, aggregations and security before the agent queries. In Tableau Cloud and Server apps live inside workbooks and query published or embedded data sources. In Tableau Next apps live inside workspaces and use Tableau Semantics. The dev docs do not describe the Tableau Next path. Treat Tableau Semantics access for apps as unconfirmed.
- MCP: used at build time, not at runtime. Hosted Tableau MCP is `https://mcp.tableau.com` (Get Started, official). The blog names a Tableau MCP server and a Tableau Next MCP server.
- Auth: the app runs as the viewer. Manifest permissions (`full data`) do not grant extra Tableau permissions. Database credentials stay in Tableau (blog, official).
- Hosting: Tableau serves the packaged files. External services stay separate dependencies.

## 4. Developer workflow

Official (Get Started, https://tableau.github.io/extensions-api/llms-dataapps.txt, plus the plugin skill) unless marked.

1. Prepare. Need a Cloud site that supports the beta, Creator or Explorer (can publish), publish rights on the target project, a published data source and an AI client with MCP, the Tableau plugin and code execution.
2. Connect Tableau MCP. Add `https://mcp.tableau.com` in the client's connector settings, sign in, pick the site. Or run the Tableau MCP locally from github.com/tableau/tableau-mcp. Check with a prompt that asks the assistant to list the Sales fields and confirm the scaffold, upload and publish tools are callable.
3. Install the Tableau plugin (github.com/tableau/tableau-plugin). From source, per the docs:

```bash
git clone https://github.com/tableau/tableau-plugin.git
cd tableau-plugin
```

   Codex or ChatGPT desktop: `./reload-plugin.sh openai`. Claude desktop: `./reload-plugin.sh claude` builds `dist/claude-tableau.zip`; then Customize, Plugins, Add, Upload plugin, connect Tableau in the Connectors tab and enable code execution.
4. Describe the app. Tell the assistant to use the data app authoring skill. Give purpose, audience, data source, metrics, controls, style and destination.
5. The skill runs five stages: scaffold and finalize, wire the data source, author app.js, package, publish. Scaffold call (verbatim from the skill):

```text
scaffold-data-app({ datappName: "Sales Demo" })
```

   The result holds a template zip (`downloadUrl`, `s3URL` or `filePath`) plus a `postUnzip` plan applied with `scripts/apply_plan.py`. Download links expire in about 60 seconds. Packaging uses `scripts/package_twbx.py`. Publishing uses `request-workbook-upload` then `publish-workbook`. The skill requires an explicit yes before publishing.
6. Preview. There is no local preview and no validator. Tableau validates at publish time and the visual review happens in Tableau after publishing. The plugin guide says this (official). A third party skill, tableau-data-app-preview (github.com/laviDrori0702/tableau-data-app-preview, unofficial), mocks the Extensions API to preview in a Claude artifact before publishing.
7. Refine and republish in the same conversation. Republish with overwrite on the same workbook.
8. Share: Tableau content permissions on the workbook plus the data sources. Opening an app does not grant data source access. The blog says publish and share a secure link and that apps are searchable beside dashboards.

Agents and tools: the docs name an AI client with MCP and code execution. Blog names Claude, ChatGPT and Codex (also Claude Desktop). Claude Code is named in the sample README ("Codex or Claude Code"). Tableau Studio is a built-in authoring route (blog).

Versioning: package `manifest.json` has `version`. A new distributed version needs consistent updated metadata (Data App Details, official). Beyond republish with overwrite, no version history feature is documented. Unconfirmed.

## 5. SDK and API surface

Official (Data App Details and Overview). No separate Data Apps SDK or CLI exists. The surface is the Extensions API library `tableau.extensions.1.latest.js`, three new methods, the Tableau MCP tools and the plugin scripts.

| Item | Role |
| --- | --- |
| `initializeAsync()` | Opens the Tableau context. Call before other APIs. |
| `workbook.getAllDataSourcesAsync()` | Lists connected sources. |
| data source `queryAsync()` | Queries fields, aggregations, filters. |
| data source `readMetadata()` | Source metadata (the plugin guide spells it `readMetadataAsync()`). |
| `fetch()` | Curated Tableau REST API requests inside the site allow list and viewer permissions. |
| MCP tools | `scaffold-data-app`, `request-workbook-upload`, `publish-workbook`, plus data source lookup and metadata tools. |

Verbatim runtime example (content/src/app.js from Data App Details):

```javascript
async function render() {
  const output = document.getElementById('result');
  try {
    await tableau.extensions.initializeAsync();
    const sources = await tableau.extensions.workbook.getAllDataSourcesAsync();
    const source = sources.find((item) => item.name === 'Sales');
    if (!source) throw new Error('The Sales data source is not connected.');

    const result = await source.queryAsync({
      fields: [{ fieldCaption: 'Region' }],
    });
    output.textContent = JSON.stringify(result, null, 2);
  } catch (error) {
    output.textContent = 'Unable to load regions. Check the data connection and access.';
    console.error(error);
  }
}

render();
```

Verbatim package manifest:

```json
{
  "id": "com.example.regional-sales",
  "version": "1.0.0",
  "name": "Regional Sales",
  "author": "Example Company"
}
```

Verbatim entry page:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Regional Sales</title>
    <link rel="stylesheet" href="./src/styles.css" />
    <script src="./src/tableau.extensions.1.latest.js" defer></script>
    <script src="./src/app.js" defer></script>
  </head>
  <body>
    <main>
      <h1>Regional Sales</h1>
      <pre id="result" role="status">Connecting to Tableau…</pre>
    </main>
  </body>
</html>
```

The .trex manifest and the .twb fragments (extension instance, `referenced-extension`, `sqlproxy` data source) are in Data App Details at https://tableau.github.io/extensions-api/llms-dataapps.txt. Read them there when hand editing a workbook. The `.trex` uses `<worksheet-extension>`, `<min-api-version>1.11</min-api-version>` and `<permission>full data</permission>`.

## 6. Limits and governance

Official (Security and Manage pages) unless marked.

- Row level security and data permissions apply because the app runs as the viewer. Keep rules in the data layer. Hiding a field in the UI does not stop a query returning it.
- Allowed external origins: HTTPS only, set by the admin. Apps declare origins in `manifest.json` (`requestedOrigins`, per the scaffold result). Each must also be in the site's `allowedOrigins`. Official (plugin skill).
- REST API: apps declare the calls they need. Admin approves by path and method.
- Sandbox: the app runs in the viz extension sandbox (plugin guide, official). Rules from the scaffold: vendor libraries locally with no CDN, prefer 2D over WebGL, no `innerHTML` with live values, surface errors on screen. Vizney (unofficial) saw a sandboxed frame with no external origins in the Content Security Policy.
- Allowed libraries: no allow list is published. Anything bundled in `content/` is allowed by the rules above. Review all code and third party libraries, including AI generated code. No secrets in the package.
- Package files are not readable with `fetch()` at runtime and files outside `content/` return 404 (plugin guide, official).
- Page size and package size limits: not documented. Unconfirmed.
- Disable a package: Packages view, Actions, Disable.

## 7. Tableau Next and Tableau Studio

- Tableau Studio (official, blog): authoring surface that switches between AI prompting and drag and drop editing. Apps built in Studio publish to Tableau Cloud or Server (blog). No Studio developer docs found. Unconfirmed beyond the blog.
- Tableau Next (official, blog): apps live in workspaces, are built on Tableau Semantics and inherit Salesforce data access controls. Third party agents publish to Cloud, Server or Next. The Tableau Next beta guide PDF was linked but not read, so Next specifics (packaging, MCP tool names) are unconfirmed.
- The Tableau Next MCP server is a separate server from the Tableau MCP server (blog, official).

## 8. Known gaps in the beta

- Cloud only in the dev docs, while the blog lists Server and Next. Unconfirmed which is current.
- Admin set up is required before a build works: packages enabled, origins listed, REST paths listed. The Get Started page tells builders to ask the admin for these.
- No local preview or validator. Visual checks need a publish (official).
- A starter has no data source until wired (official).
- `scaffold-data-app` is behind the `tableau-data-apps` feature flag and needs Explorer (can publish) or higher (PR 930, official). It may be unavailable by site role, settings or version (plugin skill, official).
- Data source permissions are the first blocker in practice: Vizney (unofficial) reports a shared source without API Access blocked queries.
- Docs say "Tool availability depends on your Tableau environment and permissions" and "Supported capabilities depend on your site configuration" (official).
- Unconfirmed: licence edition, GA dates, version history, size limits, Tableau Next packaging, whether Server supports packages in 2026.3.

## 9. Dashboard-style data apps

For a data app that behaves like a dashboard (tabs, role based panels, guided views), see cookbook.md chapter 7 "Zone visibility and data apps" (dynamic zone visibility patterns at cookbook.md section 7.1 onward). Do not repeat it here. In a data app the same switching is done in app.js with ordinary DOM state, so no Dynamic Zone Visibility is needed.
