<?php

function init() {
    echo "<h1>Backend admin</h1>";
    echo get_option('permalink_structure');
}

function setup_menu() {
    add_menu_page('backend admin', 'backend admin', 'manage_options', 'slchkr-admin', 'init' );
}
 
add_action('admin_menu', 'setup_menu');


 
?>
