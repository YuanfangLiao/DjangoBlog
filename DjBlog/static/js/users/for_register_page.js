$(function () {

    $('#do_submit').click(function () {
        $('#register_form').ajaxSubmit({
            url: '/users/do_register/',
            type: 'post',
            // dataType: 'json',
            // beforeSubmit: function () {
            // },
            success: function (data) {
                if (data === 'success') {
                    alert("恭喜你啦！注册成功，你已经是本网站的会员啦，赶快去登陆吧！");
                    // 跳转到登陆界面
                    $(location).prop('href', '../login_page/');
                } else {
                    alert("不好意思，信息有点问题呢，重新注册试试吧%……错误信息：" + data)
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
        // 这里设置false防止页面刷新
        return false;
    });
    $('#check_user_code').click(function () {
        judge_is_ok_to_register()
    });
    // input标签失去焦点，检查数据是否合法
    $("input").blur(function () {
        // console.log("Doing");
        // 先判断是哪个标签
        // 用户名
        if (this.id === 'user_id') {
            //用户名验证
            user_validation(this)
        }
        if (this.id === 'user_passwd') {
            //密码验证
            passwd_validation(this)
        }
        if (this.id === 'confirm_passwd') {
            //确认密码验证
            confirm_passwd_validation(this)
        }
        if (this.id === 'user_email') {
            //email验证
            confirm_email_validation(this)
        }
        // 完事后最后一步，判断是不是全部ok，完事再允许点击提交按钮
        judge_is_ok_to_register()
    });

    //这里的ob指的是this，那个对象调用就是那个对象，为了不使用关键字，实际就是this
    function user_validation(ob) {
        // 如果没有值
        if (!$(ob).val()) {
            $(ob).parent('.form-group').addClass('has-error');
            $(ob).attr('placeholder', '请输入用户名');
            // 弹框警告没输入用户名
            $('#warning_alert').text('*用户名不能为空');
            $('#warning_alert').css('display', 'block');
        }
        // 正则表达式匹配 是否符合用户名输入规范
        else if (!/^[a-zA-Z][a-zA-Z0-9_]{4,30}$/.test($(ob).val())) {
            $(ob).parent('.form-group').addClass('has-error');
            $('#warning_alert').text('*用户名只能由字母开头，包含字母、数字、下划线、长度为5-30个字符');
            $('#warning_alert').css('display', 'block');
        }
        //如果有值且正确，发送ajax请求查询数据库中有没有该用户名
        else {
            // 先重置错误提醒
            $(ob).parent('.form-group').removeClass('has-error');
            $(ob).attr('placeholder', '');
            $('#warning_alert').css('display', 'none');

            let user_id = $(ob).val();
            $.ajax({
                type: 'POST',
                url: '/users/check_user_exist/',
                data: {
                    'user_id': user_id,
                    // csrf安全认证
                    "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
                },
                success: function (data) {
                    if (data === 'exist') {
                        $('#user_id').parent('.form-group').addClass('has-error');
                        $('#warning_alert').text('*用户名已经存在，换个名字叭');
                        $('#warning_alert').css('display', 'block');
                    }
                }
                ,
                error: function () {
                    console.log('Ajax error')
                }
            })
        }
    }

    function passwd_validation(ob) {
        // 如果没有值
        if (!$(ob).val()) {
            $(ob).parent('.form-group').addClass('has-error');
            $(ob).attr('placeholder', '请输入密码');
            // 弹框警告没输入用户名
            $('#warning_alert').text('*密码不能为空');
            $('#warning_alert').css('display', 'block');
        }// 正则表达式匹配 是否符合用户名输入规范
        else if (!/^[a-zA-Z0-9_]{6,31}$/.test($(ob).val())) {
            $(ob).parent('.form-group').addClass('has-error');
            $('#warning_alert').text('*密码只能由字母开头，包含字母、数字、下划线、长度为6-30个字符');
            $('#warning_alert').css('display', 'block');
        }
        else {
            // 重置错误提醒
            $(ob).parent('.form-group').removeClass('has-error');
            $(ob).attr('placeholder', '');
            $('#warning_alert').css('display', 'none');
        }
    }

    function confirm_passwd_validation(ob) {
        // 如果没有值
        if (!$(ob).val()) {
            $(ob).parent('.form-group').addClass('has-error');
            $(ob).attr('placeholder', '请确认密码');
            // 弹框警告没输入用户名
            $('#warning_alert').text('*确认密码不能为空');
            $('#warning_alert').css('display', 'block');
        }// 验证两次密码是否相同
        else if ($(ob).val() !== $('#user_passwd').val()) {
            $(ob).parent('.form-group').addClass('has-error');
            $('#warning_alert').text('*两次密码输入不相同，请重新输入');
            $('#warning_alert').css('display', 'block');
        }
        else {
            // 重置错误提醒
            $(ob).parent('.form-group').removeClass('has-error');
            $(ob).attr('placeholder', '');
            $('#warning_alert').css('display', 'none');
        }
    }

    function confirm_email_validation(ob) {
        // 如果没有值
        if (!$(ob).val()) {
            $(ob).parent('.form-group').addClass('has-error');
            $(ob).attr('placeholder', '请输入邮箱');
            // 弹框警告没输入邮箱
            $('#warning_alert').text('*邮箱不能为空');
            $('#warning_alert').css('display', 'block');
        }
        // 正则表达式匹配 是否符合邮箱输入规范
        else if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test($(ob).val())) {
            $(ob).parent('.form-group').addClass('has-error');
            $('#warning_alert').text('*请输入合法的邮箱地址如123@sina.com');
            $('#warning_alert').css('display', 'block');
        }
        //如果有值且正确，发送ajax请求查询数据库中有没有该邮箱
        else {
            // 先重置错误提醒
            $(ob).parent('.form-group').removeClass('has-error');
            $(ob).attr('placeholder', '');
            $('#warning_alert').css('display', 'none');

            let user_email = $(ob).val();
            $.ajax({
                type: 'POST',
                url: '/users/check_email_exist/',
                data: {
                    'user_email': user_email,
                    // csrf安全认证
                    "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
                },
                success: function (data) {
                    if (data === 'exist') {
                        $('#user_email').parent('.form-group').addClass('has-error');
                        $('#warning_alert').text('*邮箱已经存在，换个名字叭');
                        $('#warning_alert').css('display', 'block');
                    }
                },
                error: function () {
                    console.log('Ajax error')
                }
            })
        }
    }

    function judge_is_ok_to_register() {
        // 如果没有报错的框框，并且同意用户守则已经勾选上了，允许点击注册按钮
        if ((!$('.form-group').hasClass('has-error')) &&
            ($('#check_user_code').prop('checked') == true) &&
            judge_all_input_have_value()) {

            $('#do_submit').prop('disabled', false)
        }
        else {
            $('#do_submit').prop('disabled', true)
        }
    }

// 判断是不是所有的input都有值了
    function judge_all_input_have_value() {
        return !!($('#user_id').val() && $('#user_passwd').val() &&
            $('#confirm_passwd').val() && $('#user_email').val());
    }

});