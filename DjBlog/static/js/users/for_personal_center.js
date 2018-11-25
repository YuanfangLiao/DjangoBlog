$(function () {
    $('#change_img').click(function () {
        $('#personal_center_content').load('/users/go_user_center_somewhere/change_img.html/')
    });

    $('#change_profile').click(function () {
        $('#personal_center_content').load('/users/go_user_center_somewhere/change_profile.html/')
    });

    $('#change_password').click(function () {
        $('#personal_center_content').load('/users/go_user_center_somewhere/change_password.html/')
    });

    $('#my_comment').click(function () {
        $('#personal_center_content').load('/users/go_my_comment')
    });

    $('#my_message').click(function () {
        $('#personal_center_content').load('/users/go_my_message')
    });

    $('#manage_article').click(function () {
        $('#personal_center_content').load('/users/manage_article')
    });

    $('#manage_carousel').click(function () {
        $('#personal_center_content').load('/users/manage_carousel')
    });

    $('#manage_nav').click(function () {
        $('#personal_center_content').load('/users/manage_nav')
    });

    $('#manage_swiper').click(function () {
        $('#personal_center_content').load('/users/manage_swiper')
    });

    $('#apply_admin').click(function () {
        $('#personal_center_content').load('/users/go_user_center_somewhere/apply_admin.html/')
    });

    $('#exit_system').click(function () {
        $(location).prop('href', '/users/do_log_out');
    });

});