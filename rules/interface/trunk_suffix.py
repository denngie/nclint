# pylint: disable=missing-module-docstring
from nclint import Finding, BaseNCLintRule, Severity


class NCLintRule(BaseNCLintRule):
    """L2 trunk interfaces should have a description starting
    with [tr] to indicate that they are trunk interfaces."""

    id = "L2_trunk_suffix"
    severity = Severity.HINT
    description = "L2 trunk should have [tr] suffix"

    def valid_os(self) -> bool:
        return bool(self.parse.syntax == "ios")

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        interfaces = self.parse.find_parent_objects(
            r"^interface", r"^\s*(service instance|switchport mode trunk)"
        )

        for intf in interfaces:

            description = intf.re_match_iter_typed(r"description\s+(\S.*)")
            if description[0:4] != "[tr]":
                name = intf.text.split()[-1]

                findings.append(
                    Finding(
                        rule_id=self.id,
                        severity=self.severity,
                        message=f"L2 trunk without [tr] suffix on interface {name}",
                        line=intf.linenum,
                    )
                )

        interfaces = self.parse.find_parent_objects_wo_child(
            r"^interface", r"^\s*(service instance|switchport mode trunk)"
        )

        for intf in interfaces:

            description = intf.re_match_iter_typed(r"description\s+(\S.*)")
            if description and description[0:4] == "[tr]":
                name = intf.text.split()[-1]

                findings.append(
                    Finding(
                        rule_id=self.id,
                        severity=self.severity,
                        message=f"Non trunk with [tr] suffix on interface {name}",
                        line=intf.linenum,
                    )
                )

        return findings
