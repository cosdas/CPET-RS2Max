## Maximal oxygen uptake prediction from resting and submaximal CPET variables

This repository provides code and a reproducible training/inference pipeline to predict maximal oxygen uptake ($VO_{2\max}$) from resting and submaximal CardioPulmonary Exercise Testing (CPET) variables.

>Authors <br>
>Yonghun Lee<sup>1</sup>, Jeffrey Feng<sup>1</sup>, Al Rahrooh<sup>1</sup>, Alex A.T. Bui<sup>1</sup>, Christopher B. Cooper<sup>2</sup>, Jeffrey J. Hsu<sup>3</sup><sup>4</sup><sup>5</sup> <br>
>Affiliations <br>
><sup>1</sup> Medical & Imaging Informatics (MII) Group, Dept. of Radiological Sciences, UCLA <br>
><sup>2</sup> Exercise Physiology Research Laboratory, Division of Pulmonary & Critical Care Medicine, UCLA <br>
><sup>3</sup> Division of Cardiology, Dept. of Medicine, David Geffen School of Medicine at UCLA <br>
><sup>4</sup> Dept. of Bioengineering, University of California Los Angeles, Los Angeles, CA <br>
><sup>5</sup> Dept. of Medicine, VA Greater Los Angeles Health Care System, Los Angeles, CA <br>

## Overview

- Feature names and formats defined in `data/codebook.yml`
- Provides models trained for all combinations of:
    - Groups: NG (Normal Group), OG (Other Group), NG+OG (Combined Group)
	- Feature sets: Demographic, Demographic + Rest, Demographic + Rest + Submaximal, Demographic + Rest + Submaximal + CI
- Includes ready-to-use scripts for both training and inference

## Environment Setup

Use **[uv](https://github.com/astral-sh/uv)** to create a virtual environment or install the dependencies listed in `pyproject.toml`

If using uv:
```bash
uv sync
uv run aim init # For training tracking
```

## Training

Run:
```bash
python train.py 
```
- Uses `data/data.csv` as default input
- Reference `data/training_columns.csv` to organize and prepare the training dataset according to the required variables
- **Data availability**: The training data are not publicly available, as they are the property of the UCLA Exercise Physiology Laboratory
  
## Inference

Run:
```bash
python inference.py data={path_to_your_data.csv}
```
- Uses `data/sample.csv` as default input
- Select `Groups` and `Feature Sets` using following instructions
- Reference `data/codebook.yml` for feature names and formats
  - time: `0` for demographic variables, `1` for resting variables, `2` for submaximal variables
  - type: `numeric` for continuous variables, `categorical` for categorical variables
- Organize and prepare the inference dataset according to the required variables in `data/inference_columns.csv`
