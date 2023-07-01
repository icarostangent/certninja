<?php


new UserRoute();
class UserRoute extends WP_REST_Controller
{
    public function __construct()
    {
        add_action('rest_api_init', [$this, 'register_routes']);
    }

    /**
     * Register the routes for the objects of the controller.
     */
    public function register_routes()
    {
        $version = '1';
        $namespace = 'backend/v' . $version;
        $base = 'user';

        register_rest_route($namespace, '/' . $base . '/register', array(
            'methods' => 'POST',
            'callback' => array($this, 'register'),
            'permission_callback' => '__return_true',
        ));
        register_rest_route($namespace, '/' . $base . '/(?P<author_id>[\d]+)/activate', array(
            'methods' => 'POST',
            'callback' => array($this, 'activate'),
            'permission_callback' => '__return_true',
            'args' => array(
                'author_id' => array(
                    'validate_callback' => function ($param, $request, $key) {
                        return is_numeric($param);
                    },
                    'required' => true,
                ),
            ),
        ));
        register_rest_route($namespace, '/' . $base . '/request', array(
            'methods' => 'POST',
            'callback' => array($this, 'request'),
            'permission_callback' => '__return_true',
        ));
        register_rest_route($namespace, '/' . $base . '/(?P<author_id>[\d]+)/reset', array(
            'methods' => 'POST',
            'callback' => array($this, 'reset'),
            'permission_callback' => '__return_true',
            'args' => array(
                'author_id' => array(
                    'validate_callback' => function ($param, $request, $key) {
                        return is_numeric($param);
                    },
                    'required' => true,
                ),
            ),
        ));
    }

    /**
     * Create a new user and send email notification
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function register($request)
    {
        $params = $request->get_params();

        if (!$params['username'] || !$params['email'] || !$params['password']) {
            return new WP_Error('missing-parameters', __('message', 'text-domain'));
        }
        //TODO: validate password complexity

        $user_id = wc_create_new_customer(
            $params['email'],
            $params['username'],
            $params['password'],
            [
                'user_activation_key' => sha1($params['username'] . time()),
            ]
        );
        // $user_id = wp_insert_user(
        //     array(
        //         'user_login' => $params['username'],
        //         'user_email' => $params['email'],
        //         'user_pass' => $params['password'],
        //         'user_activation_key' => sha1($params['username'] . time()),
        //     )
        // );

        if (!$user_id || is_wp_error($user_id)) {
            return new WP_Error('cant-create-user', __('message', 'text-domain'));
        }

        $account_id = wp_insert_post(
            array(
                'post_type' => 'account',
                'post_author' => $user_id,
                'post_status' => 'publish',
                'post_content' => '', // serialized billing address
                'post_title' => 'false', // activated
                'post_excerpt' => '', // stripe customer id
            )
        );

        if (!$account_id || is_wp_error($account_id)) {
            return new WP_Error('cant-create-account', __('message', 'text-domain'));
        }

        $user = get_user_by('ID', $user_id);
        $user->set_role('starter');

        $data = array();
        $data['id'] = $user->ID;
        $data['user_activation_key'] = $user->user_activation_key;
        $data['username'] = $user->user_login;
        $data['email'] = $user->user_email;
        $data['registered'] = $user->user_registered;

        $redis = new Redis();
        $redis->connect('redis', 6379);
        $redis->rpush('new_user_register', json_encode($data));
        return new WP_REST_Response(200);
    }

    /**
     * Activate a User 
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function activate($request)
    {
        $params = $request->get_params();

        if (!$params['author_id'] || !$params['key']) {
            return new WP_Error('missing-parameters', __('message', 'text-domain'));
        }

        $user = get_user_by('ID', $params['author_id']);
        if (!$user || is_wp_error($user)) {
            return new WP_Error('invalid-user', __('message', 'text-domain'));
        }

        $query = new WP_Query(
            array(
                'post_type' => 'account',
                'post_author' => $params['author_id'],
                'posts_per_page' => 1,
            )
        );

        $account = $query->posts[0];

        if ($account->post_title == 'true') { // activated
            return new WP_REST_Response(200);
        }

        if ($params['key'] != $user->user_activation_key) {
            return new WP_Error('invalid-activation-key', __('message', 'text-domain'));
        }

        $post_id = wp_update_post(
            array(
                'ID' => $account->ID,
                'post_title' => 'true',
            )
        );
        if (!$post_id || is_wp_error($post_id)) {
            return new WP_Error('error-updating-account', __('message', 'text-domain'));
        }

        return new WP_REST_Response(200);
    }

    /**
     *  Request user password reset email
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function request($request)
    {
        $params = $request->get_params();
        $user = get_user_by('email', $params['email']);

        if (!$user || is_wp_error($user)) {
            return new WP_Error('invalid-email', __('message', 'text-domain'));
        }

        $reset_key = get_password_reset_key($user);
        update_user_meta($user->ID, 'reset_key', $reset_key);

        $data = array();
        $data['id'] = $user->ID;
        $data['reset_key'] = $reset_key;
        $data['username'] = $user->user_login;
        $data['email'] = $user->user_email;

        $redis = new Redis();
        $redis->connect('redis', 6379);
        $redis->rpush('password_reset_register', json_encode($data));

        return new WP_REST_Response(200);
    }

    /**
     * Submit user password reset 
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function reset($request)
    {
        $params = $request->get_params();
        $user = get_user_by('ID', $params['id']);

        if (!$user || is_wp_error($user)) {
            return new WP_Error('invalid-user-id', __('message', 'text-domain'));
        }

        if (!$params['key'] || get_user_meta($user->ID, 'reset_key', $single = true) != $params['key']) {
            return new WP_Error('invalid-reset_key', __('message', 'text-domain'));
        }

        if (!$params['password']) {
            return new WP_Error('missing-password-field', __('message', 'text-domain'));
        }

        if (!$params['passwordConfirm']) {
            return new WP_Error('missing-password-confirm-field', __('message', 'text-domain'));
        }

        if ($params['password'] != $params['passwordConfirm']) {
            return new WP_Error('passwords-must-match', __('message', 'text-domain'));
        }
        // TODO: validate password

        wp_set_password($params['password'], $user->ID);
        delete_user_meta($user->ID, 'reset_key');

        return new WP_REST_Response('true', 200);
    }
}
