# Coding protocol — pilot version 0.1

1. Register the source ID, exact URL, captured bytes/hash, date, version, collector, publisher, purpose and usage restrictions. Public accessibility is not a confirmed redistribution licence.
2. Locate a passage by heading and short exact excerpt. Preserve the publisher's wording privately. Decompose compound clauses only with a traceable parent passage.
3. Classify regulative, constitutive, mixed or technical-description content before component coding. A schema field need not be forced into ADICO. Technical definitions remain linked resources even where no institutional coding is appropriate.
4. Populate IG 2.0 components appropriate to the statement type. Mark inferred actors/contexts explicitly. Retain recommendation versus obligation and conditional scope. Populate Or Else only where a warranted consequential statement exists. Blank does not prove a consequence is absent from other sources.
5. Link the statement to an action situation and proposed MAIA structure. Collective concerns actors/attributes; Constitutional concerns positions/institutions/authority; Physical concerns resources and capabilities; Operational concerns activities and situations; Evaluative concerns outcome indicators. Data/interface resources are an explicit project adaptation; a full computational MAIA implementation is not claimed.
6. Preserve declared data types and source units. In B01, `success` remains string and payment amount remains integer minor units. Source-required fields and optional features must stay distinct. No payload observations are generated.
7. Add one evidence-assessment cell for every applicable checklist dimension. Use `not_evidenced_in_batch` for preliminary gaps; use `not_yet_extracted` for known deferred extraction. Reserve `not_publicly_documented` for a scoped, documented search that supports that conclusion. `explicitly_absent` requires affirmative source evidence. `not_applicable` requires a reason. Do not impute unknown safeguards as absent.
8. Review each proposed record against the full source and add accepted/amended records to the independent reviewed table. Record reviewer/date, source locator and rationale. Inter-coder consistency has not yet been measured.

## Coverage checklist and denominator

Each action situation uses nine dimensions: actors, actions, input definitions, output definitions, data types, permissions, constraints, objectives and consequences. The first pass considers named objects/roles sufficient for coarse documentary availability, so this is **not a technical-depth score**. Field-level completeness needs a separate, versioned checklist. Permissions includes documented duties/access conditions; objectives refers to an explicitly stated purpose/target, not inferred algorithm weights. Broad definitions and full schemas are not treated as equivalent evidence quality.

Coverage = documented applicable cells / all applicable cells. Exclude only justified not-applicable cells; keep retrieval failures and unresolved cells in the denominator. AS04 data types is marked not applicable because that situation currently models a contractual notice rather than a documented machine interface. If a notice API is added, reassess that decision.

## Evidence and implementation scope

Keep carrier-specific, standard product, adjacent product, historical and planned references distinct. Build confirmed-deployment network views separately from documented reference/proxy views. A reference merchant actor is not Air Canada or Lufthansa. A captured standard contract is not proof of either carrier's agreement. Missing engine details do not establish mathematical partial observability of the real system.

## Conditional risks, not findings of harm

Potential issues include inconsistent event handling, credential exposure and ambiguities between recommendation, obligation and local implementation. These are hypotheses for later Hammond-informed analysis; no incident, bias, collusion or governance failure is demonstrated by B01. Documentary EDA assesses the construction process before outcome inference.
