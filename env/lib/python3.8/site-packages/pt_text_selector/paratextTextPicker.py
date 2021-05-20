import itertools, re, os, configparser, sys, json
from shutil import copyfile

BOOK_DICT = {'1CH': '13',
 '1CO': '47',
 '1JN': '63',
 '1KI': '11',
 '1PE': '61',
 '1SA': '09',
 '1TH': '53',
 '1TI': '55',
 '2CH': '14',
 '2CO': '48',
 '2JN': '64',
 '2KI': '12',
 '2PE': '62',
 '2SA': '10',
 '2TH': '54',
 '2TI': '56',
 '3JN': '65',
 'ACT': '45',
 'AMO': '30',
 'COL': '52',
 'DAN': '27',
 'DEU': '05',
 'ECC': '21',
 'EPH': '50',
 'EST': '17',
 'EXO': '02',
 'EZK': '26',
 'EZR': '15',
 'GAL': '49',
 'GEN': '01',
 'HAB': '35',
 'HAG': '37',
 'HEB': '59',
 'HOS': '28',
 'ISA': '23',
 'JAS': '60',
 'JDG': '07',
 'JER': '24',
 'JHN': '44',
 'JOB': '18',
 'JOL': '29',
 'JON': '32',
 'JOS': '06',
 'JUD': '66',
 'LAM': '25',
 'LEV': '03',
 'LUK': '43',
 'MAL': '39',
 'MAT': '41',
 'MIC': '33',
 'MRK': '42',
 'NAM': '34',
 'NEH': '16',
 'NUM': '04',
 'OBA': '31',
 'PHM': '58',
 'PHP': '51',
 'PRO': '20',
 'PSA': '19',
 'REV': '67',
 'ROM': '46',
 'RUT': '08',
 'SNG': '22',
 'TIT': '57',
 'ZEC': '38',
 'ZEP': '36'}

ENC = "UTF-8"

# Utility functions

flatten = lambda l: [item for sublist in l for item in sublist]

def showMsg(msg):
    print("[*]: " + msg)

def readFile(inPath):
    with open(inPath, 'r', encoding=ENC) as f:
        return f.read().strip()

def saveResults(path, chatpers):
    with open(path, 'w', encoding=ENC) as f:
        f.write(chapters)

def rangeMaker(x):
    if "-" in x:
        start, myend = x.split("-")
        return list(range(int(start), int(myend) + 1))
    else:
        return [int(x)]

def parseRange(raw):
    pieces = map(lambda x: rangeMaker(x), raw.split(","))
    return list(map(lambda x: int(x), flatten(pieces)))

def splitToChapters(raw):
    cs = raw.split("\\c ")
    intro = cs[0]
    chapters = {0 : intro.strip() }
    for c in cs[1:]:
        lines = c.split("\n")
        #cptNum = lines[0].strip()
        cptNum = re.match(r'^\\?c?\s?(\d+)', lines[0]).group(1)
        lines[0] = "\\c " + cptNum
        chapters[int(cptNum)] = "\n".join(lines)
    return chapters


def processFile(fcons, rawRange):
    cs = splitToChapters(fcons)
    toGet = parseRange(rawRange)
    showMsg('Getting chapters ' + ', '.join(map(lambda x: str(x), toGet)))
    wanted = [cs[0]]
    if 0 in toGet:
        del toGet[toGet.index(0)]
    for z in toGet:
        wanted.append(cs[z])
    return "\n".join(wanted)

def processFileNoIntro(fcons, rawRange):
    cs = splitToChapters(fcons)
    toGet = parseRange(rawRange)
    showMsg('Getting chapters ' + ', '.join(map(lambda x: str(x), toGet)))
    wanted = []
    for z in toGet:
        wanted.append(cs[z])
    return "\n".join(wanted)

def removeChatperLines(fcons):
    return re.sub(r'\\c \d+[^\n]*\n', "", fcons).strip()

