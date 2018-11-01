//加载时充值content最低大小，防止底部栏上来不好看
$(function () {
    let window_height = $(window).height();
    let window_width = $(window).width();
    $('#content').css('min-height',window_height);
    // 要是屏幕很窄，就改变原有注册界面的宽度
    if(window_width<800){
        $('#content').css('width','90%')
    }else {
        $('#content').css('width','600px')
    }
});