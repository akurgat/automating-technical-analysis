import os
import configparser
import sys
import argparse
import subprocess
import robin_stocks.robinhood as r
from traceback import print_tb
from pprint import pprint

VERBOSE = [True if '-d' in sys.argv else False][0]
directory = os.path.abspath(os.path.dirname(__file__))
directory_name = os.path.dirname(os.path.dirname(directory))
project_root = os.path.dirname(directory)
if not os.path.exists(os.path.join(f'{project_root}/cli_config.ini')):
    # we need to find the config file else we can't run the program: using default values is too much of a headache.
    print(f'error: cli_config.ini not found in {project_root}')
    sys.exit(1)
elif not os.path.exists(os.path.join(f'{project_root}/cli/.cli_root.txt')):
    # we need to find the config file else we can't run the program: using default values is too much of a headache.
    if VERBOSE: print(f'error: .cli_root.txt not found in {project_root}')
    # create the file
    with open(os.path.join(f'{project_root}/cli/.cli_root.txt'), 'w') as f:
        f.write(f'{project_root}')
    if VERBOSE: print(f'created .cli_root.txt in {project_root}')
else:
    if VERBOSE: print(f'cli_config.ini and cli_root.txt found in {project_root}')
        
config = configparser.ConfigParser()
config.read(os.path.join(f'{project_root}/cli_config.ini'))
CURRENT_WORKING_DIR = os.getcwd()
    
class cli:
    def __self__(self) -> None:
        #TODO
        pass

    def output(self,st, color, background=False, bright=False): 
        """
        - color - ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        - background - True or False default is False
        - bright - True or False default is False
        source: https://github.com/geohot/tinygrad/blob/d26345595d8359c8e0f49fa5645c33f2b9a6b12d/tinygrad/helpers.py#L9
        

        """
        # print(f"\u001b[{10*background+60*bright+30+['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color)}m{st}\u001b[0m")
        return f"\u001b[{10*background+60*bright+30+['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color)}m{st}\u001b[0m"  # replace the termcolor library with one line


    def inputs_to_set(self,inputSymbols):
        """Takes in the parameters passed to *args and puts them in a set and a list.
        The set will make sure there are no duplicates, and then the list will keep
        the original order of the input.

        :param inputSymbols: A list, dict, or tuple of stock tickers.
        :type inputSymbols: list or dict or tuple or str
        :returns:  A list of strings that have been capitalized and stripped of white space.
        
        code reference:https://github.com/jmfernandes/robin_stocks/blob/8359444cb75e050662520aebef8a9c1bdb26bf1c/robin_stocks/robinhood/helper.py#L203
        """

        symbols_list = []
        symbols_set = set()

        def add_symbol(symbol):
            symbol = symbol.upper().strip()
            if symbol not in symbols_set:
                symbols_set.add(symbol)
                symbols_list.append(symbol)

        if type(inputSymbols) is str:
            add_symbol(inputSymbols)
        elif type(inputSymbols) is list or type(inputSymbols) is tuple or type(inputSymbols) is set:
            inputSymbols = [comp for comp in inputSymbols if type(comp) is str]
            for item in inputSymbols:
                add_symbol(item)

        return(symbols_list)


    def additional_information(self,asset):
        for equity in asset:
            ticker = equity['equity']
            instruments = r.get_instruments_by_symbols(inputSymbols=ticker)    
            if not instruments:
                instruments = [{
                    
                    'simple_name': {'error': 'either robinhood is down,ticker is invalid, or the ticker is not supported, or robinhood went out of business.'},
                    'tradeable':  {'error': 'either robinhood is down,ticker is invalid, or the ticker is not supported, or robinhood went out of business.'},
                     'tradability': {'error': 'either robinhood is down,ticker is invalid, or the ticker is not supported, or robinhood went out of business.'}
                }]            
            for instrument in instruments:
                equity['simple_name'] = instrument['simple_name']
                equity['tradeable'] = instrument['tradeable']
                equity['tradability'] = instrument['tradability']
                equity['success'] = True
            
        
        
        print(asset)
        # return asset
        
        
        
        

            
        # equity['simple_name'] = instruments[0]['name']
        # equity['tradeable'] = instruments[0]['tradeable']
        # equity['tradability'] = instruments[0]['tradability']
        # equity['success'] = True
        # return equity
        
      

    # def return_results(self,information,tickers,interval):
    #     """Given a json object and it will assert that the information is correct and then return a list of dictionaries
    #         that contain the information.
    #     """
    #     results = []
    #     count = 0
    #     total = len(tickers) 
    #     for i in range(len(information)):
    #         count += 1
    #         # if VERBOSE:
    #         #     print(self.output(f"\nStock: {information[i]['equity']} | Buy: {information[i]['buy_price']} | Sell: {information[i]['sell_price']} Side: {information[i]['side']}", color='white', bright=True))
    #         dataList = self.include_additional_information(information[i])
    #         results.append({dataList['ticker']:dataList})
    #         if count == total:
    #             if VERBOSE:
    #                 print(self.output(f"added to list: {results}", color='white', bright=True))
    #             # with open(f'{project_dir}/fractional.json', 'w') as outfile:
    #             #     json.dump(dataLists, outfile)
    #         else:
    #             continue
    #     return results





