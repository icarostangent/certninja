<?php

// define('RELOCATE',true);
define('WP_ENVIRONMENT_TYPE', 'development');
define('WCPAY_DEV_MODE', true);

// JWT Authentication for WP REST API
define('JWT_AUTH_SECRET_KEY', 'd0e2c26f0ff9dec41d92f434657661de');
define('JWT_AUTH_CORS_ENABLE', true);

define('WP_HOME', getenv('TARGET_URL'));
define('WP_SITEURL', getenv('TARGET_URL'));

define('DB_NAME', getenv('WORDPRESS_DB_NAME'));

define('STRIPE_SECRET_KEY', getenv('STRIPE_SECRET_KEY'));
define('STRIPE_PUBLISHABLE_KEY', getenv('STRIPE_PUBLISHABLE_KEY'));
define('STRIPE_WEBHOOK_SECRET', getenv('STRIPE_WEBHOOK_SECRET'));
define('STRIPE_PRODUCTS', [
	'starter' => [
		'amount' => 0,
		'price_id' => '00000',
	], 
	'basic' => [
		'amount' => 300,
		'price_id' => 'price_1LEGKsLdajT7Ku5XW8m9jgn2'
	], 
	'growth' => [
		'amount' => 1200,
		'price_id' => 'price_1LEGKhLdajT7Ku5XQydPvL1C'
	], 
	'ultimate' => [
		'amount' => 3000,
		'price_id' => 'price_1LEGKSLdajT7Ku5XLQ0Ppf52'
	], 
]);


// If we're behind a proxy server and using HTTPS, we need to alert Wordpress of that fact
// see also http://codex.wordpress.org/Administration_Over_SSL#Using_a_Reverse_Proxy
// if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
//     $_SERVER['HTTPS'] = 'on';

//     // Force SSL in admin.
//     define('FORCE_SSL_ADMIN', true);
// }

/**

 * The base configuration for WordPress

 *

 * The wp-config.php creation script uses this file during the installation.

 * You don't have to use the web site, you can copy this file to "wp-config.php"

 * and fill in the values.

 *

 * This file contains the following configurations:

 *

 * * MySQL settings

 * * Secret keys

 * * Database table prefix

 * * ABSPATH

 *

 * This has been slightly modified (to read environment variables) for use in Docker.

 *

 * @link https://wordpress.org/support/article/editing-wp-config-php/

 *

 * @package WordPress

 */



// IMPORTANT: this file needs to stay in-sync with https://github.com/WordPress/WordPress/blob/master/wp-config-sample.php

// (it gets parsed by the upstream wizard in https://github.com/WordPress/WordPress/blob/f27cb65e1ef25d11b535695a660e7282b98eb742/wp-admin/setup-config.php#L356-L392)



// a helper function to lookup "env_FILE", "env", then fallback

if (!function_exists('getenv_docker')) {

	// https://github.com/docker-library/wordpress/issues/588 (WP-CLI will load this file 2x)

	function getenv_docker($env, $default)
	{

		if ($fileEnv = getenv($env . '_FILE')) {

			return rtrim(file_get_contents($fileEnv), "\r\n");
		} else if (($val = getenv($env)) !== false) {

			return $val;
		} else {

			return $default;
		}
	}
}



// ** MySQL settings - You can get this info from your web host ** //

/** The name of the database for WordPress */

define('DB_NAME', getenv_docker('WORDPRESS_DB_NAME', 'wordpress'));



/** MySQL database username */

define('DB_USER', getenv_docker('WORDPRESS_DB_USER', 'example username'));



/** MySQL database password */

define('DB_PASSWORD', getenv_docker('WORDPRESS_DB_PASSWORD', 'example password'));



/**

 * Docker image fallback values above are sourced from the official WordPress installation wizard:

 * https://github.com/WordPress/WordPress/blob/f9cc35ebad82753e9c86de322ea5c76a9001c7e2/wp-admin/setup-config.php#L216-L230

 * (However, using "example username" and "example password" in your database is strongly discouraged.  Please use strong, random credentials!)

 */



