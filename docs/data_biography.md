# Data biography — B01, version 0.1

## Dataset identity and purpose

**Title:** Aviation MAS documentary dataset — B01 payment-authorisation boundary. **Research collector:** Marie-Louise Thurton, with AI-assisted retrieval, extraction and proposed coding. **Original publisher/collector:** Adyen publishes the five technical/contractual documents; the research project constructs the derived tables. No payment events are collected from Adyen or any carrier.

The dataset supports a documentary analysis of actor interactions, institutional constraints and valuation-related indicators using MAIA and IG 2.0. B01 establishes a repeatable acquisition/coding process. It is not evidence of a live carrier configuration or adoption outcome.

## Provenance and original publication purpose

All five source IDs already exist in the master integrated register. Four pages explain standard payment integration, security, notification semantics or interface fields. One publishes standard customer terms and service levels. The publisher's purpose differs from the research project's analytical coding purpose. Each derived statement/field/relationship links to a neutral source ID and a located section. SHA-256 hashes identify exact raw HTML bytes; checksums do not certify the underlying claims as true.

## Format, size and dates

- Five raw HTML snapshots, totalling **3,493,315 bytes**, plus privately extracted UTF-8 text. These include navigation/client-rendering material, so raw size is not substantive text volume.
- Retrieval: **14 October 2026**, 17:05 UTC; exact per-source times are retained in the manifest.
- Four webpages have no established publication date and may change independently of the API version. The API reference identifies Webhooks v1. The contract page states last update 1 November 2023; this does not establish either carrier's signing date or negotiated terms.
- Derived formats: CSV and JSON; documentation/diagrams: Markdown and Mermaid; scripts: Python using the standard library.

## Coverage and units

Five purposively selected documents from one vendor cover a generic payment architecture and associated requirements. The source-document unit, statement unit, technical-definition unit, action-situation unit and evidence-checklist cell are distinct. The bounded MAS is the conceptual case; interactions/action situations support relational analysis. No representative sampling claim is made.

The pilot includes **3 actor roles, 5 execution components, 4 action situations, 6 activities, 9 proposed statements, 12 selected field definitions, 1 evaluation metric, 5 reference relationships and 36 coverage assessments**. It contains **0 human-reviewed statements and 0 observed event/value rows**. Counts refer to B01, not the full master register. Additional optional webhook fields and recursive schemas have not been fully extracted.

Air Canada and Lufthansa vendor relationships are context in the master; B01 uses a generic merchant and does not assign production implementation. Delta is not assigned Adyen as its fraud provider. No airports, domestic/international ticket samples or T-100 operational observations enter this first batch.

## Variables and keys

| Table | Key and principal variables |
|---|---|
| source_manifest | source_id; title; publisher; URL; format/version; captured time; SHA-256; byte size; usage status |
| statements_proposed / reviewed | statement_id; source and locator; short excerpt; type; A/D/I/B/C/O or E/F/P/M components; inferred components; interaction; review status |
| actors / systems | actor/system IDs; organisational/individual roles; component owner; autonomy and carrier-binding status |
| action_situations / activities | interaction/activity IDs; reference scope; execution component; documented activity |
| data_definitions | data_id; declared field path/type; required status; bounds; unit; semantics; empty observed value |
| relationships / maia_mappings | typed endpoints and source evidence; proposed MAIA structure; review status |
| evaluation_metrics | documented target, aggregation and measurement basis; no observed performance value |
| evidence_coverage | interaction × nine dimensions; evidence status; scope and source IDs |
| observations | Empty schema for future empirical values, with provenance and usage basis |

## Collection and processing

`capture_sources.py` retrieves public pages without credentials, saves exact bytes privately and derives text with Python's HTML parser. Text extraction removes script/style content but is not a perfect reconstruction of the visual page. No personal values or payment payload examples are fabricated. Public short excerpts are matched against captured text during validation. Proposed coding is selected and manually reviewable, not automatic exhaustive clause segmentation.

`build_batch.py` produces linked records and diagrams. It preserves the independent reviewed table and fails when source bytes drift from the committed manifest unless a new snapshot basis is explicitly accepted. `run_eda.py` counts documentation coverage; no causal, operational or centrality results are estimated.

## Missingness, representation and bias

Unknown fields remain empty with a separate evidence status; no undocumented guardrail is coded absent. The pilot uses `not_evidenced_in_batch` for gaps, because partial extraction cannot establish public non-disclosure; `not_yet_extracted` is available for explicitly deferred coding. A nine-dimension checklist defines the initial denominator, excluding one justified not-applicable technical-type cell. It is a coarse availability measure, not a comparable technical-depth score. Source selection favours accessible vendor-facing documentation, with likely disclosure bias. A single-vendor pilot cannot substantiate an aviation-wide transparency finding. No formal MCAR/MAR/MNAR category is assigned from this evidence alone.

Proposed IG/MAIA coding may contain interpretation errors. Recommendation/obligation, transport acknowledgement/payment success, vendor capability/local adoption and historical/current status must remain distinct. Review consistency and expert validation are outstanding.

## Privacy, ethics and usage terms

The dataset contains published documentary text and field definitions, not PNRs, customer/payment records, employee IDs or actual transactions. Definitions can expose categories of potentially identifying/sensitive information; the presence of a field is not evidence of a particular carrier collecting it. Do not add live values without a separate privacy/usage assessment. Naming a vendor is not a finding of wrongdoing. Conditional risk mechanisms must not be presented as observed incidents.

**Access confirmed:** all five pages returned HTTP 200 during capture. **Reuse licence:** no open licence for wholesale redistribution has been established. Vendor copyright notices and applicable site terms remain relevant; service-contract terms do not themselves license documentation. **Repository practice:** keep raw/full extracted vendor content private and Git-ignored; publish authored metadata, limited excerpts, interpretations, diagrams and scripts. No open licence is assigned to the researcher's work without their decision. A further source-by-source permissions review is required before broader redistribution of captured documents.

## Outstanding work

Human coding review, optional field/schema expansion, a stronger depth-of-evidence checklist and subsequent cross-function batches remain. BTS operational datasets can later enter as a separate layer with their own biographies and join limitations. This biography is updated with each batch and is not represented as a completed final submission.
