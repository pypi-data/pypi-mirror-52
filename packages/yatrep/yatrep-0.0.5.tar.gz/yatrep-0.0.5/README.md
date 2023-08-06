# YATREP - Yes, Another Test REsult Parser

# Usage

## Preview
[![asciicast](https://asciinema.org/a/zDgV2cAkTvAZOv2mzwrdjPGqe.svg)](https://asciinema.org/a/2fzyDOoLDSMzkcG7rREccrNHt)

## Quick setup
Just pip install it!
```sh
pip3 install --user --upgrade yatrep
```

## Quick usage
You just need to run 'bin/run_parser.py' python file.
The only argument needed is the path to the xml file generated
by C# Nunit Tests.

```sh
python3 ./bin/run_parser.py xml_result_file.xml
```
If all your tests are healthy it returns a 0 (success) code.
Otherwise, it returns -1. Currently, we are relying on these
return codes to use the parser on our CI.


# Development

## Running tests
To run tests, you must have 'green' package installed. Also, we only
tested it with Python3.
```sh
$ green
>>>
>>> Captured stdout for test_yatrep.TestYatrep.test_fail_check
>>> Parsing file 'yatrep/test/test_data/dataset2.xml'

>>> Captured stdout for test_yatrep.TestYatrep.test_failed_test_should_be_detected
>>> Parsing file 'yatrep/test/test_data/dataset3.xml'

>>> Captured stdout for test_yatrep.TestYatrep.test_parse_xml_file
>>> Parsing file 'yatrep/test/test_data/dataset1.xml'

>>> Captured stdout for test_yatrep.TestYatrep.test_success_check
>>> Parsing file 'yatrep/test/test_data/dataset1.xml'

>>> Ran 4 tests in 0.130s using 16 processes

>>> OK (passes=4)
```
