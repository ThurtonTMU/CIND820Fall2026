"""Build B01 auditable tables and diagrams; all coding is provisional.

No event observations, passenger records or simulated payload values are created.
"""
import csv
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data/batches/B01'
DOCS = ROOT/'docs'

def write_csv(name, rows, headers=None):
    path = DATA/name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=headers or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--accept-new-snapshot',action='store_true',help='Explicitly accept changed source bytes and regenerate the manifest')
    args=parser.parse_args()
    sources = json.loads((DATA/'sources.json').read_text())
    baseline={}
    if (DATA/'source_manifest.csv').exists():
        with (DATA/'source_manifest.csv').open(newline='',encoding='utf-8') as inp:
            baseline={r['source_id']:r for r in csv.DictReader(inp)}
    with (ROOT/'data/private/B01/capture_log.csv').open(newline='', encoding='utf-8') as inp:
        captures = {r['source_id']: r for r in csv.DictReader(inp)}
    source_rows=[]
    for source in sources:
        log = captures[source['source_id']]
        path = ROOT/source['snapshot_path']
        assert path.exists(), source['source_id']+' download missing'
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == log['sha256'], source['source_id']+' checksum mismatch'
        if source['source_id'] in baseline and baseline[source['source_id']]['sha256']!=digest and not args.accept_new_snapshot:
            raise ValueError(source['source_id']+' source changed; review before using --accept-new-snapshot')
        source_rows.append({**source, 'capture_status':log['status'], 'captured_at_utc':log['captured_at_utc'], 'sha256':digest, 'size_bytes':int(log['size_bytes']), 'final_url':log['final_url'], 'content_type':log['content_type'], 'redistribute_raw':False})
    write_csv('source_manifest.csv', source_rows)

    actors=[
        {'actor_id':'A01','name':'Reference merchant','actor_type':'organisational role','carrier_binding':'none assigned','source_id':'SRC0218','note':'Generic merchant in published terms; not a confirmed local carrier instance'},
        {'actor_id':'A02','name':'Adyen','actor_type':'organisation','carrier_binding':'vendor reference only','source_id':'SRC0218','note':'Contract/service provider; systems are separate execution components'},
        {'actor_id':'A03','name':'Shopper','actor_type':'individual role','carrier_binding':'none assigned','source_id':'SRC0164','note':'No personal attributes or real customer records collected'},
    ]
    write_csv('actors.csv',actors)
    systems=[
        {'system_id':'S01','name':'Merchant client website/app','owner_actor_id':'A01','autonomous_agent_status':'not established','source_id':'SRC0164'},
        {'system_id':'S02','name':'Merchant payments server','owner_actor_id':'A01','autonomous_agent_status':'not established','source_id':'SRC0164'},
        {'system_id':'S03','name':'Adyen Checkout API interface','owner_actor_id':'A02','autonomous_agent_status':'not established','source_id':'SRC0164'},
        {'system_id':'S04','name':'Merchant webhook server','owner_actor_id':'A01','autonomous_agent_status':'not established','source_id':'SRC0164'},
        {'system_id':'S05','name':'Adyen webhook delivery component','owner_actor_id':'A02','autonomous_agent_status':'not established','source_id':'SRC0167'},
    ]
    write_csv('systems.csv',systems)
    situations=[
        {'interaction_id':'AS01','name':'Shopper payment information handoff','function':'Fraud / payment','scope':'standard product reference','implementation_status':'carrier-specific implementation unverified'},
        {'interaction_id':'AS02','name':'Payment API request/response boundary','function':'Fraud / payment','scope':'standard product reference','implementation_status':'carrier-specific implementation unverified'},
        {'interaction_id':'AS03','name':'Authorisation webhook handling','function':'Fraud / payment','scope':'standard product reference','implementation_status':'carrier-specific implementation unverified'},
        {'interaction_id':'AS04','name':'Payment-interface downtime notification','function':'Fraud / payment / contractual governance','scope':'standard contract reference','implementation_status':'actual carrier contract applicability unverified'},
    ]
    write_csv('action_situations.csv',situations)
    activities=[
        ('ACT01','AS01','S01','Collect and pass shopper payment information','SRC0164'),
        ('ACT02','AS02','S02','Send API requests and receive responses','SRC0164'),
        ('ACT03','AS03','S05','Send authorisation status webhook','SRC0167'),
        ('ACT04','AS03','S04','Verify webhook authenticity as recommended','SRC0166'),
        ('ACT05','AS03','S04','Respond with HTTP status code','SRC0223'),
        ('ACT06','AS04','','Notify vendor of experienced interface downtime','SRC0218'),
    ]
    write_csv('activities.csv',[dict(zip(['activity_id','interaction_id','execution_system_id','activity','source_id'],r)) for r in activities])

    # Source excerpts are short. Inferred attributes/contexts are marked separately.
    statements=[]
    def statement(sid,src,loc,quote,kind,actor,deontic,aim,obj,condition,constituted,function,properties,situation,layers,note,inferred=''):
        statements.append(dict(statement_id=sid,source_id=src,source_locator=loc,short_excerpt=quote,statement_type=kind,attribute_A=actor,deontic_D=deontic,aim_I=aim,direct_object_Bdir=obj,activation_context_Cac=condition,execution_context_Cex='',or_else_O='',constituted_entity_E=constituted,constitutive_function_F=function,constituting_properties_P=properties,constitutive_modal_M='',inferred_components=inferred,interaction_id=situation,maia_layers=layers,coding_status='proposed',manual_review_status='pending',reviewer='',review_date='',coding_note=note))
    statement('B01-ST01','SRC0164','Integration architecture','A complete online payments integration with Adyen consists of the following parts:','constitutive_candidate','','','','','','Complete online payments integration','consists of','Payments server; client website/app; webhook server','AS01','Physical; Operational','Defines integration composition, not autonomous agency.')
    statement('B01-ST02','SRC0166','HMAC signatures','we strongly recommend that you use','regulative_candidate','[Merchant implementer]','strongly recommend','use','HMAC signatures','[When securing received webhooks]','','','','AS03','Constitutional; Operational','Recommendation is not recoded as must; no sanction supplied.','A; Cac')
    statement('B01-ST03','SRC0166','OAuth 2.0 — client secret','never embed it in client-side code','regulative_candidate','[Merchant implementer]','never','embed','OAuth client secret','[When configuring OAuth webhook access]','','','','AS03','Constitutional; Operational','Security prohibition concerns credentials; local adoption of OAuth remains unknown.','A; Cac')
    statement('B01-ST04','SRC0167','Standard webhooks — AUTHORISATION','we recommend that you rely on the webhook to trigger any business logic','regulative_candidate','[Merchant implementer]','recommend','rely on','AUTHORISATION webhook','[When triggering payment-related business logic]','','','','AS03','Constitutional; Operational','Handles sync/async flows; does not prove carrier automation or booking fulfilment.','A; Cac')
    statement('B01-ST05','SRC0223','operations — experimental field','Do not base your code on this field.','regulative_candidate','[API implementer]','do not','base','code on operations field','[When implementing this webhook interface]','','','','AS03','Constitutional; Operational','Experimental output must not become an authority matrix.','A; Cac')
    statement('B01-ST06','SRC0223','Response parameters','When you receive a webhook, you must respond with an HTTP status code.','regulative_candidate','[Webhook recipient]','must','respond','HTTP status code','upon webhook receipt','','','','AS03','Constitutional; Operational','Transport acknowledgement is separate from payment success; no rejection-of-payment sanction inferred.','A')
    statement('B01-ST07','SRC0218','7.2 Payment Interface Uptime Commitment','commercially reasonable efforts','regulative_candidate','Adyen','will','use','commercially reasonable efforts','during service provision','','','','AS04','Constitutional; Evaluative','Quarterly 99.9% receive-message uptime target with exclusions; target is not measured performance.')
    statement('B01-ST08','SRC0218','7.2 — merchant notification','Merchant will immediately notify Adyen','regulative_candidate','Merchant','will','notify','Adyen of experienced Payment Interface downtime','when Merchant experiences downtime','','','','AS04','Constitutional; Operational','Immediately is execution context; provisionally stored here for review, not an Or Else.')
    statements[-1]['execution_context_Cex']='immediately'
    statement('B01-ST09','SRC0218','11.2 Termination for Cause','Merchant may terminate the Agreement immediately if:','regulative_candidate','Merchant','may','terminate','Agreement','if section 7.2 SLA commitments are not met during two consecutive quarters','','','','AS04','Constitutional; Evaluative','Selected termination trigger; the source also lists other grounds. Actual contract applicability remains unverified.')
    statements[-1]['execution_context_Cex']='immediately'
    write_csv('statements_proposed.csv',statements)
    # Reviewed rows are an independent append-only input; never overwritten on rebuild.
    reviewed = DATA/'statements_reviewed.csv'
    if not reviewed.exists():
        write_csv('statements_reviewed.csv',[],list(statements[0]))

    defs=[
        ('amount','object',True,None,None,'Payment amount container'),
        ('amount.currency','string',True,3,3,'ISO currency code'),
        ('amount.value','integer',True,None,None,'Amount in currency-specific minor units'),
        ('eventCode','string',True,None,None,'Event classification; this endpoint is AUTHORISATION'),
        ('eventDate','string',True,None,None,'ISO 8601 timestamp as documented'),
        ('merchantAccountCode','string',True,None,None,'Merchant account identifier'),
        ('merchantReference','string',True,None,None,'Merchant payment reference'),
        ('pspReference','string',True,None,None,'Vendor transaction reference; described as 16 characters, not separately encoded here as schema length'),
        ('success','string',True,None,None,'Documented meanings true/false; keep string type'),
        ('reason','string',False,None,None,'Success/failure-dependent information; can include card-related details'),
        ('paymentMethod','string',False,None,None,'Payment method'),
        ('operations','array[string]',False,None,None,'Experimental; exclude from decision authority'),
    ]
    write_csv('data_definitions.csv',[dict(data_id=f'D{i:02}',source_id='SRC0223',source_locator='NotificationRequestItem / '+path,field_path=path,declared_type=typ,required=req,min_length=mn,max_length=mx,semantic_note=meaning,unit='currency minor units' if path=='amount.value' else '',observed_value='',review_status='pending') for i,(path,typ,req,mn,mx,meaning) in enumerate(defs,1)])
    write_csv('observations.csv',[],['observation_id','data_id','interaction_id','observed_value','observation_time','provenance','consent_or_usage_basis'])
    write_csv('evaluation_metrics.csv',[dict(metric_id='M01',source_id='SRC0218',source_locator='7.2',metric='Quarterly payment-interface uptime target',target_value=99.9,unit='percent',aggregation='quarterly average',measurement_basis='ability to receive transaction messages',exclusions='As specified in section 7.2; full review pending',observed_value='',deployment_status='standard contract only')])

    dimensions=['actors','actions','input_definitions','output_definitions','data_types','permissions','constraints','objectives','consequences']
    states={
        'AS01':['documented','documented','documented','documented','not_publicly_documented','not_publicly_documented','not_publicly_documented','not_publicly_documented','not_publicly_documented'],
        'AS02':['documented','documented','not_publicly_documented','not_publicly_documented','not_publicly_documented','not_publicly_documented','not_publicly_documented','not_publicly_documented','not_publicly_documented'],
        'AS03':['documented','documented','documented','documented','documented','documented','documented','not_publicly_documented','not_publicly_documented'],
        'AS04':['documented','documented','documented','not_publicly_documented','not_applicable','documented','documented','documented','documented'],
    }
    refs={'AS01':'SRC0164','AS02':'SRC0164','AS03':'SRC0166; SRC0167; SRC0223','AS04':'SRC0218'}
    write_csv('evidence_coverage.csv',[dict(interaction_id=interaction,dimension=dim,evidence_status='not_evidenced_in_batch' if status=='not_publicly_documented' else status,evidence_scope='standard vendor reference',source_ids=refs[interaction],coding_status='proposed',note='Preliminary selected-passage assessment; no exhaustive absence claim. Further extraction may change status.') for interaction in states for dim,status in zip(dimensions,states[interaction])])
    mappings=[dict(statement_id=r['statement_id'],maia_structure=layer.strip(),mapping_status='proposed',note='Analytical crosswalk; not claimed to reproduce the full MAIA metamodel') for r in statements for layer in r['maia_layers'].split(';')]
    write_csv('maia_mappings.csv',mappings)
    write_csv('relationships.csv',[
        dict(relationship_id=f'R{i:02}',from_id=a,to_id=b,relation=rel,source_id=src,evidence_scope='standard product architecture',review_status='pending')
        for i,(a,b,rel,src) in enumerate([
            ('A03','S01','PROVIDES_PAYMENT_INFORMATION','SRC0164'),
            ('S01','S02','PASSES_PAYMENT_INFORMATION','SRC0164'),
            ('S02','S03','REQUESTS_AND_RECEIVES_RESPONSE','SRC0164'),
            ('S05','S04','SENDS_WEBHOOK_EVENT','SRC0167'),
            ('A01','A02','NOTIFIES_EXPERIENCED_DOWNTIME','SRC0218'),
        ],1)
    ])
    DOCS.mkdir(exist_ok=True)
    mermaid='''erDiagram
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
'''
    (DOCS/'maia_erd.mmd').write_text(mermaid)
    (DOCS/'maia_erd.md').write_text('# MAIA evidence dataset ERD\n\nAdapted documentary data model, not a reproduction of the full MAIA simulation metamodel. Actor ownership, statement context and mappings require manual review. Source documents remain linked to statements and data definitions; missing evidence remains visible.\n\n```mermaid\n'+mermaid+'```\n')
    (DOCS/'payment_instance.md').write_text('''# B01 documented payment boundary

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
''')
    print(json.dumps({'sources':len(sources),'proposed_statements':len(statements),'reviewed_statements':0,'data_definitions':len(defs),'action_situations':len(situations),'coverage_cells':36}))

if __name__=='__main__':
    main()
