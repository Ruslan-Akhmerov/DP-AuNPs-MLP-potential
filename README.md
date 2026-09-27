# DP-AuNPs: Pre-Trained Machine-Learning Potential for Gold Nanoparticles

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data: CC-BY-4.0](https://img.shields.io/badge/Data-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A pre-trained Deep Potential interatomic potential for gold, covering bulk, surfaces, nanoparticles, and liquid phases. The potential is trained on DFT data (PBE) and is intended for large-scale atomistic simulations of gold nanostructures.

## Overview

This repository contains the trained DP-AuNPs potential, training/validation data, and example scripts for running molecular dynamics (MD) simulations with LAMMPS. The potential reproduces a wide range of properties: lattice parameter, cohesive energy, elastic constants, vacancy formation energy, melting temperature, surface energies, phonon dispersion, thermal expansion, and the relative stability of different nanoparticle morphologies.

The model is based on the Deep Potential Smooth Edition (DeepPot-SE) descriptor `se_e2_a`, which includes radial and angular information of the local atomic environment.

## Key Features

- **Near-DFT accuracy** for energies and forces on training and validation sets.
- **Transferable** across bulk, surfaces, nanoparticles, and liquid gold.
- **Ready-to-use** with LAMMPSand Python.
- **Open data**: all weights, training configurations, and validation scripts are provided.

## Repository Structure

```
DP-AuNPs/
├── README.md
├── LICENSE
├── LICENSE-DATA
├── CITATION.cff
├── requirements.txt
├── environment.yml
├── .gitignore
├── .gitattributes
│
├── potential/
│   ├── frozen_model.pb        # trained DeePMD model
│   ├── input.json             # training input parameters
│   ├── training_script.sh     # how the model was trained
│   └── checkpoints/           # (optional) training checkpoints
│
├── data/
│   ├── README.md              # dataset description
│   ├── training/              # training configurations
│   │   ├── bulk/
│   │   ├── surfaces/
│   │   ├── nanoparticles/
│   │   └── liquid/
│   ├── validation/            # validation configurations
│   └── raw_dft/               # (optional) raw VASP outputs
│
├── examples/
│   ├── lammps/
│   │   ├── in.lammps
│   │   ├── data.au
│   │   └── run.sh
│   ├── python/
│   │   ├── run_md.py
│   │   └── compute_properties.py
│   └── ase/
│       └── example_ase.py
│
├── scripts/
│   ├── train.py               # run training
│   ├── validate.py            # validate the potential
│   ├── plot_figures.py        # reproduce figures from the paper
│   └── utils.py
│
├── docs/
│   ├── methodology.md         # DFT and ML methods
│   ├── data_description.md    # dataset details
│   ├── validation.md          # validation results
│   └── images/
│
├── tests/
│   ├── test_potential.py
│   └── test_examples.py
│
└── .github/
    └── workflows/
        └── ci.yml
```

> **Note:** The structure above is a suggestion. Replace file names with your actual files.
