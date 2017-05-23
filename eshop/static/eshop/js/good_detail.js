var DTS = window.DTS || {};
DTS.good_detail = function ($) {
    $(document).ready(function () {

        $(".tabs_nav").on("click", "li", function () {
            var str = "." + $(this).attr("data-tab");
            $(this).addClass("active").siblings().removeClass("active");
            $(str).removeClass("hide").siblings().addClass("hide");
        });
//-----------------------------------商品详情图片切换-----------------------------------//
        $(function () {
            $(".spec-list").on("click", "li", function () {
                var str = $(this).find("img").attr("src");
                $(".spec img").attr({"src": str});
                $(this).addClass("active").siblings().removeClass("active");
            });
            var a = $(".spec-list li").length;
            var b = a;
            var l = $(".spec-list ul").width() / a;
            $(".spec-scroll").on("click", ".prev", function () {
                if (b < a) {
                    b += 1;
                    $(".spec-list ul").css({"left": -l * (a - b) + "px"});
                }
            });
            $(".spec-scroll").on("click", ".next", function () {
                if (b > 4) {
                    b -= 1;
                    $(".spec-list ul").css({"left": -l * (a - b) + "px"});
                }
            });
        });

//-----------------------------------加入收藏-----------------------------------//
        $('.add_my_favories').on('click', function () {
            $(this).find("i").attr({"class": "iconfont icon-shoucang"});
            var id_list = $(this).data('id');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'my_favorites',
                    'action': 'add',
                    'id_list': '[' + id_list + ']'
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        alert(data.msg);
                        // $('#change_price_modal').modal('hide');
                        // window.location.reload();
                        if (data.status == 0) {
                            console.log(data.log);
                            window.location.href = data.url;
                        }
                    } else {
                        // $('#change_price_modal').modal({backdrop: 'static'});
                        alert(data.msg);
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error)
                }
            })
        });

        // 缺货登记
        DTS.lack_register($(".lack_register"));

        //-----------------------------------加入购物车-----------------------------------//
        $('.add_cart').on('click', function () {
            var gid = $(this).data('id');
            var suc_page = $(this).attr("suc_page");
            var count = $('.good_count').val();
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'add_cart',
                    'action': 'add',
                    'gid': gid,
                    'count': count
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                        if (data.status == 0) {
                            console.log(data.log);
                            // window.location.href = data.url;
                        } else if (data.status == 1) {
                            $('.shopping_cart_count').text(data.count);
                            window.location.href = suc_page;
                        }
                    } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error)
                }
            })
        });

        //--------------------------加减---------------------------//
        $(".count").on("click", ".reduce", function () {
            var num = $(this).prev().val() - 1;
            if (num > 0) {
                $(this).prev().val(num);
            }
        });
        $(".count").on("click", ".add", function () {
            var num = $(this).next().val() * 1 + 1;
            if (num <= 999) {
                $(this).next().val(num);
            }
        });
        $(".good_count").change(function () {
            var num = $(this).val();
            if (isNaN(num) || num == 0) {
                DTS.alert("请输入正确数量，数量在1~999之间")
                $(this).val("1");
            }
        });
    });
}($);


