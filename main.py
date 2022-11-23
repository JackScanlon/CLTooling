import os
from api import API
from builder import CambridgePhenotypeBuilder

DEBUG = True

def create_concepts(phenotype, env, config):
  endpoint = API.get_endpoint(env, 'CREATE Concept')

  concept_ids = []
  for concept in phenotype['concepts']:
    if DEBUG:
      print(f'Attempting to create concept: {concept["name"]}')
    
    req = API(url=endpoint['URL'], credentials=config)
    try:
      response = req.request(endpoint['METHOD'], concept)
      if response['status_code'] == 201:
        concept_ids.append(response['id'])

      if DEBUG:
        print(f'\t Concept result: {response}')
    except Exception as err:
      raise err
  
  return concept_ids

def create_phenotype(phenotype, endpoint, method, config):
  req = API(url=endpoint, credentials=config)
  try:
    if DEBUG:
      print(f'Attempting to create phenotype: {phenotype["name"]}')
    
    response = req.request(method, phenotype)
    if DEBUG:
      print(f'\tPhenotype result: {response}')
  except Exception as err:
    raise err

if __name__ == '__main__':
  builder = CambridgePhenotypeBuilder(url='https://www.phpc.cam.ac.uk/pcu/research/research-groups/crmh/cprd_cam/codelists/v11/', author='CPRD@Cambridge')
  builder.build_phenotypes()
  
  config = API.request_config()
  result = API.request_endpoint()
  if result is not None:
    ((endpoint, method), env) = result
    
    os.system('cls')
    for phenotype in builder.phenotypes:
      if 'concepts' in phenotype:
        phenotype['concept_informations'] = create_concepts(phenotype, env, config)
        phenotype.pop('concepts', None)
      
      create_phenotype(phenotype, endpoint, method, config)
