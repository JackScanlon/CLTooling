import inspect
import requests
import validators
from bs4 import BeautifulSoup

class Validator:
  def valid_url(fx):
    def wrapper(*args):
      fsig = inspect.signature(fx)
      params = {k:v for k, v in zip(fsig.parameters, args)}
      assert(params['value'] is not None)
      assert(validators.url(params['value']))
      return fx(*args)
    return wrapper
  
  def has_request(fx):
    def wrapper(*args):
      fsig = inspect.signature(fx)
      params = {k:v for k, v in zip(fsig.parameters, args)}
      assert(params['self'].response is not None)
      return fx(*args)
    return wrapper
  
  def response_ok(fx):
    def wrapper(*args):
      fsig = inspect.signature(fx)
      params = {k:v for k, v in zip(fsig.parameters, args)}
      assert(params['self'].response is not None)
      assert(params['self'].response.ok)
      return fx(*args)
    return wrapper
  
  def has_soup(fx):
    def wrapper(*args):
      fsig = inspect.signature(fx)
      params = {k:v for k, v in zip(fsig.parameters, args)}
      assert(params['self'].soup is not None)
      return fx(*args)
    return wrapper

  def has_context(fx):
    def wrapper(*args):
      fsig = inspect.signature(fx)
      params = {k:v for k, v in zip(fsig.parameters, args)}
      assert(params['self'].URL is not None)
      return fx(*args)
    return wrapper

class BasicScraper:
  __slots__ = (
    'url',
    'response',
    'soup',
  )
  
  @Validator.has_context
  def __query(self):
    self.response = requests.get(self.URL)
    self.__parse()

  @Validator.response_ok
  def __parse(self):
    self.soup = BeautifulSoup(self.response.content, 'html.parser')

  @Validator.has_soup
  def select_one(self, selector):
    return self.soup.select_one(selector=selector)
  
  @Validator.has_soup
  def select(self, selector, predicate=None):
    results = self.soup.select(selector=selector)
    results = [predicate(i, v) for i, v in enumerate(results)]
    return results

  # Properties
  @property
  def URL(self):
    return self.url
  
  @URL.setter
  @Validator.valid_url
  def URL(self, value):
    self.url = value
    self.__query()
  
  @property
  @Validator.has_request
  def status(self):
    return self.response.status_code
  
  @property
  @Validator.has_request
  def is_ok(self):
    return self.response.ok

  # Static
  @staticmethod
  def get_context(url):
    scraper = BasicScraper()
    scraper.URL = url

    return scraper
