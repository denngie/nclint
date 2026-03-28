# nclint
Network config linter library - dynamically imports rule via the RuleRegistry, AnalyzerEngine runs them and reports everything back as Findings. Heavily based on ciscoconfparse2 to do the config parsing.
```pip install -r requirements.txt```

### Overview

 * `main.py`: Run the analyzation on the given configuration file.
 * `nclint/core.py`: Main nclint library file containing all classes.
 * `rules/*`: Folder containing all the unique rules the configuration file will be checked against.

main.py demo usage output:
```bash
(.venv) denngie@ubuntu:~/nclint$ python3 main.py
[error] VRF testvrf1 has an invalid RD or RT value: 1, 1, 1 (RD/RT invalid [Ln 22])
[error] VRF testvrf4 has an invalid RD or RT value: 4, 4, 4 (RD/RT invalid [Ln 34])
[error] VRF testvrf7 has an invalid RD or RT value: 7, 7, 7 (RD/RT invalid [Ln 58])
[error] VRF testvrf8 has an invalid RD or RT value: 8, 8, 8 (RD/RT invalid [Ln 70])
[warning] VRF testvrf7 defined but unused (UNUSED_VRF [Ln 222])
[hint] L2 trunk without [tr] suffix on interface Port-channel11 (L2_trunk_suffix [Ln 394])
[hint] L3 link aggregation on interface Port-channel12, consider using ECMP instead (L3_LAG [Ln 410])
[hint] L2 trunk without [tr] suffix on interface Port-channel12 (L2_trunk_suffix [Ln 410])
[hint] Non trunk with [tr] suffix on interface TenGigabitEthernet0/0/4 (L2_trunk_suffix [Ln 458])
```
