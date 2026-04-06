# pylint: disable=missing-module-docstring
from src.nclint import Finding, BaseNCLintRule, Severity


class NCLintRule(BaseNCLintRule):
    """Rule to identify prefix-lists that are defined but not used."""

    id = "UNUSED_PREFIX_LIST"
    severity = Severity.WARNING
    description = "Prefix-list defined but unused"

    def valid_os(self) -> bool:
        return bool(self.parse.syntax == "ios")

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        used: set[str] = set()

        uses = self.parse.find_objects(r"^((?!ip).)*prefix-list.*$")
        for use in uses:
            name = use.re_match_typed(r"^((?!ip).)*prefix-list\s(\S+)", group=2)
            used.add(name)

        dl_uses = self.parse.find_objects(r"^\s*distribute-list prefix.*$")
        for use in dl_uses:
            name = use.re_match_typed(r"^\s*distribute-list prefix\s(\S+)", group=1)
            used.add(name)

        prefix_lists = self.parse.find_objects(r"^ip prefix-list\s\S+")
        for prefix_list in prefix_lists:
            name = prefix_list.re_match_typed(r"^ip prefix-list\s(\S+)")
            if name in used:
                continue

            # Add prefix-list as used to avoid duplicate findings for the same prefix-list
            used.add(name)

            findings.append(
                Finding(
                    rule_id=self.id,
                    severity=self.severity,
                    message=f"Prefix-list {name} defined but unused",
                    line=prefix_list.linenum,
                )
            )

        return findings
