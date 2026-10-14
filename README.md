# CIND820Fall2026

Documentary dataset for modelling aviation multi-agent governance through **MAIA** and **Institutional Grammar 2.0**.

The research models documented interaction boundaries, institutional constraints and valuation-related indicators. It does not reproduce airline production systems or infer deployed autonomous agents from vendor names.

## First batch: B01 payment authorisation

Five public Adyen source pages are captured locally. The batch contains nine **proposed**, unreviewed statement codings, twelve selected field definitions, four bounded action situations and a thirty-six-cell evidence checklist. No passenger data, observed payment events or synthetic payload values are present.

The generic merchant architecture is a standard-product reference. Air Canada and Lufthansa relationships in the master register provide research context; this batch is **not** assigned to either carrier's actual configuration.

- [Data biography](docs/data_biography.md)
- [Data bibliography](docs/data_bibliography.md)
- [MAIA evidence ERD](docs/maia_erd.md)
- [Payment-boundary diagram](docs/payment_instance.md)
- [Coding and review protocol](docs/coding_protocol.md)
- [Initial documentary EDA](results/B01/initial_eda.md)
- [Review checklist](docs/review_checklist.md)

## Reproduce on Windows / VS Code

The core scripts use Python 3.12+ and the standard library, with no pandas or Neo4j requirement.

```powershell
python scripts/capture_sources.py
python scripts/build_batch.py
python scripts/validate_batch.py
python scripts/run_eda.py
```

Source pages may change. Rebuilding checks the downloaded bytes against the committed manifest and stops on drift. Review changes before explicitly using `python scripts/build_batch.py --accept-new-snapshot`. That creates a new capture basis; it does not reproduce the original bytes. Existing snapshots are preserved unless `capture_sources.py --replace` is explicitly used. An existing capture log retains its original retrieval time on reuse.

## What belongs in Git

Authored metadata, short excerpts, proposed/reviewed coding, data definitions, diagrams and scripts are publishable project records. Vendor HTML/full extracted text remain under `data/private/`, excluded by `.gitignore`, because no open licence for their wholesale redistribution has been established. The repository does not license vendor source material. Keep private captures under suitable access controls and retention practices; publisher links and checksums remain public.

## Dataset organisation

`data/batches/B01/` contains source metadata and linked CSV tables. `statements_proposed.csv` is generated; **do not edit it as the reviewed record**. Add manually accepted or amended rows to `statements_reviewed.csv`, retaining the original statement ID and recording reviewer/date. That file is not overwritten by a rebuild. `observations.csv` has an empty schema reserved for future empirical values.

This is a pilot extraction set, not exhaustive coding of five documents. Field coverage is deliberately restricted to twelve boundary fields; optional `additionalData` fields and recursive schema expansion remain pending. A node or interface is not automatically an autonomous agent. All network relationships and MAIA mappings currently require manual review.

## Publication status

Repository: https://github.com/ThurtonTMU/CIND820Fall2026. B01 is a provisional research batch for review. Source interpretation, MAIA mapping and coverage assessments require human validation before analytical findings are reported.
