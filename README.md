# Poetry Scansion Tool

This repo is an experimental fork of the publically available [Russian Poetry Scansion Tool](https://github.com/RussianNLP/RussianPoetryScansionTool). I will use this fork as a playground for testing experimental features and new approaches before merging them into the official project repository.

The **Russian Poetry Scansion Tool** (RPST) is a Python library designed for the analysis, evaluation, and labeling of Russian-language poetry. It provides tools for the following tasks:

- **Stress Placement**: Automatically places stresses in Russian poems and songs, adjusting for poetic meter.
- **Meter**: Detects the poetic meter of a given poem if possible.
- **Technicality Scoring**: Evaluates prosodic defects and calculates a *technicality* score, ranging from 0 (complete non-compliance with poetic constraints) to 1 (perfect compliance with a poetic meter).
- **Rhyme Detection**: Identifies rhymes, including slant (fuzzy) rhymes.

Please refer to my paper for more details: [Automated Evaluation of Meter and Rhyme in Russian Generative and Human-Authored Poetry](https://arxiv.org/abs/2502.20931).

### Usage notes

The stress prediction model and pronunciation dictionary files required for `RPST` exceed my GitHub's LFS quota. These files are available in a compressed archive hosted on Google Drive.
[Download the archive](https://drive.google.com/file/d/1ofySC3c8EDTkx2GxDakw6gQJf_y0UUMA) and extract it into the root directory of the repository.

To see `RPST` in action, run the provided `usage_example.py` script. The output must be as follows:

```
score=0.5403600876626367 meter=ямб scheme=None
Вменя́йте ж мне́ в вину́, что я́ столь ма́л,
Чтоб за благодея́нья Ва́м возда́ть,
Что к Ва́шей я́ любви́ не воззыва́л,
Чтоб у́зами прочне́й с собо́й связа́ть,
Что ча́сто тё́мным по́мыслом я са́м
Часы́, Вам дороги́е сто́ль, дари́л,
Что я́ вверя́лся ча́сто паруса́м,
Чей ве́тр меня́ от Ва́с вдаль уноси́л.
Внеси́те в спи́сок Ва́ш: мой ди́кий нра́в,
Оши́бки, фа́кты, подозре́ний ло́жь,
Но, по́лностью вину́ мою́ призна́в,
Возненави́дя, не казни́те всё́ ж.
```

The primary stress in a word is marked in the output using the `Combining Acute Accent` symbol with the code U+0301. Secondary stresses, if detected and allowed to be output, are marked using the `Combining Grave Accent` symbol with the code U+0300.

## Markup Speed

Performance benchmarks for the Russian Poetry Scansion Tool (measured on an Intel i7-9700K CPU @ 3.60GHz):

| Dataset       | Samples Processed | Sample Type       | Processing Time |
|---------------|-------------------|-------------------|-----------------|
| [Rifma](https://github.com/Koziev/Rifma)         | 3,647             | Mostly quatrains  | ~116 seconds    |

*Note: Processing times may vary depending on hardware configuration and poem complexity.*


### Accompanying Datasets

The `RIFMA` dataset, used for evaluation of stress placement and rhyme detection precision, is available at [https://github.com/Koziev/Rifma](https://github.com/Koziev/Rifma).

The `ArsPoetica` dataset, containing approximately 8.5k poems pre-processed by `PRST`, is avaibalbe at [https://huggingface.co/datasets/inkoziev/ArsPoetica](https://huggingface.co/datasets/inkoziev/ArsPoetica).

Both datasets are openly available for research purposes.

### Development History

This library originated as part of the [verslibre](https://github.com/Koziev/verslibre) project. The accentuation model and wrapper code were later separated and released as [accentuator](https://huggingface.co/inkoziev/accentuator) on Hugging Face. The `RPST` code eventually became available as a standalone library [here](https://github.com/RussianNLP/RussianPoetryScansionTool).

Future development plans include:
- Improving Russian poetry processing capabilities
- Adding support for other languages (starting with English)

### License

This project is licensed under the MIT License. For details, see the [LICENSE](./LICENSE) file.


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

GitHub Issues for bug in this fork: [Open an issue](https://github.com/Koziev/RussianPoetryScansionTool/issues)
