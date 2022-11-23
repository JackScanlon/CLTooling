import re
import json
import requests as request
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth
from warnings import warn
from http.client import responses as ResponseDescriptions
from operator import itemgetter
from utils import API_RULES_REGEX, API_DEFINE_REGEX, API_ENDPOINTS
from consolemenu import *

class API():
  validation_issues = ['Invalid URL', 'Invalid credentials']

  __slots__ = (
    'address',
    'authentication'
  )

  def __init__(self, url, credentials):
    validation = [API.is_valid_url(url), API.is_valid_auth(credentials)]
    if all(validation):
      self.address = url
      self.authentication = HTTPBasicAuth(
        credentials['username'],
        credentials['password']
      )
    else:
      raise API.generate_constructor_error(validation)
  
  def request(self, method, packet):
    req = None
    match (method.lower()):
      case 'put':
        req = request.put
      case 'post':
        req = request.post
      case 'get':
        req = request.get
    
    if req is None:
      raise ValueError('Invalid request method')
    
    response = req(self.address, auth=self.authentication, json=packet)
    status_code = response.status_code
    readable_response = f"Status Code [{status_code}]: {ResponseDescriptions[status_code]}" if response.status_code in ResponseDescriptions else status_code
    if API.jsonifiable(response):
      content = {
        'status_code': status_code,
        'status_description': readable_response,
      }
      content.update(json.loads(response.content))
      return content
    else:
      warn(readable_response)

  @classmethod
  def jsonifiable(cls, response):
    if 'Content-Type' in response.headers:
      return 'json' in response.headers['Content-Type'].lower()
    return False

  @classmethod
  def generate_constructor_error(cls, validation):
    global issue_count
    issue_count = 0
    def step_issues():
      global issue_count
      issue_count += 1
      return issue_count

    issues = [f"\n{step_issues()}. {API.validation_issues[i]}" for i, v in enumerate(validation) if not v]
    raise ValueError(''.join(issues))

  @classmethod
  def is_valid_url(cls, url):
    try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
    except ValueError:
      return False

  @classmethod
  def is_valid_auth(cls, credentials):
    try:
      validation = (['username' in credentials, 'password' in credentials]
                 + [isinstance(credentials['username'], str), isinstance(credentials['password'], str)]
                 + [credentials['username'] != '', credentials['password'] != ''])
      return all(validation)
    except Exception:
      return False
  
  @classmethod
  def read_config_file(cls, path):
    with open(path, 'r') as f:
      return json.load(f)
  
  @classmethod
  def dump_config(cls, config):
    with open('./config.json', 'w') as f:
      json.dump(config, f, ensure_ascii=False, indent=2)
  
  @classmethod
  def request_config(cls):
    print('Please enter your credentials:')
    username = input('Username: ')
    password = input('Password: ')

    config = {'username': username, 'password': password}
    if API.is_valid_auth(config):
      try:
        API.dump_config(config)
      except:
        return API.request_config()
      else:
        print('Your credentials have been saved to file, located at ./config.json')
      
      return config
    else:
      return API.request_config()
  
  @classmethod
  def request_endpoint(cls):
    endpoint_list = list(API_ENDPOINTS.keys())
    selection = SelectionMenu.get_selection(endpoint_list)
    
    if selection < len(endpoint_list):
      environment = endpoint_list[selection]

      method_list = list(API_ENDPOINTS[environment])
      selection = SelectionMenu.get_selection(method_list)

      if selection < len(method_list):
        endpoint = method_list[selection]
        selection = API_ENDPOINTS[environment][endpoint]
        return (itemgetter('URL', 'METHOD')(selection)), environment
  
  @classmethod
  def get_packet(cls, path):
    try:
      with open(path, 'r') as f:
        return json.load(f)
    except:
      warn('No valid packet.json found, using template instead')

      from template import API_TEMPLATE_PACKET
      return API_TEMPLATE_PACKET.copy()

  @classmethod
  def apply_rules(cls, packet, rules, save_path=None):
    if isinstance(packet, dict) or isinstance(packet, list):
      packet = json.dumps(packet, indent=2)
    
    if not isinstance(packet, str):
      warn('Couldn\'t apply rules to packet, unable to dump to string')
      return packet
    
    modified = re.sub(
      API_RULES_REGEX,
      lambda m: rules[re.findall(API_DEFINE_REGEX, m.group())[0]](),
      packet
    )

    if save_path is not None:
      try:
        with open(save_path, 'w') as f:
          json.dump(packet, f, ensure_ascii=False, indent=2)
      except:
        warn(f'Couldn\'t save packet to {save_path}')
      else:
        print(f'Saved packet to file @ {save_path}')

    return modified

  @staticmethod
  def request_config():
    try:
      config = API.read_config_file('./config.json')
    except:
      warn('No config.json file found')
      config = API.request_config()
    
    return config
  
  @staticmethod
  def get_endpoint(env, endpoint):
    return API_ENDPOINTS[env][endpoint]
