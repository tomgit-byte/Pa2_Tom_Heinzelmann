# Trajectory-Level Metrics for Detecting Failure Modes in Multi-Agent AI Systems: An Empirical Evaluation

Companion repository to the project work (PA2) by Tom Heinzelmann (DHBW, course WWI2024, 2026).

It holds the Jupyter notebooks whose results the thesis reports and every file the thesis cites by path. Nothing else from the working repositories is included.

## The study in brief

The thesis tests lexical and structural trajectory metrics for two inter-agent failure modes of the MAST taxonomy: the failure to ask for clarification (code 2.2) and task derailment (code 2.3). The first experiment is pre-registered and uses 1,642 execution traces from seven frameworks. Directions, column sets and the test family were fixed on a discovery half (ChatDev, AG2) before the sealed test half (MetaGPT, Magentic One) was opened for the confirmation. The second experiment evaluates generalised deterministic and judge-based detectors on the AG2 traces.

## Repository layout

The results come from two implementations of the analysis. Each keeps its own folder:

```text
.
├── Framework_Traces/experiment/        experiment pipeline: pre-registered confirmation
│   ├── notebooks/02_confirmation.ipynb
│   └── data/sealed/UNSEAL_LOG.txt      provenance log of the sealed test table (Appendix 2/1)
└── mad_pipeline_refactor/              notebook pipeline: all other results
    ├── notebooks/                      the ten notebooks listed below
    ├── results/<notebook>/             cited tables, figures, result files and run manifests
    ├── tools/pipeline_src/             prereg.py and honest_signals.py
    └── data/
        ├── frozen/                     metrics_discovery.parquet
        └── sealed/                     unseal logs of the notebook pipeline (Appendix 2/2)
```

## Finding a file cited in the thesis

- Paths that begin with `Framework_Traces/experiment/` or `mad_pipeline_refactor/` start at the root of this repository.
- All other paths (`results/...`, `tools/...`, `data/...`) are relative to `mad_pipeline_refactor/`. For example, `results/01_discovery/01_discovery_refits.csv` is at `mad_pipeline_refactor/results/01_discovery/01_discovery_refits.csv`.
- Where the thesis writes `<notebook>` or `<model>`, insert a notebook name from the table below, or `Claude` or `GPT-4o`.

File and folder names are kept exactly as the thesis cites them.

## Notebooks used in the thesis

| Notebook | Corpus | Traces | Run (UTC) | Used in |
|---|---|--:|---|---|
| `02_confirmation` (experiment pipeline) | MetaGPT, Magentic One | 625 | 2026-09-20 | Sections 4.3, 4.4; Appendix 3 |
| `01_discovery` | ChatDev, AG2 | 927 | 2026-10-07 | Section 4.2; Appendix 3 |
| `05_honest_signals` | all frameworks | 1,642 | 2026-10-07 | Section 3.3; Appendix 5 |
| `07_network_centrality` | all frameworks | 1,642 | 2026-10-07 | Section 3.3; Appendix 5 |
| `MAST_2_5_Metrik` | all frameworks | 1,642 | 2026-10-07 | Appendix 4/1 (exploratory code 2.5) |
| `analysis_2_2_clarification_AG2_Claude` | AG2, Claude | 193 | 2026-10-07 | Section 5.2; Appendix 4/2 |
| `analysis_2_2_clarification_AG2_GPT-4o` | AG2, GPT-4o | 236 | 2026-10-07 | Section 5.2; Appendix 4/2 |
| `analysis_2_3_task_derailment_AG2_Claude` | AG2, Claude | 193 | 2026-10-07 | Section 5.2; Appendix 4/3 |
| `analysis_2_3_task_derailment_AG2_GPT-4o` | AG2, GPT-4o | 236 | 2026-10-07 | Section 5.2; Appendix 4/3 |
| `analysis_cgd` | AG2 training half | 478 | 2026-10-07 | Section 5.3; Appendix 4/4 |
| `analsis2` | AG2 training half | 478 | 2026-10-07 | Section 5.3; Appendix 4/4 |

`02_confirmation` is in `Framework_Traces/experiment/notebooks/`, all others are in `mad_pipeline_refactor/notebooks/`. `Claude` and `GPT-4o` in a name denote the language model that produced the AG2 traces of that subset. Appendix 1 of the thesis (Artefact inventory) lists the same notebooks.

Every notebook of the notebook pipeline is self-contained. It carries the generated pipeline code inline and writes its tables, a JSON result file, its figures and a `manifest.json` (timestamps, seed, library versions) to `results/<notebook>/`. This repository keeps only the files the thesis cites.

## Software environment

All runs of the notebook pipeline used the random seed 42 and these versions (thesis, Appendix 1):

| Library | Version | Library | Version |
|---|---|---|---|
| Python | 3.14.6 | statsmodels | 0.15.0 |
| NumPy | 2.5.2 | NetworkX | 3.6.1 |
| pandas | 3.0.5 | Matplotlib | 3.11.1 |
| SciPy | 1.18.1 | seaborn | 0.13.2 |
| scikit-learn | 1.9.0 | | |

## Re-running the notebooks

The notebooks are stored with their outputs, so all results can be read without running anything. Re-running them needs input data that is not part of this repository. Depending on the notebook, that is:

- the cleaned corpus file `MAD_full_dataset(2)_cleaned.json` (about 190 MB), prepared from the trace corpus published by Cemri et al. (2025), *Why Do Multi-Agent LLM Systems Fail?*;
- the AG2 split files `train_80.json` and `test_20.json`;
- for `analysis_cgd` and `analsis2`, the stored judge verdicts in `data/judge_cache/`. With these, no inference key is needed.

A notebook takes as project root the first directory, from the working directory upwards, that contains both `data/` and `notebooks/`. Start Jupyter in `mad_pipeline_refactor/notebooks/`. Data files are read from `mad_pipeline_refactor/data/` or, if they are not there, from the directory given in the environment variable `MAD_DATA_DIR`.

`02_confirmation` is included for its stored outputs from the run of 2026-09-20. It imports the `src` package of the experiment pipeline and reads the sealed test table. Neither is part of this repository.