def splitBy(inpath, sep):
    return readFile(inpath).split(sep)

# Not currently in use. May be able to be removed in the future
def getBackmatterBook(inPath, outPath, sep, sectionsRange):
    toGet = parseRange(sectionsRange) if not(sectionsRange.strip() == "") else ""
    if toGet == "":
        copyfile(inPath.strip(), outPath.strip())
    else:
        parts = splitBy(inPath.strip(), sep)
        output = map(lambda x: parts[x], toGet)
        saveResults(outPath.strip(), output)

def fix(t):
    if '\\' in t:
        return t
    return '\\\\' + t.replace('\\', '')

def parseConvertTags(taglist):
    return list(map(lambda l: [fix(l[0]), fix(l[1])] , json.loads(taglist)))

def convertIntroTagsToTextTags(fcons, tags):
    try:
        tags = parseConvertTags(tags)
        for t in tags:
            fcons = re.sub(t[0], t[1], fcons)#t[0].sub(t[1], fcons)
        return fcons
    except:
        print("[!]: Error parsing tags list. Make sure that the backslashes are correct.")
        print("[!]: tags NOT converted!")
        return fcons

def removeDraftGloEntries(fcons, marker):
    print("[*]: Removing drafts from Glossary")
    out = []
    for line in fcons.split("\n"):
        if not(marker in line):
            out.append(line)
    return "\n".join(out)


def inAndTrue(cfg, s):
    return (cfg in s) # and s[cfg].upper() == 'TRUE')

def processSection(section, default, sname, outputPath, pname):
    #Upper case section parts in so users don't have to deal with caps
    section = {k.upper():v for (k,v) in section.items()}
#    import pprint
#    pprint.pprint(section)
    if sname[0] == '*':
        fname = sname[1:]
    elif sname in BOOK_DICT:
        fname = BOOK_DICT[sname] + sname + pname + '.SFM'
    else:
        fname = sname + '.SFM'
    if '$' in fname:
        fname = re.sub(r'\$\d+', '', fname)
    fpath = os.path.join(default, fname)

    if 'PATH' in section:
        fpath = os.path.join(section['PATH'], fname)
        showMsg("Using section specific path (" + section['PATH'] + ')' )
    if not(os.path.exists(fpath)):
        showMsg(sname + " not found!")
        return None
    else:
        showMsg(fpath)
    ofile = os.path.join(outputPath, section['OUTPUT']) if 'OUTPUT' in section else os.path.join(outputPath, fname)
    filecons = ""
    with open(fpath, 'r', encoding = 'UTF-8') as f:
        filecons = f.read()
    if 'CHAPTERS' in section:
        if 'NOINTRO' in section:
            filecons = processFileNoIntro(filecons, section['CHAPTERS'])
        else:
            filecons = processFile(filecons, section['CHAPTERS'])
    if inAndTrue('CONVERTTAGS', section):
        showMsg('Converting intro tags')
        tags = section['CONVERTTAGS']
        filecons = convertIntroTagsToTextTags(filecons, tags)
    if inAndTrue('REMOVECHAPTERLINES', section):
        showMsg('Removing chapter lines')
        filecons = removeChatperLines(filecons)
    if inAndTrue('REMOVEDRAFTGLOENTRIES', section):
        showMsg('Removing draft entries from GLO')
        filecons = removeDraftGloEntries(filecons, section['REMOVEDRAFTGLOENTRIES'])

    with open(ofile, 'w', encoding="UTF-8") as f:
        f.write(filecons)


def process(config_file_path):


    config = configparser.ConfigParser()

    config.read(config_file_path)

    sections = config.sections()

    sections.remove('config')

    configs = {k.upper():v for (k,v) in config['config'].items()}

    defaultPath = configs['PTPATH']
    defaultOutputPath = configs['OUTPUTPATH']
    projectname = configs['PROJECTNAME']

    for s in sections:
        processSection(config[s], defaultPath, s, defaultOutputPath, projectname)