/** MySQL hostname */

define('DB_HOST', getenv_docker('WORDPRESS_DB_HOST', 'mysql'));



/** Database charset to use in creating database tables. */

define('DB_CHARSET', getenv_docker('WORDPRESS_DB_CHARSET', 'utf8'));



/** The database collate type. Don't change this if in doubt. */

define('DB_COLLATE', getenv_docker('WORDPRESS_DB_COLLATE', ''));



/**#@+

 * Authentication unique keys and salts.

 *

 * Change these to different unique phrases! You can generate these using

 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.

 *

 * You can change these at any point in time to invalidate all existing cookies.

 * This will force all users to have to log in again.

 *

 * @since 2.6.0

 */

define('AUTH_KEY',         getenv_docker('WORDPRESS_AUTH_KEY',         'eccd0f29b1b32a414ca2aca4c6ad6829335e07b4'));

define('SECURE_AUTH_KEY',  getenv_docker('WORDPRESS_SECURE_AUTH_KEY',  '96676ae7a04dd2279fcce48fe35e048c4f795226'));

define('LOGGED_IN_KEY',    getenv_docker('WORDPRESS_LOGGED_IN_KEY',    '9d6e43db7cd46c9d1d2ac3c94173a2d0f0f86b0d'));

define('NONCE_KEY',        getenv_docker('WORDPRESS_NONCE_KEY',        '1c401f1c5b0d5eca6e528074620f80a648fb99f2'));

define('AUTH_SALT',        getenv_docker('WORDPRESS_AUTH_SALT',        'ba3edc664e65ac0065ab988aa222f044fdeb1538'));

define('SECURE_AUTH_SALT', getenv_docker('WORDPRESS_SECURE_AUTH_SALT', '222410bf42b4bfcc849eceee696753ef5f6bcc52'));

define('LOGGED_IN_SALT',   getenv_docker('WORDPRESS_LOGGED_IN_SALT',   '5315e724ce2084eab3262088d7217b4b024a2341'));

define('NONCE_SALT',       getenv_docker('WORDPRESS_NONCE_SALT',       '4c885e3062d2052670ecd46829da9fca6db61e5c'));

// (See also https://wordpress.stackexchange.com/a/152905/199287)



/**#@-*/



/**

 * WordPress database table prefix.

 *

 * You can have multiple installations in one database if you give each

 * a unique prefix. Only numbers, letters, and underscores please!

 */

$table_prefix = getenv_docker('WORDPRESS_TABLE_PREFIX', 'wp_');



/**

 * For developers: WordPress debugging mode.

 *

 * Change this to true to enable the display of notices during development.

 * It is strongly recommended that plugin and theme developers use WP_DEBUG

 * in their development environments.

 *

 * For information on other constants that can be used for debugging,

 * visit the documentation.

 *

 * @link https://wordpress.org/support/article/debugging-in-wordpress/

 */

define('WP_DEBUG', !!getenv_docker('WORDPRESS_DEBUG', 'true'));



/* Add any custom values between this line and the "stop editing" line. */



// If we're behind a proxy server and using HTTPS, we need to alert WordPress of that fact

// see also https://wordpress.org/support/article/administration-over-ssl/#using-a-reverse-proxy

if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false) {

	$_SERVER['HTTPS'] = 'on';
}

// (we include this by default because reverse proxying is extremely common in container environments)



if ($configExtra = getenv_docker('WORDPRESS_CONFIG_EXTRA', '')) {

	eval($configExtra);
}



/* That's all, stop editing! Happy publishing. */



/** Absolute path to the WordPress directory. */

if (!defined('ABSPATH')) {

	define('ABSPATH', __DIR__ . '/');
}



/** Sets up WordPress vars and included files. */

require_once ABSPATH . 'wp-settings.php';
