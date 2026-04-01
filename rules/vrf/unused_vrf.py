# pylint: disable=missing-module-docstring
from nclint import Finding, BaseNCLintRule, Severity


class NCLintRule(BaseNCLintRule):
    """Rule to identify VRFs that are defined but not used in any interface."""

    id = "UNUSED_VRF"
    severity = Severity.WARNING
    description = "VRF defined but unused"

    def valid_os(self) -> bool:
        return bool(self.parse.syntax == "ios")

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        vrfs = self.parse.find_objects(r"^vrf definition")
        interfaces = self.parse.find_parent_objects_wo_child(
            r"^interface", r"^\s*shutdown"
        )
        used: set[str] = set()

        for intf in interfaces:

            vrf = intf.find_child_objects("vrf forwarding")

            if vrf:
                name = vrf[0].text.split()[-1]
                used.add(name)

        for vrf in vrfs:

            name = vrf.text.split()[-1]

            if name not in used:

                findings.append(
                    Finding(
                        rule_id=self.id,
                        severity=self.severity,
                        message=f"VRF {name} defined but unused",
                        line=vrf.linenum,
                    )
                )

        return findings
