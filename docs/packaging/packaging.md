# Packaging CCmetagen for PyPi

Using `Python>=3.6`, `setuptool`, `twine` and `pip` to upload CCmetagen
releases to PyPi.

The examples run in the git root directory of `CCmetagen` and assume a
configured [`.pypirc`](https://packaging.python.org/specifications/pypirc/) for
the username and password. Otherwise, use the corresponding parameters for
`twine`

## Linux:

 CCmetagen.py and CCmetagen_merge.py should be installed in `${HOME}/.local/bin`:

`python ~/.local/bin/CCMetagen.py -h`


## Clean

- Remove old build files:

`find . \( -name build -o -name dist -o -name "*.egg*" \)  -type d -exec rm -rf {} +;`

## Bump version

- Adjust version in `ccmetagen/setup.cfg`
- Commit change

- Run:

    `$: python setup.py sdist bdist_wheel`

- Required files should be in `build/` and `dist/`

## Test upload and install

Upload to test.pypi and install

```
$: twine upload --repository-url https://test.pypi.org/legacy/ dist/*
$: python -m pip install --index-url https://test.pypi.org/simple/ --user -U ccmetagen
```

## Upload to PyPi for release and install

Upload to upload.pypi.org.

```
$: twine upload dist/*
```

### Note:

Do not run the install in the repository. I experienced pip assuming the
repo as proper install, for example:

```
$:~/projects/ccmetagen: python3.7 -m pip install --index-url https://test.pypi.org/simple/ ccmetagen
Looking in indexes: https://test.pypi.org/simple/
Requirement already satisfied: ccmetagen in /home/jan/projects/ccmetagen (1.1.4)
Collecting ete3 (from ccmetagen)
..cut..
```

```
$: twine upload dist/*
$: python -m pip install ccmetagen --user
```

