# nclint
Network config linter library - dynamically imports rule via the RuleRegistry, AnalyzerEngine runs them and reports everything back as Findings. Heavily based on ciscoconfparse2 to do the config parsing.
```pip install -r requirements.txt```

### Overview

 * `main.py`: Run the analyzation on the given configuration file.
 * `nclint/core.py`: Main nclint library file containing all classes.
 * `rules/*`: Folder containing all the unique rules the configuration file will be checked against.

main.py demo usage output:
```bash
(.venv) dennis@Dennis-PC:~/nclint$ python3 main.py
VRF_UNUSED [Severity.WARNING] - VRF testvrf15 defined but unused (line 46)
VRF_SINGLE_INTF [Severity.WARNING] - VRF Mgmt-intf only contains one single interface (line 82)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf1 only contains one single interface (line 90)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf10 only contains one single interface (line 102)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf11 only contains one single interface (line 114)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf12 only contains one single interface (line 126)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf13 only contains one single interface (line 138)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf14 only contains one single interface (line 150)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf2 only contains one single interface (line 162)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf3 only contains one single interface (line 174)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf4 only contains one single interface (line 186)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf5 only contains one single interface (line 198)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf6 only contains one single interface (line 210)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf8 only contains one single interface (line 231)
VRF_SINGLE_INTF [Severity.WARNING] - VRF testvrf_global only contains one single interface (line 243)
```
