# library.qai.utilities

v2! A REST server and helper functions and classes for interacting with the rest of the Qordoba platform.

See GitHub history for 1.x docs.

## Upgrading to v2

Upgrading to v2 does require a few changes. Some noteable one:

* `get_config` will break. Sorry, you have to deal with that yourself
* `QConnect` is gone, and `QRest` is imported more explicitly
* There is no more `qai` Docker image. You are free to use whatever base image you want. May I recommend `qsam/spacy_alpine`.
* `qai` is now a pip dependency, so must be in your `requirements.txt`

However! There's help. Follow these steps:

```sh
cd qai_v1_service
vactivate  # or however you go into a virtualenv
pip uninstall -y qai
# uninstalls old qai
pip install qai
# installs qai from PyPi
python -m qai.upgrade .
# shows you how it would change your files to make the project ready for v2
# n to reject, y to accept
```

Now all that remains is seeing if you use `get_configs`, and if so: **pass `get_configs` an absolute path (v2), instead of a relative path split into a list (v1).**

Note: I went a bit fast, and long story short, versions 2.0.x and 2.1.x are not salvageable. Just use 2.2.0+.

## Things to know

See [The Changelog](CHANGELOG.md) for details.

### Required "conventions"

All projects *must* have a `config.json`, and that config *must* specify `SUPPORTED_LANGUAGES`, which is either a string or list of strings, of the form `"en"` or `["en", "de", "zh"]` (the prefix of the ISO code). QAI will not let your service start unless it thinks you have a valid `SUPPORTED_LANGUAGES` field. By default, QAI will look for this in `conf/config.json`. This is overridable. Here is the minimal config:

```json
{
  "SUPPORTED_LANGUAGES": "en"
}
```

You can specify the service name in the config file with

```json
{
  "SUPPORTED_LANGUAGES": "en",
  "SERVICE_NAME": "hey look at me service",
}
```

To change the config path to, for example, `./my_config_dir/a_sub_dir/my_wacky_config.json`:

```python
QRest(analyzer,
         category='service name, e.g. formality',
         white_lister=white_lister,
         config_path=['my_config_dir', 'a_sub_dir', 'my_wacky_config.json'])
```

## Usage

You can explicitly create a REST connection like this:

```python
from app import Analyzer, whitelist

from qai.qconnect.qrest import QRest


SERVICE_NAME = 'service_name'
host = '0.0.0.0'
port = 5000


if __name__ == '__main__':
    analyzer = Analyzer()
    rest_connection = QRest(analyzer,
                            category=category,
                            white_lister=white_lister,
                            host=host,
                            port=port)
    # create a blocking connection:
    rest_connection.connect()
```

The above will create *as many workers as you have cores.* This is great, _unless_ you are using AutoML. There is a known bug where AutoML crashes if you are using more than one worker.

So if you're using AutoML, the above would look like:

```python
from app import Analyzer, whitelist

from qai.qconnect.qrest import QRest


SERVICE_NAME = 'service_name'
host = '0.0.0.0'
port = 5000
workers = 1


if __name__ == '__main__':
    analyzer = Analyzer()
    rest_connection = QRest(analyzer,
                            category=category,
                            white_lister=white_lister,
                            host=host,
                            port=port,
                            workers=workers)
    # create a blocking connection:
    rest_connection.connect()
```

There is also a helper class for turning spaCy `Span`s into issues the rest of the platform can process:

```python
from spacy.tokens import Span
from app.factor import SpacyFactor


SOV = SpacyFactor(
    "subject_object_verb_spacing",
    "Keep the subject, verb, and object of a sentence close together to help the reader understand the sentence."
)

Span.set_extension("score", default=0)
Span.set_extension("suggestions", default=[])

doc = nlp("Holders of the Class A and Class B-1 certificates will be entitled to receive on each Payment Date, to the extent monies are available therefor (but not more than the Class A Certificate Balance or Class B-1 Certificate Balance then outstanding), a distribution.")
score = analyze(doc)
if score is not None:
    span = Span(doc, 0, len(doc))  # or whichever TOKENS are the issue (don't have to worry about character indexes)
    span._.score = score
    span._.suggestions = get_suggestions(doc)
    issues = SOV(span)
```

## Installation

pip?

## Testing

See Confluence for docs on input format expectations.

`scripts/test_qai.sh` has some helpful testing functions.

## Development

Source of truth is `VERSION` file, read by `setup.py` and `Jenkinsfile`. When you run `python setup.py sdist/bdist`, this creates `qai/version.py`, which is read in `qai/__init__.py`. This was done for reasons having to do with python's module system being frustrating. It allows one to not have to know the absolute path of a file at runtime, which is a big bonus in Python. Anyway, that means `VERSION` is the source of truth.

### License

This software is not licensed. If you do not work at Qordoba, you are not legally allowed to use it. Also, it's just helper functions that really won't help you. If something in it does look interesting, and you would like access, open an issue.
