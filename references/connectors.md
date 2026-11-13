# Connectors: Snowflake and Databricks

Checked 13 Nov 2026. Covers Tableau first, then the Power BI equivalent for Tableau to Power BI migrations.

Labels: each item is tagged `official` with the source URL, or `derived` (inference or house practice, verify before quoting to a client). Vendor pages change often, so re-check any version number or date before it goes into a client document.

## Sources

Tableau
- https://help.tableau.com/current/pro/desktop/en-us/examples_snowflake.htm
- https://help.tableau.com/current/pro/desktop/en-us/examples_databricks.htm
- https://help.tableau.com/current/online/en-us/to_sync_local_data.htm (Tableau Bridge)
- https://help.tableau.com/current/online/en-us/dm_vconn_overview.htm (virtual connections)
- https://help.tableau.com/current/pro/desktop/en-us/connect_basic_initialsql.htm
- https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_how_to_query_tagging.htm
- https://help.tableau.com/current/online/en-us/snowflake_oauth_idp.htm
- https://help.tableau.com/current/pro/desktop/en-us/publish_tableau_online_ip_authorization.htm
- https://help.tableau.com/current/server/en-us/rls_datasource.htm
- https://help.tableau.com/current/pro/desktop/en-us/publishing_sharing_authentication.htm

Snowflake
- https://docs.snowflake.com/en/user-guide/oauth-partner
- https://docs.snowflake.com/en/user-guide/key-pair-auth
- https://docs.snowflake.com/en/user-guide/partner-authentication-support
- https://docs.snowflake.com/en/user-guide/warehouses-considerations
- https://docs.snowflake.com/en/user-guide/querying-persisted-results
- https://docs.snowflake.com/en/user-guide/cost-attributing
- https://docs.snowflake.com/en/user-guide/security-row-intro
- https://docs.snowflake.com/en/user-guide/oauth-powerbi

Databricks
- https://docs.databricks.com/aws/en/partners/bi/tableau
- https://docs.databricks.com/aws/en/dev-tools/auth/
- https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m
- https://docs.databricks.com/aws/en/compute/sql-warehouse/
- https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior
- https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/

Microsoft
- https://learn.microsoft.com/en-us/power-query/connectors/snowflake
- https://learn.microsoft.com/en-us/power-query/connectors/databricks-azure
- https://learn.microsoft.com/en-us/power-query/connectors/databricks
- https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about
- https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem
- https://learn.microsoft.com/en-us/azure/databricks/partners/bi/power-bi

Fetch failures: help.tableau.com connect_basic.htm and connect_customsql.htm returned 404. docs.snowflake.com oauth-tableau and query-tags returned 404 (the cost-attributing page was used for query tags instead). The Databricks pages for personal access tokens, Partner Connect and the ODBC driver version table were not read in full, so those points are marked `derived`. The Tableau Cloud IP table itself was not read. No tableau.com blog pages were used.

Placeholders used throughout: `<account>.snowflakecomputing.com`, `adb-<workspace-id>.<n>.azuredatabricks.net`, `/sql/1.0/warehouses/<warehouse-id>`, `<catalog>`, `<schema>`, `<role>`, `<warehouse>`. Never paste real hosts, tokens, secrets or account names into the skill output or a client document.

## Questions to ask before connecting

1. Which platform and cloud (Snowflake on AWS, Azure or GCP; Databricks on AWS or Azure)? `derived`
2. Where will the dashboard live (Tableau Cloud, Tableau Server, Power BI service) and is the warehouse reachable from there, or behind private networking? `derived`
3. Who may see which rows: one audience, or per user or per role? Is row security already defined in the warehouse? `derived`
4. Which identity should the connection use: each viewer, a service account or a service principal? Who owns rotation of its secret or key? `derived`
5. Is single-factor password sign-in still allowed on the account? (Snowflake retired it in 2025. Databricks basic auth ended in July 2024.) `official` https://help.tableau.com/current/pro/desktop/en-us/examples_snowflake.htm and https://help.tableau.com/current/pro/desktop/en-us/examples_databricks.htm
6. Which warehouse or SQL warehouse is the dashboard allowed to use, what size and who pays for it (cost centre or tag)? `derived`
7. How fresh must the data be: live, hourly, daily? What is the largest table the dashboard touches? Is there an aggregate table? `derived`
8. Are there IP allowlists or network policies on the account? Who can add the Tableau Cloud or Power BI service ranges? `official` https://help.tableau.com/current/pro/desktop/en-us/publish_tableau_online_ip_authorization.htm
9. Which role, catalog and schema should the dashboard default to? `derived`
10. For Databricks: is the data in Unity Catalog (not the legacy Hive metastore)? Which SQL warehouse type (serverless, pro or classic)? `official` https://docs.databricks.com/aws/en/partners/bi/tableau
11. Which Tableau or Power BI version and driver version are installed on the desktop and on any Bridge or gateway host? `derived`
12. Is Data Management (virtual connections) or a Premium or Fabric capacity licensed? `official` https://help.tableau.com/current/online/en-us/dm_vconn_overview.htm

