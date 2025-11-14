# Decor
Decor framework for evaluating non-linear functions in Secure Multiparty Computation.

## Installation

**Note:** Decor runs only on Linux at the moment.

Install Decor by running a following set of commands:
```bash
mkdir -p $HOME/.codon && curl -L https://github.com/exaloop/codon/releases/download/v0.17.0/codon-$(uname -s | awk '{print tolower($0)}')-$(uname -m).tar.gz | tar zxvf - -C $HOME/.codon --strip-components=1 && \
curl -L https://github.com/0xTCG/sequre/releases/download/v0.0.20-alpha/sequre-$(uname -s | awk '{print tolower($0)}')-$(uname -m).tar.gz | tar zxvf - -C $HOME/.codon/lib/codon/plugins && \
git clone -b decor-patch-64 --depth 1 https://github.com/0xTCG/sequre.git .sequre && \
cp -r .sequre/stdlib/ $HOME/.codon/lib/codon/plugins/sequre/ && \
alias decor="find . -name 'sock.*' -exec rm {} \; && CODON_DEBUG=lt $HOME/.codon/bin/codon run --disable-opt="core-pythonic-list-addition-opt" -plugin $HOME/.codon/lib/codon/plugins/sequre"
```

And then export GMP library to Decor like so (either custom or the one provided at `external/GMP/lib/libgmp.so`)
```bash
export SEQURE_GMP_PATH=external/GMP/lib/libgmp.so
```

## Run

Navigate to the root of this directory and run all essential experiments by executing `tests.sequre`
```bash
decor -release tests.sequre --skip-mhe-setup --use-ring --local
```

Inspect the results by running all cells in provided `plots.ipynb` notebook.

## Troubleshooting

In some cases Decor might be unable to link a Python library. Make sure to export `CODON_PATH` in that case to the location of your `libpython.so`. For example:
```bash
export CODON_PYTHON=$HOME/miniconda3/lib/libpython3.13.so
```
