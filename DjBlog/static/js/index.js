$(function () {
    let $swiper_con = $('.swiper-container');
    let swiper_width = $swiper_con.width();
    let swiper_height = swiper_width * 9 / 16;
    $swiper_con.css('height', swiper_height);
    console.log(swiper_width);
    // if (!$('#myCanvas').tagcanvas({
    //     textColour: '#ffffff',
    //     outlineThickness: 1,
    //     maxSpeed: 0.03,
    //     depth: 0.75
    // })) 
    {
        // TagCanvas failed to load
        $('#myCanvasContainer').hide();
    }
    // your other jQuery stuff here...
});
