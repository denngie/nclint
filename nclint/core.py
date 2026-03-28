"""Core classes and logic for NCLint."""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType
from typing import Protocol, runtime_checkable
from ciscoconfparse2 import CiscoConfParse  # type: ignore[import-untyped]


class Severity(Enum):
    """Severity levels for findings."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


@dataclass
class Finding:
    """Represents a single finding from a rule analysis."""

    def __init__(self, rule_id: str, severity: Severity, message: str, line: int = 0):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line


class BaseNCLintRule(metaclass=ABCMeta):
    """Base class for all NCLint rules."""

    id: str
    severity: Severity
    description: str

    def __init__(  # type: ignore[no-any-unimported]
        self, parse: CiscoConfParse, id_: str, severity: Severity, description: str
    ):
        self.parse = parse
        self.id = id_
        self.severity = severity
        self.description = description

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not isinstance(cls.severity, Severity):
            raise AttributeError(
                f"Severity Enum class must be used, got {cls.severity!r}"
            )

    @abstractmethod
    def analyze(self) -> list[Finding]:
        """Analyze the configuration and return a list of findings."""


@runtime_checkable
class BaseNCLintRuleClass(Protocol):
    """Protocol describing the class-level interface of an BaseNCLintRule subclass."""

    id: str
    severity: Severity
    description: str

    def __call__(  # type: ignore[no-any-unimported]
        self,
        parse: CiscoConfParse,
        id_: str,
        severity: Severity,
        description: str,
    ) -> BaseNCLintRule: ...


class AnalyzerEngine:
    """Engine to run all registered rules against a given configuration."""

    def __init__(  # type: ignore[no-any-unimported]
        self, parse: CiscoConfParse, rules: list[BaseNCLintRuleClass]
    ):
        self.parse = parse
        self.rules = rules

    def run(self) -> list[Finding]:
        """Run all rules and collect findings."""
        findings: list[Finding] = []
        for rule_cls in self.rules:
            rule = rule_cls(
                self.parse, rule_cls.id, rule_cls.severity, rule_cls.description
            )
            try:
                results = rule.analyze()

                if results:
                    findings.extend(results)

            except ValueError as e:
                findings.append(Finding(rule_cls.id, Severity.ERROR, str(e)))

        return sorted(findings, key=lambda f: f.line)


class RuleRegistry:
    """Registry to discover and store all available rules."""

    def __init__(self, package: ModuleType):
        self.rules: list[BaseNCLintRuleClass] = []
        self._discover(package)

    def _discover(self, package: ModuleType) -> None:
        """Discover and import all rule modules in the given package."""
        for _, modname, _ in walk_packages(package.__path__, package.__name__ + "."):
            try:
                module = import_module(modname)
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, BaseNCLintRuleClass):
                        self.rules.append(obj)
                    elif isinstance(obj, ABCMeta) and obj.__name__ != "BaseNCLintRule":
                        raise ModuleNotFoundError(
                            f"{obj.__name__} does not conform to BaseNCLintRuleClass protocol."
                        )
            except (AttributeError, ModuleNotFoundError) as e:
                print(f"Error importing {modname}: {e}")
