#!/usr/bin/env python3
import sys
import traceback

from sys import platform

try:
    import colorama
    from colorama import init
except ImportError as exc:
    print('\nScript need \'colorama\' module to work. Read README.md to resolve the issue \n')
    exit(1)

if platform == 'win32':
    init()

from colors import Color

if sys.version_info < (3, 4, 0):
    print(Color.error('\nYou need python 3.4 or later to run this script. Possibly you should start the command from calling \'python3\' instead of \'python\'\n'))
    exit(1)

try:
    import requests
except ImportError as exc:
    print(Color.error('\nScript need \'requests\' module to work. Read README.md to resolve the issue \n'))
    exit(1)

try:  # Suppress requests warning connected with disabled verify. Needed only in python 3.5. In python 3.4 that package doesn't exist and message is not visible
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError as exc:
    pass

import argparse
import logging

from constants import *
from exceptions import *

import datetime
import os.path
import json

from collections import OrderedDict
# import cli.arguments_builders

from api.callers.api_caller import ApiCaller

from api.callers.search import *
from cli.wrappers.search import *

from api.callers.key import *
from cli.wrappers.key import *

from cli.arguments_builders import *

from cli.cli_helper import CliHelper
from cli.cli_msg_printer import CliMsgPrinter
from cli.cli_prompts import CliPrompts

from _version import __version__

from copy import copy, deepcopy

