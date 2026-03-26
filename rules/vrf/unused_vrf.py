"""Rule to identify VRFs that are defined but not used in any interface."""

from nclint import Finding, NCLintRule, Severity


class UnusedVRFRule(NCLintRule):
    """Rule to identify VRFs that are defined but not used in any interface."""

    id = "VRF_UNUSED"
    severity = Severity.WARNING
    description = "VRF defined but unused"

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        vrfs = self.parse.find_objects(r"^vrf definition")
        interfaces = self.parse.find_objects(r"^interface")

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