---

# Part 1: Tableau

## 1.1 Snowflake in Tableau

### Driver and versions

- Tableau needs the Snowflake ODBC driver. If it is missing the connection dialog links to the download page. `official` https://help.tableau.com/current/pro/desktop/en-us/examples_snowflake.htm
- Key pair authentication needs Snowflake ODBC driver 3.4.0 or newer. Key pair support is in Desktop, Prep and Cloud from 2024.3 and in Tableau Server from 2025.1. Create keys with OpenSSL 3.x or newer. `official` same page
- On a Mac use a fully qualified server name. `official` same page

### Connection fields

| Field | Notes | Label |
|---|---|---|
| Server | `<account>.snowflakecomputing.com` | official (examples_snowflake.htm) |
| Role | Optional. Set it explicitly so published content does not depend on a user's default. | official for the field, derived for the advice |
| Warehouse | Optional. Blank means the user's default warehouse. Published content uses each viewer's default. Always set it for shared dashboards. | official for behaviour, derived for the advice |
| Database, Schema, Table | Chosen on the data source page after connecting. | official |
| Initial SQL | Runs at the start of every connection. | official |
| Advanced tab | Custom driver parameters and Default VARCHAR size. Not available on Tableau Cloud. | official |

### Authentication options

| Option | Use when | Setup | Label |
|---|---|---|---|
| Snowflake OAuth (Sign In) | Named users, interactive Desktop and Cloud use. Best default for viewers who each hold a Snowflake login. | Admin creates a security integration with `OAUTH_CLIENT = TABLEAU_DESKTOP` or `TABLEAU_SERVER` (Tableau Cloud). The user clicks Sign In. | official https://docs.snowflake.com/en/user-guide/oauth-partner |
| External OAuth (Entra ID or Okta) | The company already federates identity and wants IdP controlled tokens. | Create OAuth clients on the IdP for Desktop and for Cloud or Server, build a config file with IDs prefixed `custom_` (36 characters maximum), install it in each OAuthConfigs folder or in Cloud site settings. | official https://help.tableau.com/current/online/en-us/snowflake_oauth_idp.htm |
| OAuth Client Credentials | Machine-to-machine. Added in Tableau 2026.2. Client ID goes in Username and secret in Password. Usually needs the token request URL and scope. | Configure on the IdP, then enter in the dialog. | official examples_snowflake.htm |
| Key pair | Service accounts and unattended refresh. | Generate keys, run `ALTER USER ... ADD KEY PAIR` (named key pair, supports rotation and expiry), browse to the `.p8` file in Tableau. | official https://docs.snowflake.com/en/user-guide/key-pair-auth |
| Programmatic access token (PAT) | Service users on Tableau Cloud where key pair is awkward. Token goes in the Password field. | Snowflake admin issues the token. The client IP must be allowed or error 390422 appears. | official examples_snowflake.htm and https://docs.snowflake.com/en/user-guide/partner-authentication-support |
| Okta username and password | Legacy SAML IdP setups. | Enter the Okta URL as SAML IdP. | official examples_snowflake.htm |
| Username and password | Avoid. Single-factor password sign-in was retired in May 2025. | Check Tableau's knowledge base article before using. | official examples_snowflake.htm |

