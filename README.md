# Poetry Scansion Tool

This repo is an experimental fork of the publically available [Russian Poetry Scansion Tool](https://github.com/RussianNLP/RussianPoetryScansionTool). I will use this fork as a playground for testing experimental features and new approaches before merging them into the official project repository.

The **Russian Poetry Scansion Tool** (RPST) is a Python library designed for the analysis, evaluation, and labeling of Russian-language poetry. It provides tools for the following tasks:

- **Stress Placement**: Automatically places stresses in Russian poems and songs, adjusting for poetic meter.
- **Meter**: Detects the poetic meter of a given poem if possible.
- **Technicality Scoring**: Evaluates prosodic defects and calculates a *technicality* score, ranging from 0 (complete non-compliance with poetic constraints) to 1 (perfect compliance with a poetic meter).
- **Rhyme Detection**: Identifies rhymes, including slant (fuzzy) rhymes.

Please refer to the following paper for more details: [Automated Evaluation of Meter and Rhyme in Russian Generative and Human-Authored Poetry](https://arxiv.org/abs/2502.20931).

We used this library to evaluate the generated poem in our research paper [Generation of Russian Poetry of Different Genres and Styles Using Neural Networks with Character-Level Tokenization](https://aclanthology.org/2025.latechclfl-1.6.pdf).


### Installation

Run the following commands in console:

```bash
git clone https://github.com/Koziev/RussianPoetryScansionTool
cd RussianPoetryScansionTool
pip install .
```

The algorithm requires some models and pronunciation dictionary files.
These files exceed my GitHub's LFS quota so I made them available in a compressed archive hosted on Google Drive:
[Download the archive](https://drive.google.com/file/d/1ofySC3c8EDTkx2GxDakw6gQJf_y0UUMA) and extract it somewhere.
Then pass the path to extraction directory in `create_rpst_instance` function - see below.


### Usage

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
  - > 0.1: Likely syllabo-tonic verse
  - < 0.1: Probable prose or non-metrical text

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


#### Compound Words

Russian frequently uses compound words in poetry (especially in certain genres).
The RPST accounts for these by detecting such words, analyzing both roots and adjusting stress placement accordingly.

How it works:

1. **Stress Allocation**:

   - The algorithm detects both roots in a compound word.
   - Places a *secondary stress* on the first root.
   - Places the *primary stress* on the second root.

2. **Example**:

   In the word **"гро̀зогро́м"** (from the words *"гроза́"* + *"гром"*):
   - The primary stress falls on the second root (`гро́м`).
   - The secondary stress shifts to the first syllable (`гро̀з`) in *"гроза́"* because the original stress in *"гроза́"* (on the ending `-а́`) is truncated in the compound form.

**Illustration**:

```
Августо́вый гро̀зогро́м
Расшуме́лся среди но́чки,
И веде́рко за ведро́м
Ли́лось из небе́сной бо́чки.
```

The secondary stress on the first root of the compound word can be completely
suppressed as a result of adjustment to the meter, as for example in the following stanza
on the word "о̀гнетво́рчество":

```
Расчища́я простра́нство Земли́,
Огнетво́рчество Ду́х закали́т
И во Бла́го Небе́сной Зари́,
Краски Све́та повсю́ду внедри́т!
```

#### Verb derivation


Another frequent source of nonce words in Russian poems and songs is the prefix derivation of verbs.
For example, the verb "оттрепещу́" in the stanza below is formed using the prefix "от-" and
the imperfective verb "трепещу́". Applying this method of word formation, the RPST algorithm always preserves
the stress on the original verb form.

```
Я все́ми кра́сками оси́ны
Оттрепещу́ и облечу́,
Трево́жным кри́ком журавли́ным
Тебе́ проща́нье прокричу́.
```


#### Rhyme scheme representation

When using the rhyme scheme derived from the analysis of poems, the following features should be taken into account.

1) Stanzas are analyzed independently, so the same letter in the rhyme schemes for different stanzas can be repeated, while the corresponding lines in the stanzas are not connected by rhyme.

The following poem has rhyme scheme `-A-A -A-A -A-A`:

```
А еще́ хочу́ найти́ я
Ме́л. Цвето́чки рисова́ть.
Потому́ что в "ма̀ртоми́ре"
И́х под сне́гом не сыска́ть.

И в моско́вской подворо́тне,
Где́ поку́да ка́мер не́т,
Разукра́сить "стѐного́род"
В мо́й люби́мый же́лтый цве́т.

Бѐнзора́дугу на лу́же
Допроси́ть. Ты ту́т на ко́й?
- Что́б, отве́тит, в "ма̀ртоми́ре"
Бы́ть прекра́сной чепухо́й!
```

2) Usually, a line that does not rhyme with another line is designated by the symbol "-".
An exception is the `AABA` scheme, typical for quatrains in the ruba'i genre:

```
Сизой ды́мкой подё́рнулся со́лнца захо́д,
Он проро́чит нам все́м неизбе́жный ухо́д.
Проведё́м же в поко́е оста́вшийся сро́к наш,
Каждый де́нь, как после́дний, живя́ без забо́т.
```


### Genres and forms

Below are examples of different genres and forms of Russian poetry processed by `RPST`.


**две девятки**

A couplet written in iambic meter, with two lines of 9 syllables each and a rhyme scheme of AA.

```
во мне́ нашли́ поро́чный ге́н но
мне с ни́м легко́ и офиге́нно
```

```
зря к ку́клам ру́ки распростё́р ты
их ли́ца ту́склы кра́ски стё́рты
```


**порошки**

A quatrain written in iambic meter, with a rhyme scheme of *-A-A* and syllable counts of 9-8-9-2 per line.
These poems are always written without capital letters, without punctuation marks, often with deliberate deviations from spelling norms.

```
кафе́ францу́зское закры́лось
в беспе́чном га́рлеме вчера́
фуа́ там ча́сто подава́ли
не гра́
```


**пирожки**

A quatrain written in iambic meter without rhymes; the syllable counts per line are 9-8-9-8.
Like a ***порошки***, these poems are written without capital letters, without punctuation marks, often with deliberate deviations from spelling norms.

```
я ва́м жела́ю что́ б не зна́ли
вы бе́д печа́ли и тоски́
и что́б меня́ совсе́м забы́ли
и то́ что де́нег до́лжен ва́м
```


**депрессяшки**

A quatrain written in trochee meter with -A-A rhyme scheme; the syllable counts per line are 6-5-6-5.
For this hard form, the same comments about spelling, punctuation and text formatting apply as for the genres ***пирожки*** and ***порошки***.

```
ма́нит заграни́ца
и ещё́ крова́ть
во́т бы пря́м с крова́тью
иммигри́ровать
```


**артишоки**

A quatrain is written in amphibrach with ABAB rhyme scheme, 9-8-9-2 syllables per line.
Rules for spelling, punctuation and text formatting are the same as for ***пирожки*** and ***порошки***.

```
усво́ив что и́стина та́м где вино́
и пы́шные же́нщины в бро́ском
оле́г продолжа́ет иска́ть всё равно́
в бро́дском
```


... ***To be continued*** ...




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


### Where it is used

We used this library to evaluate the generated poem in our research paper [Generation of Russian Poetry of Different Genres and Styles Using Neural
Networks with Character-Level Tokenization](https://aclanthology.org/2025.latechclfl-1.6.pdf).


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
