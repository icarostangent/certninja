<?php

new DomainRoute();
class DomainRoute extends WP_REST_Controller
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
        $base = 'domain';
        register_rest_route($namespace, '/author/(?P<author_id>[\d]+)/' . $base, array(
            array(
                'methods'             => 'GET',
                'callback'            => array($this, 'get_items'),
                'permission_callback' => array($this, 'get_items_permissions_check'),
                'args' => array(
                    'author_id' => array(
                        'validate_callback' => function ($param, $request, $key) {
                            return is_numeric($param);
                        },
                        'required' => true,
                    ),
                    'page' => array(
                        'required' => false,
                    ),
                ),
            ),
            array(
                'methods'             => 'POST',
                'callback'            => array($this, 'create_item'),
                'permission_callback' => array($this, 'create_item_permissions_check'),
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
        register_rest_route($namespace, '/author/(?P<author_id>[\d]+)/' . $base . '/(?P<domain_id>[\d]+)', array(
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
                    'domain_id' => array(
                        'validate_callback' => function ($param, $request, $key) {
                            return is_numeric($param);
                        },
                        'required' => true,
                    ),
                ),
            ),
            array(
                'methods'             => 'DELETE',
                'callback'            => array($this, 'delete_item'),
                'permission_callback' => array($this, 'delete_item_permissions_check'),
                'args' => array(
                    'author_id' => array(
                        'validate_callback' => function ($param, $request, $key) {
                            return is_numeric($param);
                        },
                        'required' => true,
                    ),
                    'domain_id' => array(
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
     * Get a collection of items
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function get_items($request)
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
        if ($account->post_title == 'false') { // activated
            return new WP_Error('user-inactive', __('message', 'text-domain'));
        }

        $query = new WP_Query(
            array(
                'post_type'         => 'domain',
                'author'            => $params['author_id'],
                'posts_per_page'    => 10,
                'paged'             => $params['page'],
                'orderby'           => 'date',
                'order'             => 'desc',
            )
        );

        $data = array(
            'items' => $query->posts,
            'totalItems' => $query->found_posts,
            'totalPages' => $query->max_num_pages,
        );

        return new WP_REST_Response($data, 200);
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

        $account_query = new WP_Query(
            array(
                'post_type' => 'account',
                'post_author' => $params['author_id'],
                'posts_per_page' => 1,
            )
        );

        $account = $account_query->posts[0];
        if ($account->post_title == 'false') { // activated
            return new WP_Error('user-inactive', __('message', 'text-domain'));
        }

        $item = get_post($params['domain_id']);

        if ($item->post_author != $params['author_id']) {
            return new WP_Error('invalid-user', __('message', 'text-domain'));
        }

        if ($item->post_type != 'domain') {
            return new WP_Error('domain-not-found', __('message', 'text-domain'));
        }

        return new WP_REST_Response($item, 200);
    }

    /**
     * Create one item from the collection
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function create_item($request)
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
        if ($account->post_title == 'false') { // activated
            return new WP_Error('user-inactive', __('message', 'text-domain'));
        }

        $ip = ($params['ip']) ? explode(':', $params['ip'])[0] : '';
        $port = ($params['ip'] && strpos($params['ip'], ':')) ? explode(':', $params['ip'])[1] : '';
        $ip_str = ($params['ip']) ? $params['ip'] : '';

        if (!$this->is_valid_domain_name($params['domain'])) {
            return new WP_Error('invalid-domain', __('message', 'text-domain'));
        }

        if ($ip && !$this->is_valid_ip_address($ip)) {
            return new WP_Error('invalid-ip', __('message', 'text-domain'));
        }

        if ($port && !$this->is_valid_port($port)) {
            return new WP_Error('invalid-port', __('message', 'text-domain'));
        }

        $query = new WP_Query(
            array(
                'post_type'         => 'domain',
                'author'            => $params['author_id'],
                'posts_per_page'    => -1,
            )
        );

        error_log(json_encode($query->post_count));
        if ($this->user_has_role(wp_get_current_user()->ID, 'starter')) {
            if ($query->post_count >= 1) {
                return new WP_Error('starter-account', __('message', 'text-domain'));
            }
        }

        if ($this->user_has_role(wp_get_current_user()->ID, 'basic')) {
            if ($query->post_count >= 5) {
                return new WP_Error('basic-account', __('message', 'text-domain'));
            }
        }

        if ($this->user_has_role(wp_get_current_user()->ID, 'growth')) {
            if ($query->post_count >= 25) {
                return new WP_Error('growth-account', __('message', 'text-domain'));
            }
        }

        if ($this->user_has_role(wp_get_current_user()->ID, 'ultimate')) {
            if ($query->post_count >= 100) {
                return new WP_Error('ultimate-account', __('message', 'text-domain'));
            }
        }

        $post_id = wp_insert_post(
            array(
                'post_type'         => 'domain',
                'post_author'       => $params['author_id'],
                'post_title'        => $params['domain'],
                'post_excerpt'      => $ip_str,
                'post_status'       => 'publish',
                'comment_status'    => 'closed',
                'ping_status'       => 'closed',
            )
        );

        if ($post_id == 0) {
            return new WP_Error('cant-create', __('message', 'text-domain'));
        }

        return new WP_REST_Response(get_post($post_id), 200);
    }

    /**
     * Delete one item from the collection
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|WP_REST_Response
     */
    public function delete_item($request)
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
        if ($account->post_title == 'false') { // activated
            return new WP_Error('user-inactive', __('message', 'text-domain'));
        }
        if (!wp_delete_post($params['domain_id'], $force_delete = true)) {
            return new WP_Error('cant-delete', __('message', 'text-domain'));
        }

        return new WP_REST_Response(true, 200);
    }

    /**
     * Check if a given request has access to get items
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|bool
     */
    public function get_items_permissions_check($request)
    {
        //return true; <--use to make readable by all
        return current_user_can('read');
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

    /**
     * Check if a given request has access to create items
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|bool
     */
    public function create_item_permissions_check($request)
    {
        return current_user_can('publish_posts');
        // return true;
    }

    /**
     * Check if a given request has access to delete a specific item
     *
     * @param WP_REST_Request $request Full data about the request.
     * @return WP_Error|bool
     */
    public function delete_item_permissions_check($request)
    {
        return current_user_can('delete_posts');
    }

    /**
     * Prepare the item for create or update operation
     *
     * @param WP_REST_Request $request Request object
     * @return WP_Error|object $prepared_item
     */
    protected function prepare_item_for_database($request)
    {
        return array();
    }

    /**
     * Prepare the item for the REST response
     *
     * @param mixed $item WordPress representation of the item.
     * @param WP_REST_Request $request Request object.
     * @return mixed
     */
    public function prepare_item_for_response($item, $request)
    {
        return array();
    }

    /**
     * Validate a domain name
     *
     * @param domain name as string.
     * @return boolean
     */
    protected function is_valid_domain_name($domain_name)
    {
        return (preg_match("/^([a-z\d](-*[a-z\d])*)(\.([a-z\d](-*[a-z\d])*))*$/i", $domain_name) //valid chars check
            && preg_match("/^.{1,253}$/", $domain_name) //overall length check
            && preg_match("/^[^\.]{1,63}(\.[^\.]{1,63})*$/", $domain_name)); //length of each label
    }

    /**
     * Validate an IP address
     *
     * @param IP address as string
     * @return boolean
     */
    protected function is_valid_ip_address($ip_address)
    {
        return filter_var($ip_address, FILTER_VALIDATE_IP);
    }

    /**
     * Validate an Port number
     *
     * @param Port number
     * @return boolean
     */
    protected function is_valid_port($port)
    {
        return $port > 0 && $port <= 65535;
    }

    function user_has_role($user_id, $role_name)
    {
        $user_meta = get_userdata($user_id);
        $user_roles = $user_meta->roles;
        return in_array($role_name, $user_roles);
    }
}
