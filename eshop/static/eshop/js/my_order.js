var DTS = window.DTS || {};
DTS.admin_enterprise = function ($) {
    $(document).ready(function () {
	/*-------------------------商品信息数据------------------------*/
				
        $(".sort-of-goods").on("click", function () {
            if ($(this).closest("li").find(".goods-information").css("display") == "none") {
                $(this).closest("li").find(".goods-information").show();
                $(this).addClass("active");
            } else {
                $(this).closest("li").find(".goods-information").hide();
                $(this).removeClass("active");
            }
        });

        var hash = window.location.hash;
        $(hash).css('display', 'block');

        /*-------------------------日期------------------------*/
        // 获取url中"?"符后的字串
        // TODO 用uri.js代替
        function GetRequest() {
            var url = location.search;
            var theRequest = new Object();
            if (url.indexOf("?") != -1) {
                var str = url.substr(1);
                strs = str.split("&");
                for (var i = 0; i < strs.length; i++) {
                    theRequest[strs[i].split("=")[0]] = decodeURI(strs[i].split("=")[1]);
                }
            }
            return theRequest;
        }
        /*-------------------------日期------------------------*/
        var url = URI(document.location.href);
        if (url.hasQuery('date')) {
            var query = URI.parseQuery(url.query());
            $('#order_date_past').val(query.date);
            url.removeQuery('data');
        }
        $('#order_date_past').on('change', function () {
            console.log($(this).val());
            var url = URI(document.location.href);
            url.removeQuery('data');
            url.setQuery('date', $(this).val());
            var query = URI.parseQuery(url.query());
            console.log(url.toString());
            console.log(query.date);
            window.location.href = url.toString();
        });
        /*--------------------------加入购物车-------------------------------*/
        $('.add_cart').on('click', function () {
            console.log('fasdfa');
            var gid = $(this).data('id');
            var count = 1;
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
                        alert(data.msg);
                        if (data.status == 0) {
                            console.log(data.log);
                            window.location.href = data.url;
                        }else if(data.status == 1){
                            $('.cart_count').text(data.count);
                        }
                    } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            })
        });

        /*-------------------------菜单加active------------------------*/
        var li_href = $('.order_nav').find('li a');
        var local_url = URI(document.location.href);
        var local_href = URI.parseQuery(local_url.query());

        li_href.each(function (index) {
            var href = URI($(this).prop('href'));
            var parse_href = URI.parseQuery(href.query());
            if(parse_href.state == local_href.state ){
                $(this).parent().addClass('active');
            }
        });
        /*************************搜索页码************************/
        $(".skip").on("click",function(){
            var num=$(".input_page").val();
            $(".page_num").val(num);
            $("#order_form").submit();
        });

        /****************** 取消订单 *****************/
        $(".cancel-order").on('click',function() {
            var ord_id = $(this).attr("data-id");
            DTS.confirm("您确定要取消此订单吗？", function () {
                $.ajax({
                    url: '/eshop/my_order/',
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'op_type': 'cal_ord',
                        'obj_id': ord_id
                    },
                    cache: false,
                    success: function (data) {
                        if (data.status == 0) {
                            DTS.alert(data.msg);
                        } else {
                            DTS.alert(data.msg, function () {
                                window.location.reload();
                            });
                        }
                    }, error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            });
        });

        /****************** 确认收货 *****************/
        $(".conf-rec").on('click',function(){
            var ord_id = $(this).attr("data-id");
            $.ajax({
                url:'/eshop/my_order/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'op_type': 'conf_rec',
                    'obj_id': ord_id
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        DTS.alert(data.msg);
                    } else {
                        DTS.alert(data.msg,function(){
                            window.location.reload();
                        });
                    }
                },error:function(){
                    DTS.alert(DTS.tips_error);
                }
            });
        });
        /****************** 交易状态筛选 *****************/
        $("#trade_state").change(function(){
            window.location.href='/eshop/my_order/?trade_state=' + $(this).val();
        });
       
       
       

        return {
            // 接口定义
        };

    })
}($);