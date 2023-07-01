<?php

new ScanRoute();
class ScanRoute extends WP_REST_Controller {
    public function __construct() {
        add_action( 'rest_api_init', [$this, 'register_routes'] );
    }

    /**
     * Register the routes for the objects of the controller.
     */
    public function register_routes() {
        $namespace = 'backend/v1';
        register_rest_route( $namespace, '/author/(?P<author_id>[\d]+)/domain/(?P<domain_id>[\d]+)/scan', array(
            array(
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => array( $this, 'get_items' ),
                'permission_callback' => array( $this, 'get_items_permissions_check' ),
                'args' => array(
                    'author_id' => array(
                        'validate_callback' => function($param, $request, $key) {
                            return is_numeric( $param );
                        },
                        'required' => true,
                    ),
                    'domain_id' => array(
                        'validate_callback' => function($param, $request, $key) {
                            return is_numeric( $param );
                        },
                        'required' => true,
                    ),
                    'page' => array(
                        'required' => false,
                    ),
                ),
            ),
        ) );
    }
 
    /**
    * Get a collection of items
    *
    * @param WP_REST_Request $request Full data about the request.
    * @return WP_Error|WP_REST_Response
    */
    public function get_items( $request ) {
        $params = $request->get_params();

        if ( $params['author_id'] != wp_get_current_user()->ID ) {
            return new WP_Error( 'invalid-user-id', __( 'message', 'text-domain' ) );
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
                'post_type'         => 'scan',
                'author'            => $params['author_id'],
                'title'             => $params['domain_id'],
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

        return new WP_REST_Response( $data, 200 );
    }
 
    /**
    * Check if a given request has access to get items
    *
    * @param WP_REST_Request $request Full data about the request.
    * @return WP_Error|bool
    */
    public function get_items_permissions_check( $request ) {
        //return true; <--use to make readable by all
        return current_user_can( 'read' );
    }
}

?>
