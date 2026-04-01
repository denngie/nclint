# pylint: disable=missing-module-docstring
from nclint import Finding, BaseNCLintRule, Severity


class NCLintRule(BaseNCLintRule):
    """Rule to identify prefix-lists that are defined but does not exist."""

    id = "NONEXISTANT_PREFIX_LIST"
    severity = Severity.ERROR
    description = "Prefix-list defined but does not exist"

    def valid_os(self) -> bool:
        return bool(self.parse.syntax == "ios")

    def analyze(self) -> list[Finding]:

        findings: list[Finding] = []

        used: set[str] = set()
        dl_used: set[str] = set()

        uses = self.parse.find_objects(r"^((?!ip).)*prefix-list.*$")
        for use in uses:
            name = use.re_match_typed(r"^((?!ip).)*prefix-list\s(\S+)", group=2)
            used.add(name)
        dl_uses = self.parse.find_objects(r"^\s*distribute-list prefix.*$")
        for use in dl_uses:
            name = use.re_match_typed(r"^\s*distribute-list prefix\s(\S+)", group=1)
            dl_used.add(name)

        prefix_lists = self.parse.find_objects(r"^ip prefix-list\s\S+")
        for prefix_list in prefix_lists:
            name = prefix_list.re_match_typed(r"^ip prefix-list\s(\S+)")
            if name in used:
                used.remove(name)
            elif name in dl_used:
                dl_used.remove(name)
            else:
                continue

        for prefix_list in used:
            use = self.parse.find_objects(rf"^((?!ip).)*prefix-list\s{prefix_list}.*$")
            findings.append(
                Finding(
                    rule_id=self.id,
                    severity=self.severity,
                    message=f"Prefix-list {prefix_list} applied but does not exist",
                    line=use[0].linenum,
                )
            )

        for prefix_list in dl_used:
            use = self.parse.find_objects(
                rf"^^\s*distribute-list prefix\s{prefix_list}.*$"
            )
            findings.append(
                Finding(
                    rule_id=self.id,
                    severity=self.severity,
                    message=f"Prefix-list {prefix_list} applied but does not exist",
                    line=use[0].linenum,
                )
            )

        return findings
