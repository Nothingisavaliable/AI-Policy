"""Offline tests for the prompt-engineering experiment log.

These tests avoid any network or pandas dependency for the core logic. The
pandas-backed loaders are exercised only when pandas is importable, so the
suite runs in a bare environment too.
"""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from ai_policy.experiment_log import (  # noqa: E402
    PREDICTIONS_FILENAME,
    RUNS_FILENAME,
    log_run,
    load_gold_labels,
)
from ai_policy.qwen_framing import compute_run_metrics, prompt_fingerprint  # noqa: E402


def make_predictions():
    return [
        {'country': 'X', 'sentence': 's1', 'label': 'AI-friendly', 'confidence': 0.9,
         'total_tokens': 100, 'latency_seconds': 0.5, 'attempts': 1, 'parse_failed': False},
        {'country': 'X', 'sentence': 's2', 'label': 'AI-cautious', 'confidence': 0.8,
         'total_tokens': 120, 'latency_seconds': 0.6, 'attempts': 2, 'parse_failed': False},
        {'country': 'X', 'sentence': 's3', 'label': 'neutral', 'confidence': 0.3,
         'total_tokens': 80, 'latency_seconds': 0.4, 'attempts': 1, 'parse_failed': True},
        {'country': 'X', 'sentence': 's4', 'label': 'mixed', 'confidence': 0.5,
         'total_tokens': 110, 'latency_seconds': 0.7, 'attempts': 1, 'parse_failed': False},
    ]


class FingerprintTests(unittest.TestCase):
    def test_stable_and_distinct(self):
        self.assertEqual(prompt_fingerprint('hello'), prompt_fingerprint('hello'))
        self.assertNotEqual(prompt_fingerprint('hello'), prompt_fingerprint('world'))
        self.assertEqual(len(prompt_fingerprint('hello')), 12)


class MetricsTests(unittest.TestCase):
    def test_gold_free_metrics(self):
        metrics = compute_run_metrics(make_predictions())
        self.assertEqual(metrics['sentence_count'], 4)
        self.assertEqual(metrics['neutral count'], 1)
        self.assertAlmostEqual(metrics['neutral_rate'], 0.25)
        self.assertAlmostEqual(metrics['parse_failure_rate'], 0.25)
        self.assertAlmostEqual(metrics['retry_rate'], 0.25)
        self.assertEqual(metrics['total_tokens'], 410)
        self.assertAlmostEqual(metrics['mean_total_tokens'], 102.5)
        self.assertFalse(metrics['has_gold'])
        self.assertAlmostEqual(metrics['median_confidence'], 0.65)

    def test_gold_metrics(self):
        gold = {'s1': 'AI-friendly', 's2': 'AI-friendly', 's3': 'neutral'}
        metrics = compute_run_metrics(make_predictions(), gold=gold)
        self.assertTrue(metrics['has_gold'])
        self.assertEqual(metrics['gold_overlap'], 3)
        # s1 correct, s2 wrong (predicted cautious), s3 correct -> 2/3
        self.assertAlmostEqual(metrics['accuracy'], round(2 / 3, 4))
        self.assertIn('macro_f1', metrics)
        self.assertIn('precision_AI-friendly', metrics)

    def test_empty_predictions(self):
        metrics = compute_run_metrics([])
        self.assertEqual(metrics['sentence_count'], 0)
        self.assertEqual(metrics['neutral_rate'], 0.0)


class LogRoundTripTests(unittest.TestCase):
    def test_log_run_writes_both_csvs(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs = Path(tmp)
            row = log_run(
                outputs,
                run_id='r1',
                timestamp='2026-01-01T00:00:00Z',
                model='qwen-plus',
                temperature=0.0,
                prompt_name='baseline',
                prompt_text='PROMPT TEXT',
                countries=['X'],
                predictions=make_predictions(),
                notes='unit test',
            )
            self.assertEqual(row['run_id'], 'r1')
            self.assertEqual(row['sentence_count'], 4)

            runs_path = outputs / RUNS_FILENAME
            preds_path = outputs / PREDICTIONS_FILENAME
            self.assertTrue(runs_path.exists())
            self.assertTrue(preds_path.exists())

            with runs_path.open(newline='', encoding='utf-8') as file:
                run_rows = list(csv.DictReader(file))
            self.assertEqual(len(run_rows), 1)
            self.assertEqual(run_rows[0]['prompt_name'], 'baseline')
            self.assertEqual(run_rows[0]['prompt_text'], 'PROMPT TEXT')
            self.assertEqual(run_rows[0]['prompt_fingerprint'], prompt_fingerprint('PROMPT TEXT'))

            with preds_path.open(newline='', encoding='utf-8') as file:
                pred_rows = list(csv.DictReader(file))
            self.assertEqual(len(pred_rows), 4)
            self.assertTrue(all(r['run_id'] == 'r1' for r in pred_rows))

    def test_append_second_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs = Path(tmp)
            log_run(outputs, run_id='r1', timestamp='t', model='m', temperature=0.0,
                    prompt_name='a', prompt_text='A', countries=['X'],
                    predictions=make_predictions())
            log_run(outputs, run_id='r2', timestamp='t', model='m', temperature=0.7,
                    prompt_name='b', prompt_text='B', countries=['X'],
                    predictions=make_predictions())
            with (outputs / RUNS_FILENAME).open(newline='', encoding='utf-8') as file:
                run_rows = list(csv.DictReader(file))
            self.assertEqual(len(run_rows), 2)
            with (outputs / PREDICTIONS_FILENAME).open(newline='', encoding='utf-8') as file:
                pred_rows = list(csv.DictReader(file))
            self.assertEqual(len(pred_rows), 8)


class GoldLoaderTests(unittest.TestCase):
    def test_missing_file_returns_empty(self):
        self.assertEqual(load_gold_labels(Path('/nonexistent/gold.csv')), {})

    def test_loads_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'gold.csv'
            with path.open('w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['sentence', 'gold_label'])
                writer.writeheader()
                writer.writerow({'sentence': 's1', 'gold_label': 'neutral'})
            self.assertEqual(load_gold_labels(path), {'s1': 'neutral'})


@unittest.skipUnless(
    __import__('importlib').util.find_spec('pandas'), 'pandas not installed'
)
class PandasBackedTests(unittest.TestCase):
    def test_compare_and_agreement(self):
        from ai_policy.experiment_log import compare_runs, prompt_agreement

        with tempfile.TemporaryDirectory() as tmp:
            outputs = Path(tmp)
            log_run(outputs, run_id='r1', timestamp='t', model='m', temperature=0.0,
                    prompt_name='a', prompt_text='A', countries=['X'],
                    predictions=make_predictions())
            # Second run: same sentences, one label flipped -> 3/4 agreement.
            flipped = make_predictions()
            flipped[0]['label'] = 'neutral'
            log_run(outputs, run_id='r2', timestamp='t', model='m', temperature=0.0,
                    prompt_name='b', prompt_text='B', countries=['X'],
                    predictions=flipped)

            comparison = compare_runs(outputs)
            self.assertEqual(len(comparison), 2)

            result = prompt_agreement(outputs, 'r1', 'r2')
            self.assertEqual(result['overlap'], 4)
            self.assertAlmostEqual(result['agreement'], 0.75)


if __name__ == '__main__':
    unittest.main(verbosity=2)
