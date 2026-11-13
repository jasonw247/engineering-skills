"""Run the supplied deterministic fixture using only Python's standard library."""
import copy
import hashlib
import importlib.util
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT_NAMES = ('fixture_system.py', 'queries.json', 'corpus.json')
VARIANTS = ('baseline', 'candidate')


def file_hash(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def rate(numerator, denominator):
    return {'numerator': numerator, 'denominator': denominator,
            'rate': numerator / denominator if denominator else None}


def summarize(rows):
    answerable = [r for r in rows if r['reference']['answerable']]
    unanswerable = [r for r in rows if not r['reference']['answerable']]
    claims = [r for r in rows if r['scores']['emitted_pressure_claim']]
    fields = {
        'candidate_complete_evidence': ('candidate_sufficient', answerable),
        'delivered_complete_evidence': ('delivered_sufficient', answerable),
        'answerable_correctness': ('answer_correct', answerable),
        'answerable_completeness': ('answer_correct', answerable),
        'task_correctness': ('task_correct', rows),
        'supported_claims': ('claim_supported', claims),
        'citation_support': ('citation_supported', claims),
        'citation_coverage': ('citation_present', claims),
        'unanswerable_abstention': ('appropriate_abstention', unanswerable),
        'answered_fraction': ('emitted_pressure_claim', rows),
    }
    result = {name: rate(sum(r['scores'][field] is True for r in group), len(group))
              for name, (field, group) in fields.items()}
    result['execution_failures'] = rate(sum(r['status'] != 'ok' for r in rows), len(rows))
    result['delivered_scope_violations'] = rate(
        sum(len(r['diagnostics']['scope_violations']) for r in rows),
        sum(len(r.get('output', {}).get('evidence', [])) for r in rows))
    result['delivered_outside_candidates'] = rate(
        sum(len(r['diagnostics']['outside_candidates']) for r in rows),
        sum(len(r.get('output', {}).get('evidence', [])) for r in rows))
    return result


def evaluate(query, output, corpus):
    for key in ('candidates', 'evidence', 'citations'):
        if not isinstance(output.get(key), list) or not all(isinstance(x, str) for x in output[key]):
            raise ValueError('Malformed ' + key)
    if not isinstance(output.get('abstained'), bool) or 'answer_mpa' not in output:
        raise ValueError('Malformed answer/abstention')
    value = output['answer_mpa']
    if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
        raise ValueError('Non-numeric pressure')
    unknown = sorted(set(output['candidates'] + output['evidence'] + output['citations']) - corpus.keys())
    if unknown:
        raise ValueError('Unknown source IDs requiring adjudication: ' + repr(unknown))

    def applicable(ids):
        return {i for i in ids if corpus[i]['entity'] == query['entity']
                and corpus[i]['revision'] == query['revision']}

    def sufficient(ids):
        if not query['answerable']:
            return None
        eligible = applicable(ids)
        return any(set(s).issubset(eligible) for s in query['sufficient_sets'])

    emitted = value is not None
    answer_correct = (emitted and not output['abstained'] and value == query['expected_mpa']) if query['answerable'] else None
    abstention = (output['abstained'] and not emitted) if not query['answerable'] else None
    delivered = sufficient(output['evidence'])
    cited_delivered = set(output['citations']) & set(output['evidence'])
    # The fixture rubric describes the one applicable pressure claim. Claim support
    # checks both applicability/conditions (via sufficient sets) and its actual value.
    claim_supported = bool(query['answerable'] and delivered and value == query['expected_mpa']) if emitted else None
    citation_supported = bool(query['answerable'] and sufficient(cited_delivered) and value == query['expected_mpa']) if emitted else None
    return {
        'candidate_sufficient': sufficient(output['candidates']),
        'delivered_sufficient': delivered,
        'answer_correct': answer_correct,
        'task_correct': answer_correct if query['answerable'] else abstention,
        'emitted_pressure_claim': emitted,
        'claim_supported': claim_supported,
        'citation_supported': citation_supported,
        'citation_present': bool(output['citations']) if emitted else None,
        'appropriate_abstention': abstention,
    }, {
        'scope_violations': sorted(set(output['evidence']) - applicable(output['evidence'])),
        'outside_candidates': sorted(set(output['evidence']) - set(output['candidates'])),
        'citation_ids_exist': all(i in corpus for i in output['citations']) if emitted else None,
        'citations_not_delivered': sorted(set(output['citations']) - set(output['evidence'])),
        'unknown_ids': unknown,
    }


def main():
    before = {name: file_hash(name) for name in INPUT_NAMES}
    corpus = json.loads((ROOT / 'corpus.json').read_text())
    queries = json.loads((ROOT / 'queries.json').read_text())
    assert len({q['id'] for q in queries}) == len(queries), 'Duplicate query IDs'
    for q in queries:
        assert q['answerable'] == bool(q['sufficient_sets'])
        for s in q['sufficient_sets']:
            assert s and all(i in corpus for i in s)
    # Avoid writing a bytecode cache beside the immutable supplied implementation.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('supplied_fixture', ROOT / 'fixture_system.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = []
    for variant in VARIANTS:
        for query in queries:
            row = {'variant': variant, 'query_id': query['id'], 'query': query,
                   'reference': {k: query[k] for k in ('answerable', 'expected_mpa', 'sufficient_sets')}}
            started = time.perf_counter_ns()
            try:
                # Separate copies also reveal rather than propagate accidental input mutation.
                query_copy, corpus_copy = copy.deepcopy(query), copy.deepcopy(corpus)
                output = module.run(query_copy, corpus_copy, variant)
                row['function_elapsed_ns'] = time.perf_counter_ns() - started
                row['output'] = output
                row['in_memory_inputs_unchanged'] = query_copy == query and corpus_copy == corpus
                scores, diagnostics = evaluate(query, output, corpus)
                row.update(status='ok', scores=scores, diagnostics=diagnostics)
            except Exception as error:
                row.update(status='failure', error={'type': type(error).__name__, 'message': str(error)},
                           function_elapsed_ns=time.perf_counter_ns() - started,
                           scores={key: False for key in (
                               'candidate_sufficient', 'delivered_sufficient', 'answer_correct',
                               'task_correct', 'emitted_pressure_claim', 'claim_supported',
                               'citation_supported', 'citation_present', 'appropriate_abstention')},
                           diagnostics={'scope_violations': [], 'outside_candidates': []})
            rows.append(row)
    after = {name: file_hash(name) for name in INPUT_NAMES}
    assert before == after, 'Raw input file changed during run'
    summaries = {v: summarize([r for r in rows if r['variant'] == v]) for v in VARIANTS}
    paired = []
    for q in queries:
        a = next(r for r in rows if r['variant'] == 'baseline' and r['query_id'] == q['id'])
        b = next(r for r in rows if r['variant'] == 'candidate' and r['query_id'] == q['id'])
        paired.append({'query_id': q['id'], 'baseline_task_correct': a['scores']['task_correct'],
                       'candidate_task_correct': b['scores']['task_correct'],
                       'change': int(b['scores']['task_correct']) - int(a['scores']['task_correct'])})
    result = {
        'mode': 'run', 'scope': 'deterministic synthetic functionality only',
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'configuration': {
            'variants': VARIANTS, 'query_count': len(queries), 'calls_per_variant': len(queries),
            'repetitions': 1, 'concurrency': 1, 'randomness': 'none in supplied implementation',
            'python': sys.version, 'platform': platform.platform(), 'machine': platform.machine(),
            'processor': platform.processor() or 'not exposed',
            'cache_conditions': 'normal Python process; no model/index/retrieval cache; no warmup',
            'timing_boundary': 'deep-copy inputs plus fixture call; local diagnostic only, not service latency',
            'models_prompts_parser_index': 'not applicable: deterministic Python fixture',
            'evidence_cap': 'implementation returns zero or one source, no token budget',
            'external_calls': 0, 'production_cost_latency_build_refresh': 'not measured',
            'label_origin': 'supplied queries.json; not an independently reviewed benchmark',
            'protocol_sha256': file_hash('protocol.md'), 'runner_sha256': file_hash('evaluate.py'),
        },
        'input_sha256_before': before, 'input_sha256_after': after, 'raw_inputs_unchanged': before == after,
        'rows': rows, 'aggregates': summaries, 'paired_task_outcomes': paired,
        'comparison_scope': 'bundled evidence selection and missing-query abstention changes; no isolated component attribution',
    }
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'aggregates': summaries, 'paired': paired, 'raw_inputs_unchanged': before == after}, indent=2))


if __name__ == '__main__':
    main()
