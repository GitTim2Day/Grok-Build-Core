import copy
import json
import unittest
from reference import Reference, canonical, demo, reconstruct


class MilestoneTests(unittest.TestCase):
    def setUp(self):
        self.engine, self.request = demo()

    def test_exact_result_and_denied_contributor(self):
        records, graph = reconstruct(self.engine.export(), self.engine.keys, self.engine.events[-1].hash)
        self.assertEqual(records[6]['payload']['result'], [5, 4])
        self.assertEqual(records[7]['payload']['execution'], 'NOT_EXECUTED')
        self.assertEqual(len(graph[self.engine.events[-1].hash]), 2)
        self.assertEqual(records[0]['payload']['initiator'], 'OPERATOR')
        self.assertEqual(records[1]['payload']['identity'], 'PENDING')
        self.assertEqual(records[3]['actor'], 'CONTRIBUTOR_1')

    def test_deterministic_bytes(self):
        self.assertEqual(self.engine.export(), demo()[0].export())

    def test_snapshots_cannot_mutate_history(self):
        before = self.engine.export()
        data = self.engine.events[0].data()
        data['payload']['initiator'] = 'OTHER'
        self.assertEqual(before, self.engine.export())

    def test_tamper_and_chain_attacks(self):
        lines = self.engine.export().splitlines()
        altered = json.loads(lines[1]); altered['body']['payload']['identity'] = 'VERIFIED'
        for raw in (b'\n'.join([lines[0], canonical(altered)] + lines[2:]),
                    b'\n'.join(lines[:-1]), b'\n'.join(lines[1:]),
                    b'\n'.join([lines[0], lines[2], lines[1]] + lines[3:]),
                    b'\n'.join(lines + [lines[-1]])):
            with self.subTest(raw=raw[:30]), self.assertRaises(ValueError):
                reconstruct(raw, self.engine.keys, self.engine.events[-1].hash)

    def test_wrong_key(self):
        keys = dict(self.engine.keys); keys['OPERATOR'] = b'X' * 32
        with self.assertRaises(ValueError):
            reconstruct(self.engine.export(), keys, self.engine.events[-1].hash)

    def test_scope_and_expiry(self):
        changed = copy.deepcopy(self.request); changed['inputs']['x'] = [2, 1]
        self.engine.execute('CONTRIBUTOR_1', changed, [self.engine.events[-1].hash], 9)
        self.assertEqual(self.engine.events[-1].data()['kind'], 'REJECTION')
        self.engine.execute('CONTRIBUTOR_1', self.request, [self.engine.events[-1].hash], 20)
        self.assertEqual(self.engine.events[-1].data()['kind'], 'REJECTION')

    def test_authorized_external_is_blocked(self):
        changed = copy.deepcopy(self.request); changed['destination'] = 'API_DEMO'
        self.engine.grant('CONTRIBUTOR_1', changed, 9, 20, 9)
        self.engine.execute('CONTRIBUTOR_1', changed, [self.engine.events[-1].hash], 10)
        self.assertIn('EXTERNAL_TRANSPORT_UNIMPLEMENTED', self.engine.events[-1].data()['payload']['reasons'])

    def test_invalid_exact_inputs(self):
        for pair in ([1, 0], [True, 1], [1.5, 2], [1]):
            with self.subTest(pair=pair):
                engine, request = demo(); request['inputs']['x'] = pair
                engine.grant('CONTRIBUTOR_1', request, 9, 20, 9)
                engine.execute('CONTRIBUTOR_1', request, [engine.events[-1].hash], 10)
                self.assertIn('INPUT_INVALID', engine.events[-1].data()['payload']['reasons'])

    def test_missing_or_duplicate_parents(self):
        for parents in (['missing'], [self.engine.events[0].hash] * 2, []):
            with self.subTest(parents=parents), self.assertRaises(ValueError):
                self.engine.append('OBSERVATION', 'OPERATOR', parents, {}, 9)

    def test_root_and_time_cannot_be_replaced(self):
        for kind, tick in (('ROOT', 9), ('OBSERVATION', 7)):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.engine.append(kind, 'OPERATOR', [self.engine.events[-1].hash], {}, tick)

    def test_identity_required(self):
        engine = Reference('PROCESS_ROOT', self.engine.keys)
        root = engine.append('ROOT', 'OPERATOR', [], {}, 0)
        actor, registration = engine.register([root], 1)
        with self.assertRaises(ValueError):
            engine.grant(actor, self.request, 2, 20, 2)
        engine.execute(actor, self.request, [registration], 2)
        self.assertIn('IDENTITY_PENDING', engine.events[-1].data()['payload']['reasons'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
