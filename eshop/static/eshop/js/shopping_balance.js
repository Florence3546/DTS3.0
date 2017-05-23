var DTS = window.DTS || {};
DTS.shopping_balance = function ($) {
    $(document).ready(function () {
        // 更多地址
        $(".btn-more-address").on('click', function () {
            var txt = $(this).text();
            if (txt == "收起地址") {
                $(this).text("更多地址");
                $("#address_list").addClass("hide");
                $("#address_show").removeClass("hide");
                // 替换选择的地址
                var active_address = $('.address_item.active').removeClass('address_item').parent().html();
                $('#address_show').html(active_address);
            } else {
                $(this).text("收起地址");
                $("#address_list").removeClass("hide");
                $("#address_show").addClass("hide")
            }
        });

        // 选择地址
        $('#receiving_address').val($('.delivery-name').data('id'));

        $(".delivery-name").on('click', function () {
            $("#address_list .delivery-name").removeClass("active");
            $(this).addClass("active");
            $('#receiving_address').val($(this).data('id'));
        });
        // // 设为默认地址
        // $(".set-def").on('click', function () {
        //     $("#address_list").addClass("hide");
        //     $(".delivery-address").removeClass("hide");
        // });

        //发票
        $(".invoice-open").on('click', function () {
            $(".invoice-box input").val("");
            $(".error").hide();
            var i_child = $(this).find("i");
            if (i_child.hasClass("icon-jia")) {
                i_child.addClass("icon-jian").removeClass("icon-jia");
                $(".invoice-box").show();
            } else {
                i_child.addClass("icon-jia").removeClass("icon-jian");
                $(".invoice-box").hide();
            }
        });

        // 保存发票内容
        $("#invoice_save").on('click', function () {
            var flag = 1;
            if ($("#company_name").val() == '') {
                $("#company_name").next().show();
                flag = 0;
            }
            if ($("#taxpayer_no").val() == '') {
                $("#taxpayer_no").next().show();
                flag = 0;
            }
            if ($("#address_phone").val() == '') {
                $("#address_phone").next().show();
                flag = 0;
            }
            if ($("#bank_account").val() == '') {
                $("#bank_account").next().show();
                flag = 0;
            }
            if (flag == 1) {
                DTS.affirm("保存发票成功！");
                $(".invoice-open").find("i").addClass("icon-jia").removeClass("icon-jian");
                $(".invoice-box").hide(1000);
            }
        });
        //不要发票
        $("#invoice_cancel").on('click', function () {
            $(".invoice-open").find("i").addClass("icon-jia").removeClass("icon-jian");
            $(".invoice-box").hide(1000);
        });

        // 手机号码或者座机号验证
        jQuery.validator.addMethod("isMobile", function (value, element) {
            var length = value.length;
            // var mobile = /^1(3|4|5|7|8)\d{9}$/;
            var mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0-9]|170)\d{8}$/;
            // var phone = /^\d{3}-\d{8}|\d{4}-\d{7}$/;
            return this.optional(element) || (mobile.test(value));
        }, "请正确填写您的电话号码");

        //表单验证
        $.validator.setDefaults({
            submitHandler: function () {
                if ($("#form_address").data("type") == 0) {
                    if ($(".delivery-address").length == 21) {
                        DTS.affirm("您最多可以添加20个收货地址，您当前的收货地址已经有20个，请删除不常用的地址再添加新地址")
                    } else {
                        $.ajax({
                            url: $('#save_add_address').attr('api'),
                            type: 'POST',
                            data: $('#form_address').serialize(),
                            dataType: 'json',
                            cache: false,
                            success: function (data) {
                                $("#modal_address").modal('hide');
                                DTS.affirm(data.msg, data.status == 1);
                            },
                            error: function () {
                                DTS.alert(DTS.tips_error);
                            }
                        });
                    }

                } else {
                    $.ajax({
                        url: $('#save_update_address').attr('api'),
                        type: 'POST',
                        data: $('#form_address').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            $("#modal_address").modal('hide');
                            DTS.affirm(data.msg, data.status == 1);
                        },
                        error: function () {
                            DTS.alert(DTS.tips_error);
                        }
                    });
                }
            },
            rules: {
                telephone: {
                    isMobile: true
                }
            },
            message: {}
        });

        // 新增收货地址
        $("#add_new_address").on('click', function () {
            DTS.clear_form('#form_address');
            $(".city").addClass("hide");
            $(".district").addClass("hide");
            $('#modal_address').modal({backdrop: 'static', keyboard: false});
            $('.modal-title').text('添加收货地址');
            $('#save_add_address').show();
            $('#save_update_address').hide();
            distpicker();
            $("#form_address").validate();
        });

        // 地区控件
        function distpicker() {
            $("#distpicker").distpicker();
            var Province, City, District;
            $(".province").change(function () {
                $(".city").removeClass('hide');
                $(".district").addClass('hide');
                Province = $(".province").val();
                $('#region').val(Province);
            });
            $(".city").change(function () {
                $(".district").removeClass('hide');
                City = $(".city").val();
                $('#region').val(Province + ' ' + City);
            });
            $(".district").change(function () {
                District = $(".district").val();
                $('#region').val(Province + ' ' + City + ' ' + District);
            });
        }

        //新增收货地址提交
        $(document).on('click', '#save_add_address', function () {
            $('#form_address').attr({"data-type": 0});
            $('#form_address').submit();
        });

        // 编辑收货地址
        $('.edit-address').on('click', function () {
            var pk = $(this).data('id');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('#form_address [name=csrfmiddlewaretoken]').val(),
                    'method': 'receiving_address',
                    'action': 'get_address',
                    'pk': pk
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        $('#modal_address').replaceWith(data);
                        $('#modal_address').modal({backdrop: 'static', keyboard: false});
                        $('.modal-title').text('修改收货地址');
                        $('#save_add_address').hide();
                        $('#save_update_address').show();
                        $("#form_address").validate();

                        //地区选择
                        var region = $('#region').val().split(' ');
                        if (region[2]) {
                            $("#distpicker").distpicker({
                                province: region[0],
                                city: region[1],
                                district: region[2]
                            });
                        } else {
                            $(".district").addClass("hide");
                            $("#distpicker").distpicker({
                                province: region[0],
                                city: region[1]
                            });
                        }
                        var Province, City, District;
                        $(".province").change(function () {
                            $(".city").removeClass('hide');
                            $(".district").addClass('hide');
                            Province = $(".province").val();
                            if (Province == undefined) {
                                Province = region[0];
                            }
                            $('#region').val(Province);
                        });
                        $(".city").change(function () {
                            $(".district").removeClass('hide');
                            City = $(".city").val();
                            if (Province == undefined) {
                                Province = region[0];
                            }
                            if (City == undefined) {
                                City = region[1];
                            }
                            $('#region').val(Province + ' ' + City);
                        });
                        $(".district").change(function () {
                            District = $(".district").val();
                            if (Province == undefined) {
                                Province = region[0];
                            }
                            if (City == undefined) {
                                City = region[1];
                            }
                            $('#region').val(Province + ' ' + City + ' ' + District);
                        });
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // 编辑提交
        $(document).on('click', '#save_update_address', function () {
            $('#form_address').attr({"data-type": 1});
            $('#form_address').submit();
        });

        // 删除收货地址
        $('.delete-address').on('click', function () {
            var url = $(this).attr('api');
            var this_id = $(this).data("id");
            DTS.confirm("删除后不可恢复，您确定要删除吗？", function () {
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'id': this_id
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                    },
                    error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            }, "删除提醒");
        });

        // 设为默认地址
        $(".set_default").on('click', function () {
            $(this).addClass("hide");
            var pk = $(this).data('id');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'receiving_address',
                    'action': 'address_default',
                    'pk': pk
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            })
        });

        /*-------------------------支付方式------------------------*/
        $('.payment-method-box div').eq(2).addClass('active');
        $('.payment-method-box div').on('click', function () {
            $(this).addClass('active');
            $(this).siblings().removeClass('active');
            $('#payment_method').val($(this).data('value'))
        });

        /*-------------------------配送方式------------------------*/
        $('.delivery-method-box div').eq(0).addClass('active');
        $('.delivery-method-box div').on('click', function () {
            $(this).addClass('active');
            $(this).siblings().removeClass('active');
            $('#shipping_method').val($(this).data('value'))
        });

        /*-------------------------提交生成订单号------------------------*/
        $('.submit_order').on('click', function () {

            var receiving_address_id = $('#receiving_address').val();
            if (receiving_address_id == '') {
                alert("请提供有效的收货地址！");
                return false;
            }

            // 订单类型 购物车 快速下单
            var order_type = $('#order_type').val();
            var url = $('#submit_order').val();
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'create_order',
                    'action': order_type,
                    'receiving_address': receiving_address_id,
                    'shipping_method': $('#shipping_method').val(),
                    'payment_method': $('#payment_method').val(),
                    'note': $('#note').val(),
                    'company_name': $("#company_name").val(),
                    'taxpayer_no': $("#taxpayer_no").val(),
                    'address_phone': $("#address_phone").val(),
                    'bank_account': $("#bank_account").val()
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data.status == 2) {
                        window.location.href = data.url;
                    } else if (data.status == 0) {
                        alert(data.msg);
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
            // window.location.href = successUrl + "?orderId=" + result.orderId + "&rid=" + Math.random();
        });

        update_total_prices('.total_prices');
        update_total_prices_and_shipping('.total_prices_and_shipping');

        /*-------------------------总价处理------------------------*/
        // 商品总金额
        function update_total_prices(select) {
            var total_prices = 0;
            $('.subtotal').each(function () {
                var price = $(this).text();
                if (price) {
                    return total_prices += parseFloat(price);
                }
            });
            $(select).text(total_prices.toFixed(2));
        }

        // 商品总金额(含运费)
        function update_total_prices_and_shipping(select) {

            var total_prices_and_shipping = 0;
            $('.price_item').each(function () {
                var price = $(this).text();
                if (price) {
                    return total_prices_and_shipping += parseFloat(price);
                }
            });

            $(select).text(total_prices_and_shipping.toFixed(2));
        }
    });

}($);
