# MAIA evidence dataset ERD

Adapted documentary data model, not a reproduction of the full MAIA simulation metamodel. Actor ownership, statement context and mappings require manual review. Source documents remain linked to statements and data definitions; missing evidence remains visible.

```mermaid
erDiagram
    ACTOR ||--o{ SYSTEM : owns_reference_component
    ACTOR ||--o{ SOURCE : publishes
    SOURCE ||--o{ STATEMENT : supports
    SOURCE ||--o{ DATA_DEFINITION : specifies
    ACTION_SITUATION ||--o{ ACTIVITY : contains
    SYSTEM o|--o{ ACTIVITY : executes
    ACTION_SITUATION ||--o{ STATEMENT : contextualises
    STATEMENT ||--o{ MAIA_MAPPING : mapped_to
    ACTION_SITUATION ||--o{ EVIDENCE_ASSESSMENT : assessed_by
    SOURCE ||--o{ EVALUATION_METRIC : defines
    DATA_DEFINITION ||--o{ OBSERVATION : permits_future_values
    ACTOR {
        string actor_id PK
        string role_type
        string carrier_binding
    }
    SYSTEM {
        string system_id PK
        string owner_actor_id FK
        string autonomy_status
    }
    SOURCE {
        string source_id PK
        string url
        string sha256
    }
    STATEMENT {
        string statement_id PK
        string source_id FK
        string ig_type
        string review_status
    }
    ACTION_SITUATION {
        string interaction_id PK
        string implementation_status
    }
    ACTIVITY {
        string activity_id PK
        string execution_system_id FK
    }
    DATA_DEFINITION {
        string data_id PK
        string declared_type
        boolean required
    }
    MAIA_MAPPING {
        string statement_id FK
        string structure
    }
    EVIDENCE_ASSESSMENT {
        string interaction_id FK
        string dimension
        string evidence_status
    }
    EVALUATION_METRIC {
        string metric_id PK
        string measurement_basis
    }
    OBSERVATION {
        string observation_id PK
        string data_id FK
        string observed_value
    }
```