Facts to remember:
- Snowflake OAuth access tokens last 600 seconds by default. Refresh tokens default to 10 hours for Desktop and 90 days for Cloud. `official` https://docs.snowflake.com/en/user-guide/oauth-partner
- ACCOUNTADMIN, SECURITYADMIN, ORGADMIN and GLOBALORGADMIN are blocked from OAuth by default. Do not build dashboards that need them. `official` same page
- Key pair workbooks and data sources cannot be published or edited in web authoring. Author in Desktop and save credentials on Cloud or Server before publishing. `official` examples_snowflake.htm
- Tableau Cloud 2024.2 or later over private connectivity needs a custom security integration (`OAUTH_CLIENT = CUSTOM`). `official` oauth-partner page
- Support matrix for person and service users (External OAuth, Snowflake OAuth, key pair, PAT) is in https://docs.snowflake.com/en/user-guide/partner-authentication-support. `official`

Key pair setup, verbatim pattern (placeholders only):

```sql
ALTER USER <service_user> ADD KEY PAIR <key_name> RSA_PUBLIC_KEY = '<public key without PEM delimiters>';
```

### Live versus extract

- Live: always current, uses warehouse credits on every interaction, depends on warehouse size and caching. Good for governed, small to medium aggregated tables and when row security must stay in Snowflake. `derived`
- Extract: Tableau stores a Hyper copy and refreshes on a schedule. Fast and cheap per view, but data ages and the extract refresh itself needs credentials and a warehouse. Good for large detail tables behind simple dashboards. `derived`
- Initial SQL also runs when an extract refreshes. `official` https://help.tableau.com/current/pro/desktop/en-us/connect_basic_initialsql.htm
- Default rule of thumb: extract an aggregated view for executive dashboards, go live when freshness or in-warehouse security is a requirement. `derived`

### Performance

- Warehouse sizing: match size to workload. Bigger is not always faster for simple queries. Billing is per second after a 60-second minimum. Use a multi-cluster warehouse (Enterprise edition) for many concurrent viewers rather than resizing. `official` https://docs.snowflake.com/en/user-guide/warehouses-considerations
- Auto suspend: around 5 to 10 minutes or less limits idle credits, but suspension drops the warehouse cache and the first queries after resume are slower. Set auto suspend longer than the normal gap between dashboard interactions. `official` same page
- Result cache: results are reused for 24 hours when query text matches exactly and underlying data is unchanged. `USE_CACHED_RESULT` is on by default. Functions such as `RANDOM` and `UUID_STRING` defeat it. `official` https://docs.snowflake.com/en/user-guide/querying-persisted-results
- Because Tableau generates the query text, identical filters from different users share cache only if the generated SQL matches. User-specific initial SQL breaks connection sharing (see Security). `derived`
- Aggregate tables: build a pre-aggregated table or view at dashboard grain and point Tableau at it. `derived`
- Custom SQL versus tables: prefer tables or views. Custom SQL is wrapped as a subquery for every query, which can block pushdown. If Tableau reports "This Field XXX Does Not Exist" after editing custom SQL, use Replace Field References. `official` for the error fix (examples_snowflake.htm), `derived` for the preference
- Unbounded VARCHAR columns make Tableau use a small fetch size and hurt speed. Set a column limit or the Default VARCHAR size on the Advanced tab. `official` examples_snowflake.htm
- Row limits: there is no fixed Tableau row cap, but each mark pulls rows from the warehouse. Aggregate before drawing. `derived`

### Cost tracking: initial SQL and query tags

- Tableau tags Snowflake sessions by default. The origin data (workbook, view and data source LUIDs, site LUID and, on Server, the user) sits in the session query tag, not in the SQL text. Tableau Cloud supports tagging only for Hyper, Snowflake and Teradata connections. `official` https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_how_to_query_tagging.htm
- A session query tag feeds `QUERY_ATTRIBUTION_HISTORY` (365 days of history, warehouse compute only, idle time excluded). Untagged work is grouped with `COALESCE(NULLIF(query_tag, ''), 'untagged')`. `official` https://docs.snowflake.com/en/user-guide/cost-attributing
- Custom tag by initial SQL (add it only if the built-in Tableau tag is not enough, as it may replace that tag): `derived`

```sql
ALTER SESSION SET QUERY_TAG = 'team=<team>;dashboard=<dashboard-name>';
```

- The simplest cost split needs no SQL: give each dashboard family its own warehouse or its own service user, then use warehouse and user columns in `QUERY_HISTORY`. `derived`
- Tableau runs initial SQL exactly as written without checking it. Test it in a Snowflake worksheet first. `official` connect_basic_initialsql.htm

## 1.2 Databricks in Tableau

### Driver and versions

