$(function () {
    let $swiper_con = $('.swiper-container');
    let swiper_width = $swiper_con.width();
    let swiper_height = swiper_width * 9 /16;
    $swiper_con.css('height',swiper_height);
    console.log(swiper_width)
})