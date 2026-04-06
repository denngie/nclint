# pylint: disable=missing-module-docstring
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint.rules.private.rd_rt_invalid import NCLintRule


def test_rd_rt_invalid() -> None:
    """Test that VRFs with invalid RD or RT values are identified."""
    lines = [
        "vrf definition testvrf1",
        " rd 65170:1",
        " route-target export 65170:1",
        " route-target import 65170:1",
        " !",
        " address-family ipv4",
        " exit-address-family",
        " !",
        " address-family ipv6",
        " exit-address-family",
        "!",
        "vrf definition testvrf8",
        " rd 8:8",
        " route-target export 8:8",
        " route-target import 8:8",
        " !",
        " address-family ipv4",
        " exit-address-family",
        " !",
        " address-family ipv6",
        " exit-address-family",
        "!",
    ]
    cfg = CiscoConfParse(lines, syntax="ios")
    rule = NCLintRule(cfg)
    findings = rule.analyze()
    assert len(findings) == 1
    assert findings[0].rule_id == "RD_RT_INVALID"
    assert findings[0].severity == "error"
    assert findings[0].message == "VRF testvrf8 has an invalid RD or RT value: 8, 8, 8"
    assert findings[0].line == 11
