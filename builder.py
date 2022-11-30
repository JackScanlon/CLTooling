import os
import re
import json
import glob
import pandas as pd
from copy import deepcopy
from scraper import BasicScraper
from utils import PHENOTYPE_IN, CONCEPT_IN, COMPONENT_IN, CODING_LKUP

AGREEMENT_DATE = "October 1st, 2018"
MODIFIED_DATE = "October 30th, 2022"
LIST_PREFIX = " - "
CAM_DESC = "CPRD Gold code list version 1.1 created by CPRD @ Cambridge research group (available at https://www.phpc.cam.ac.uk/pcu/research/research-groups/crmh/cprd_cam/codelists/v11/)"
CITE_REQ = ""

class Utils:
  @staticmethod
  def try_load_df(path):
    if os.path.exists(path):
      try:
        df = pd.read_csv(path)
        df = df.fillna('')
        return df
      except:
        return None
      
    return None

  @staticmethod
  def is_valid_codelist(df):
    return all([x in df.columns for x in ['TYPE', 'ALLCODES']])
  
  @staticmethod
  def is_valid_description(df):
    return any([x in df.columns for x in ['productname', 'Description']])

  @staticmethod
  def try_get_value(row, key, default='NULL'):
    if key in row:
      return row[key]
    
    return default

