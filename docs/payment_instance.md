# B01 documented payment boundary

Standard Adyen reference architecture; no carrier configuration asserted. Proposed execution components are not automatically autonomous agents. Dotted arrows are recommendations/requirements addressed to the implementer, not observed runtime behaviour.

```mermaid
flowchart TD
    C["Merchant client"] -->|"payment information · SRC0164"| P["Payments server"]
    P -->|"request · SRC0164"| A["Adyen Checkout interface"]
    A -->|"response · SRC0164"| P
    E["Adyen webhook delivery"] -->|"AUTHORISATION · SRC0167"| W["Merchant webhook server"]
    H["HMAC recommendation · SRC0166"] -.-> W
    T["HTTP response requirement · SRC0223"] -.-> W
    U["Uptime target and notice · SRC0218"] -.-> P
```

Collective: merchant, vendor and shopper roles. Constitutional: security recommendations, HTTP response requirement and contractual notice. Physical: documented fields and execution components (a project extension to MAIA's physical/information resources). Operational: request/response and notification activities. Evaluative: contractual uptime target; observed performance and optimisation weights are unknown. Internal routing from Checkout processing to webhook delivery is deliberately not asserted as a documented system-to-system edge.
