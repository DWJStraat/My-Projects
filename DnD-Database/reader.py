import json
import regex

with open('spells_of_antiquity.txt', encoding='utf-8') as f:
    file = f.read()

if True:
    source = input('Source: ')
    writer = input('Writer: ')
    spells = regex.split(r'\s(?=\d{1,2}(?:st|nd|rd|th)-level ('
                         r'?:evocation|necromancy|conjuration|abjuration'
                         r'|divination|conjuration|transmutation|enchantment'
                         r'|illusion))', file)
    newspells = []
    for spell_id in range(len(spells)):
        spell = spells[spell_id]
        split = regex.split(r'\s(?:Evocation|Necromancy|Conjuration|Abjuration'
                            r'|Divination|Conjuration|Transmutation|'
                            r'Enchantment|Illusion) cantrip\n', spell)
        newspells.extend(split[i] for i in range(len(split)))
    newnewspells = []
    title = 'HEADER'
    for spell_id in range(len(newspells)):
        spell = newspells[spell_id]
        if spell_id < len(newspells) and title != 'HEADER':
            text = newspells[spell_id].split('\n')[:-1]
            if 'cantrip' in text[0]:
                level = 0
                school = text[0].split(' ')[0]
            else:
                level = text[0].split(' ')[0][0]
                school = text[0].split(' ')[1]
            text = '\n'.join(text)
            CastTime = text[text.find('Casting Time: ') + 13:
                            (text.find('Range: ') - 1)]
            Range = text[
                    text.find('Range: ') + 7:text.find('Components: ') - 1]
            Components = text[text.find('Components: ') + 12:
                              text.find('Duration: ') - 1]
            Verbal = 'V' in Components
            Somatic = 'S' in Components
            Material = 'M' in Components
            ritual = '(ritual)' in text
            if Material:
                Material_component = Components[Components.find('(') + 1:
                                                Components.find(')')]
            else:
                Material_component = ''

            if text.find('Classes: ') == -1:
                Classes = ['Unknown']
                Duration = text[text.find('Duration: ') + 10:].split('\n')[0]
                Description = text[text.find(Duration) + len(Duration):]
            else:
                Duration = text[text.find('Duration: ') + 10:
                                text.find('Classes: ') - 1]
                Classes = text[text.find('Classes: ') + 9:
                          ].split('\n')
                if Classes[0][-1] == ',':
                    Classes = Classes[0]+' '+Classes[1]
                    Classes = Classes.split(', ')
                else:
                    Classes = Classes[0].split(', ')

                Description = text[text.find(Classes[-1]) + len(Classes[-1]):]
            spell_dict = {'title': title,
                          'school': school,
                          'ritual': ritual,
                          'level': level,
                          'casttime': CastTime.strip(),
                          'range': Range.strip(),
                          'verbal': Verbal,
                          'somatic': Somatic,
                          'material': Material,
                          'material_component': Material_component,
                          'duration': Duration.strip(),
                          'classes': Classes,
                          'description': Description.replace('\n', ' ').strip(),
                          'source': source,
                          'writer': writer}

            newnewspells.append(spell_dict)
        title = spell.split('\n')[-1]
with open('spelllist.json', 'r') as f:
    spelllist = json.load(f)
    for spell in newnewspells:
        id = len(spelllist)
        spelllist[id] = spell
with open('spelllist.json', 'w') as f:
    json.dump(spelllist, f, indent=4)
#     return newnewspells
#
# spells = reader(file)
# spell = spells[0]
# spell = spell.split('\n')
# name = spell[0]
# level_and_school = spell[1]
# if 'cantrip' in level_and_school:
#     level = 0
#     school = level_and_school.split(' ')[0]
# else:
#     level = level_and_school.split(' ')[0][0]
#     school = level_and_school.split(' ')[1]