class CambridgePhenotypeBuilder:
  __slots__ = (
    'url',
    'author',
    'phenotypes',
    'root_data_path',
    'download_dir',
    'processed_dir',
    'descriptors',
  )

  def __init__(self, url, author, root_data_path='./data', download_dir='downloaded', processed_dir='processed'):
    self.url = url
    self.author = author
    self.root_data_path = root_data_path
    self.download_dir = download_dir
    self.processed_dir = processed_dir
    self.descriptors = None

  def scrape_code_table(self):
    scraper = BasicScraper.get_context(self.url)
    table = scraper.select_one('#tablepress-33')
    id_column = table.select('td.column-1')
    codes = [re.search(r'[^()]+(?=\))', x.text.rstrip()).group() for x in id_column]

    links, keys = [], []
    for row in id_column:
      list_id = row.select_one('a')
      keys.append(list_id.text.rstrip())
      links.append(list_id['href'])
    
    df = pd.read_html(str(table))[0]
    df = df.fillna('')
    df.rename(columns={old:new for (old, new) in zip(df.columns, ['links', 'name', 'desc', 'provenance', 'prevalence', 'usage'])}, inplace=True)
    df['links'] = links
    df['keys'] = keys
    df['codes'] = codes
    return df

  def scrape_publication_list(self):
    scraper = BasicScraper.get_context(self.url)
    table = scraper.select_one('#tablepress-33')
    pub_list = table.find_next_sibling('ol')
    items = pub_list.select('li')

    publications = { }
    for i, item in enumerate(items):
      publications[str(i + 1)] = item.text
    
    return publications

  def collect_code_table(self, path):
    df = Utils.try_load_df(path)

    if df is None:
      df = self.scrape_code_table()
      df.to_csv(path, index=False)

    return df
    
  def collect_publication_list(self, path):
    publications = None
    if os.path.exists(path):
      with open(path, 'r') as f:
        publications = json.load(f)

    if publications is None:
      publications = self.scrape_publication_list()
      
      with open(path, 'w') as f:
        json.dump(publications, f, sort_keys=False, indent=2, ensure_ascii=False)

    return publications

  def try_process_descriptor(self, df):
    if not Utils.is_valid_description(df):
      return
    
    if self.descriptors is None:
      self.descriptors = {
        'medcodes': { },
        'prodcodes': { }
      }

    df = df.fillna('')
    for i, row in df.iterrows():
      description = ''
      if 'Description' in row:
        description = row['Description']
      elif 'productname' in row:
        description = row['productname']
      
      code, system = '', ''
      if 'medcode' in row:
        code = row['medcode']
        system = 'medcodes'
      elif 'prodcode' in row:
        code = row['prodcode']
        system = 'prodcodes'
      
      if system != '':
        self.descriptors[system][code] = description

  def try_process_concepts(self, df, name):
    if not Utils.is_valid_codelist(df):
      return
    
    df = df.fillna('')
    for i, row in df.iterrows():
      concept = {
        'name': Utils.try_get_value(row, 'CONDITION DESCRIPTION'),
        'description': Utils.try_get_value(row, 'PROVENANCE'),
        'coding_system': Utils.try_get_value(row, 'TYPE'),
        'condition_code': Utils.try_get_value(row, 'CONDITION CODE'),
        'codelist': Utils.try_get_value(row, 'ALLCODES').split(';')
      }

      with open(f'{self.root_data_path}/{self.processed_dir}/{name}-{i}.json', 'w') as file:
        json.dump(concept, file, sort_keys=False, indent=2, ensure_ascii=False)

  def try_build_codelist(self, name, url):
    save_path = f'{self.root_data_path}/{self.download_dir}/{name}/'
    if os.path.exists(save_path):
      return
    
    os.mkdir(save_path)

    from io import BytesIO
    from urllib.request import urlopen
    from zipfile import ZipFile

    with urlopen(url) as res:
      with ZipFile(BytesIO(res.read())) as zfile:
        zfile.extractall(save_path)
    
    for file in glob.glob(f"{save_path}/*.csv"):
      df = pd.read_csv(file, encoding='cp1252')
      self.try_process_descriptor(df)
      self.try_process_concepts(df, os.path.basename(os.path.dirname(file)))

  def collect_concepts(self, path, key):
    if not os.path.exists(path):
      raise FileNotFoundError(f"Unable to locate dir @ {path}")
    
    concepts = []
    for file in glob.glob(f"{path}/{key}-*.json"):
      with open(file, 'r') as f:
        concepts.append(json.loads(f.read()))
    
    return concepts

  def collect_data(self, df):
    download_path = f'{self.root_data_path}/{self.download_dir}'
    if not os.path.exists(download_path):
      os.mkdir(download_path)
    
    processed_path = f'{self.root_data_path}/{self.processed_dir}'
    if not os.path.exists(processed_path):
      os.mkdir(processed_path)
    
    data = { }
    for key, link in zip(df['keys'], df['links']):
      self.try_build_codelist(key, link)

      data[key] = self.collect_concepts(processed_path, key)
    
    if self.descriptors is not None:
      with open(f'{self.root_data_path}/descriptors.json', 'w') as f:
        json.dump(self.descriptors, f, sort_keys=False, indent=2, ensure_ascii=False)

    return data

  def parse_publications(self, provenance, publications):
    pattern = re.compile(r'\([^\d]*(\d+)[^\d]*\)')

    pub_list = [ ]
    for reference in re.findall(pattern, provenance):
      if reference in publications:
        pub_list.append(publications[reference])
    
    return pub_list

  def try_get_descriptor(self, code, system):
    system = system.lower()

    if self.descriptors is None:
      with open(f'{self.root_data_path}/descriptors.json', 'r') as f:
        self.descriptors = json.load(f)
    
    if code in self.descriptors[system]:
      return self.descriptors[system][code]
    
    return ''
  
  def transform_desc(self, desc, provenance, prevalence, usage):
    if desc is not None and desc != "":
      desc = f"# Summary\n{LIST_PREFIX}{CAM_DESC}\n{LIST_PREFIX}{desc}\n"
    else:
      desc = f"# Summary\n{LIST_PREFIX}{CAM_DESC}\n"
    
    if provenance is not None and provenance != "":
      provenance = f"# Provenance\n{LIST_PREFIX}{provenance}\n"
    else:
      provenance = ""
    
    if prevalence is not None and prevalence != "":
      prevalence = f"# Prevalence\n{LIST_PREFIX}{prevalence}%\n"
    else:
      prevalence = ""
    
    if usage is not None and usage != "":
      usage = f"# Usage\n{LIST_PREFIX}{usage}\n"
    else:
      usage = ""
    
    return f"{desc}{provenance}{prevalence}{usage}\n"

  def transform_data(self, row, codelists, publications=None):
    phenotype = deepcopy(PHENOTYPE_IN)
    phenotype['title'] = row['name']
    phenotype['name'] = row['name']
    phenotype['author'] = self.author
    phenotype['sex'] = 'Male/Female'
    phenotype['type'] = 'Disease or Syndrome'
    phenotype['source_reference'] = self.url
    phenotype['data_sources'] = [5]
    phenotype['hdr_created_date'] = AGREEMENT_DATE
    phenotype['hdr_modified_date'] = MODIFIED_DATE
    phenotype['description'] = self.transform_desc(row['desc'], row['provenance'], row['prevalence'], row['usage'])

    if publications is not None:
      phenotype['publications'] = self.parse_publications(row['provenance'], publications)

      if len(phenotype['publications']) > 0:
        phenotype['paper_published'] = True

    concepts = []
    for codelist in codelists:
      concept = deepcopy(CONCEPT_IN)
      concept['name'] = f"{codelist['name']} ({codelist['condition_code']}, {codelist['coding_system']})"
      concept['author'] = self.author
      concept['description'] = codelist['description']
      concept['coding_system'] = CODING_LKUP[codelist['coding_system']]
      concept['source_reference'] = self.url
      concept['paper_published'] = phenotype['paper_published']

      component = deepcopy(COMPONENT_IN)
      component['name'] = codelist['condition_code']
      component['codes'] = [{'code': x, 'description': self.try_get_descriptor(x, codelist['coding_system'])} for x in codelist['codelist']]
      concept['components'] = [component]
      concepts.append(concept)
    
    phenotype['concepts'] = concepts
    return phenotype

  def build_phenotypes(self):
    df = self.collect_code_table(f'{self.root_data_path}//table.csv')
    df = df.fillna('')

    pl = self.collect_publication_list(f'{self.root_data_path}/publications.json')
    cl = self.collect_data(df)

    self.descriptors = None

    self.phenotypes = []
    for i, row in df.iterrows():
      pheno = self.transform_data(row, cl[row['keys']], pl)
      self.phenotypes.append(pheno)

    return self.phenotypes
