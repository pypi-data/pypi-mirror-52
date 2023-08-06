"""
scientpyfic

Usage:
  scientpyfic all [--news=number --format=format --dlen=length --tlen=length ]
  scientpyfic top [--news=number --format=format --dlen=length --tlen=length]
  scientpyfic science [--news=number --format=format --dlen=length --tlen=length ]
  scientpyfic health [--news=number --format=format --dlen=length --tlen=length ]
  scientpyfic technology [--news=number --format=format --dlen=length --tlen=length --type=type]
  scientpyfic environment [--news=number --format=format --dlen=length --tlen=length --type=type]
  scientpyfic society [--news=number --format=format --dlen=length --tlen=length --type=type]
  scientpyfic strange_offbeat [--news=number --format=format --dlen=length --tlen=length --type=type]
  scientpyfic most_popular [--news=number --format=format --dlen=length --tlen=length ]
  scientpyfic -h | --help
  scientpyfic -v | --version

Options:
  all  prints titles of latest news
  top  prints only top news
  science prints only scientific news
  health  prints only health news

  All commands can be called with the following options:
  --news=number returns given number of news
  --format=format returns formatted news in one of possible ways: 
    pb%t%d prints all news including public date, title and description
    pb%t   prints all news including only public date and title
    pb%d   prints all news includeing only public date and description
    pb     prints only public date
    t      prints only title
    d      prints only description
    Default format is set to pb%t
  --dlen=length prints all descriptions with the specified length
  --tlen=length prints all titles with the specified length
  --dformat=format

  Given option can be called only with commands: science, health, technology, environment, society, strange_offbeat
  --type=type 
    type depends from what command is used with:
    
    health:
    workplace-health, pharmaceuticals, cosmetics, 
    medical-devices, bladder-disorders, copd, ebola, irritable-bowel-syndrome, 
    resltess-leg-syndrome, cerebral-palsy, influenza, swine-flu, malaria, 
    prostate-health, birth-defects, eathing-disorder-research, pneumonia, 
    cervical-cancer, std, back-and-neck-pain, encephalitis, vioxx, 
    infectious-diseases, bladder-cancer, multiple-myeloma, cold-and-flu, 
    alzheimers-research, pancreatic-cancer, allergy, brain-tumor, 
    colon-cancer, epilepsy-research, fibromyalgia, gastrointestinal-problems, 
    cholesterol, mups-measles-rubella, obesity, 
    thyroid-disease, tryglycerides, tuberculosis, breast-cancer, 
    insomnia-research, hormone-disorders, joint-pain, ulcers, cancer,
    colitis, cystic-fibrosis, asthma, lung-cancer, mesothelioma,
    erectile-dysfunction, lyme-disease, multiple-sclerosis-research,
    mental-health-research, skin-cancer, lung-disease, crohns-disease,
    parkinsons-research, attention-deficit-disorder, stroke-prevention,
    down-syndrome, hiv-and-aids, hair-loss, heart-disease,
    herpes, anemia, arthritis, blood-clots, ovarian-cancer,
    prostate-cancer, chronic-fatigue-syndrome, bird-flu, lupus, 
    muscular-dystrophy, psoriasis, sleep-disorder-research, headache-research,
    hypertension,, lyphoma, neuropathy, leukemia, liver-disease, 
    sickle-cell-anemia, amyotrophic-lateral-sclerosis, diabetes, 
    hearing-loss, osteoporosis, kidney-disease, heartburn, 
    diseases-and-conditions, public-health-education,  
    patient-education-and-counseling, healthy-agins, mens-health, nutrition, 
    teen-health, pregnancy-and-childbirth, elder-care, fitness,
    womens-health, skin-care, todays-healthcare, breastfeeding,
    sexual-health, fertility, cosmetic-surgery, vegeterian, 
    infants-health, diet-and-weight-loss, foot-health,
    vitamin, alternative-medicine, nervous-system,
    immune-system, chronic-illnes, disability, 
    menopause, eye-care, gene-therapy, food-additives, 
    forensics, bone-and-spine, birth-control, vitamin-a,
    medical-imaging, wounds-and-healing, vitamin-b, health-policy,
    psychology-research, dietary-supplements-and-minerals, smoking, 
    medical-education-and-training, staying-healthy, childrens-health, 
    joint-health, gynecolo,gy, stem-cells, controlled-substances, 
    foodborne-illness, pain-control, vitamin-e, accident-and-trauma,
    personalized-medicine, vitamin-c, vitamin-d, human-biology, pharmacology,
    vaccines, viruses, epigenetics, genes,  sports-medicine,

  Other options:
  -h --help  shows possible commands.
  -v --version  shows current version of the package.
Help:
  For suggestions/problems and etc. visit the github reposityory https://github.com/monzita/scientpyfic
"""
import datetime as dt
import re

from docopt import docopt

from scientpyfic.commands.all import All
from scientpyfic.url_from_type import url_from_type

VERSION = '0.0.0'

URL = 'https://www.sciencedaily.com/rss/'
def main():
  global VERSION
  global URL
  options = docopt(__doc__, version=VERSION)

  OPTIONS = ['all', 'science', 'top', 'health', 'technology', 'environment', 'society', 'strange_offbeat', 'most_popular']
  set_option = list(filter(lambda key: key in OPTIONS and options[key], options))[0]

  urls_including_top = ['science', 'health', 'technology', 'environment', 'society']
  if not set_option in urls_including_top and options['--type'] is None:
    URL += '{}.xml'.format(set_option)
  elif set_option in urls_including_top and options['--type'] is None:
    URL += 'top/{}.xml'.format(set_option)
  else: #fix
    URL += 'top/{}.xml'.format(set_option)

  number_of_news = options['--news'] if not options['--news'] is None else 0
  format_display = options['--format'] if not options['--format'] is None else 'pb%t'
  description_len = options['--dlen'] if not options['--dlen'] is None else 0
  title_len = options['--tlen'] if not options['--tlen'] is None else 0
  All.exec(url=URL, number_of_news=number_of_news, 
    format_display=format_display, dlen=description_len, tlen=title_len)