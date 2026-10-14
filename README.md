# Aviation cross carrier interactions

Provisional IG 2.0 coding for revenue and fraud management across Air Canada, Delta and Lufthansa. Airport interfaces retain YYZ, ORD and FRA as cases; deployment links require evidence.

| Component | Files |
|---|---|
| Revenue pricing and inventory | [Coded statements](statements/revenue/pricing_inventory_interfaces.csv) |
| Fraud payment and webhook controls | [Technical statements](statements/fraud/payment_webhook_controls.csv) · [Contract clauses](statements/fraud/payment_contracts.csv) |
| Shared integration | [Composition statement](statements/shared/payment_integration.csv) |
| Airport carrier and vendor interfaces | [Source register](schemas/source_register.csv) · [Airport schema index](schemas/airport_schema_index.csv) |
| Native fields | [Payment](schemas/fields/payment_webhooks.csv) · [Pricing](schemas/fields/pricing_inventory.csv) |
| Authority and institutional force | [Coding scales](model/coding_scales.json) |
| Partner and competing carrier links | [Evidence register](model/cross_carrier_linkages.csv) |

All statements are pending manual review. Unknown is not zero. Standard compatibility does not prove deployment, access rights or an agent interaction. The MAIA diagram and assignment bibliography remain in the Word document. No EDA or passenger records are included.

Original schemas are included where reuse terms are confirmed; other sources are linked with extraction gaps.

[Original Adyen webhook schema](schemas/vendor/adyen/Webhooks-v1.json) is included with its MIT licence and provenance. Publisher example values are not observed data.
