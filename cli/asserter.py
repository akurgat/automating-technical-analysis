import os
import configparser
import sys
import argparse
import subprocess
import robin_stocks.robinhood as r
from traceback import print_tb
from pprint import pprint
import json


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
                
        # check of no errors
        found_error = [True if 'error' in erorr else None for erorr in instruments].pop()
        if found_error == True:
            equity['success'] = False
        else:
            equity['success'] = True
            
        return asset
        
        
        
        
        



source = cli()    
parser = argparse.ArgumentParser(description='Automating Technical Analysis')
parser.add_argument('-p', '--path', action='store_true', help='show the path of the Automating Technical Analysis directory')
parser.add_argument('-d', '--null', action='store_true', help='verbose mode')
parser.add_argument('-cd', '--cddir', action='store_true', help='change directory to the Automating Technical Analysis directory')


parser.add_argument('-ta', '--tickers', nargs='+', type=str, action='append', help='Ticker symbols')
parser.add_argument('-f', '--quick', type=str, action='append', help='just provide the ticker symbols and the program will do the rest using default values')
parser.add_argument('-r', '--risk', type=str, action='append', help='Risk level')
parser.add_argument('-i', '--interval', type=str, action='append', help='Interval')
parser.add_argument('-asset', '--asset', type=str, action='append', help='Asset type')
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

    

def return_paramenter(symbols):
    output = {}
    analysis_risk = ['Low', 'Medium', 'High']
    analysis_interval = ['5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day', '1 Week']
    
    defualt_risks = 'High'
    defualt_interval = '1 Day'
    defualt_asset = 'Stocks'
    if args.tickers:
        equity = args.tickers
    else:
        equity = list(map(lambda x: [x], symbols))
    
    for ticker_index, ticker in enumerate(equity):
        ticker_data = {}
        if args.risk and len(args.risk) > ticker_index:
            ticker_data['risk'] = args.risk[ticker_index].capitalize()
        else:
            ticker_data['risk'] = defualt_risks
            
        if args.interval and len(args.interval) > ticker_index:
            ticker_data['interval'] = args.interval[ticker_index]
        else:
            ticker_data['interval'] = defualt_interval
            
        if args.asset and len(args.asset) > ticker_index:
            ticker_data['asset'] = args.asset[ticker_index]
        else:
            ticker_data['asset'] = defualt_asset
        output[ticker[0]] = ticker_data

    # Convert the JSON output to a string
    output_json = json.dumps(output, indent=4)
    if VERBOSE:
        print(source.output(f'REQUESTED prediction:\n{output_json}', color='yellow'))
    return output

    




def predict():
    if args.quick:
        try:
            symbol = args.quick[0].split(',') if args.quick else []
        except Exception as e:
            print(source.output(f'error: {e}', color='red',bright=True))
        assest_ticker = source.inputs_to_set(symbol)
        asset = return_paramenter(assest_ticker)
    elif args.tickers:
        asset = return_paramenter(args.tickers)
    try:
        from  cli.Trade import predict_direction
        returned_assets = predict_direction(asset,file=config)
        results = source.additional_information(returned_assets)
        # pprint(results)
        
        # print(source.output(f'\n{results}', color='white',bright=True))
    except Exception as e:
        print(source.output(f'error: {e}', color='red',bright=True))
        sys.exit(1)
    # don't really need to return anything, but for the future, this may be useful for api calls.
    pprint(results)
    # return results
        
        
        # results = source.additional_information(asset)
        # print(results)
        
        # results = [source.include_additional_information(item) for item in direction]
        # pprint(results)
            
            
            # print(source.output(f'\n{direction}', color='green',bright=True))
            
        # results = source.include_additional_information(direction,assest_ticker,loss_intervals)
        # print(source.output(f'\n{results}', color='white',bright=True))
        
        
        # sys.exit(0)


if not len(sys.argv) > 1:
    parser.print_help()
    print('\n-v for verbose mode')    
    sys.exit(1)
    

        