- Tableau needs the Databricks ODBC driver. Missing driver prompts a download link in the dialog. `official` examples_databricks.htm
- Unity Catalog: Tableau Desktop 2021.4 or later with ODBC driver 2.6.19 or later. Legacy Hive metastore: Desktop 2019.3 or later with driver 2.6.15 or later. `official` https://docs.databricks.com/aws/en/partners/bi/tableau
- Service principal (M2M) needs Cloud or Desktop 2025.2 or later, Server or Bridge 2025.3 or later and ODBC driver 2.8.2 or later. `official` same page
- Tableau Server on Linux needs a Simba Spark ODBC entry in `/etc/odbcinst.ini`. `official` same page

### Connection fields

| Field | Notes | Label |
|---|---|---|
| Server Hostname | `adb-<workspace-id>.<n>.azuredatabricks.net` (Azure) or the AWS or GCP equivalent. Fully qualified on a Mac. | official (examples_databricks.htm) |
| HTTP Path | `/sql/1.0/warehouses/<warehouse-id>`. Copy from the compute resource's connection details. | official |
| Catalog | Set a default with `Catalog=<catalog>` under Advanced connection properties or `USE CATALOG <catalog>` in Initial SQL. | official (Databricks Tableau page) |
| Schema | Chosen on the data source page. | official |
| Role | No role field. If you hold Assume permission on a role you can authorise the OAuth connection as that role. | official (Databricks Tableau page) |

### Authentication options

| Option | Use when | Setup | Label |
|---|---|---|---|
| OAuth U2M (Databricks login) | Named users. Databricks recommends it. Enabled by default for Desktop and Cloud. Tokens expire after 90 days by default. | Sign in through the browser. Tableau Server needs separate setup. | official https://docs.databricks.com/aws/en/partners/bi/tableau |
| Service principal (OAuth M2M) | Published data sources and scheduled refresh with no human. | Create the principal, generate a secret (up to 730 days, shown once), grant it access to the SQL warehouse and the data, then enter client ID and secret in Tableau. | official https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m |
| Personal access token (PAT) | Quick tests only. Tied to one person, so refresh breaks when they leave. Token goes in the Password field. | Generate in Databricks user settings. | official for the field (examples_databricks.htm), derived for the advice |
| Username and password | Do not use. Basic authentication ended in July 2024. | None. | official examples_databricks.htm |

Notes:
- M2M access tokens last one hour and Databricks deletes a secret unused for 90 days, so a seasonal dashboard can lose its secret. `official` oauth-m2m page
- Databricks also recommends OAuth token federation (IdP tokens) where available. `official` https://docs.databricks.com/aws/en/dev-tools/auth/

### Live versus extract

- Live: every viewer interaction wakes the SQL warehouse (it auto-restarts on a JDBC or ODBC connection), so a cold start affects the first query and idle cost depends on auto stop. `official` https://docs.databricks.com/aws/en/compute/sql-warehouse/ for restart, `derived` for the dashboard effect
- Extract: publish the data source with refresh access enabled, set a schedule, then publish the workbook. Tableau Cloud checks for changes on that schedule. `official` Databricks Tableau page
- Tableau caching: "Refresh Less Often" keeps data cached up to 12 hours. Subscriptions can warm the cache. `official` same page
- Default choice: extract for broad dashboards, live on a serverless warehouse for fresh operational views. `derived`

### Performance

- Prefer a serverless SQL warehouse where available. It scales and queues by predicted workload. For classic and pro, Databricks suggests one cluster per 10 concurrent queries and 1,000 queued queries as the maximum. `official` https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior
- Start with one larger warehouse and size down. Raise size if the query profile shows spill. `official` same page
- Watch Peak Queued Queries. A steady value above zero means more size or more clusters. `official` same page
- Reduce records per chart and queries per dashboard. Limit quick filters because each filter multiplies queries. Use actions instead, use context filters for stable filters, avoid table calculations and aggregate before drilling down. `official` Databricks Tableau page
- Tune `RowsFetchedPerBlock` in the `.tds` or `.tdc` file to raise rows per fetch. `official` same page
- Primary and foreign keys (Databricks Runtime 15.2 or later) are informational, but Tableau uses them to detect relationships. `official` same page
- Use Tableau performance recording: query latency points at Databricks or the connector, layout latency points at Tableau. `official` same page
- Avoid pointing a dashboard at the hive metastore or the samples catalog. `official` same page
- Query tags: the Power BI connector exposes a `QueryTags` option written to `system.query.history` (see Part 2). For Tableau no equivalent field was found in the pages read. Use a dedicated service principal and SQL warehouse per dashboard family to split cost. `derived`

