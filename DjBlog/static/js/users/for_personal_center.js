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
        $('#personal_center_content').load('/users/go_user_center_somewhere/my_comment.html/')
    });

    $('#my_message').click(function () {
        $('#personal_center_content').load('/users/go_user_center_somewhere/my_message.html/')
    });

    $('#exit_system').click(function () {
        $(location).prop('href', '/users/do_log_out');
    });


    // //初始化fileinput控件（第一次初始化）
    // function initFileInput(ctrlName, uploadUrl) {
    //     var control = $('#' + ctrlName);
    //     control.fileinput({
    //         language: 'zh', //设置语言
    //         uploadUrl: 'static/js/users', //上传的地址
    //         allowedFileExtensions: ['jpg', 'png', 'gif'],//接收的文件后缀
    //         showUpload: true, //是否显示上传按钮
    //         showCaption: false,//是否显示标题
    //         browseClass: "btn btn-primary", //按钮样式
    //         previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
    //     });
    // }
    //
    //
    // //初始化fileinput控件（第一次初始化）
    // initFileInput("file-Portrait", "/User/EditPortrait");
});