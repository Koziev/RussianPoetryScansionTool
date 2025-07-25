"""
Нормализация пробелов в сгенерированных стихах.

Так как в генеративках используется особая силлабо-тоническая токенизация, мы в сгенерированном тексте теряем информацию
о том, чем является символ "-": соединителем в многословных элементах типа "кто-либо" или синтаксическим заменителем глагола-связки.

Поэтому приходится использовать словарный lookup для тех строк, про которые мы точно знаем, что там не нужны пробелы вокруг дефиса.
"""

import re


rx2_entries = []

def normalize_whitespaces(s):
    global rx2_entries
    s = s.replace('\u200c', ' ')

    # Уберем пробелы перед некоторыми знаками пунктуации
    for c in ',.?!…;:':
        s = s.replace(' ' + c, c)

    # Уберем ненужные пробелы у лапок
    s = s.replace('« ', '«').replace(' »', '»')

    # Уберем ненужные пробелы у кавычек “ и ”
    s = s.replace('“ ', '“').replace(' ”', '”')

    # Если есть 2 кавычки, то убираем пробел ПОСЛЕ первой и ПЕРЕД второй:
    # И тишина " звучит " со старенькой пластинки,
    n_quotes = s.count('"')
    if n_quotes == 2:
        s = re.sub(r'" (.+) "', r'"\1"', s, flags=re.DOTALL)
    elif n_quotes > 0:
        s = re.sub(r'" ([^\n]+) "', r'"\1"', s)

    # Нормализация пробелов около круглых скобочек.
    s = re.sub(r'\(\s+([\w0-9])', r'(\1', s)
    #s = re.sub(r'([\w0-9])\s+\)', r'\1)', s)
    s = re.sub(r'\s+\)', r')', s)

    # Пробел перед процентом в некоторых случаях можно спокойно убирать: 1 %
    s = re.sub(r'(\d)\s%', r'\1%', s)

    # ° C
    s = re.sub(r'°\s+C', '°C', s)

    # н. э́.
    s = re.sub(r'н\. э́\.', 'н.э́.', s)
    s = re.sub(r'н\.\s([эпдк])\.', r'н.\1.', s)

    # км / ч
    # м / с

    # Уберем пробелы вокруг дефиса в MWE типа "кто-то"
    uline = s.lower()
    for w in 'когда кто кого чего где как куда откуда почему отчего зачем потому что чем кем кому ком чём чему чей чья чье чьё чьи чьих чьим чьей чью какой какая какое какие какого какую какие каких каким'.split():
        wx = [w]
        for i, c in enumerate(w):
            if c in 'уеыаоэёяию':
                w2 = w[:i] + c + '\u0301' + w[i+1:]
                wx.append(w2)

        for w2 in wx:
            if w2 in uline:
                s = re.sub('(' + w2 + ') - то', '\\1-то', s, flags=re.I)

    # Если строка начинается с кавычки, то после кавычки не должно быть пробела:
    # " Всё!! Закончилась в жизни непруха!
    # ^^
    if s and s[0] == '"':
        s = re.sub('^"[ ]+', '"', s)

    # Если строка заканчивается кавычкой, то перед ней не должно быть пробела:
    # Будет новый... Ну, чем не житуха! "
    #                                  ^^
    s = re.sub('[ ]+"([\W]*)$', r'"\1', s)

    if ' - ' in s:
        # Коррекция пробелов вокруг дефиса.
        s = re.sub(r' - ка([^\w\u0301\u0300]|$)', r'-ка\1', s)  # Глянь - ка ==> Глянь-ка

        s = re.sub(r' - (нибу\u0301?дь)\b', '-\\1', s, flags=re.I)  # Кто - нибудь ==> Кто-нибудь
        s = re.sub(r'\b(по) - (.+?)\b', r'\1-\2', s, flags=re.I)  # по - новому ==> по-новому
        s = re.sub(r'(то́?чь) - в - (то́?чь)', '\\1-в-\\2', s, flags=re.I)

        s = re.sub(r'\b(я́?рко|алкого́?льно|бле́?дно|ви́?нно|вое́?нно|доро́?жно|же́?лто|жё́?лто|фиоле́?тово|кори́?чнево|инти́?мно|краснова́?то|культу́?рно|моло́?чно|нау́?чно|о́?пто́?во|пло́?ско|розова́?то|све́?тло|се́?веро|се́?ро|те́?мно|тё́?мно|усло́?вно|уче́?бно|че́?рно|чё́?рно|чи́?сто|я́?блочно|я́?дерно|си́?не|алма́?|а́?ль|бле́?к|ви́?п|йо́?шка́?р|не́?жно|янта́?рно|бе́?ло|кра́?сно) - (\w+)\b', r'\1-\2', s, flags=re.I)  # Не ярко - красные, как говорят в народе.

        if len(rx2_entries) == 0:
            entries = ['все - таки', 'всё - таки', 'рахат - лукум', 'давным - давно', 'очень - очень', 'чуть - чуть',
                       'жил - был', 'туда - сюда', 'вот - вот', 'кое - кем', 'кое - чем', 'кое - кому', 'кое - чему', 'кое - кто',
                       'кое - где', 'кое - куда', 'кое - когда', 'кое - как', 'кое - что', 'сикось - накось', 'крест - накрест', 'ай - кью',
                       'из - за', 'из - под', 'общем - то', 'в - восьмых', 'в - девятых', 'в - десятых', 'в - пятых', 'в - седьмых',
                       'в - третьих', 'в - четвертых', 'в - шестых', 'ва - банк', 'давным - давно', 'джиу - джитсу', 'едва - едва',
                       'едва - лишь', 'едва - только', 'зачем - либо', 'зачем - то', 'из - подо', 'как - либо', 'как - никак',
                       'как - то', 'какая - либо', 'какая - то', 'каким - либо', 'каким - то', 'какими - либо', 'какими - то',
                       'каких - либо', 'каких - то', 'какой - либо', 'какой - то', 'каком - либо', 'каком - то',
                       'какому - либо', 'какому - то', 'какою - либо', 'какою - то', 'какую - либо', 'какую - то',
                       'ей - богу', 'когда - либо', 'когда - то', 'кой - где', 'кой - как', 'кой - кем', 'кой - когда',
                       'кой - кого', 'кой - кому', 'кой - кто', 'кой - куда', 'ком - либо', 'ком - то', 'кому - либо',
                       'кому - то', 'куда - либо', 'куда - то', 'наконец - то', 'ноу - хау', 'то - то', 'опять - таки',
                       'откуда - либо', 'откуда - то', 'подобру - поздорову', 'полным - полно', 'потому - то',
                       'почему - либо', 'почему - то', 'раным - ранехонько', 'раным - ранешенько', 'сан - франциско',
                       'сикось - накось', 'сперва - наперво', 'так - сяк', 'так - то', 'там - сям', 'там - то',
                       'темным - темно', 'тогда - то', 'туда - сюда', 'туда - то', 'тут - то', 'тяп - ляп',
                       'хухры - мухры', 'чей - либо', 'чей - то', 'чем - либо', 'чем - то', 'чему - либо', 'чему - то',
                       'чуть - только', 'чуть - чуть', 'чьей - либо', 'чьей - то', 'чьем - либо',
                       'чьем - то', 'чьему - либо', 'чьему - то', 'чьею - либо', 'чьею - то',
                       'чьи - либо', 'чьи - то', 'чьим - либо', 'чьим - то', 'чьими - либо',
                       'чьими - то', 'чьих - либо', 'чьих - то', 'чью - либо', 'чью - то',
                       'чья - либо', 'чья - то', 'шиворот - навыворот', 'нон - стоп', 'кто - либо',
                       'всего - то', 'много - много', 'во - первых', 'во - вторых', 'в - третьих', 'в - четвертых',
                       'в - пятых', 'в - шестых', 'в - седьмых', 'в - восьмых', 'в - девятых', 'в - десятых',
                       'еле - еле', 'общем - то', 'жила - была', 'день - деньской', 'ё - моё', 'тихо - тихо',
                       'совсем - совсем', 'взад - вперёд', 'еле - еле',
                      ]

            for entry in entries:
                # TODO: скомпилировать в отдельные регулярки паттерны типа "***-либо"
                r2 = re.sub(r'([аеёиоуыэюя])', r'\1́?', entry)
                m2 = re.match(r'^(.+) - (.+)$', r2)
                part1 = m2.group(1)
                part2 = m2.group(2)
                rx_str = re.compile('({}) - ({})'.format(part1, part2), flags=re.I)
                rx2_entries.append(rx_str)

                rx2_entries.append(re.compile(r'(баб\w+) - (яг\w+)\b', flags=re.I))  # Баба - Яга
                rx2_entries.append(re.compile(r'(бизнес\w+) - (блок\w+)\b', flags=re.I))
                rx2_entries.append(re.compile(r'(бизнес\w+) - (дам\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(буэнос\w+) - (айрес\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(вагон\w+) - (ресторан\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(гогол\w+) - (могол\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(город\w+) - (геро\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(грин\w+) - (карт\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(далай\w+) - (лам\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(дресс\w+) - (код\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(жар\w+) - (птиц\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(жить\w+) - (быть\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(жук\w+) - (скарабе\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(каминг\w+) - (аут\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(кают\w+) - (компание\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(киндер\w+) - (сюрприз\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(кок\w+) - (кол\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(кокер\w+) - (спаниел\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(лас\w+) - (вегас\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(лос\w+) - (анджелес\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(ляпис\w+) - (лазур\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(мюзик\w+) - (холл\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(нарьян\w+) - (мар\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(норд\w+) - (вест\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(норд\w+) - (ост\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(нью) - (йорк\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(пепси) - (кол\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(пин) - (код\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(пинг\w+) - (понг\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(пит) - (стоп\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(плащ) - (палатк\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(плей) - (офф\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(поп) - (див\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(прайс) - (лист\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(прима) - (балерин\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(рахат) - (лукум\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(рок) - (групп\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(рок) - (зв[её]зд\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(санкт) - (петербург\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(сант\w+) - (барбар\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(сант\w+) - (клаус\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(секонд) - (хенд\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(секс) - (бомб\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(сим) - (карт\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(стоп) - (кран\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(стоп) - (линие\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(стоп) - (сигнал\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(сыр) - (бор\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(тайм\w+) - (аут\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(там) - (там\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(тель) - (авив\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(той) - (терьер\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(торрент) - (трекер\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(тянь) - (шан\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(фокус\w+) - (покус\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(ханты) - (мансийск\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(хит) - (парад\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(хот) - (дог\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(хула) - (хуп\w+)', flags=re.I))
                rx2_entries.append(re.compile(r'(хэппи) - (энд\w+)', flags=re.I))

        for entry in rx2_entries:
            s = entry.sub(r'\1-\2', s)

    return s



