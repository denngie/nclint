# pylint: disable=missing-module-docstring
from nclint import Finding, BaseNCLintRule, Severity


class NCLintRule(BaseNCLintRule):
    """Rule to identify L3 link aggregation and suggest using ECMP instead."""

    id = "L3_LAG"
    severity = Severity.HINT
    description = "L3 link aggregation, consider using ECMP"

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        interfaces = self.parse.find_parent_objects(
            r"^interface Port-channel", r"^\s*ip address"
        )

        for intf in interfaces:

            name = intf.text.split()[-1]

            findings.append(
                Finding(
                    rule_id=self.id,
                    severity=self.severity,
                    message=f"L3 link aggregation on interface {name}, consider using ECMP instead",
                    line=intf.linenum,
                )
            )

        return findings
