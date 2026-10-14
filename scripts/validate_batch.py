"""Validate source traceability, declared types, review separation and denominators."""
import csv
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/batches/B01'
def read(name):
    with (DATA/name).open(newline='',encoding='utf-8') as inp:
        return list(csv.DictReader(inp))

def main():
    sources=read('source_manifest.csv'); source_ids={s['source_id'] for s in sources}
    assert len(source_ids)==len(sources)==5
    statements=read('statements_proposed.csv'); statement_ids={s['statement_id'] for s in statements}
    assert len(statement_ids)==len(statements)
    private_count=0
    for source in sources:
        raw=ROOT/source['snapshot_path']
        if raw.exists():
            assert hashlib.sha256(raw.read_bytes()).hexdigest()==source['sha256']
            private_count+=1
    quoted=Counter()
    for s in statements:
        assert s['source_id'] in source_ids and s['source_locator']
        assert s['coding_status']=='proposed' and s['manual_review_status']=='pending'
        quoted[s['source_id']]+=len(s['short_excerpt'].split())
        txt=ROOT/f"data/private/B01/{s['source_id']}.txt"
        if txt.exists():
            haystack=' '.join(txt.read_text().split()).casefold()
            needle=' '.join(s['short_excerpt'].split()).casefold()
            assert needle in haystack, f"Source excerpt not found: {s['statement_id']}"
    assert all(n<=25 for n in quoted.values()), quoted
    assert all(r['statement_id'] in statement_ids for r in read('statements_reviewed.csv'))
    definitions=read('data_definitions.csv')
    success=next(r for r in definitions if r['field_path']=='success')
    amount=next(r for r in definitions if r['field_path']=='amount.value')
    assert success['declared_type']=='string', 'Never coerce source string flag to Boolean in raw definitions'
    assert amount['declared_type']=='integer' and amount['unit']=='currency minor units'
    assert not read('observations.csv'), 'B01 must not invent event or passenger observations'
    coverage=read('evidence_coverage.csv')
    allowed={'documented','explicitly_absent','not_publicly_documented','not_evidenced_in_batch','not_yet_extracted','retrieval_failed','not_applicable'}
    assert all(r['evidence_status'] in allowed for r in coverage)
    assert len({(r['interaction_id'],r['dimension']) for r in coverage})==36
    assert len(coverage)==36
    for name in ['activities.csv','data_definitions.csv','evaluation_metrics.csv','relationships.csv']:
        assert all(r['source_id'] in source_ids for r in read(name)),name
    print(json.dumps({'status':'passed','source_snapshots_verified':private_count,'proposed_statements':len(statements),'reviewed_statements':len(read('statements_reviewed.csv')),'coverage_cells':len(coverage),'quote_words_by_source':dict(quoted)}))

if __name__=='__main__':main()
