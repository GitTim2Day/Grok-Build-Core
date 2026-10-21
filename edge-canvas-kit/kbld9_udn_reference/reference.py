"""Minimal simulated KBLD9/SVCT/UDN milestone; Python standard library only.
No network transport, biometrics, production key management, or frozen protocol edits.
"""
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import hmac
import json


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def digest(value):
    return sha256(canonical(value)).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Event:
    """Immutable canonical body: no mutable caller-owned references retained."""
    body: bytes
    hash: str
    mac: str

    def data(self):
        return json.loads(self.body)


class Reference:
    def __init__(self, process, keys):
        require(isinstance(process, str) and bool(process), 'invalid process')
        require(all(isinstance(k, bytes) and len(k) >= 32 for k in keys.values()), 'invalid demo key')
        require('OPERATOR' in keys, 'operator key absent')
        self.process, self.keys, self._events = process, dict(keys), []

    @property
    def events(self):
        return tuple(self._events)

    def append(self, kind, actor, parents, payload, tick):
        require(type(tick) is int and tick >= 0, 'invalid logical tick')
        require(not self._events or tick >= self._events[-1].data()['tick'], 'time reversed')
        require(actor in self.keys, 'credential absent')
        known = {e.hash for e in self._events}
        require(len(parents) == len(set(parents)), 'duplicate parent')
        require(all(p in known for p in parents), 'parent absent')
        if self._events:
            require(kind != 'ROOT', 'root replacement')
            require(bool(parents), 'parentless descendant')
        else:
            require(kind == 'ROOT' and actor == 'OPERATOR' and not parents, 'invalid root')
        data = dict(version=1, process=self.process, seq=len(self._events), kind=kind,
                    actor=actor, parents=sorted(parents), payload=payload, tick=tick,
                    previous=self._events[-1].hash if self._events else None)
        body = canonical(data)
        event = Event(body, sha256(body).hexdigest(), hmac.new(self.keys[actor], body, 'sha256').hexdigest())
        self._events.append(event)
        return event.hash

    def participant(self, actor):
        return next((e for e in self._events if e.data()['kind'] == 'PARTICIPANT'
                     and e.data()['payload']['participant'] == actor), None)

    def register(self, parents, tick):
        count = sum(e.data()['kind'] == 'PARTICIPANT' for e in self._events)
        actor = f'CONTRIBUTOR_{count + 1}'
        require(actor in self.keys, 'credential absent')
        return actor, self.append('PARTICIPANT', 'OPERATOR', parents,
                                 dict(participant=actor, identity='PENDING'), tick)

    def verify_identity(self, actor, identity_ref, tick):
        registration = self.participant(actor)
        require(registration is not None, 'unregistered participant')
        require(isinstance(identity_ref, str) and bool(identity_ref), 'empty identity')
        # Simulation only: production must verify independently enrolled evidence.
        return self.append('IDENTITY', actor, [registration.hash],
                           dict(participant=actor, identity_ref=identity_ref, method='SIMULATED'), tick)

    def identity(self, actor):
        return next((e for e in reversed(self._events) if e.data()['kind'] == 'IDENTITY'
                     and e.data()['actor'] == actor), None)

    def grant(self, actor, request, valid_from, valid_until, tick):
        identity = self.identity(actor)
        require(identity is not None, 'identity pending')
        require(type(valid_from) is int and type(valid_until) is int
                and valid_from <= tick < valid_until, 'invalid validity')
        return self.append('AUTHORIZATION', actor, [identity.hash],
                           dict(request_hash=digest(request), decision='ALLOW',
                                valid_from=valid_from, valid_until=valid_until), tick)

    def execute(self, actor, request, parents, tick):
        """UDN selects the explicit exact path; GOSUB invokes only the allowlisted routine."""
        require(self.participant(actor) is not None, 'unregistered participant')
        require(type(tick) is int and tick >= 0, 'invalid logical tick')
        identity = self.identity(actor)
        grant = next((e for e in reversed(self._events) if e.data()['kind'] == 'AUTHORIZATION'
                      and e.data()['actor'] == actor
                      and e.data()['payload']['request_hash'] == digest(request)
                      and e.data()['payload']['valid_from'] <= tick < e.data()['payload']['valid_until']), None)
        reasons = []
        if identity is None:
            reasons.append('IDENTITY_PENDING')
        if grant is None:
            reasons.append('AUTHORIZATION_ABSENT')
        # A stub intentionally blocks even authorized external requests.
        if request.get('destination') != 'LOCAL':
            reasons.append('EXTERNAL_TRANSPORT_UNIMPLEMENTED')
        if request.get('path') != 'EXACT' or request.get('operation') != 'POLYNOMIAL':
            reasons.append('ROUTINE_UNAVAILABLE')
        linked = list(parents) + ([grant.hash] if grant and grant.hash not in parents else [])
        if reasons:
            return self.append('REJECTION', actor, linked,
                               dict(request=request, execution='NOT_EXECUTED', reasons=reasons), tick)
        # KBLD9 boundary stub: strict exact pair validation, no coercion or floats.
        try:
            require(set(request) == {'operation_id', 'operation', 'path', 'destination', 'disclosure', 'inputs'}, 'request fields')
            require(isinstance(request['operation_id'], str) and bool(request['operation_id']), 'operation id')
            require(request['disclosure'] == [], 'local disclosure')
            inputs = request['inputs']
            require(set(inputs) == {'m', 'x', 'n', 'b'}, 'input fields')
            values = {}
            for name in ('m', 'x', 'b'):
                pair = inputs[name]
                require(isinstance(pair, list) and len(pair) == 2 and
                        all(type(v) is int for v in pair) and pair[1] != 0, 'invalid rational')
                values[name] = Fraction(*pair)
            n = inputs['n']
            require(type(n) is int and 0 <= n <= 64, 'exponent outside demo bound')
            result = values['m'] * values['x'] ** n + values['b']
            # Independent loop evaluation verifies the power calculation exactly.
            power = Fraction(1)
            for _ in range(n):
                power *= values['x']
            require(result == values['m'] * power + values['b'], 'verification failed')
        except (ValueError, TypeError, KeyError) as exc:
            return self.append('REJECTION', actor, linked,
                               dict(request=request, execution='NOT_EXECUTED', reasons=['INPUT_INVALID'], detail=str(exc)), tick)
        return self.append('RESULT', actor, linked,
                           dict(request=request, execution='EXECUTED', verified=True,
                                result=[result.numerator, result.denominator]), tick)

    def export(self):
        return b''.join(canonical(dict(body=e.data(), hash=e.hash, mac=e.mac)) + b'\n' for e in self._events)


