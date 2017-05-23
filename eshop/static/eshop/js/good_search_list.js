var DTS = window.DTS || {};
DTS.good_search_list = function ($) {
    $(document).ready(function () {

        // 缺货登记
        DTS.lack_register($(".lack_register"));

        /*-------------------------搜索项显示------------------------*/
        var href = URI(document.location.href);
        var local_href = URI.parseQuery(href.query());

        // 第一版 ,分割参数
        // var parm = local_href.brand.split(',');
        // parm.forEach(function (i) {
        //     console.log(i);
        //     var select = ".s_item[data-value='" + i +"']";
        //     $(select).addClass('active');
        // });

        // 第二版 uri
        $.each(local_href, function (k, v) {
            // 去掉页数
            if (k == 'page') {
                return true
            }
            if (v.constructor == Array) {
                v.forEach(function (i) {
                    console.log(i);
                    var select = ".s_item[data-value='" + i + "']";
                    $(select).addClass('active');

                    var html = "<li><div>";
                    html += i;
                    html += '<span class="search_item_remove" data-name="';
                    html += k;
                    html += '" data-value="';
                    html += i;
                    html += '"><i class="iconfont icon-shanchu"></i></span></div></li>';
                    $('.search_item').append(html);

                })
            } else if (v.constructor == String && v != '') {
                console.log(v);
                var select = ".s_item[data-value='" + v + "']";
                $(select).addClass('active');

                var html = '<li><div>';
                html += v;
                html += '<span class="search_item_remove" data-name="';
                html += k;
                html += '" data-value="';
                html += v;
                html += '"><i class="iconfont icon-shanchu"></i></span></div></li>';
                $('.search_item').append(html);
            }
        });

        /*-----------------------分页加入---------------------------*/
        $('.search_page').on('click', function () {
            console.log('a');
            href.removeQuery('page');
            var page = $(this).data('page').toString();
            href.addQuery('page', page);
            console.log(href.toString());
            window.location.href = href.toString();

        });

        /*------------------------搜索页码------------------------------*/
        $(".skip").on("click", function () {
            var num = $(".input_page").val();
            // $(".page_num").val(num);
            // $("#search_page_form").submit();
            href.removeQuery('page');
            href.addQuery('page', num);
            console.log(href.toString());
            window.location.href = href.toString();
        });

        // 移除搜索项
        $('.search_item_remove').on('click', function () {
            var data_name = $(this).data('name');
            var data_value = $(this).data('value');
            var href = URI(document.location.href);
            href.removeQuery(data_name.toString(), data_value.toString());
            document.location.href = href.toString();
            console.log(href.toString());
        });

        // 移除所有搜索项
        $('.search_item_remove_all').on('click', function () {
            var data_name = $(this).data('name');
            var data_value = $(this).data('value');
            var href = URI(document.location.href);
            href.removeQuery('keyword');
            href.removeQuery('brand');
            href.removeQuery('locality');
            href.removeQuery('dosage_form');
            href.removeQuery('category');
            document.location.href = href.toString();
        });

        /*-------------------------搜索项点击------------------------*/
        $('.s_item').on('click', function () {
            var data_name = $(this).data('name');
            var data_value = $(this).data('value');
            var href = URI(document.location.href);
            href.removeQuery('page');
            href.addQuery(data_name.toString(), data_value.toString());
            console.log(href.toString());
            var local_href = URI.parseQuery(href.query());
            // var parm = local_href.brand.split(',');
            // parm.push(data_value);
            // parm = parm.join(',');
            // console.log(parm);
            console.log($(this).data('name'));
            $(this).prop('href', href.toString());
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
                    DTS.alert(DTS.tips_error);
                }
            })
        });

        //-----------------------------------加入购物车-----------------------------------//
        $('.add_cart').on('click', function () {
            var gid = $(this).data('id');
            var count = $(this).siblings('.good_count_group').find('.good_count').val() || 1;
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
                        }
                    } else {
                        alert(data.msg);
                        console.log(data.log);
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            })
        });

        /*-------------------------数量加减-----------------------------*/
        $(".good_count_group").on("click", ".reduce", function () {
            var num = $(this).next().val() - 1;
            if (num > 0) {
                $(this).next().val(num);
            }
        });
        $(".good_count_group").on("click", ".add", function () {
            var num = $(this).prev().val() * 1 + 1;
            if (num <= 999) {
                $(this).prev().val(num);
            }
        });

        /*-------------------------更多选择-----------------------------*/
        $('.more_choices').on('click', function () {
            if ($('.formulation-attr').hasClass('hide')) {
                $('.formulation-attr').removeClass("hide");
                $('.sort-attr').removeClass("hide");
            } else {
                $('.formulation-attr').addClass("hide");
                $('.sort-attr').addClass("hide");
            }
        });

        /*-------------------------搜索项清空按钮隐藏-----------------------------*/
        if (!$(".search_item li").length) {
            $(".search_item_remove_all").hide();
        }

        return {
            // 接口定义
        };
    })
}($);