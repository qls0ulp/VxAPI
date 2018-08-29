from api.callers.api_caller import ApiCaller


class ApiOverviewSummary(ApiCaller):
    endpoint_url = '/overview/:sha256/summary'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_RESTRICTED
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
