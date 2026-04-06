"""Main entry point for NCLint."""

from argparse import ArgumentParser
from json import dumps
import sys
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]
from src.nclint import AnalyzerEngine, RuleRegistry
from src.nclint import rules


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
    arg_parser.add_argument(
        "--json",
        help="Output findings in JSON format",
        action="store_true",
    )
    arg_parser.add_argument(
        "--exclude",
        help="List of rules to exclude from analysis",
        nargs="+",
        default=[],
    )
    arg_parser.add_argument(
        "--rule",
        help="List of rules to exclusively in analysis",
        nargs="+",
        default=[],
    )

    args = arg_parser.parse_args()
    try:
        parse = CiscoConfParse(args.config_file, syntax=args.os)
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config_file}' not found.")
        sys.exit(1)
    except (ValueError, UnicodeDecodeError) as e:
        print(f"Error parsing configuration file: {e}")
        sys.exit(1)

    registry = RuleRegistry(rules, exclude_list=args.exclude, include_list=args.rule)
    engine = AnalyzerEngine(parse, registry.rules)
    findings = engine.run()

    if args.json:
        print(dumps([f.__dict__ for f in findings], indent=2))
    else:
        for finding in findings:
            print(
                f"[{finding.severity.value}] {finding.message}"
                f" ({finding.rule_id} [Ln {finding.line}])"
            )

    has_errors = any(f.severity.value == "error" for f in findings)
    sys.exit(has_errors)


if __name__ == "__main__":
    main()
