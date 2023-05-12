import os
import configparser
from  cli.Trade import predict_direction
import sys
import argparse
import subprocess

VERBOSE = [True if '-d' in sys.argv else False][0]
directory = os.path.abspath(os.path.dirname(__file__))
directory_name = os.path.dirname(os.path.dirname(directory))
config = configparser.ConfigParser()
config.read(os.path.join('cli_config.ini'))
CURRENT_WORKING_DIR = os.getcwd()
# check if the config file exists
if not os.path.exists(os.path.join('cli_config.ini')):
    print(f'error: {os.path.join("cli_config.ini")} does not exist')
    sys.exit(1)
        


class cli:
    def __self__(self) -> None:
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






source = cli()    
parser = argparse.ArgumentParser(description='Automating Technical Analysis')
parser.add_argument('-v','--version', action='store_true', help='show the version of Automating Technical Analysis')
parser.add_argument('-p','--path', action='store_true', help='show the path of the Automating Technical Analysis directory')
parser.add_argument('-d','--null', action='store_true', help='verbose mode')
parser.add_argument('-cd','--cddir', action='store_true', help='change directory to the Automating Technical Analysis directory')
parser.add_argument('-ta','--technical',help=f'generates ticker predictions', nargs='+', default=None)
parser.add_argument('-r', help='risk level', nargs=1, default='Low')
parser.add_argument('-i', help='interval', nargs=1, default='1 Day')
parser.add_argument('-asset', help='provide an asset if none is given Default to cli_config.ini file', nargs=1, default=config['default_asset']['asset_type'])
args = parser.parse_args()
if args.path:
    if VERBOSE:
        print(source.output(f'calling from current working directory: {CURRENT_WORKING_DIR}', color='yellow'))
    sys.exit(0)
# print(args)
if args.cddir:
    # matching = [s for s in os.listdir(directory_name) if "automating-technical-analysis" in s] bad idea.. what if its something else.
    if VERBOSE:
        print(source.output(f'project directory: {directory}', color='yellow'))
    subprocess.call(f'bash {directory}/setup.sh directory_change {directory}', shell=True)
    sys.exit(0)

    

def predict():
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
            print(source.output(f'predicting: {asset_types}: {assest_ticker} interval: {loss_intervals} risk: {potential_risk}', color='yellow',bright=True))
        # everything from this point is handled by automated-technical-analysis.
        
        predict_direction(stock=assest_ticker, interval=loss_intervals, risk=potential_risk,asset=asset_types)
        sys.exit(0)




if not len(sys.argv) > 1:
    parser.print_help()
    print('\n-v for verbose mode')    
    sys.exit(1)
    

        

