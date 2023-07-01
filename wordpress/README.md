# Wordpress Service

Backend layer, facilitates interaction with the Database Service, and with the Redis Service, and provides an API.

## Models
### User
Base wordpress `user` model with some `usermeta` added

### Account
Custom Post Type, Stores information about an `account`
| field | mapping | Description |
| ----- | ------- | ----------- |
| ID |
| post_author |
| post_date |
| post_date_gmt |
| post_content |
| post_title | activated |
| post_excerpt | stripe customer id |
| post_status |
| comment_status |
| ping_status |
| post_password |
| post_name |
| to_ping |
| pinged |
| post_modified |
| post_modified_gmt |
| post_content_filtered |
| post_parent |
| guid |
| menu order |
| post_type |
| post_mime_type |
| comment_count |

### Domain
Custom Post Type, Stores information about a `domain`
| field | mapping | Description |
| ----- | ------- | ----------- |
| ID | Domain ID |
| post_author | User ID |
| post_date | |
| post_date_gmt | |
| post_content | Last scan JSON Output |
| post_title | Domain Name |
| post_excerpt | IP:PORT string |
| post_status | |
| comment_status | |
| ping_status | |
| post_password | |
| post_name | |
| to_ping | |
| pinged | |
| post_modified | |
| post_modified_gmt | |
| post_content_filtered | |
| post_parent | |
| guid | |
| menu order | |
| post_type | |
| post_mime_type | |
| comment_count | |


### Scan
Custom Post Type, Stores information about a `scan`
| field | mapping | Description |
| ----- | ------- | ----------- |
| ID | Scan ID |
| post_author | User ID |
| post_date | |
| post_date_gmt | |
| post_content | JSON Output |
| post_title | Domain ID |
| post_excerpt | |
| post_status | |
| comment_status | |
| ping_status | |
| post_password | |
| post_name | Scan UUID |
| to_ping | |
| pinged | |
| post_modified | |
| post_modified_gmt | |
| post_content_filtered | |
| post_parent | |
| guid | |
| menu order | |
| post_type | |
| post_mime_type | |
| comment_count | |
