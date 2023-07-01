<?php

new ThemeRoute();
class ThemeRoute extends WP_REST_Controller {
    public function __construct() {
        add_action( 'rest_api_init', [$this, 'register_routes'] );
    }

    /**
     * Register the routes for the objects of the controller.
     */
    public function register_routes() {
        $namespace = 'backend/v1';
        register_rest_route( $namespace, '/theme', array(
            array(
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => array( $this, 'get_item' ),
                'permission_callback' => '__return_true',
            ),
        ) );
    }
 
    /**
    * Get a collection of items
    *
    * @param WP_REST_Request $request Full data about the request.
    * @return WP_Error|WP_REST_Response
    */
    public function get_item( $request ) {
        return new WP_REST_Response( get_stylesheet_uri(), 200 );
    }
}

?>
