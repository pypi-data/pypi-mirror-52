# rfc2xml
Tool to process an RFC or Internet Standard into XML. Structure can also be accessed directly within a seperate Python project.

Note that this is not a general purpose tool and contains some restrictions. This is currently really slow. This is due partly to to overhead from Python, the parsing library and some inefficient parser grammar.

## Usage
```bash
python -m rfc2xml <filename> [--suppress-result]
```

## Examples
Download an Internet Standard to process:
```bash
wget https://www.ietf.org/id/draft-ietf-quic-transport-19.txt
```

The tool can then be run on that file using the following command (in the top level src directory):
```bash
python -m rfc2xml draft-ietf-quic-transport-19.txt
```

## Import
The tool can also be imported into a different python script and used there:

```python
from rfc2xml import Rfc2Xml
with open("draft-ietf-quic-transport-19.txt") as fp:
    contents = fp.read()
dom = Rfc2Xml.parse(contents)
```