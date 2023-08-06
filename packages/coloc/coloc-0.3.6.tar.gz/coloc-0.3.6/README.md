# coloc

An implementation of the COLOC method for colocalization of GWAS and/or eQTL
signals by [Giambartolomei et al](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004383).

# Installation

```sh
pip3 install coloc
```
or
```sh
pip3 install --user coloc
```

# Example usage

```python
from coloc import coloc, print_coloc_result
help(coloc)
print_coloc_result('not colocalized', *coloc([1, 4, 9], [9, 4, 1]))
```
```
not colocalized

PP0: [|||||               ] [ 0.26540194014704316 ]
PP1: [||||                ] [ 0.21657860877712054 ]
PP2: [||||                ] [ 0.21657860877712054 ]
PP3: [|||                 ] [ 0.17661198683565493 ]
PP4: [||                  ] [ 0.12482885546306076 ]
```
```python
print_coloc_result('colocalized', *coloc([1, 4, 9], [1, 4, 9]))
```
```
colocalized

PP0: [                    ] [ 0.0015168270421050444 ]
PP1: [                    ] [ 0.001237791593959775 ]
PP2: [                    ] [ 0.001237791593959775 ]
PP3: [                    ] [ 1.4094001056824932e-05 ]
PP4: [||||||||||||||||||| ] [ 0.9959934957689188 ]
```