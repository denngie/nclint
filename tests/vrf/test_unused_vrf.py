# pylint: disable=missing-module-docstring
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint.rules.vrf.unused_vrf import NCLintRule


def test_unused_vrf() -> None:
    """Test that unused VRFs are identified."""
    lines = [
        "vrf definition VRF1",
        "!",
        "vrf definition VRF2",
        "!",
        "interface Loopback0",
        " vrf forwarding VRF1",
        "!",
    ]
    cfg = CiscoConfParse(lines, syntax="ios")
    rule = NCLintRule(cfg)
    findings = rule.analyze()
    assert len(findings) == 1
    assert findings[0].rule_id == "UNUSED_VRF"
    assert findings[0].severity == "warning"
    assert findings[0].message == "VRF VRF2 defined but unused"
    assert findings[0].line == 2