## 1.3 Tableau Cloud and Server specifics

- Tableau Bridge connects Tableau Cloud to data it cannot reach, such as sources behind a firewall. Drivers must be installed on the Bridge host. Embedded data sources need a configured pool, not the default pool. `official` https://help.tableau.com/current/online/en-us/to_sync_local_data.htm
- Snowflake is not supported with virtual connections through Bridge. `official` same page
- Bridge does not support SQL impersonation using initial SQL. `official` https://help.tableau.com/current/pro/desktop/en-us/connect_basic_initialsql.htm
- Publicly reachable Snowflake and Databricks do not need Bridge. Schedule refreshes directly in Tableau Cloud. `official` Bridge page
- IP allowlists: Tableau Cloud sites with live connections to cloud data may need the Tableau Cloud IP ranges on the data provider's allowlist. Find your pod, look up its range in the published table. New addresses are published at least 30 days before they apply. For Snowflake on AWS in the same region with internal stage protection, use a VPC endpoint ID instead. `official` https://help.tableau.com/current/pro/desktop/en-us/publish_tableau_online_ip_authorization.htm
- Virtual connections (Data Management licence) centralise credentials, extract schedules and data policies for row security. They apply to live and extract use. `official` https://help.tableau.com/current/online/en-us/dm_vconn_overview.htm
- Whether a specific connector is supported by virtual connections must be checked in the connector list, as the overview page did not list them. `derived`

## 1.4 Publishing: embedded credentials versus prompt

| Mode | Behaviour | Use for | Label |
|---|---|---|---|
| Embedded password (saved credentials) | Saved in the connection and used for everyone. The only way to schedule extract refresh. Viewers of a published data source need no View or Connect permission. | Extracts, service account or service principal dashboards, broad audiences. | official https://help.tableau.com/current/pro/desktop/en-us/publishing_sharing_authentication.htm |
| Prompt user | Each viewer signs in with their own database credentials. | Small audiences where warehouse identity must be personal. | official same page |
| Viewer credentials (SSO) | Viewer identity passed through, usually Kerberos. | Where the warehouse enforces row security per viewer. | official same page |
| OAuth (saved or per user) | Tokens held by Tableau. Check the saved credentials match the workbook connection, including role. | Cloud dashboards on Snowflake or Databricks OAuth. | official examples_snowflake.htm |

Rules of thumb: `derived`
- Never embed a personal account or PAT. Use a service user (key pair) or service principal.
- Embedded credentials bypass in-warehouse row security, because every viewer runs as the same identity. If security matters, either enforce it in Tableau (user filter or data policy) or use per-user OAuth.
- Key pair connections cannot be web edited, so keep the Desktop source file.

## 1.5 Tableau security

- OAuth over passwords: password sign-in is retired or ended on both platforms. `official` examples_snowflake.htm and examples_databricks.htm
- Service accounts: Snowflake offers `TYPE = SERVICE` users with key pair (and PAT on Tableau Cloud). Tableau Server does not support key pair for service users per the partner support table. `official` https://docs.snowflake.com/en/user-guide/partner-authentication-support
- RLS in the warehouse: Snowflake row access policies (Enterprise edition) filter by `CURRENT_ROLE()` or an entitlement mapping table. Metadata shortcuts like `COUNT(*)` slow down. `official` https://docs.snowflake.com/en/user-guide/security-row-intro
- RLS in Unity Catalog: row filters and column masks (SQL UDFs) or ABAC policies, on Runtime 12.2 LTS or later. They cannot be applied to views. `official` https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/
- RLS in Tableau: user filters, calculated fields using `USERNAME()` and virtual connection data policies. `official` for data policies (dm_vconn_overview.htm), `derived` for the rest
- Initial SQL with `TableauServerUser` can set a session identity for database-side security. It creates a dedicated connection that cannot be shared, which lowers cache reuse. Embedded data sources are risky here because web editors or downloaders can remove the initial SQL. The Tableau RLS page does not describe Snowflake or Databricks. Also note usernames on Tableau Cloud are email addresses that often do not match database identities. `official` https://help.tableau.com/current/server/en-us/rls_datasource.htm
- Pick one place to enforce security. Duplicating rules in Tableau and in the warehouse invites drift. `derived`

