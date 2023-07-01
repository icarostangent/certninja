# Cleaner Service

This service will pop jobs off of the `deletions_register` and delete old scans from the database, where the `account->downgrade` flag is set to `false`, and based on the owners Wordpress Role.

| Role | Expiry |
| ---- | ------ |
| starter | 1 day |
| basic | 1 week |
| growth | 3 months |
| ultimate | 6 months |
