# Decor
Decor framework for evaluating non-linear functions in Secure Multiparty Computation.

## Installation

**Note:** Decor runs only on Linux at the moment.

Install [Codon](https://github.com/exaloop/codon) first:
```bash
mkdir $HOME/.codon && curl -L https://github.com/exaloop/codon/releases/download/v0.17.0/codon-$(uname -s | awk '{print tolower($0)}')-$(uname -m).tar.gz | tar zxvf - -C $HOME/.codon --strip-components=1
```

Then install [Shechi/Sequre](https://github.com/0xTCG/sequre):
```bash
curl -L https://github.com/0xTCG/sequre/releases/download/v0.0.20-alpha/sequre-$(uname -s | awk '{print tolower($0)}')-$(uname -m).tar.gz | tar zxvf - -C $HOME/.codon/lib/codon/plugins
```

Apply necessary patches:
```bash
git clone -b decor-patch-64 --depth 1 https://github.com/0xTCG/sequre.git && cd sequre && \
cp -r stdlib/ $HOME/.codon/lib/codon/plugins/sequre/
```

Export necessary libraries to Shechi/Sequre (either custom or the one provided at `external/GMP/lib/libgmp.so`)
```bash
export SEQURE_GMP_PATH=external/GMP/lib/libgmp.so
```

Afterwards, add alias for `decor` command:
```bash
alias decor="find . -name 'sock.*' -exec rm {} \; && CODON_DEBUG=lt $HOME/.codon/bin/codon run --disable-opt="core-pythonic-list-addition-opt" -plugin sequre"
```

## Run

Navigate to the root of this directory and run all essential experiments by executing `tests.sequre`
```bash
decor -release tests.sequre --skip-mhe-setup --use-ring --local
```

Inspect the results by running all cells in provided `plots.ipynb` notebook.

## Troubleshooting

In some cases Codon may [fail to link Python library](https://docs.exaloop.io/integrations/python/python-from-codon/). Make sure to export `CODON_PATH` in that case to the location of your `libpython.so`. For example:
```bash
export CODON_PYTHON=$HOME/miniconda3/lib/libpython3.13.so
```
