# Scanner Service

This service will pop jobs off of the `domains_register` queue and perform a scan, commiting results to the database service, and resetting the scan status on the parent domain.
