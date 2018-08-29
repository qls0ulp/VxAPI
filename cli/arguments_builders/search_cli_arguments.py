from cli.arguments_builders.default_cli_arguments import DefaultCliArguments


class SearchCliArguments(DefaultCliArguments):

    def add_search_term_filename_opt(self):
        self.parser.add_argument('--filename', type=str, help='Filename e.g. invoice.exe')

    def add_search_term_filetype_opt(self):
        self.parser.add_argument('--filetype', type=str, help='Filetype e.g. docx')

    def add_search_term_filetype_desc_opt(self):
        self.parser.add_argument('--filetype-desc', type=str, help='Filetype description e.g. PE32 executable')

    def add_search_term_env_id_opt(self):
        self.parser.add_argument('--env-id', type=int, help='Environment Id')

    def add_search_term_country_opt(self):
        self.parser.add_argument('--country', type=str, help='Country (3 digit ISO) e.g. swe')

    def add_search_term_verdict_opt(self):
        self.parser.add_argument('--verdict', type=str, help='Verdict', choices={1: 'whitelisted', 2: 'no verdict', 3: 'no specific threat', 4: 'suspicious', 5: 'malicious'})

    def add_search_term_av_detect_opt(self):
        self.parser.add_argument('--av-detect', type=str, help='AV Multiscan range e.g. 50-70 (min 0, max 100)')

    def add_search_term_vx_family_opt(self):
        self.parser.add_argument('--vx-family', type=str, help='AV Family Substring e.g. nemucod')

    def add_search_term_tag_opt(self):
        self.parser.add_argument('--tag', type=str, help='Hashtag e.g. ransomware')

    def add_search_term_port_opt(self):
        self.parser.add_argument('--port', type=str, help='Port e.g. 8080')

    def add_search_term_host_opt(self):
        self.parser.add_argument('--host', type=str, help='Host e.g. 192.168.0.1')

    def add_search_term_domain_opt(self):
        self.parser.add_argument('--domain', type=str, help='Domain e.g. checkip.dyndns.org')

    def add_search_term_url_opt(self):
        self.parser.add_argument('--url', type=str, help='HTTP Request Substring e.g. google')

    def add_search_term_similar_to_opt(self):
        self.parser.add_argument('--similar-to', type=str, help='Similar Samples e.g. <sha266>')

    def add_search_term_context_opt(self):
        self.parser.add_argument('--context', type=str, help='Sample Context e.g. <sha266>')

    def add_search_term_imp_hash_opt(self):
        self.parser.add_argument('--imphash', type=str)

    def add_search_term_ssdeep_opt(self):
        self.parser.add_argument('--ssdeep', type=str)

    def add_search_term_authentihash_opt(self):
        self.parser.add_argument('--authentihash', type=str)
