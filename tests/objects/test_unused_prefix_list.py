# pylint: disable=missing-module-docstring
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint.rules.objects.unused_prefix_list import NCLintRule


def test_unused_prefix_list() -> None:
    """Test that unused prefix lists are identified."""
    lines = [
        "ip prefix-list PL1 seq 5 permit 192.168.1.0/24",
        "ip prefix-list PL2 seq 5 permit 192.168.2.0/24",
        "!",
        "router ospf 1",
        " distribute-list prefix PL1 in",
        "!",
    ]
    cfg = CiscoConfParse(lines, syntax="ios")
    rule = NCLintRule(cfg)
    findings = rule.analyze()
    assert len(findings) == 1
    assert findings[0].rule_id == "UNUSED_PREFIX_LIST"
    assert findings[0].severity == "warning"
    assert findings[0].message == "Prefix-list PL2 defined but unused"
    assert findings[0].line == 1