## 1.6 Tableau troubleshooting

| Error or symptom | Likely cause | Fix | Label |
|---|---|---|---|
| Driver missing message in the connection dialog | ODBC driver not installed on Desktop, Bridge or Server | Install the vendor driver (Snowflake ODBC or Databricks ODBC), restart Tableau | official examples_snowflake.htm |
| Key pair option missing or fails | Snowflake ODBC older than 3.4.0 or Tableau older than 2024.3 | Upgrade driver and Tableau | official examples_snowflake.htm |
| 390422 INCOMING_REQUEST_BLOCKED with a PAT | Client IP not on the Snowflake allowlist or network policy | Add the Tableau Cloud or Bridge IP | official examples_snowflake.htm |
| 40470 numeric value out of range | Number (Whole) field above supported range | Change field to Number (Decimal) or String | official examples_snowflake.htm |
| OAuth sign-in fails or expires | Access token lifetime (600 seconds) or refresh token expiry | Sign in again, check integration token settings | official oauth-partner page |
| OAuth role refused | Role is in the blocked list (ACCOUNTADMIN and similar) | Use a custom analyst role | official oauth-partner page |
| Custom OAuth config silently ignored | Config ID longer than 36 characters or missing `custom_` prefix | Shorten and prefix | official snowflake_oauth_idp.htm |
| Workbook slow on first open each morning | Warehouse auto suspended, cache lost | Lengthen auto suspend or schedule a warm-up subscription | official for cache loss (warehouses-considerations), derived for the fix |
| Slow fetch on text columns | Unbounded VARCHAR | Limit column length or set Default VARCHAR size | official examples_snowflake.htm |
| "This Field XXX Does Not Exist" | Custom SQL changed | Use Replace Field References | official examples_snowflake.htm |
| Databricks connection refused or 403 | Wrong HTTP path, no CAN USE on the warehouse, or expired PAT or secret | Recopy the path from the warehouse then grant access then regenerate the credential | derived |
| Databricks first query very slow | SQL warehouse stopped and restarting | Use serverless or keep a warm-up schedule | official for auto restart (sql-warehouse page), derived for the fix |
| Initial SQL error | Statement sent as written without a check | Test in the vendor SQL editor | official connect_basic_initialsql.htm |
| Live viewer sees no data on Cloud | Cloud cannot reach the source | Allowlist Tableau Cloud IPs or use Bridge | official IP authorisation page |
| Refresh fails after staff leave | Embedded personal credential | Move to key pair service user or service principal | derived |

---

# Part 2: Power BI equivalent

Use this part when migrating a Tableau dashboard to Power BI or when a client asks which Power BI settings match a Tableau choice.

## 2.1 Snowflake in Power BI

### Driver and versions

- The Snowflake connector is moving from the embedded Simba ODBC driver to the Snowflake ADBC driver. New Desktop connections have used implementation 2.0 (ADBC) by default since July 2025. Key pair authentication always uses ADBC. `official` https://learn.microsoft.com/en-us/power-query/connectors/snowflake
- The on-premises data gateway must be the January 2025 release or later for implementation 2.0. 64-bit Desktop only. `official` same page
- Known issues listed on the page: a `count distinct` incorrect result and higher memory use under implementation 2.0. `official` same page. Test both before migrating.
- Set implementation in M: `Snowflake.Databases("<account>.snowflakecomputing.com", "<warehouse>", [Implementation="2.0"])`. `official`

### Connection fields

| Field | Notes | Label |
|---|---|---|
| Server | `<account>.snowflakecomputing.com` | official |
| Warehouse | Required in Power BI (unlike Tableau). | official |
| Role | Advanced option. Must be available to the user, otherwise no role is set. | official |
| Database | Advanced option, Desktop only. | official |
| Connection and command timeout | Advanced options, in seconds. | official |
| SQL statement | Native query, advanced option. | official |

### Authentication

