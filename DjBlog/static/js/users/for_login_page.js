$(function () {
    $('#do_submit').prop('disabled', true);

    // 设置点击事件,点击验证码刷新
    $('#verificationCode').click(function () {
        $(this).attr('src', '/users/get_verification_code/' + Math.random())
    });

    //点击登录按钮
    $('#do_submit').click(function () {
        console.log('aaa');
        // 收集用户输入信息
        let your_user_id = $('#user_id').val();
        let your_user_passwd = $('#user_passwd').val();
        let your_verificaiton_code = $('#your_verificaiton_code').val();


        $('#login_form').ajaxSubmit({
            url: '/users/do_login/',
            type: 'post',

            success: function (data) {
                if (data == 'success') {
                    alert("恭喜你啦！登陆成功");
                    // 跳转主页
                    $(location).prop('href', '../../blog/')
                } else {
                    // 告诉用户登陆失败的原因,并刷新验证码
                    alert("登陆失败，" + data);
                    $('#verificationCode').attr('src', '/users/get_verification_code/' + Math.random())
                }

            },
            error: function (xhr, status, err) {
                alert("抱歉，服务器出了点小问题TAT,快联系作者上报bug吧TAT");
                console.log(xhr.responseText);
                console.log(status);
                console.log(err);
            },

            clearForm: false,//禁止清除表单
            resetForm: false //禁止重置表单
        });
        // 这里返回false防止页面刷新
        return false;

    });

    // input标签失去焦点，检查数据是否合法
    $("input").blur(function () {
        // console.log("Doing");
        // 先判断是哪个标签
        // 用户名
        if (!$(this).val()) {
            $(this).parent('.form-group').addClass('has-error');
            $('#warning_alert').text('*请填写用户名/密码');
            $('#warning_alert').css('display', 'block');
        } else {
            $(this).parent('.form-group').removeClass('has-error');
            $('#warning_alert').css('display', 'none');
        }


        // 完事后最后一步，判断是不是全部ok，完事再允许点击提交按钮
        judge_is_ok_to_login()
    });

    function judge_is_ok_to_login() {
        if (judge_all_input_have_value()) {
            $('#do_submit').prop('disabled', false);
        } else {
            $('#do_submit').prop('disabled', true);
        }
    }

    // 判断是不是所有的input都有值了
    function judge_all_input_have_value() {
        return !!($('#user_id').val() && $('#user_passwd').val() &&
            $('#your_verificaiton_code').val());
    }
});

