"""Documentary coverage EDA only; no operational or causal estimates."""
import csv
from collections import Counter
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/batches/B01'
def read(name):
    with (DATA/name).open(newline='',encoding='utf-8') as inp:return list(csv.DictReader(inp))

def main():
    rows=read('evidence_coverage.csv')
    out=ROOT/'results/B01';out.mkdir(parents=True,exist_ok=True)
    summaries=[]
    for interaction in sorted({r['interaction_id'] for r in rows}):
        selected=[r for r in rows if r['interaction_id']==interaction]
        applicable=[r for r in selected if r['evidence_status']!='not_applicable']
        documented=sum(r['evidence_status']=='documented' for r in applicable)
        summaries.append(dict(interaction_id=interaction,checklist_cells=len(selected),applicable_cells=len(applicable),documented_cells=documented,unknown_cells=sum(r['evidence_status'] in ('not_publicly_documented','not_evidenced_in_batch','not_yet_extracted','retrieval_failed') for r in applicable),documentary_coverage=round(documented/len(applicable),4) if applicable else None))
    with (out/'coverage_by_interaction.csv').open('w',newline='',encoding='utf-8') as output:
        writer=csv.DictWriter(output,fieldnames=list(summaries[0]));writer.writeheader();writer.writerows(summaries)
    counts=dict(Counter(r['evidence_status'] for r in rows))
    summary={'sources':len(read('source_manifest.csv')),'proposed_statements':len(read('statements_proposed.csv')),'reviewed_statements':len(read('statements_reviewed.csv')),'data_definitions':len(read('data_definitions.csv')),'observations':len(read('observations.csv')),'coverage_status_counts':counts,'scope':'five-source standard-vendor pilot; qualitative checklist coding provisional'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    lines=['# B01 initial documentary EDA','','All statement and coverage coding is provisional. This is an extraction-method pilot, not a comparison of carriers or actual system safeguards.','','| Interaction | Applicable cells | Documented | Unknown | Coverage |','|---|---:|---:|---:|---:|']
    for r in summaries:lines.append(f"| {r['interaction_id']} | {r['applicable_cells']} | {r['documented_cells']} | {r['unknown_cells']} | {r['documentary_coverage']:.1%} |")
    lines+=['','Each action situation has the same nine-dimension checklist; one technical-type cell is marked not applicable. Unknown substantive values are not imputed as zero. Coverage concerns availability within this selected batch; generic role descriptions and full field specifications are different depths of evidence. All reference edges remain provisional and no carrier centrality is estimated.','',f"Sources: {summary['sources']}; proposed statements: {summary['proposed_statements']}; reviewed statements: {summary['reviewed_statements']}; selected field definitions: {summary['data_definitions']}; observed events: 0."]
    (out/'initial_eda.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