| Option | Use when | Setup | Label |
|---|---|---|---|
| Microsoft Entra ID SSO (Microsoft account) | Recommended. Each viewer queries as themselves. Works only with DirectQuery. | Snowflake admin creates an `external_oauth` security integration with `external_oauth_type = azure`, issuer `https://sts.windows.net/<tenant_id>/`, UPN mapped to `login_name`. | official https://docs.snowflake.com/en/user-guide/oauth-powerbi |
| Key pair | Service user, scheduled import refresh. Encrypted or unencrypted keys. Not supported in Dataflows Gen1 or Power Apps dataflows. | Upload the key, passphrase field appears if needed. | official Microsoft connector page |
| Service principal or workspace identity | Fabric scenarios needing a non-user identity. Support depends on Snowflake configuration. | Configure in Fabric. | official Microsoft connector page |
| Username and password | Avoid. Marked for deprecation. | None. | official Microsoft connector page |

SSO details: `official` https://docs.snowflake.com/en/user-guide/oauth-powerbi
- Entra ID is the only supported IdP for Power BI SSO. Primary role comes from the token scope or the user's default role. Default secondary roles are not activated unless `EXTERNAL_OAUTH_ANY_ROLE_MODE` is enabled.
- Without a gateway, private connectivity is not supported and the Power BI service IP ranges must be in the network policy. With a gateway, private connectivity works.
- The warehouse must auto resume or Power BI returns an unlisted error.
- Power BI sends a Snowflake query tag since April 2025, for example `{"PowerQuery":true,"Host":"PBI_SemanticModel_MWC","HostContext":"PowerBIPremium-DirectQuery"}`. `official` Microsoft connector page

### Import versus DirectQuery

- Import is the default recommendation: in-memory engine, richest features, fast, but needs scheduled refresh (8 a day on Pro, 48 on Premium or PPU). `official` https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about
- DirectQuery: no data stored, each visual queries Snowflake, latency depends on warehouse. Needed for SSO per viewer. One million row limit on a query or intermediate result (higher on Premium) and a 4 minute query timeout in the service. `official` same page
- Cold start: Snowflake, BigQuery and Databricks cold starts affect the first query. Send a warm-up or schedule periodic activity. `official` same page
- Mitigations: aggregation tables, hybrid tables (recent DirectQuery, history import), Dual mode dimensions, dynamic M parameters and query reduction settings. `official` same page
- Default of 10 DirectQuery connections per data source on Pro. Raising it increases warehouse load. `official` same page
- Tableau mapping: Tableau extract is close to Import. Tableau live is close to DirectQuery. `derived`

### Gateways

- An on-premises data gateway (standard mode) is needed when the service cannot reach the source directly, for DirectQuery, for live connections with shared sources or for private connectivity. A VNet data gateway serves sources inside a virtual network. `official` https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem
- Public Snowflake with SSO needs no gateway but needs network policy entries. `official` oauth-powerbi page
- Tableau Bridge corresponds to the gateway. `derived`

### Performance, cost and security

- Warehouse sizing, auto suspend and result cache rules are the same as Tableau (section 1.1). `official` Snowflake pages above
- Initial SQL has no direct equivalent. Use the native SQL statement option, a view or the Snowflake user's default settings. For cost tracking rely on the built-in Power BI query tag plus a dedicated warehouse or service user. `derived`
- Prefer tables and views over native SQL so Power Query folding works. Check View Native Query. `official` for folding guidance (DirectQuery page), `derived` for the Snowflake view advice
- RLS: Snowflake row access policies enforce security when SSO passes the viewer's identity. Otherwise define RLS roles in the semantic model, because unless SSO is configured DirectQuery uses the stored credential for all viewers. `official` DirectQuery page and security-row-intro page
- Publishing: Power BI stores connection credentials on the semantic model in the service. Choose SSO or a service user key pair for the stored credential. `derived`

## 2.2 Azure Databricks in Power BI

### Driver and versions

- Azure Databricks connector (`Databricks.Catalogs`) moves from the Simba Spark ODBC driver to the Databricks ADBC driver. Since February 2026 new connections use ADBC by default. Existing connections stay on ODBC until changed with `Implementation="2.0"`. `official` https://learn.microsoft.com/en-us/power-query/connectors/databricks-azure
- Use the Azure Databricks connector for all SQL warehouses unless told otherwise. The separate Databricks connector is for AWS warehouses using OAuth. `official` same page and https://learn.microsoft.com/en-us/power-query/connectors/databricks
- Limitation: `Databricks.Query` is not supported with DirectQuery. Automatic proxy settings from `.pac` files are not supported. `official` Azure Databricks connector page

### Connection fields