def check_unchanged(text: str):
    normalized_text = normalize_whitespaces(text)
    if normalized_text != text:
        print('Normalization failed for text {}.\nOutput: {}'.format(text, normalized_text))
        exit(2)


def check_changed(text: str, expected_text: str):
    normalized_text = normalize_whitespaces(text)
    if normalized_text != expected_text:
        print('Normalization failed for text {}.\nOutput: {}\nExpected: {}'.format(text, normalized_text, expected_text))
        exit(2)


if __name__ == '__main__':

    check_unchanged("По-настоящему несгибаемым человека делает не характер или воспитание, а межпозвоночная грыжа.")
    check_unchanged('Верши́на вла́сти - ка́к же э́то бо́льно')

    check_changed("рети́руюсь - ка я ́.", "рети́руюсь-ка я ́.")
    check_changed("Время прошло \".", "Время прошло\".")
    check_changed("\" Всё!! Закончилась в жизни непруха!", "\"Всё!! Закончилась в жизни непруха!")
    check_changed("Будет новый... Ну, чем не житуха! \"", "Будет новый... Ну, чем не житуха!\"")
    check_changed("По - настоящему", "По-настоящему")


    text = """Печа́льные се́стры и бра́тья
( Как в на́с непоня́тна приро́да! )
Рыда́ли при ра́достной встре́че
С четве́ртою ча́стью дохо́да."""
    print(normalize_whitespaces(text))
    print('='*80)


    text = """\" Поэт в России - больше, чем поэт \",
Но и читатель - больше, чем читатель.
Он не стихов сторонний наблюдатель,
Не звонких рифм холодный созерцатель -
Твоих трудов он верный почитатель
И вдохновитель всех твоих побед."""
    print(normalize_whitespaces(text))
    print('='*80)

    text = '''" Друзья! - сказал он, - мы не просто
На этом свете собрались!
Сегодня я хочу вам в кости
Вручить подарок - первый приз!

Мы пьём за дружбу, за компот,
За то, что друг всегда поймёт! "
'''
    print(normalize_whitespaces(text))
    print('='*80)

    text = """Я проснулся по утру
И спросил себя: " Ну, почему
Лето холодом дохнуло? "
Потянулся и зевнул сурок,
Почесал свой левый бок
И опять заснул, понуро."""
    print(normalize_whitespaces(text))
    print('='*80)

    print(normalize_whitespaces('Что, в общем - то, весьма приятно.'))
    print(normalize_whitespaces('Жила - была смешная кошка,'))

    print(normalize_whitespaces('Загрустил и дышит еле - еле.'))
    print(normalize_whitespaces('Во - первых, Данилка - мужчина'))
    print(normalize_whitespaces('Во - вторых, ты не супергерой'))
    print(normalize_whitespaces('А всего - то в декабре,'))
    print(normalize_whitespaces('От дерева - он серый.'))
    print(normalize_whitespaces('Фейерверков много - много,'))
    print(normalize_whitespaces('Езжайте куда - либо в Алма - Ату'))
    print(normalize_whitespaces('Кто - либо из Нью - Йорка написал зачем - то'))
    print(normalize_whitespaces('Повстречал кто - то Бабу - Ягу'))
    print(normalize_whitespaces('Всё шиворот - навыворот и тяп - ляп'))
    print(normalize_whitespaces('Точь - в - точь сине - зелёная'))
    print(normalize_whitespaces('Бледно - розовые всполохи'))
    print(normalize_whitespaces('Не ярко - красные, как говорят в народе.'))
    print(normalize_whitespaces('Вот - вот сорвётся в бездну под ногами!'))
    print(normalize_whitespaces('Что где-то есть, он, все - таки, творец,'))
    print(normalize_whitespaces('и рахат - лукум'))
    print(normalize_whitespaces('Давным - давно, ты знаешь, все так было,'))
    print(normalize_whitespaces('Очень - очень славный дед,'))
    print(normalize_whitespaces('Чтоб задержаться на чуть - чуть...'))
    print(normalize_whitespaces('Жил - был у бабушки серенький козлик,'))
    print(normalize_whitespaces('Опять с подружками ходить туда - сюда.'))

    print(normalize_whitespaces('Давай - ка миленький мой, слазь'))
    print(normalize_whitespaces('по - новому работай'))
    print(normalize_whitespaces('из - под полы'))
    print(normalize_whitespaces('уснул из - за мороза'))

    print(normalize_whitespaces('Я когда - то пел'))
    print(normalize_whitespaces('Какой - то серый кот'))
    print(normalize_whitespaces('Но кто - нибудь придет'))
    print(normalize_whitespaces('Из - за кручи'))
    print(normalize_whitespaces('все бы́стро ка́к - то, впопыха́х'))
    print(normalize_whitespaces('а пла́тье гля́нь - ка уцеле́ло'))
    print(normalize_whitespaces('Как нежно - розовый румянец,'))
    print(normalize_whitespaces('Сиренью пахнет день - деньской.'))
    print(normalize_whitespaces('Ах, ты леший, ё - моё!'))
    print(normalize_whitespaces('И тишина " звучит " со старенькой пластинки,'))
    print(normalize_whitespaces('Суббота. Тихо - тихо.'))
    print(normalize_whitespaces('Я ей совсем - совсем не нужен,'))
    print(normalize_whitespaces('То вприпрыжку, взад - вперёд,'))
    print(normalize_whitespaces('Об обычном помнят еле - еле.'))



