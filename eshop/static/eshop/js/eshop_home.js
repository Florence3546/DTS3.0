/**
 * Created by king5699 on 17/1/10.
 */
var DTS = window.DTS || {};
DTS.eshop_home = function ($) {
    $(document).ready(function () {
        var good_placeholder = '' +
                '<a href="javascript:;">' +
                '<span><img src="' + $('#good_placeholder_img').val() + '"/></span>' +
                '<p class="not-log-in">商品价格：￥0.00</p>' +
                '<p>商品名称</p>' +
                '<p>商品规格</p>' +
                '</a>';
        $('.tab-content>.goods').each(function () {
            var temp_num = 6 - $(this).children().length;
            if (temp_num > 0) {
                while(temp_num > 0) {
                    $(this).append(good_placeholder);
                    temp_num--;
                }
            }

        });
        $('.floor>.goods').each(function () {
            var temp_num = 10 - $(this).children('.good_thumb').length;
            if (temp_num > 0) {
                while(temp_num > 0) {
                    $(this).append(good_placeholder);
                    temp_num--;
                }
            }

        });
    });
    $("#info_notic .info_notic_span").on('click', function () {
        var info_type = $(this).attr('info_type');
        console.log(info_type);
        if (info_type == 'N') {
            $("#info_span").removeClass('active');
            $("#info_list").addClass('hide');
            $("#notic_span").addClass('active');
            $("#notic_list").removeClass('hide');
        } else {
            $("#notic_span").removeClass('active');
            $("#notic_list").addClass('hide');
            $("#info_span").addClass('active');
            $("#info_list").removeClass('hide');
        }
        $("#info_notic_more").attr("href", "/eshop/notice_list/" + info_type + "/")
    })
    /*******************楼层*********************/
    $(window).scroll(function () {
        $(".floor").each(function () {
            var h = $(this).offset().top - $(window).scrollTop();
            if (h < window.innerHeight / 2 & h > 0) {
                $(".left-tab a").eq($(this).index()).addClass("active").siblings().removeClass("active");
            }
        });
        var maxH = $(".floor").eq(0).offset().top - $(window).scrollTop();
        if (maxH > window.innerHeight / 2) {
            $(".tab_floor").removeClass("active");
        }
    });
    $(".left-tab").on("click", "a", function () {
        if ($(this).hasClass("tab_floor")) {
            $(this).addClass("active").siblings().removeClass("active");
        } else {
            $(this).siblings().removeClass("active");
        }
    });


    // 接口定义
    return {}
}($);