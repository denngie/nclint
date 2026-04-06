# pylint: disable=missing-module-docstring
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint.rules.private.trunk_suffix import NCLintRule


def test_trunk_suffix() -> None:
    """Test that interfaces with incorrect trunk suffixes are identified."""
    lines = [
        "interface TwentyFiveGigE1/0/1",
        " description [tr] Trunk interface",
        " switchport mode trunk",
        "!",
        "interface TwentyFiveGigE1/0/2",
        " description Trunk interface",
        " switchport mode trunk",
        "!",
        "interface TenGigabitEthernet0/0/5",
        " description [tr] Trunk interface",
        " ip address 198.18.0.0 255.255.255.254",
        "!",
        "interface TenGigabitEthernet0/0/6",
        " description [tr] Trunk interface",
        " service instance 1 ethernet",
        "  encapsulation dot1q 100",
        "  ip address",
        " !",
        "!",
    ]
    cfg = CiscoConfParse(lines, syntax="ios")
    rule = NCLintRule(cfg)
    findings = rule.analyze()
    assert len(findings) == 2
    assert findings[0].rule_id == "L2_TRUNK_SUFFIX"
    assert findings[0].severity == "hint"
    assert (
        findings[0].message
        == "L2 trunk without [tr] suffix on interface TwentyFiveGigE1/0/2"
    )
    assert findings[0].line == 4
    assert (
        findings[1].message
        == "Non trunk with [tr] suffix on interface TenGigabitEthernet0/0/5"
    )
    assert findings[1].line == 8
