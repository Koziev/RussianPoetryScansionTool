# Poetry Scansion Tool

This repo is an experimental fork of the publically available [Russian Poetry Scansion Tool](https://github.com/RussianNLP/RussianPoetryScansionTool). I will use this fork as a playground for testing experimental features and new approaches before merging them into the official project repository.

The **Russian Poetry Scansion Tool** (RPST) is a Python library designed for the analysis, evaluation, and labeling of Russian-language poetry. It provides tools for the following tasks:

- **Stress Placement**: Automatically places stresses in Russian poems and songs, adjusting for poetic meter.
- **Meter**: Detects the poetic meter of a given poem if possible.
- **Technicality Scoring**: Evaluates prosodic defects and calculates a *technicality* score, ranging from 0 (complete non-compliance with poetic constraints) to 1 (perfect compliance with a poetic meter).
- **Rhyme Detection**: Identifies rhymes, including slant (fuzzy) rhymes.

Please refer to my paper for more details: [Automated Evaluation of Meter and Rhyme in Russian Generative and Human-Authored Poetry](https://arxiv.org/abs/2502.20931).


### Installation

Run the following commands in console:

```bash
git clone https://github.com/Koziev/RussianPoetryScansionTool
cd RussianPoetryScansionTool
pip install .
```

The algorithm requires some models and pronunciation dictionary files. These files exceed my GitHub's LFS quota so
I made them available in a compressed archive hosted on Google Drive:
[Download the archive](https://drive.google.com/file/d/1ofySC3c8EDTkx2GxDakw6gQJf_y0UUMA) and extract it somewhere.
Then pass the path to extraction directory in `create_rpst_instance` function - see below.

To see `RPST` in action, install it and run the following code:

```python
import russian_scansion


tool = russian_scansion.create_rpst_instance('models/extraction/directory')

poem = """Вменяйте ж мне в вину, что я столь мал,
Чтоб за благодеянья Вам воздать,
Что к Вашей я любви не воззывал,
Чтоб узами прочней с собой связать,
Что часто тёмным помыслом я сам
Часы, Вам дорогие столь, дарил,
Что я вверялся часто парусам,
Чей ветр меня от Вас вдаль уносил.
Внесите в список Ваш: мой дикий нрав,
Ошибки, факты, подозрений ложь,
Но, полностью вину мою признав,
Возненавидя, не казните всё ж."""

scansion = tool.align(poem.split('\n'))

print('score={} meter={} scheme={}'.format(scansion.score, scansion.meter, scansion.rhyme_scheme))
print(scansion.get_stressed_lines(show_secondary_accentuation=True))
```


The output must be like this:

```
score=0.34583045610408747 meter=ямб scheme=None
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

The primary stress in a word is marked in the output using the `Combining Acute Accent` symbol with the code U+0301.
Secondary stresses, if detected and allowed to be output, are marked using the `Combining Grave Accent` symbol with the code U+0300:

```
Октя́брь багря́ным пла́менем пыла́ет,
Влюблё́нный в о́сень, угоди́ть ей ра́д,
Берё́зово - клено́вый лѝстопа́д
Ей по́д ноги смущё́нно расстила́ет,
```

### Technicality Scoring and its interpretation

The analysis outputs a **technicality score** (0 to 1) measuring how strictly the text follows Russian versification rules:

- **1.0**: Perfect meter adherence with clear rhymes
- **0.0**: No detectable meter or rhyme

Values between 0 and 1 indicate varying degrees of metrical irregularities, rhyme absence or different type of lexical defects.
Practical threshold:
  - >0.1: Likely syllabo-tonic verse
  - <0.1: Probable prose or non-metrical text

An example of perfect score (1.0):

```
Эо́ловой а́рфой вздыха́ет печа́ль
И зве́зд восковы́х зажига́ются све́чи
И да́льний зака́т, как перси́дская ша́ль,
Кото́рой оку́таны не́жные пле́чи.
```

This is a poem written in amphibrach meter with ABAB rhyme by Georgy Ivanov.

An example of poor poem (~0.00095):

```
Маленький мальчик компьютер купил
И к Интернету его подключил!
Не может никто понять и узреть -
Как же накрылась всемирная сеть!
```

The third line in this quatrain doesn't follow the dactylic meter, causing the overall score to fall below 0.1.


### Algorithm Features

#### Stanza Processing

The algorithm processes each stanza independently. This approach:  
1. Allows different stanzas to use distinct meter patterns  
2. May introduce inaccuracies in:  
  - Part-of-speech tagging (due to enjambment), resulting in homograph resolution mistakes  
  - Rhyme scheme detection (when rhyming lines span adjacent stanzas)  

#### Unstructured Text Handling

For long poems (7+ lines) without stanza breaks:  
1. The text is automatically split into 4-7 line segments  
2. Each segment is analyzed separately  

This segmentation reduces computational complexity but may:  
- Decrease part-of-speech tagging accuracy  
- Prevent correct rhyme detection between lines in different segments  

#### Single-Line Processing

The algorithm forces single lines into metrical patterns, sometimes at the cost of:  
- Unnatural stress placement  
- Stress dropping in certain words  

**Classification Challenges:**  
The system uses heuristics to distinguish between:  

1) Monostich (intentional one-line poem)

```Веде́м по жи́зни мы́ друг дру́га за́ нос```

2) Rhyming proverb

```Зе́ркало не винова́то, что ро́жа кривова́та.```

3)  Regular prose (shouldn't be forced into meter)

```Име́ть дли́нные во́лосы – э́то повсю́ду оставля́ть части́чку себя́.```

In some cases, the heuristics fails that leads to misclassification. The overall result of the markup in such cases may be incorrect.

### Markup Speed

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


### Citation

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
