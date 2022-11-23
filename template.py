API_TEMPLATE_JSON = """{
  "id": "$(id)",
  "name": "$(name)",
  "author": "$(author)",
  "description": "$(description)",
  "citation_requirements": "$(citations)",
  "type": "$(type)",
  "publications": "$(publications)",
  "tags": "$(tags)",
  "collections": "$(collections)",
  "data_sources": "$(datasources)",
  "phenotypes_concepts_data": "$(attributes)"
}"""

API_TEMPLATE_PACKET = {
  'id': 'WS1',
  'name': 'workingset object',
  'author': 'john.doe',
  'description': 'i have been updated',
  'citation_requirements': 'updated requirements',
  'type': 1,
  'publications': ["hello", "publications"],
  'tags': [1],
  'collections': [18],
  'data_sources': [24],
  'phenotypes_concepts_data': [
    {
      "Attributes": [
      {
        "name": "attr_1",
        "type": "INT",
        "value": "123"
      },
      {
        "name": "attr_2",
        "type": "STRING",
        "value": "male/female"
      }
      ],
      "concept_id": "C714",
      "phenotype_id": "PH1",
      "concept_version_id": 2567,
      "phenotype_version_id": 2
    },
    {
      "Attributes": [
      {
        "name": "attr_1",
        "type": "INT",
        "value": "87523"
      },
      {
        "name": "attr_2",
        "type": "STRING",
        "value": "male"
      }
      ],
      "concept_id": "C717",
      "phenotype_id": "PH3",
      "concept_version_id": 2573,
      "phenotype_version_id": 6
    },
    {
      "Attributes": [
      {
        "name": "attr_1",
        "type": "INT",
        "value": "654"
      },
      {
        "name": "attr_2",
        "type": "STRING",
        "value": "female"
      }
      ],
      "concept_id": "C717",
      "phenotype_id": "PH3",
      "concept_version_id": 2573,
      "phenotype_version_id": 6
    }
  ]
}