dtool CLI commands for working with per item metadata
=====================================================

.. image:: https://badge.fury.io/py/dtool-overlay.svg
   :target: http://badge.fury.io/py/dtool-overlay
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtool-overlay.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtool-overlay
   :alt: Travis CI build status (Linux)

.. image:: https://codecov.io/github/jic-dtool/dtool-overlay/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtool-overlay?branch=master
   :alt: Code Coverage

Installation
------------

::

    pip install dtool-overlay

Example usage
-------------

Get a dataset to play with::

    LOCAL_DS_URI=$(dtool cp -q http://bit.ly/Ecoli-ref-genome .)

Show the existing overlays::

    $ dtool overlays show $LOCAL_DS_URI
    identifiers,relpaths
    23ebd7cd21a905d5f255919ca1d0491901cb8718,reference.4.bt2
    37e2d68bb38271036d96b6979d24666e0d4fd814,reference.rev.1.bt2
    41fb9ae5d4f6c37226ff324c701b84bc3110709e,reference.1.bt2
    828ebf503926b7c1b8b07c1995b4ca818814b404,reference.rev.2.bt2
    b445ff5a1e468ab48628a00a944cac2e007fb9bc,U00096.3.fasta
    d21454a7338c53eabc8d8ed7c2f9c3ff4585c4cf,reference.3.bt2
    dda8452b346d51b9cf60f0662ef3d6e3b6da2e74,reference.2.bt2

The output above show that there are no overlays on this dataset. (The
"identifiers" and "relpaths" columns are there for bookkeeping).

Create a "is_fasta" boolean overlay template by using a glob pattern::

    $ dtool overlays template glob $LOCAL_DS_URI is_fasta '*.fasta' > is_fasta.csv
    $ cat is_fasta.csv
    identifiers,is_fasta,relpaths
    23ebd7cd21a905d5f255919ca1d0491901cb8718,False,reference.4.bt2
    37e2d68bb38271036d96b6979d24666e0d4fd814,False,reference.rev.1.bt2
    41fb9ae5d4f6c37226ff324c701b84bc3110709e,False,reference.1.bt2
    828ebf503926b7c1b8b07c1995b4ca818814b404,False,reference.rev.2.bt2
    b445ff5a1e468ab48628a00a944cac2e007fb9bc,True,U00096.3.fasta
    d21454a7338c53eabc8d8ed7c2f9c3ff4585c4cf,False,reference.3.bt2
    dda8452b346d51b9cf60f0662ef3d6e3b6da2e74,False,reference.2.bt2

Write the overlay template to the dataset::

    $ dtool overlays write $LOCAL_DS_URI is_fasta.csv
    
Show the newly created overlay::

    $ dtool overlays show $LOCAL_DS_URI
    identifiers,is_fasta,relpaths
    23ebd7cd21a905d5f255919ca1d0491901cb8718,False,reference.4.bt2
    37e2d68bb38271036d96b6979d24666e0d4fd814,False,reference.rev.1.bt2
    41fb9ae5d4f6c37226ff324c701b84bc3110709e,False,reference.1.bt2
    828ebf503926b7c1b8b07c1995b4ca818814b404,False,reference.rev.2.bt2
    b445ff5a1e468ab48628a00a944cac2e007fb9bc,True,U00096.3.fasta
    d21454a7338c53eabc8d8ed7c2f9c3ff4585c4cf,False,reference.3.bt2
    dda8452b346d51b9cf60f0662ef3d6e3b6da2e74,False,reference.2.bt2

To extract multiple pieces of metadata from the items' relpath one can use the
``dtool overlays template parse`` command. This takes as input a dataset URI, a
parse rule (see https://pypi.org/project/parse/ for more details) and a glob
rule. The latter decides which relpaths to apply the parsing to.

Consider for example the dataset below::

    $ dtool ls http://bit.ly/Ecoli-reads-minified
    8bda245a8cd526673aab775f90206c8b67d196af  ERR022075_2.fastq.gz
    9760280dc6313d3bb598fa03c5931a7f037d7ffc  ERR022075_1.fastq.gz


The command below could be used to generate a template for the overlays
"useful_name" and "read"::

    $ dtool overlays template parse  \
        http://bit.ly/Ecoli-reads-minified  \
        '{useful_name}_{read:d}.fastq.gz'

Results in the CSV output below::

    identifiers,read,useful_name,relpaths
    8bda245a8cd526673aab775f90206c8b67d196af,2,ERR022075,ERR022075_2.fastq.gz
    9760280dc6313d3bb598fa03c5931a7f037d7ffc,1,ERR022075,ERR022075_1.fastq.gz

To ignore a variable element when parsing one can use unnamed curly braces. The
command below for example only generates the overlay "useful_name"::

    $ dtool overlays template parse  \
        http://bit.ly/Ecoli-reads-minified  \
        '{useful_name}_{:d}.fastq.gz'
    identifiers,useful_name,relpaths
    8bda245a8cd526673aab775f90206c8b67d196af,ERR022075,ERR022075_2.fastq.gz
    9760280dc6313d3bb598fa03c5931a7f037d7ffc,ERR022075,ERR022075_1.fastq.gz

 
Sometimes it is useful to be able to find pairs of items. For example when
dealing with genomic sequencing data that has forward and reverse reads.

One can create a "pair_id" overlay CSV template for this dataset using the
command below::

    $  dtool overlays template pairs http://bit.ly/Ecoli-reads-minified .fastq.gz
    identifiers,pair_id,relpaths
    8bda245a8cd526673aab775f90206c8b67d196af,9760280dc6313d3bb598fa03c5931a7f037d7ffc,ERR022075_2.fastq.gz
    9760280dc6313d3bb598fa03c5931a7f037d7ffc,8bda245a8cd526673aab775f90206c8b67d196af,ERR022075_1.fastq.gz

In the above the suffix ".fastq.gz" is used to extract the prefix ``ERR022075_``
that is used to find matching pairs.


Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-create <https://github.com/jic-dtool/dtool-create>`_
