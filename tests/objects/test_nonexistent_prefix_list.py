# pylint: disable=missing-module-docstring
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint.rules.objects.nonexistent_prefix_list import NCLintRule


def test_nonexistent_prefix_list() -> None:
    """Test that nonexistent prefix lists are identified."""
    lines = [
        "ip prefix-list PL1 seq 5 permit 192.168.1.0/24",
        "!",
        "router ospf 1",
        " distribute-list prefix PL1 in",
        "!",
        "route-map default-route permit 10",
        " match ip address prefix-list PL2",
        "!",
    ]
    cfg = CiscoConfParse(lines, syntax="ios")
    rule = NCLintRule(cfg)
    findings = rule.analyze()
    assert len(findings) == 1
    assert findings[0].rule_id == "NONEXISTENT_PREFIX_LIST"
    assert findings[0].severity == "error"
    assert findings[0].message == "Prefix-list PL2 applied but does not exist"
    assert findings[0].line == 6
