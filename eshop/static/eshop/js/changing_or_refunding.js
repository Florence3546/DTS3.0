var DTS = window.DTS || {};
DTS.good_search_list = function ($) {
    $(document).ready(function () {
        //--------------------------退款金额----------------//
        /*if($(".money").val()>5000){
         $(".money").val("5000.00");
         }*/
        $(".money").change(function () {
            var num = $(this).val();
            if (isNaN(num)) {
                alert("请输入数字");
                return;
            }
            if ($(this).val() * 1 > $(this).attr("real_price") * 1) {
                alert("退款金额不能大于实付金额");
                $(this).val($(this).attr("real_price"));
                return;
            }
            /*
             if($(this).val()>5000){
             alert("退款金额不能大于5000元");
             $(this).val("5000.00");
             }*/
        });
        //--------------------------显示商品信息----------------//
        $(".sort-of-goods").on("click", function () {
            if ($(this).closest("li").find(".goods-information").css("display") == "none") {
                $(this).closest("li").find(".goods-information").show();
                $(this).addClass("active");
            } else {
                $(this).closest("li").find(".goods-information").hide();
                $(this).removeClass("active");
            }
        });

        //--------------------------切换类型----------------//
        $(".type").on("click", "a", function () {
            if ($(this).attr("refund_type") == "") {
                $(".cause").removeClass("hide");
                $(".wait").addClass("hide");
                $(this).addClass("active").siblings().removeClass("active");
                if ($(this).hasClass("return-good")) {
                    $(".step-good").removeClass("hide");
                    $(".step-money").addClass("hide");
                    $(".return-good-form").removeClass("hide");
                    $(".return-money-form").addClass("hide");
                } else {
                    $(".step-money").removeClass("hide");
                    $(".step-good").addClass("hide");
                    $(".return-good-form").addClass("hide");
                    $(".return-money-form").removeClass("hide");
                }
            }

        });

        //--------------------------修改----------------//
        $(".revise").on("click", function () {
            $(".type a").attr({
                "refund_type": ""
            });
            $(".wait").addClass("hide");
            $(this).addClass("active").siblings().removeClass("active");
            if ($(".return-good").hasClass("active")) {
                $(".take-good").addClass("hide");
                $(".return-good-form").removeClass("hide");
                $(".return-money-form").addClass("hide");
            } else {
                $(".take-good").removeClass("hide");
                $(".return-good-form").addClass("hide");
                $(".return-money-form").removeClass("hide");
            }
        });
        /****************提交退款申请*******************/
        $("#submit_refund").on("click", function () {
            var reasons = $(".refund_reasons").val();
            var money = ($("#refund_money").val() * 1).toFixed(2);
            $("form").addClass("hide");
            $(".wait-money").removeClass("hide");
            if ($(".shut_down")) {
                $(".shut_down").addClass("hide");
            }
            $.ajax({
                url: $(this).attr("api"),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    "id": $(this).data("id"),
                    "op_type": $(this).attr("op_type"),
                    "reasons": reasons,
                    "money": money,
                    "refund_type": $(this).attr("refund_type") * 1,
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    alert(data.msg);
                    window.location.reload();
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });
        /****************提交退货申请*******************/
        $("#submit_return").on("click", function () {
            var reasons = $(".return_reasons").val();
            var money = ($("#return_money").val() * 1).toFixed(2);
            $("form").addClass("hide");
            $(".wait-good").removeClass("hide");
            if ($(".shut_down")) {
                $(".shut_down").addClass("hide");
            }
            $.ajax({
                url: $(this).attr("api"),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    "id": $(this).data("id"),
                    "op_type": $(this).attr("op_type"),
                    "reasons": reasons,
                    "money": money,
                    "refund_type": $(this).attr("refund_type") * 1,
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    alert(data.msg);
                    window.location.reload();
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /****************取消申请*******************/
        $(".cancel").on("click", function () {
            $.ajax({
                url: $(this).attr("api"),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    "id": $(this).data("id"),
                    "op_type": $(this).attr("op_type"),
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    alert(data.msg);
                    window.location.reload();
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /****************提交退货信息*******************/
        $("#return_info").on("click", function () {
            var shipping_method = $(".shipping_method").val();
            var waybill_no = $(".waybill_no").val();
            console.log(shipping_method);
            console.log(waybill_no);
            if (shipping_method && waybill_no) {
                $.ajax({
                    url: $(this).attr("api"),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        "id": $(this).data("id"),
                        "op_type": $(this).attr("op_type"),
                        "shipping_method": shipping_method,
                        "waybill_no": waybill_no,
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        alert(data.msg);
                        window.location.reload();
                    },
                    error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            } else {
                alert("请填写完整退货信息");
            }
        });
        //-----------------------------------加入购物车-----------------------------------//
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
                        } else if (data.status == 1) {
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

        return {
            // 接口定义
        };
    })
}($);