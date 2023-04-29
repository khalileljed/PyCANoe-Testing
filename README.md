# Readme

The software side of the testing environment consists of three parts:

1. The "Restbussimulation" (Matching the SW-Version of the ECU, not part of this repository)
2. The main Testrunner-Framework (in this repository)
3. The actual Testcases (Multiple sets of testcases, maybe part of this repository - todo)

## Setup and execution of tests

- Module "pywin32" has to be installed
- Connect everything on testbench
- Make sure the right "Restbussimulation" is configured in the Testrunner
- Run the testcases via testrunner