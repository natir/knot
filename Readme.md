# KNOT

KNOT: for Knoledge Network Overlap exTraction is a tool to add information on long read assembly.

![Globale pipeline](images/pipeline.png)

Legend: 
- input `#2D882D`
- minimap2 `#AA3939`
- fpa `#AA7539`
- yacrd `#27556C`
- output `#5D2971`
- pipeline internal tool `#FFD300`

## Input

The tool takes as input long reads (corrected or not), assembly graph (in gfa1), and contigs (in fasta)

## Output

A AAG Augmented Assembly Graph describ in publication[^link to publication], AAG are represent as csv like that:
```
tig1 extremity, read of extremity of tig1, tig2 extremity, read of extremity of tig2, length of path between this extremity, number of read in path map against contigs 
```

## Instalation and Usage

### Instalation

#### Installation with conda

Recommended solution (2 command, 5 minutes)

```
wget https://gitlab.inria.fr/pmarijon/knot/raw/master/conda_env.yml
conda env create -f conda_env.yml
```

Activate environement :
```
source activate knot_env
```

Unactivate environement :
```
source deactivate knot_env
```

#### Installation without conda

Requirements:

- python >= 3.6
- snakemake >= 5.3
- [yacrd](https://github.com/natir/yacrd) avaible in bioconda or cargo >= 4.1
- [fpa](https://github.com/natir/fpa) avaible in bioconda or cargo >= 0.3

Instruction:

```
pip3 install git+https://gitlab.inria.fr/pmarijon/knot.git 
```

## Usage

We assume your :
- long reads are store in `raw_reads.fasta`
- contigs are store in `contigs.fasta`
- contgis graph are store in `contigs.gfa`

```
knot -i raw_reads.fasta -C contigs.fasta -g contigs.gfa -o {output prefix}
```

knot run a snakemake pipeline and produce `{output prefix}_AAG.csv` see [output section](#output) for more details, and a directory `{output prefix}_knot` where intermediate file are store.

You can use corrected long reads inplace of raw_reads with `-m` option.

Full command line usage:
```

```

Snakemake parameter can be used !

## Update

### Conda installation

The recommended way to update this tool is to remove the conda environement and reinstall it :

```
source deactivate knot_env
conda env remove -n knot_env
wget https://gitlab.inria.fr/pmarijon/knot/raw/master/conda_env.yml
conda env create -f conda_env.yml
```

### Non-conda installation

```
pip3 install --upgrade git+https://gitlab.inria.fr/pmarijon/knot.git
```

[^link to publication]: Not yet publish 
