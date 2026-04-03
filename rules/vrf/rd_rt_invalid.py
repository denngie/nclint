# pylint: disable=missing-module-docstring
from nclint import Finding, BaseNCLintRule, Severity


class NCLintRule(BaseNCLintRule):
    """NCLint rule to check for invalid RD and RT values in VRF definitions."""

    id = "RD_RT_INVALID"
    severity = Severity.ERROR
    description = "VRF has an invalid RD or RT value"

    # Replace values below with the actual valid values for RD and RT as per your requirements
    valid_values = ["65167", "65170", "65200"]

    def valid_os(self) -> bool:
        return bool(self.parse.syntax == "ios")

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        vrfs = self.parse.find_objects(r"^vrf definition")

        for vrf in vrfs:

            name = vrf.text.split()[-1]
            values = vrf.re_list_iter_typed(
                r"(rd|route-target (ex|im)port)\s+(\S+):", group=3
            )

            if set(values).issubset(self.valid_values):
                continue

            findings.append(
                Finding(
                    rule_id=self.id,
                    severity=self.severity,
                    message=f"VRF {name} has an invalid RD or RT value: {', '.join(values)}",
                    line=vrf.linenum,
                )
            )

        return findings
