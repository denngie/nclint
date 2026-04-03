"""Main entry point for NCLint."""

from argparse import ArgumentParser
from sys import exit as sys_exit
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from nclint import AnalyzerEngine, RuleRegistry
import rules


def main() -> None:
    """Main function to execute the NCLint analysis."""
    arg_parser = ArgumentParser(description="NCLint - Network Configuration Linter")
    arg_parser.add_argument(
        "config_file", help="Path to the network configuration file to analyze"
    )
    arg_parser.add_argument(
        "--os",
        help="Operating system of the network device (e.g., ios, junos, eos)",
        default="ios",
    )
    args = arg_parser.parse_args()

    try:
        parse = CiscoConfParse(args.config_file, syntax=args.os)
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config_file}' not found.")
        sys_exit(1)

    registry = RuleRegistry(rules)
    engine = AnalyzerEngine(parse, registry.rules)
    findings = engine.run()

    for finding in findings:
        print(
            f"[{finding.severity.value}] {finding.message} ({finding.rule_id} [Ln {finding.line}])"
        )

    has_errors = any(f.severity.value == "error" for f in findings)
    sys_exit(has_errors)


if __name__ == "__main__":
    main()