| Field | Notes | Label |
|---|---|---|
| Server Hostname | `adb-<workspace-id>.<n>.azuredatabricks.net` | official |
| HTTP Path | `/sql/1.0/warehouses/<warehouse-id>` | official |
| Catalog | Advanced option, default catalog. | official |
| Database (schema) | Advanced option. Speeds listing but blocks folding across databases. | official |
| QueryTags | Advanced option, `tag1:value1,tag2:value2`, recorded in `system.query.history`. Use it for cost tracking. | official |
| Protocol | ADBC option, `rest` uses the Statement Execution API. | official |

### Authentication

| Option | Use when | Setup | Label |
|---|---|---|---|
| Microsoft Entra ID (Azure only) | Named users, SSO on Azure. Recommended for viewers. | Sign in through the browser prompt. | official Azure Databricks connector page |
| Service principal (Entra, Azure only) | Cloud or gateway connection, unattended refresh. | Choose in Power Query Online when setting the connection. | official same page |
| Databricks client credentials (OAuth M2M) | Databricks service principal for refresh. | Create secret as in section 1.2. | official same page and oauth-m2m page |
| Personal access token | Tests only. | Generate in Databricks. | official for availability, derived for advice |
| Username and password (Basic) | Not available if MFA is on. Avoid. | None. | official Databricks connector page |

- If you hold Assume permission on a role you can authorise the OAuth connection as that role and Power BI runs all queries as it. `official` https://learn.microsoft.com/en-us/azure/databricks/partners/bi/power-bi

### Import versus DirectQuery

- Both are supported. The Import and DirectQuery trade-offs match section 2.1. `official` DirectQuery page
- With DirectQuery each visual wakes the SQL warehouse, so use serverless or accept cold start. `derived`
- Tableau mapping is the same: extract to Import, live to DirectQuery. `derived`

### Network and gateways

- Private networks need `*.blob.core.windows.net` and `*.store.core.windows.net` open, plus the Azure certificate revocation lists on the allowlist. If the workspace storage account has a firewall, use a VNet or on-premises gateway so CloudFetch keeps working, or set `EnableQueryResultDownload=0`. `official` Azure Databricks connector page

### Performance and security

- Warehouse sizing, serverless and queue guidance are the same as section 1.2. `official`
- Row security uses Unity Catalog row filters, column masks or ABAC. With a service principal or stored credential every viewer shares one identity, so the filters see that identity only. Use Entra ID SSO or per-viewer OAuth when filters must key on the viewer. `derived`
- Prefer Unity Catalog tables or views at dashboard grain, which fold well. `derived`

## 2.3 Power BI troubleshooting

| Error or symptom | Likely cause | Fix | Label |
|---|---|---|---|
| "SQL compilation error: Object does not exist, or operation cannot be performed" (Snowflake) | The user's default database is invalid | `DESC USER <username>`, then `ALTER USER <username> SET DEFAULT_NAMESPACE=<database>.<schema>` | official Microsoft Snowflake connector page |
| Invalid token or user not found (Snowflake SSO) | Issuer, audience or user mapping mismatch (case and trailing slash matter) | Drop and recreate the security integration with exact values. Check `LOGIN_HISTORY` for `OAUTH_ACCESS_TOKEN` | official oauth-powerbi page |
| Unlisted error on first query (Snowflake SSO) | Warehouse not set to auto resume | Enable auto resume | official oauth-powerbi page |
| Views not visible after upgrading to implementation 2.0 | Older March 2025 Desktop build | Update Desktop | official Microsoft Snowflake connector page |
| `count distinct` wrong or memory errors | Known issues in implementation 2.0 | Remove `Implementation="2.0"` to return to ODBC while a fix lands | official same page |
| Resource Governing: not enough memory | Large import on ADBC | Limit imported data or raise capacity | official same page |
| Query returns over 1,000,000 rows (DirectQuery) | Intermediate result limit | Aggregate, filter early, add aggregation tables | official DirectQuery page |
| Visual times out after 4 minutes | Slow source in the service | Fix warehouse size or model, or switch to Import | official DirectQuery page |
| Databricks private network read fails | Storage firewall blocks CloudFetch | Use gateway or set `EnableQueryResultDownload=0` | official Azure Databricks connector page |
| Credentials rejected after refresh | PAT or secret expired | Regenerate, update the connection in Data source settings | derived |
| Gateway refresh fails | Gateway too old for ADBC | Update to January 2025 or later (Snowflake) | official Microsoft Snowflake connector page |
