DTS = window.DTS || {};
DTS.trading_record = function ($) {
    $('.form-control.date').datetimepicker({
        language: 'zh-CN',
        weekStart: 1,
        todayBtn: 1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0
    });
    $("form").on("click", "a", function () {
        $(this).addClass("active").siblings().removeClass("active");
    });
    $("form input").focus(function () {
        $(".sure").removeClass("hide");
    });
    $(".sure").on("click", function () {
        $(this).addClass("hide");
    });
}($);
