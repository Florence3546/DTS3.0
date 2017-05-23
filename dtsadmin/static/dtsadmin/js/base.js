var DTS = window.DTS || {};
DTS.admin_base = function ($) {
    $(document).ready(function () {
        $(".menu-btn").on('click', function () {
            if ($(".sidebar-left").css("margin-left") == "0px") {
                $(".sidebar-left").stop().animate({
                    "margin-left": "-150px"
                });
                $(".section").stop().animate({
                    "left": 0
                });
            } else {
                $(".sidebar-left").stop().animate({
                    "margin-left": "0"
                });
                $(".section").stop().animate({
                    "left": "150px"
                });
            }
        });
    });

    return {
        // 接口定义
    }

}($);