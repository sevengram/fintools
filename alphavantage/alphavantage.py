import inspect
import json
import re
from functools import wraps
from urllib.request import urlopen

import pandas


class AlphaVantage:
  """ 
  Base class where the decorators and base function for the other
  classes of this python wrapper will inherit from.
  """
  _ALPHA_VANTAGE_API_URL = "http://www.alphavantage.co/query?"
  _ALPHA_VANTAGE_MATH_MAP = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'T3',
                             'KAMA', 'MAMA']
  _EXCHANGE_SUPPORTED = {'ASX': 'Australian Securities Exchange',
                         'BOM': 'Bombay Stock Exchange',
                         'BIT': 'Borsa Italiana Milan Stock Exchange',
                         'TSE': 'Canadian/Toronto Securities Exchange',
                         'FRA': 'Deutsche Boerse Frankfurt Stock Exchange',
                         'ETR': 'Deutsche Boerse Frankfurt Stock Exchange',
                         'AMS': 'Euronext Amsterdam',
                         'EBR': 'Euronext Brussels',
                         'ELI': 'Euronext Lisbon',
                         'EPA': 'Euronext Paris',
                         'LON': 'London Stock Exchange',
                         'MCX': 'Moscow Exchange',
                         'NASDAQ': 'NASDAQ Exchange',
                         'CPH': 'NASDAQ OMX Copenhagen',
                         'HEL': 'NASDAQ OMX Helsinki',
                         'ICE': 'NASDAQ OMX Iceland',
                         'STO': 'NASDAQ OMX Stockholm',
                         'NSE': 'National Stock Exchange of India',
                         'NYSE': 'New York Stock Exchange',
                         'SGX': 'Singapore Exchange',
                         'SHA': 'Shanghai Stock Exchange',
                         'SHE': 'Shenzhen Stock Exchange',
                         'TPE': 'Taiwan Stock Exchange',
                         'TYO': 'Tokyo Stock Exchange'}

  def __init__(self, key=None, retries=5, output_format='json'):
    """ Initialize the class

    Keyword Arguments:
        key:  Alpha Vantage api key
        retries:  Maximum amount of retries in case of faulty connection or
            server not able to answer the call.
        output_format:  Either 'json' or 'pandas'
    """
    if key is None:
      raise ValueError('Get a free key from the alphavantage website')
    self.key = key
    self.retries = retries
    self.output_format = output_format

  def _retry(func):
    """ Decorator for retrying api calls (in case of errors from the api
    side in bringing the data)

    Keyword Arguments:
        func:  The function to be retried
    """

    @wraps(func)
    def _retry_wrapper(self, *args, **kwargs):
      error_message = ""
      for retry in range(self.retries + 1):
        try:
          return func(self, *args, **kwargs)
        except ValueError as err:
          error_message = str(err)
      raise ValueError(str(error_message))

    return _retry_wrapper

  @classmethod
  def _call_api_on_func(cls, func):
    """ Decorator for forming the api call with the arguments of the
    function, it works by taking the arguments given to the function
    and building the url to call the api on it

    Keyword Arguments:
        func:  The function to be decorated
    """

    # Argument Handling
    argspec = inspect.getargspec(func)
    try:
      # Asumme most of the cases have a mixed between args and named
      # args
      positional_count = len(argspec.args) - len(argspec.defaults)
      defaults = dict(zip(argspec.args[positional_count:], argspec.defaults))
    except TypeError:
      if argspec.args:
        # No defaults
        positional_count = len(argspec.args)
        defaults = {}
      elif argspec.defaults:
        # Only defaults
        positional_count = 0
        defaults = argspec.defaults

    # Actual decorating

    @wraps(func)
    def _call_wrapper(self, *args, **kwargs):
      used_kwargs = kwargs.copy()
      # Get the used positional arguments given to the function
      used_kwargs.update(zip(argspec.args[positional_count:],
                             args[positional_count:]))
      # Update the dictionary to include the default parameters from the
      # function
      used_kwargs.update({k: used_kwargs.get(k, d)
                          for k, d in defaults.items()})
      # Form the base url, the original function called must return
      # the function name defined in the alpha vantage api and the data
      # key for it and for its meta data.
      function_name, data_key, meta_data_key = func(self, *args, **kwargs)
      url = "{}function={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
                                   function_name)
      for idx, arg_name in enumerate(argspec.args[1:]):
        try:
          arg_value = args[idx]
        except IndexError:
          arg_value = used_kwargs[arg_name]
        if 'matype' in arg_name and arg_value:
          # If the argument name has matype, we gotta map the string
          # or the integer
          arg_value = self.map_to_matype(arg_value)
        if arg_value:
          # Discard argument in the url formation if it was set to
          # None (in other words, this will call the api with its
          # internal defined parameter)
          url = '{}&{}={}'.format(url, arg_name, arg_value)
      url = '{}&apikey={}'.format(url, self.key)
      return self._handle_api_call(url), data_key, meta_data_key

    return _call_wrapper

  @classmethod
  def _output_format(cls, func, override=None):
    """ Decorator in charge of giving the output its right format, either
    json or pandas

    Keyword Arguments:
        func:  The function to be decorated
        override:  Override the internal format of the call, default None
    """

    @wraps(func)
    def _format_wrapper(self, *args, **kwargs):
      json_response, data_key, meta_data_key = func(self, *args, **kwargs)
      data = json_response[data_key]
      if meta_data_key is not None:
        meta_data = json_response[meta_data_key]
      else:
        meta_data = None
      # Allow to override the output parameter in the call
      if override is None:
        output_format = self.output_format.lower()
      elif 'json' or 'pandas' in override.lower():
        output_format = override.lower()
      # Choose output format
      if output_format == 'json':
        return data, meta_data
      elif output_format == 'pandas':
        data_pandas = pandas.DataFrame.from_dict(data, orient='index',
                                                 dtype=float)
        # Rename columns to have a nicer name
        col_names = [re.sub(r'\d+.', '', name).strip(' ')
                     for name in list(data_pandas)]
        data_pandas.columns = col_names
        return data_pandas, meta_data
      else:
        raise ValueError('Format: {} is not supported'.format(
            self.output_format))

    return _format_wrapper

  def map_to_matype(self, matype):
    """ Convert to the alpha vantage math type integer. It returns an
    integer correspondant to the type of math to apply to a function. It
    raises ValueError if an integer greater than the supported math types
    is given.

    Keyword Arguments:
        matype:  The math type of the alpha vantage api. It accepts integers
            or a string representing the math type.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
    """
    # Check if it is an integer or a string
    try:
      value = int(matype)
      if abs(value) > len(AlphaVantage._ALPHA_VANTAGE_MATH_MAP):
        raise ValueError("The value {} is not supported".format(value))
    except ValueError:
      value = AlphaVantage._ALPHA_VANTAGE_MATH_MAP.index(matype)
    return value

  @_retry
  def _handle_api_call(self, url):
    """ Handle the return call from the  api and return a data and meta_data
    object. It raises a ValueError on problems

    Keyword Arguments:
        url:  The url of the service
        data_key:  The key for getting the data from the jso object
        meta_data_key:  The key for getting the meta data information out of
            the json object
    """
    response = urlopen(url)
    url_response = response.read()
    json_response = json.loads(url_response.decode('utf8'))
    if 'Error Message' in json_response or not json_response:
      if json_response:
        raise ValueError('ERROR getting data from api',
                         json_response['Error Message'])
      else:
        raise ValueError('Error getting data from api, no return'
                         ' message from the api url (possibly wrong symbol/param)')
    return json_response

  def is_exchange_supported(self, exchange_name):
    """
        Get if a specific global exchange type is supported by this library

        Keyword Arguments:
            exchange_name: The exchange type to check for
        Returns:
            The description of the given key or None
    """
    try:
      return AlphaVantage._EXCHANGE_SUPPORTED[exchange_name]
    except KeyError:
      return None
