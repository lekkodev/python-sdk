from dataclasses import dataclass
from typing import List, Optional

from google.protobuf.any_pb2 import Any as ProtoAny

from lekko_client.evaluation.rules import ClientContext, evaluate_rule
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Any as LekkoAny
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Constraint, Feature


@dataclass
class EvaluationResult:
    value: ProtoAny
    # Stores the path of the tree node that returned the final value
    # after successful evaluation.
    path: List[int]


@dataclass
class TraverseResult:
    value: Optional[ProtoAny]
    passes: bool
    path: List[int]


def evaluate(config: Feature, namespace: str, context: ClientContext = None) -> EvaluationResult:
    if not config.HasField("tree"):
        raise ValueError("config tree is empty")

    for i, constraint in enumerate(config.tree.constraints):
        child_result = traverse(constraint, namespace, config.key, context)
        if child_result.passes:
            if child_result.value:
                return EvaluationResult(value=child_result.value, path=[i, *child_result.path])
            break
    return EvaluationResult(value=_get_any(config.tree.default, config.tree.default_new), path=[])


def traverse(override: Constraint, namespace: str, config_name: str, context: ClientContext = None) -> TraverseResult:
    if not override:
        return TraverseResult(None, False, [])
    passes = evaluate_rule(override.rule_ast_new, namespace, config_name, context)
    if not passes:
        return TraverseResult(None, False, [])

    for i, constraint in enumerate(override.constraints):
        child_result = traverse(constraint, namespace, config_name, context)
        if child_result.passes:
            if child_result.value:
                return TraverseResult(child_result.value, True, [i, *child_result.path])
            break
    return TraverseResult(_get_any(override.value, override.value_new), True, [])


def _get_any(val: Optional[ProtoAny], val_new: Optional[LekkoAny]) -> ProtoAny:
    if val_new and val_new.type_url:
        return ProtoAny(type_url=val_new.type_url, value=val_new.value)
    if val:
        return val
    raise ValueError("config value not found")
