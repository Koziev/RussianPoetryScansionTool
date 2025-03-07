# Russian Poetry Scansion Tool

The **Russian Poetry Scansion Tool** (RPST) is a Python library designed for the analysis, evaluation, and labeling of Russian-language poetry. It provides tools for the following tasks:

- **Stress Placement**: Automatically places stresses in Russian poems and songs, adjusting for poetic meter. Detects the poetic meter of a given text.
- **Technicality Scoring**: Evaluates prosodic defects and calculates a *technicality* score, ranging from 0 (complete non-compliance with poetic constraints) to 1 (perfect compliance with a poetic meter).
- **Rhyme Detection**: Identifies rhymes, including slant (fuzzy) rhymes.

Please refer to our paper for more details: [Automated Evaluation of Meter and Rhyme in Russian Generative and Human-Authored Poetry](https://arxiv.org/abs/2502.20931).


### Usage notes

The model and dictionary files required for `RPST` exceed GitHub's LFS quota. These files are available in a compressed archive hosted on Google Drive.
[Download the archive](https://drive.google.com/file/d/1ofySC3c8EDTkx2GxDakw6gQJf_y0UUMA) and extract it into the root directory of the repository.

To see `RPST` in action, run the provided `usage_example.py` script.


### License

This project is licensed under the MIT License. For details, see the [LICENSE](./LICENSE) file.



### The RIFMA Dataset

The `RIFMA` dataset, used for evaluation, is available at [https://github.com/Koziev/Rifma](https://github.com/Koziev/Rifma).



## Citation

If you use this library in your research or projects, please cite it as follows:

```
@misc{koziev2025automatedevaluationmeterrhyme,
      title={Automated Evaluation of Meter and Rhyme in Russian Generative and Human-Authored Poetry},
      author={Ilya Koziev},
      year={2025},
      eprint={2502.20931},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.20931},
}
```

### Contacts

For questions, suggestions, or collaborations, feel free to reach out:

Email: [mentalcomputing@gmail.com]

GitHub Issues: [Open an issue](https://github.com/Koziev/RussianPoetryScansionTool/issues)
