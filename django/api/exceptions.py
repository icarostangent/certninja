from rest_framework.exceptions import APIException


class DomainIDRequired(APIException):
    status_code = 400
    default_detail = 'Domain id required.'
    default_code = 'domain_id_required'

class DomainNotFound(APIException):
    status_code = 400
    default_detail = 'Domain not found.'
    default_code = 'domain_not_found'

class DomainLimitExceeded(APIException):
    status_code = 400
    default_detail = 'Domain limit exceeded for subscription.'
    default_code = 'domain_limit_exceeded'

class AccountInactive(APIException):
    status_code = 400
    default_detail = 'Account is not active.'
    default_code = 'account_inactive'