"""VRF_SINGLE_INTF: VRF only contains one single interface"""

from nclint import Finding, NCLintRule, Severity


class VRFSingleIntfRule(NCLintRule):
    """VRF_SINGLE_INTF: VRF only contains one single interface"""

    id = "VRF_SINGLE_INTF"
    severity = Severity.WARNING
    description = "VRF only contains one single interface"

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        vrfs = self.parse.find_objects("^vrf definition")
        interfaces = self.parse.find_parent_objects_wo_child(
            r"^interface", r"^ shutdown"
        )

        used: list[str] = list()

        for intf in interfaces:

            vrf = intf.find_child_objects("vrf forwarding")

            if vrf:
                name = vrf[0].text.split()[-1]
                used.append(name)

        for vrf in vrfs:

            name = vrf.text.split()[-1]
            count = used.count(name)
            if count == 1:

                findings.append(
                    Finding(
                        rule_id=self.id,
                        severity=self.severity,
                        message=f"VRF {name} only contains one single interface",
                        line=vrf.linenum,
                    )
                )

        return findings
