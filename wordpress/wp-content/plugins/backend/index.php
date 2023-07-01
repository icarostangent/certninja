<?php
/**
*  Plugin Name:       backend
*  Author:            icarostangent
*  
**/

include( plugin_dir_path( __FILE__ ) . '/jwt-authentication-for-wp-rest-api/jwt-auth.php');
include( plugin_dir_path( __FILE__ ) . 'hooks.php');
include( plugin_dir_path( __FILE__ ) . 'roles.php');
include( plugin_dir_path( __FILE__ ) . 'admin.php');
include( plugin_dir_path( __FILE__ ) . 'cron.php');
include( plugin_dir_path( __FILE__ ) . 'api/DomainRoute.php');
include( plugin_dir_path( __FILE__ ) . 'api/ScanRoute.php');
include( plugin_dir_path( __FILE__ ) . 'api/ThemeRoute.php');
include( plugin_dir_path( __FILE__ ) . 'api/UserRoute.php');
include( plugin_dir_path( __FILE__ ) . 'api/AccountRoute.php');

?>
