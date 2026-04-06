# pylint: disable=missing-module-docstring
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint.rules.interface.l3_lag import NCLintRule


def test_l3_lag() -> None:
    """Test that L3 link aggregation is identified and a hint is provided to use ECMP instead."""
    lines = [
        "interface Port-channel1",
        " switchport mode trunk",
        "!",
        "interface Port-channel2",
        " ip address 198.18.0.0 255.255.255.254",
        "!",
    ]
    cfg = CiscoConfParse(lines, syntax="ios")
    rule = NCLintRule(cfg)
    findings = rule.analyze()
    assert len(findings) == 1
    assert findings[0].rule_id == "L3_LAG"
    assert findings[0].severity == "hint"
    assert (
        findings[0].message
        == "L3 link aggregation on interface Port-channel2, consider using ECMP instead"
    )
    assert findings[0].line == 3
