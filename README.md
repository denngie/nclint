# nclint
Network config linter library - RuleRegistry dynamically imports rules, AnalyzerEngine runs them and reports everything back as Findings. Heavily based on ciscoconfparse2 to do the config parsing.

```pip install -r requirements.txt```

### Overview

 * `main.py`: Run the analyzation on the given configuration file.
 * `src/nclint/core.py`: Main nclint library file containing all classes.
 * `src/nclint/rules/*.py`: Folder containing all the unique rules the configuration file will be checked against.
 * `tests/*`: Folder containing all pytest files for the rules.

main.py demo usage output:
```bash
(.venv) denngie@ubuntu:~/nclint$ python3 main.py ../config.txt
[error] VRF testvrf1 has an invalid RD or RT value: 1, 1, 1 (RD/RT invalid [Ln 22])
[error] VRF testvrf4 has an invalid RD or RT value: 4, 4, 4 (RD/RT invalid [Ln 34])
[error] VRF testvrf7 has an invalid RD or RT value: 7, 7, 7 (RD/RT invalid [Ln 46])
[error] VRF testvrf8 has an invalid RD or RT value: 8, 8, 8 (RD/RT invalid [Ln 58])
[warning] VRF testvrf2 defined but unused (UNUSED_VRF [Ln 210])
[hint] L2 trunk without [tr] suffix on interface Port-channel11 (L2_trunk_suffix [Ln 381])
[hint] L3 link aggregation on interface Port-channel12, consider using ECMP instead (L3_LAG [Ln 397])
[hint] L2 trunk without [tr] suffix on interface Port-channel12 (L2_trunk_suffix [Ln 397])
[hint] Non trunk with [tr] suffix on interface TenGigabitEthernet0/0/4 (L2_trunk_suffix [Ln 445])
[error] Prefix-list default-route2 applied but does not exist (NONEXISTANT_PREFIX_LIST [Ln 1189])
[warning] Prefix-list vrf7-prefix_list defined but unused (UNUSED_PREFIX_LIST [Ln 1203])
[warning] Prefix-list vrf7-prefix_list defined but unused (UNUSED_PREFIX_LIST [Ln 1204])
[warning] Prefix-list area3-in defined but unused (UNUSED_PREFIX_LIST [Ln 1206])
[warning] Prefix-list area3-in defined but unused (UNUSED_PREFIX_LIST [Ln 1207])
[warning] Prefix-list area3-in defined but unused (UNUSED_PREFIX_LIST [Ln 1208])
[warning] Prefix-list area3-in defined but unused (UNUSED_PREFIX_LIST [Ln 1209])
[warning] Prefix-list deny_all defined but unused (UNUSED_PREFIX_LIST [Ln 1213])
[warning] Prefix-list uplinks defined but unused (UNUSED_PREFIX_LIST [Ln 1227])
```
