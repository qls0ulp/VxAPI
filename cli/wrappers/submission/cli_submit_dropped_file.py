from cli.wrappers.cli_caller import CliCaller


class CliSubmitDroppedFile(CliCaller):

    help_description = 'Submit dropped file for analysis by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitDroppedFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_sha256_arg('Sha256 of dropped file for analyze')
        parser_argument_builder.add_submission_no_share_third_party_opt()