def main():

    try:
        # TODO - test the moment when some file privileges are missing....
        # logging.basicConfig(filename='cli.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        # logging.debug('This message should go to the log file')
        # logging.info('So should this')
        # logging.warning('And this, too')

        if os.path.exists('config.py'):
            from config import get_config
            config = get_config()
        else:
            raise MissingConfigurationError('Configuration is missing. Before running CLI, please copy the file \'config_tpl.py\' from current dir, rename it to \'config.py\', and fill')

        program_name = 'VxWebService Python API Connector'
        program_version = __version__
        vxapi_cli_headers = {'User-agent': 'VxApi CLI Connector'}

        if config['server'].endswith('/'):
            config['server'] = config['server'][:-1]

        if config['server'].endswith('vxstream-sandbox.com'):
            config['server'] = config['server'].replace('vxstream-sandbox.com', 'falcon-sandbox.com')


        map_of_available_actions = OrderedDict([
            # (ACTION_GET_API_LIMITS, CliApiLimitsSummary(ApiApiLimitsSummary(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_API_QUERY_LIMITS, CliApiQueryLimits(ApiApiQueryLimits(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_API_SUBMISSION_LIMITS, CliApiSubmissionLimits(ApiApiSubmissionLimits(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_ENVIRONMENTS, CliEnvironments(ApiEnvironments(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_FEED, CliFeed(ApiFeed(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_NSSF_FILES, CliNssfDownload(ApiNssfDownload(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_NSSF_LIST, CliNssfList(ApiNssfList(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_RELATIONSHIPS, CliRelationships(ApiRelationships(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_RESULT, CliResult(ApiResult(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SAMPLE_DROPPED_FILES, CliSampleDroppedFiles(ApiSampleDroppedFiles(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SAMPLE_SCREENSHOTS, CliSampleScreenshots(ApiSampleScreenshots(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SCAN, CliScan(ApiScan(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_BULK_SCAN, CliBulkScan(ApiBulkScan(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_STATE, CliState(ApiState(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SUMMARY, CliSummary(ApiSummary(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_BULK_SUMMARY, CliBulkSummary(ApiBulkSummary(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_BACKEND, CliSystemBackend(ApiSystemBackend(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_IN_PROGRESS, CliSystemInProgress(ApiSystemInProgress(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_HEARTBEAT, CliSystemHeartbeat(ApiSystemHeartbeat(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_STATE, CliSystemState(ApiSystemState(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_STATS, CliSystemStats(ApiSystemStats(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_QUEUE_SIZE, CliSystemQueueSize(ApiSystemQueueSize(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_URL_HASH, CliUrlHash(ApiUrlHash(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_REANALYZE_SAMPLE, CliReanalyze(ApiReanalyze(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SEARCH_HASH, CliSearchHash(ApiSearchHash(config['api_key'], config['server']))),
            (ACTION_SEARCH_HASHES, CliSearchHashes(ApiSearchHashes(config['api_key'], config['server']))),
            (ACTION_SEARCH_STATES, CliSearchStates(ApiSearchStates(config['api_key'], config['server']))),
            (ACTION_SEARCH_TERMS, CliSearchTerms(ApiSearchTerms(config['api_key'], config['server']))),
            # (ACTION_SEARCH_HASHES, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SEARCH_STATES, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SEARCH_TERMS, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_DROPPED_FILE, CliDroppedFileSubmit(ApiDroppedFileSubmit(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_FILE, CliSubmitFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_URL_FILE, CliSubmitUrlFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_URL, CliSubmitUrl(ApiSubmitUrl(config['api_key'], config['api_secret'], config['server']))),
        ])

        request_session = requests.Session()

        api_object_key_current = ApiKeyCurrent(config['api_key'], config['server'])
        api_object_key_current.call(request_session, vxapi_cli_headers)
        api_key_current_response = api_object_key_current.get_api_response()
        api_key_current_response_headers = api_key_current_response.headers
        api_object_key_current.call(request_session, vxapi_cli_headers)
        api_key_data_json_response = api_object_key_current.get_response_json()

        if api_object_key_current.get_response_status_code() != 200 or bool(api_key_data_json_response) is False:
            base_error_message = 'Can\'t retrieve data for given API Key \'{}\' in the webservice: \'{}\'. Response status code: \'{}\''.format(config['api_key'], config['server'], api_object_key_current.get_response_status_code())
            if 'message' in api_key_data_json_response:
                base_error_message += '. Response message: \'{}\''.format(api_key_data_json_response['message'])

            raise RetrievingApiKeyDataError(base_error_message)

        used_api_key_data = api_key_data_json_response
        parser = argparse.ArgumentParser(description=program_name, formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
        parser.add_argument('--version', '-ver', action='version', version='{} - version {}'.format(program_name, program_version))
        DefaultCliArguments(parser).add_help_argument()

        subparsers = parser.add_subparsers(help='Action names for \'{}\' auth level'.format(used_api_key_data['auth_level_name']), dest="chosen_action")

        for name, cli_object in map_of_available_actions.items():
            if cli_object.api_object.endpoint_auth_level <= used_api_key_data['auth_level']:
                child_parser = subparsers.add_parser(name=name, help=cli_object.help_description, add_help=False)
                cli_object.add_parser_args(child_parser)

        args = vars(parser.parse_args())

        if args['chosen_action'] is not None:
            args_iterations = []
            if_multiple_calls = True if args['chosen_action'] == ACTION_SUBMIT_FILE and len(args['file']) > 1 else False
            if args['chosen_action'] == ACTION_SUBMIT_FILE:
                for file in args['file']:
                    arg_iter = args.copy()
                    arg_iter['file'] = file
                    args_iterations.append(arg_iter)
            else:
                args_iterations = [args]

            cli_object = map_of_available_actions[args['chosen_action']]

            if args['verbose'] is True:
                cli_object.init_verbose_mode()
                start_msg = 'Running \'{}\' in version \'{}\'. Webservice version: \'{}\', API version: \'{}\''.format(program_name, program_version, api_key_current_response_headers['Webservice-Version'], api_key_current_response_headers['Api-Version'])
                print(Color.control(start_msg))

            CliPrompts.prompt_for_dir_content_submission(args)
            CliPrompts.prompt_for_sharing_confirmation(args, config['server'])
            CliHelper.check_if_version_is_supported(args, api_key_current_response_headers['Webservice-Version'], config['server'])
            submission_limits = json.loads(api_key_current_response_headers['Submission-Limits']) if 'Submission-Limits' in api_key_current_response_headers else {}
            api_limits = json.loads(api_key_current_response_headers['Api-Limits'])

            for index, arg_iter in enumerate(args_iterations):
                cli_object.attach_args(arg_iter)

                if api_limits['limit_reached'] is True:
                    raise ReachedApiLimitError('Exceeded maximum API requests per {}({}). Please try again later.'.format(api_limits['name_of_reached_limit'], api_limits['used'][api_limits['name_of_reached_limit']]))

                if arg_iter['verbose'] is True:
                    if arg_iter['chosen_action'] != ACTION_GET_API_LIMITS and (if_multiple_calls is False or index == 0):
                        if api_limits['used']:
                            api_usage = OrderedDict()
                            api_usage_limits = api_limits['limits']
                            is_api_limit_reached = False

                            for period, used_limit in api_limits['used'].items():
                                # Given request is made after checking api limits. It means that we have to add 1 to current limits, to simulate that what happen after making requested API call TODO - check that logic
                                api_usage[period] = used_limit + 1
                                if is_api_limit_reached is False and api_usage[period] == api_usage_limits[period]:
                                    is_api_limit_reached = True

                            print(Color.control('API Limits for used API Key'))
                            print('Webservice API usage limits: {}'.format(api_usage_limits)) # TODO - add submission limits there
                            print('Current API usage: {}'.format(json.dumps(api_usage)))
                            print('Is limit reached: {}'.format(Color.success('No') if is_api_limit_reached is False else Color.error('Yes')))

                    if if_multiple_calls is False or index == 0:
                        print(Color.control('Used API Key'))
                        print('API Key: {}'.format(used_api_key_data['api_key']))
                        print('Auth Level: {}'.format(used_api_key_data['auth_level_name']))
                        if used_api_key_data['user'] is not None:
                            print('User: {} ({})'.format(used_api_key_data['user']['name'], used_api_key_data['user']['email']))

                    if arg_iter['chosen_action'] == ACTION_SUBMIT_FILE:
                        if if_multiple_calls is True and index == 0:
                            print(Color.control('Starting the process of sending multiple files ...'))

                        cli_object.attach_file(arg_iter['file'])

                    CliMsgPrinter.print_call_info(cli_object)
                elif arg_iter['chosen_action'] == ACTION_SUBMIT_FILE:
                    cli_object.attach_file(arg_iter['file'])

                try:
                    cli_object.api_object.call(request_session, vxapi_cli_headers)
                except Exception as e:
                    if if_multiple_calls is True:
                        CliMsgPrinter.print_error_info(e)
                    else:
                        raise e

                if arg_iter['verbose'] is True:
                    print(Color.control('Received response at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                    print('Response status code: {}'.format(cli_object.get_colored_response_status_code()))
                    print('Message: {}'.format(cli_object.get_colored_prepared_response_msg()))
                    show_response_msg = 'Showing response'
                    if if_multiple_calls is True:
                        show_response_msg = '{} for file \'{}\''.format(show_response_msg, arg_iter['file'].name)
                    print(Color.control(show_response_msg))
                elif if_multiple_calls:
                    print(Color.control(arg_iter['file'].name))

                print(cli_object.get_result_msg())

                if cli_object.api_object.if_request_success() is False and if_multiple_calls is True and cli_object.api_object.api_expected_data_type == ApiCaller.CONST_EXPECTED_DATA_TYPE_JSON:
                    response_json = cli_object.api_object.get_response_json()
                    if 'response_code' in response_json and 'Exceeded maximum API requests' in response_json['response']['error']:
                        raise Exception('Requests exceeded maximum API requests, the rest of the unsubmitted files won\'t be processed, exiting ...')
                cli_object.do_post_processing()

                if arg_iter['verbose'] is True:
                    print('\n')
        else:
            print(Color.control('No option was selected. To check CLI options, run script in help mode: \'{} -h\''.format(__file__)))
    except Exception as e:
        CliMsgPrinter.print_error_info(e)

if __name__ == "__main__":
    main()

