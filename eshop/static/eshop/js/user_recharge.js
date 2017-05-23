DTS = window.DTS || {};
DTS.user_recharge = function ($) {
    $(".recharge-method").on("click", "span", function () {
        $(this).addClass("active").siblings().removeClass("active");
        var str = "." + $(this).attr("data-class");
        $(str).show().siblings().hide();
    });

    $(".online-payment li").on("click", function () {
        $(this).addClass("active").siblings().removeClass("active");
    });

    return {
        //
    }

}($);

