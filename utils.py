# Builder utils
PHENOTYPE_IN = {
  'title': '',
  'name': '',
  'phenotype_uuid': None,
  'phenoflowid': '',
  'data_sources': '',
  'author': '',
  'sex': '',
  'type': '',
  'status': '',
  'layout': 'Phenotype',
  'valid_event_data_range': '',
  'hdr_created_date': '',
  'hdr_modified_date': '',
  'description': '',
  'implementation': '',
  'source_reference': '',
  'concept_informations': [],
  'paper_published': False,
  'validation_performed': False,
  'validation': '',
  'primary_publications': '',
  'publication_link': '',
  'publication_doi': '',
  'publications': [],
  'secondary_publication_links': '',
  'citation_requirements': '',
  'world_access': 1,
  'group_access': 1,
  'group': None,  # 3 production
  'tags': None,    # [16] # 2 production
  'collections': [18],
  'publish_immediately': True
}

CONCEPT_IN = {
  'name': '',
  'author': '',
  'description': '',
  'source_reference': '',
  'paper_published': False,
  'publication_link': '',
  'publication_doi': '',
  'secondary_publication_links': '',
  'citation_requirements': '',
  'validation_performed': False,
  'validation_description': '',
  'world_access': 1,
  'group_access': 1,
  'group': None, 
  'tags': None,
  'collections': [18],
  'coding_system': '',
  'code_attribute_header': [],
  'components': [],
  'publish_immediately': True
}

COMPONENT_IN = {
  'name': '',
  'comment': '',
  'component_type': 4,
  'logical_type': 1,
  'codes': [{
    'code': None,
    'description': '',
  }]
}

CODING_LKUP = {
  'ICD-9':        17, #18 in demo
  'ICD-10':       4, 
  'ICD-11':       18, #19 in demo
  'READ':         5,
  'OPCS':         7,
  'MEDCODES':     8,
  'SNOMED':       9,
  'PRODCODES':    10,
  'BNF':          11,
  'UKBIOBANK':    12,
  'NON-STANDARD': 13,
  'CPRD':         14,
  'OXMIS':        15,
  'MULTILEX':     16  #17 in demo
}

# API utils
API_RULES_REGEX  = r'(\$\(.*?\))'
API_DEFINE_REGEX = r'\$\((.*?)\)'

API_ENDPOINTS = {
  'DEMO': {
    'CREATE Phenotypes': {
      'URL': 'https://conceptlibrary.demo.saildatabank.com/api/v1/api_phenotype_create/',
      'METHOD': 'POST',
    },

    'UPDATE Phenotypes': {
      'URL': 'https://conceptlibrary.demo.saildatabank.com/api/v1/api_phenotype_update/',
      'METHOD': 'PUT',
    },

    'CREATE Concept': {
      'URL': 'https://conceptlibrary.demo.saildatabank.com/api/v1/api_concept_create/',
      'METHOD': 'POST'
    },

    'UPDATE Concept': {
      'URL': 'https://conceptlibrary.demo.saildatabank.com/api/v1/api_concept_update/',
      'METHOD': 'PUT'
    }
  },

  'PROD': {
    'CREATE Phenotypes': {
      'URL': 'https://conceptlibrary.saildatabank.com/api/v1/api_phenotype_create/',
      'METHOD': 'POST',
    },

    'UPDATE Phenotypes': {
      'URL': 'https://conceptlibrary.saildatabank.com/api/v1/api_phenotype_update/',
      'METHOD': 'PUT',
    },

    'CREATE Concept': {
      'URL': 'https://conceptlibrary.saildatabank.com/api/v1/api_concept_create/',
      'METHOD': 'POST'
    },

    'UPDATE Concept': {
      'URL': 'https://conceptlibrary.saildatabank.com/api/v1/api_concept_update/',
      'METHOD': 'PUT'
    }
  },

  'LOCAL': {
    'CREATE Phenotypes': {
      'URL': 'http://127.0.0.1:8000/api/v1/api_phenotype_create/',
      'METHOD': 'POST',
    },

    'UPDATE Phenotypes': {
      'URL': 'http://127.0.0.1:8000/api/v1/api_phenotype_update/',
      'METHOD': 'PUT',
    },
    
    'CREATE Concept': {
      'URL': 'http://127.0.0.1:8000/api/v1/api_concept_create/',
      'METHOD': 'POST'
    },

    'UPDATE Concept': {
      'URL': 'http://127.0.0.1:8000/api/v1/api_concept_update/',
      'METHOD': 'PUT'
    }
  }
}
