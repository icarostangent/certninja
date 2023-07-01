<?php

new AccountRoute();
class AccountRoute extends WP_REST_Controller
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
        $base = 'account';
        register_rest_route($namespace, '/author/(?P<author_id>[\d]+)/' . $base, array(
            array(
                'methods'             => 'GET',
                'callback'            => array($this, 'get_item'),
                'permission_callback' => array($this, 'get_item_permissions_check'),
                'args' => array(
                    'author_id' => array(
                        'validate_callback' => function ($param, $request, $key) {
                            return is_numeric($param);
                        },
                        'required' => true,
                    ),
                ),
            ),
        ));
    }

    /**
     * Get one item from the collection
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function get_item($request)
    {
        $params = $request->get_params();

        if ($params['author_id'] != wp_get_current_user()->ID) {
            return new WP_Error('invalid-user-id', __('message', 'text-domain'));
        }

        $query = new WP_Query(
            array(
                'post_type' => 'account',
                'post_author' => $params['author_id'],
                'posts_per_page' => 1,
            )
        );

        $account = $query->posts[0];
        $address = unserialize($account->post_content);
        // error_log('address ---------- ');
        // error_log(json_encode($address));

        if ($address) {
            $account->first_name = $address['first_name'];
            $account->last_name = $address['last_name'];
            $account->line1 = $address['line1'];
            $account->line2 = $address['line2'];
            $account->city = $address['city'];
            $account->state = $address['state'];
            $account->postal_code = $address['postal_code'];
            $account->country = $address['country'];
        }

        $user_meta = get_userdata(wp_get_current_user()->ID);
        $user_roles = $user_meta->roles;

        $account->user_role = $user_roles[1];

        return new WP_REST_Response($account, 200);
    }

    /**
     * Check if a given request has access to get a specific item
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|bool
     */
    public function get_item_permissions_check($request)
    {
        return current_user_can('read');
    }
}
