"""Main entry point for NCLint."""

from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from nclint import AnalyzerEngine, RuleRegistry
import rules


def run(config_file: str) -> None:
    """Run the analysis engine on the given configuration file."""
    parse = CiscoConfParse(config_file)
    registry = RuleRegistry(rules)
    engine = AnalyzerEngine(parse, registry.rules)
    findings = engine.run()
    for finding in findings:
        print(
            f"[{finding.severity.value}] {finding.message} ({finding.rule_id} [Ln {finding.line}])"
        )


if __name__ == "__main__":
    run("../config.txt")
