<?php

add_filter( 'cron_schedules', 'dw_add_cron_interval_5m' );
function dw_add_cron_interval_5m( $schedules ) {
    $schedules['five_minutes'] = array(
        'interval' => 60*5,
        'display'  => esc_html__( 'Every Five Minutes' ), );
    return $schedules;
}

add_filter( 'cron_schedules', 'dw_add_cron_interval_15s' );
function dw_add_cron_interval_15s( $schedules ) {
    $schedules['fifteen_seconds'] = array(
        'interval' => 15,
        'display'  => esc_html__( 'Every Fifteen Seconds' ), );
    return $schedules;
}

add_action( 'dw_cron_hook_ssl_connect_15_seconds', 'dw_cron_exec_ssl_connect' );
function dw_cron_exec_ssl_connect() {
    $redis = new Redis();
    $redis->connect('redis', 6379);

    $the_query = new WP_Query(
        array( 
            'post_type' => 'domain',
            'posts_per_page' => -1,
            'date_query'    => array(
                'column'  => 'post_modified',
                'before'   => '1 day ago'
            )
        )
    );
    if ( $the_query->have_posts() ) {
        while ( $the_query->have_posts() ) : $the_query->the_post(); 
            $data = [
                'domain' => get_the_title(),
                'ip' => get_the_excerpt(),
                'domain_id' => get_the_ID(),
                'author_id' => get_the_author_meta('ID'),
            ];
            $redis->rpush("domains_register", json_encode($data));

            $pid = wp_update_post([
                'post_id' => get_the_ID(),
            ]);
            error_log('update post: ' . $pid);
        endwhile;
    } else {
            // no posts found
    }
    wp_reset_postdata(); 
}

if ( !wp_next_scheduled( 'dw_cron_hook_ssl_connect_15_seconds' ) ) {
    error_log('schedule ssl connect');
    wp_schedule_event( time(), 'fifteen_seconds', 'dw_cron_hook_ssl_connect_15_seconds' );
}

?>