source = cli()    
parser = argparse.ArgumentParser(description='Automating Technical Analysis')
# parser.add_argument('-v','--version', action='store_true', help='show the version of Automating Technical Analysis')
parser.add_argument('-p','--path', action='store_true', help='show the path of the Automating Technical Analysis directory')
parser.add_argument('-d','--null', action='store_true', help='verbose mode')
parser.add_argument('-cd','--cddir', action='store_true', help='change directory to the Automating Technical Analysis directory')
parser.add_argument('-ta','--technical',help=f'generates ticker predictions', nargs='+', default=None)
parser.add_argument('-r', help='risk level', nargs=1, default=['Low'])
parser.add_argument('-i', help='interval', nargs=1, default= ['1 Day'])
parser.add_argument('-asset', help='provide an asset if none is given Default to cli_config.ini file', nargs=1, default=[config['default_asset']['asset_type']])
args = parser.parse_args()
if args.path:
    if VERBOSE:
        print(source.output(f'calling from current working directory: {CURRENT_WORKING_DIR}', color='yellow'))
    sys.exit(0)
if args.cddir:
    # matching = [s for s in os.listdir(directory_name) if "automating-technical-analysis" in s] bad idea.. what if its something else.
    if VERBOSE:
        print(source.output(f'project directory: {directory}', color='yellow'))
    subprocess.call(f'bash {directory}/setup.sh directory_change {directory}', shell=True)
    sys.exit(0)

    

def predict():
    # it takes a while to load due to keras... so we only load it when we need it.
    # from  cli.Trade import predict_direction
    if args.technical:
        try:
            symbol = args.technical[0].split(',') if args.technical else []
            loss_intervals = args.i
            potential_risk = args.r
            assest_ticker = source.inputs_to_set(symbol)
            asset_types = args.asset
        except Exception as e:
            print(source.output(f'error: {e}', color='red',bright=True))
            sys.exit(1)
        if VERBOSE:
            print(source.output(f'\npredicting: {asset_types}: {assest_ticker} interval: {loss_intervals} risk: {potential_risk}', color='white',bright=True))
        # everything from this point is handled by automated-technical-analysis.
        # direction = predict_direction(stock=assest_ticker, interval=loss_intervals, risk=potential_risk,asset=asset_types, verbose=VERBOSE,cli_file=config)
        assest = [{'equity': 'UCO', 'current_price': '22.75', 'side': 'buy', 'confidence': '80.1% confident', 'requested_prediction_price': '23.28', 'buy_price': '22.66', 'sell_price': '23.51', 'forecast_score': '98.2% confident', 'date_used_for_analysis': '2023-05-12 00:00:00', 'interval': '1 Day', 'date_generated': '05-13-2023', 'time_generated': '11:42:40 PM'}, {'equity': 'AAPL', 'current_price': '172.57', 'side': 'hold', 'confidence': '80.8% confident', 'requested_prediction_price': '170.67', 'buy_price': '171.37', 'sell_price': '173.71', 'forecast_score': '96.3% confident', 'date_used_for_analysis': '2023-05-12 00:00:00', 'interval': '1 Day', 'date_generated': '05-13-2023', 'time_generated': '11:42:47 PM'}]
        results = source.include_additional_information(assest)
        # results = [source.include_additional_information(item) for item in direction]
        # pprint(results)
            
            
            # print(source.output(f'\n{direction}', color='green',bright=True))
            
        # results = source.include_additional_information(direction,assest_ticker,loss_intervals)
        # print(source.output(f'\n{results}', color='white',bright=True))
        
        
        sys.exit(0)


if not len(sys.argv) > 1:
    parser.print_help()
    print('\n-v for verbose mode')    
    sys.exit(1)
    

        

