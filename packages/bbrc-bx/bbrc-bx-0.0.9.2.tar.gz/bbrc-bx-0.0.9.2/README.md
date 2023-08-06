# bx

[![pipeline status](https://gitlab.com/xgrg/bx/badges/master/pipeline.svg)](https://gitlab.com/xgrg/bx/commits/master)
[![coverage report](https://gitlab.com/xgrg/bx/badges/master/coverage.svg)](https://gitlab.com/xgrg/bx/commits/master)
[![downloads](https://img.shields.io/pypi/dm/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)
[![python versions](https://img.shields.io/pypi/pyversions/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)
[![pypi version](https://img.shields.io/pypi/v/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)

BarcelonaBeta + XNAT = BX


## Usage

```
bx <command> <subcommand> <resource_id> --config /path/to/.xnat.cfg --dest /tmp [--overwrite]
```

### Examples:

```
bx spm12 volumes <resource_id>
```

```
bx spm12 files <resource_id>
```

```
bx spm12 report <resource_id>
```

```
bx spm12 tests <resource_id>
```

```
bx freesurfer6 aseg <resource_id>
```

```
bx freesurfer6 aparc <resource_id>
```

```
bx freesurfer6 hippoSfVolumes <resource_id>
```

```
bx freesurfer6 files <resource_id>
```

```
bx mrdates <resource_id>
```

## Dependencies

Requires the `bbrc` branch of [`pyxnat`](https://gitlab.com/xgrg/pyxnat).


## Install

```
pip install bbrc-bx
```

## Development

Please contact us for details on how to contribute.

[![BarcelonaBeta](https://www.barcelonabeta.org/sites/default/files/logo-barcelona-beta_0.png)](https://www.barcelonabeta.org/)
