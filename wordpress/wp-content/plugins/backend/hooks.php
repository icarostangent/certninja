<?php

add_action('init', 'domain_cpt');
function domain_cpt()
{
    register_post_type('domain', array(
        'labels' => array('name' => 'Domains', 'singular_name' => 'Domain'),
        'description' => 'Post type Domain',
        'supports' => array('title', 'excerpt'),
        'public' => true,
        'show_in_rest' => false,
        'label' => 'Domains',
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'capability_type' => array('domain', 'domains'),
        'map_meta_cap' => true,
    ));
}

add_action('init', 'scan_cpt');
function scan_cpt()
{
    register_post_type('scan', array(
        'labels'              => array('name' => 'Scans', 'singular_name' => 'Scan'),
        'hierarchical'        => false,
        'public'              => true,
        'show_ui'             => true,
        'show_in_menu'        => true,
        'show_in_nav_menus'   => true,
        'show_in_admin_bar'   => true,
        'can_export'          => true,
        'has_archive'         => true,
        'exclude_from_search' => false,
        'publicly_queryable'  => true,
        'show_in_rest'        => false,
        'capability_type' => array('scan', 'scans'),
        'map_meta_cap' => true,
    ));
}

add_action('init', 'account_cpt');
function account_cpt()
{
    register_post_type('account', array(
        'labels'              => array('name' => 'Account', 'singular_name' => 'Account'),
        'hierarchical'        => false,
        'public'              => true,
        'show_ui'             => true,
        'show_in_menu'        => true,
        'show_in_nav_menus'   => true,
        'show_in_admin_bar'   => true,
        'can_export'          => true,
        'has_archive'         => true,
        'exclude_from_search' => false,
        'publicly_queryable'  => true,
        'show_in_rest'        => false,
        'capability_type' => array('account', 'accounts'),
        'map_meta_cap' => true,
    ));
}

add_filter('woocommerce_rest_check_permissions', 'allow_rest_api_queries', 10, 4);
function allow_rest_api_queries($permission, $context, $zero, $object)
{
    // wc_create_new_customer( 'anon7@email.com', 'anon7', 'anonsayshello' );
    if (wp_get_current_user()->ID > 0) {
        return true;
    }
    return false;
}

add_action('woocommerce_checkout_order_processed', 'order_processed',  1, 1);
function order_processed($order_id)
{

    //You can do here whatever you want
    error_log(print_r('order id: ' . $order_id, true));
}

add_filter('woocommerce_rest_insert_shop_order_object', 'set_customer_id', 10, 3);
function set_customer_id($object, $arg2, $arg3)
{
    $object->customer_id = 101010101;;
    error_log(json_encode($object));
    error_log(json_encode($arg2));
    error_log(json_encode($arg3));
    return $object;
}

add_action('woocommerce_order_status_changed', 'status_changed', 10, 3);
function status_changed($order_id, $old_status, $new_status)
{
    $order = wc_get_order($order_id);
    $customer_id = $order->customer_id;
    $user = get_user_by('ID', $customer_id);
    //$order_total = $order->get_formatted_order_total();
    error_log(print_r('user: ' . $user, true));
    error_log(print_r('order: ' . $order, true));
    error_log(print_r('customer id: ' . $customer_id, true));
    error_log(print_r('old status: ' . $old_status, true));
    error_log(print_r('new status: ' . $new_status, true));
}