def reconstruct(raw, keys, expected_tip):
    """Replay authenticated DAG and audit chain; trusted tip detects tail truncation.
    HMAC authenticates shared-key holders, not publicly verifiable signatures.
    This structural verifier does not replace policy validation during execution.
    """
    records, graph, previous, process, tick = [], {}, None, None, -1
    for seq, line in enumerate(raw.splitlines()):
        envelope = json.loads(line)
        require(set(envelope) == {'body', 'hash', 'mac'}, 'envelope fields')
        data = envelope['body']
        require(set(data) == {'version', 'process', 'seq', 'kind', 'actor', 'parents', 'payload', 'tick', 'previous'}, 'body fields')
        require(data['version'] == 1 and type(data['seq']) is int and data['seq'] == seq, 'sequence invalid')
        require(type(data['tick']) is int and data['tick'] >= tick, 'tick invalid')
        tick = data['tick']
        require(data['actor'] in keys, 'unknown credential')
        body = canonical(data)
        require(hmac.compare_digest(sha256(body).hexdigest(), envelope['hash']), 'hash invalid')
        require(hmac.compare_digest(hmac.new(keys[data['actor']], body, 'sha256').hexdigest(), envelope['mac']), 'credential invalid')
        require(data['previous'] == previous, 'chain invalid')
        parents = data['parents']
        require(isinstance(parents, list) and parents == sorted(set(parents)), 'parents invalid')
        require(all(p in graph for p in parents), 'parent absent or forward reference')
        if seq == 0:
            require(data['kind'] == 'ROOT' and data['actor'] == 'OPERATOR' and not parents, 'root invalid')
            process = data['process']
        else:
            require(data['kind'] != 'ROOT' and bool(parents), 'root replacement')
        require(data['process'] == process, 'cross process')
        require(envelope['hash'] not in graph, 'duplicate event')
        graph[envelope['hash']] = tuple(parents)
        records.append(data)
        previous = envelope['hash']
    require(bool(records) and previous == expected_tip, 'trusted tip mismatch')
    return records, graph


def demo():
    # Public deterministic test keys: NOT credentials suitable for deployment.
    keys = {a: sha256(('DEMO_ONLY/' + a).encode()).digest()
            for a in ('OPERATOR', 'CONTRIBUTOR_1', 'CONTRIBUTOR_2')}
    engine = Reference('PROCESS_ROOT', keys)
    root = engine.append('ROOT', 'OPERATOR', [], {'initiator': 'OPERATOR'}, 0)
    c1, p1 = engine.register([root], 1)
    c2, p2 = engine.register([root], 2)
    i1 = engine.verify_identity(c1, 'SIMULATED_ID_1', 3)
    i2 = engine.verify_identity(c2, 'SIMULATED_ID_2', 4)
    request = dict(operation_id='OP_1', operation='POLYNOMIAL', path='EXACT',
                   destination='LOCAL', disclosure=[], inputs=dict(m=[2, 3], x=[3, 2], n=2, b=[-1, 4]))
    engine.grant(c1, request, 5, 20, 5)
    result = engine.execute(c1, request, [i1], 6)
    rejected = engine.execute(c2, request, [i2], 7)
    engine.append('CONVERGENCE', 'OPERATOR', [result, rejected], {'operation_id': 'OP_1'}, 8)
    return engine, request


if __name__ == '__main__':
    import sys
    engine, _ = demo()
    reconstruct(engine.export(), engine.keys, engine.events[-1].hash)
    sys.stdout.buffer.write(engine.export())
