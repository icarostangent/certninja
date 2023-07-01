<?php

add_action('init', 'register_roles');
function register_roles()
{
    add_role(
        'ultimate',
        __('Ultimate'),
        array(
            'read'  => true,
            'create_posts'  => true,
            'publish_posts'  => true,
            'delete_posts'  => true,
        )
    );

    add_role(
        'growth',
        __('Growth'),
        array(
            'read'  => true,
            'publish_posts'  => true,
            'delete_posts'  => true,
        )
    );

    add_role(
        'basic',
        __('Basic'),
        array(
            'read'  => true,
            'publish_posts'  => true,
            'delete_posts'  => true,
        )
    );

    add_role(
        'starter',
        __('Starter'),
        array(
            'read'  => true,
            'publish_posts'  => true,
            'delete_posts'  => true,
        )
    );

    remove_role('subscriber');
    remove_role('contributor');
    remove_role('author');
    remove_role('editor');
}
