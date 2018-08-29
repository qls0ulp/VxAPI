class CliPrompts:
    @staticmethod
    def prompt_for_sharing_confirmation(args, instance_url):
        if 'nosharevt' in args:
            if args['nosharevt'] == 'no' and args['quiet'] is False:
                warning_msg = 'You are about to submit your file to all users of {} and the public.'.format(instance_url)
                if 'hybrid-analysis.com' in instance_url:
                    warning_msg += ' Please make sure you consent to the Terms and Conditions of Use and Data Privacy Policy available at: {} and {}.'.format('https://www.hybrid-analysis.com/terms', 'https://www.hybrid-analysis.com/data-protection-policy')
                warning_msg += ' [y/n]'
                submit_warning = input(warning_msg)
                if not submit_warning or submit_warning[0].lower() != 'y':
                    print('You did not indicate approval, exiting ...')
                    exit(1)

    @staticmethod
    def prompt_for_dir_content_submission(args):
        pass
        # if args['chosen_action'] == ACTION_SUBMIT_FILE:
        #     number_of_files_to_submit = len(args['file'])
        #     if args['quiet'] is False and number_of_files_to_submit > 1:
        #         warning_msg = 'Are you sure that you want to submit the content of selected directory? It contains {} of files. [y/n]'.format(number_of_files_to_submit)
        #         submit_warning = input(warning_msg)
        #         if not submit_warning or submit_warning[0].lower() != 'y':
        #             print('You did not indicate approval, exiting ...')
        #             exit(1)
