# [genice-rdf](https://github.com/vitroid/genice-rdf/)

A GenIce format plugin to calculate radial distribution functions.

version 0.3.1

## Requirements

* PairList>=0.2.3
* GenIce>=0.25

## Installation from PyPI

    % pip install genice_rdf

## Manual Installation

### System-wide installation

    % make install

### Private installation

Copy the files in formats/ into your local formats/ folder.

## Usage

    
    Usage: 
        % genice 1c -r 3 3 3 -w tip4p -f _RDF > 1c.rdf
        % genice 1c -r 3 3 3 -w tip4p -f _RDF[OW:H=HW1=HW2] > 1c.rdf
        % analice data.gro  -O OW -H HW[12] -w tip3p -f _RDF[OW:HW1=HW2] > data.rdf
    
    Options:
        Atom name
        Atom name and aliases chained with "=".
        json      Output in JSON format.
    
    Options must be separated with colons.
    
    You can specify the list of atom types to be calculated.
    
    For example, in the following case, TIP4P water has four different atom
    types (OW, HW1, HW2, and MW), so all the possible 10 combinations of 
    atom types will be examined.
    
        % genice 1c -r 3 3 3 -w tip4p -f _RDF > 1c.rdf
    
    If you just want the RDF of OW and H, and HW1 and HW2 should be 
    abbreviated by H, specify the option string like following.
    
        % genice 1c -r 3 3 3 -w tip4p -f _RDF[OW:H=HW1=HW2] > 1c.rdf

## Test in place

    % make test
