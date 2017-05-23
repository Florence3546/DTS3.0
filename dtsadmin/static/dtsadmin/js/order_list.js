var DTS = window.DTS || {};
DTS.admin_order = function ($) {
    $(document).ready(function () {
        /*-------------------------表格多选按钮------------------------*/
        DTS.Check('.check-all', '.check-item');

        /*-------------------------表格排序------------------------*/
        // 分页事件绑定
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.admin_order.load_order_data);
            DTS.data_table('#table_order');
        }

        /*-------------------------查看订单信息------------------------*/
        $('#content').on('click', '.look_order', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'look_order',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#approve_goods_modal').replaceWith(data);
                        $('.verify_order').hide();
                        $('#approve_goods_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        $('#approve_goods_modal .modal-footer').hide();
                        DTS.single_real_price();
                        $('.modal-title').text('查看订单');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        /*-------------------------审核订单信息------------------------*/
        $('#content').on('click', '.get_verify_order', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'look_order',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#approve_goods_modal').replaceWith(data);
                        $('#approve_goods_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $('.modal-title').text('审核订单');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------审核通过------------------------*/
        $(document).on('click', '.verify_order', function () {
            console.log('fasdfa');
            var pk = $(this).data('pk');
            var method = $(this).data('method');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'verify_order',
                    'method': method,
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg, data.status == 1);
                        if (data.status == 1) {
                            $('#approve_goods_modal').modal('hide');
                        }
                    } else {
                        $('#approve_goods_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------获取改价模态框------------------------*/
        $('#content').on('click', '.get_change_price', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'change_price',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#change_price_modal').replaceWith(data);
                        $('.verify_order').hide();
                        $('#change_price_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        $(".total_real_price").each(function () {
                            var obj = $(this).closest("tr");
                            var total;
                            if (obj.find(".discount_price").val()) {
                                total = (obj.find(".price").text() - obj.find(".discount_price").val()) * obj.find(".quantity").text();
                            } else {
                                total = (obj.find(".price").text() - obj.find(".discount_price").text()) * obj.find(".quantity").text();
                            }

                            $(this).text(total.toFixed(2));
                        });
                        $('.modal-title').text('改价申请');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 单价折扣处理
        $(document).on('change', '.discount', function () {
            var obj = $(this).closest("tr");
            var price = obj.find(".price").text();
            var quantity = obj.find(".quantity").text();
            var total_real_price;
            var discount = $(this).val();
            if (discount > price) {
                DTS.affirm("单价优惠不得大于单价");
                $(this).val("0.00");
            } else {
                total_real_price = ((price - discount) * quantity).toFixed(2);
                obj.find(".total_real_price").text(total_real_price);
            }
        });

        /*-------------------------提交改价处理------------------------*/
        $(document).on('click', '.submit_change_price', function () {
            var change_price_list = [];
            var flag = false;
            $('.discount_price').each(function () {
                change_price_list.push({
                    "pk": $(this).data('pk'),
                    "change_price": $(this).val()
                });
                if ($(this).val() > 0) {
                    flag = true;
                }
            });
            if (flag) {
                $.ajax({
                    url: $(this).attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'change_price_list': JSON.stringify(change_price_list),
                        'action': 'change_price',
                        'method': 'submit_change_price',
                        'pk': $('[name="pk"]').val()
                    },
                    cache: false,
                    success: function (data, status, xhr) {
                        if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                            DTS.affirm(data.msg, data.status == 1);
                            if (data.status == 1) {
                                $('#change_price_modal').modal('hide');
                            }
                        } else {
                            $('#change_price_modal').modal({
                                backdrop: 'static',
                                keyboard: false
                            });
                        }
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            } else {
                DTS.affirm("请填写单价优惠再提交");
            }

        });

        /*-------------------------撤销改价处理------------------------*/
        $(document).on('click', '.submit_change_price_cancel', function () {
            var change_price_list = [];
            $('.discount_price').each(function () {
                change_price_list.push($(this).data('pk'));
            });

            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'change_price_list': JSON.stringify(change_price_list),
                    'action': 'change_price',
                    'method': 'submit_change_price_cancel',
                    'pk': $('[name="pk"]').val()
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg, data.status == 1);
                        if (data.status == 1) {
                            $('#change_price_modal').modal('hide');
                        }
                    } else {
                        $('#change_price_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------开票------------------------*/
        $('#content').on('click', '.order_invoice', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'order_invoice',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#order_invoice_modal').replaceWith(data);
                        $('.verify_order').hide();
                        $('#order_invoice_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $('.modal-title').text('开票');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------开票处理------------------------*/
        $(document).on('click', '.submit_order_invoice', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#order_invoice_form').serialize(),
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg, data.status == 1);
                        if (data.status == 1) {
                            $('#order_invoice_modal').modal('hide');
                        }
                    } else {
                        $('#order_invoice_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        //查看开票号
        $('#content').on('click', '.look_invoice_no', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'order_invoice',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#order_invoice_modal').replaceWith(data);
                        $('.verify_order').hide();
                        $('#order_invoice_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $('.modal-title').text('查看开票');
                        $(".submit_order_invoice").hide();
                        $(".invoice_cancel").hide();
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------发货------------------------*/
        $('#content').on('click', '.deliver_order', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'deliver_order',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        alert(data.msg);
                    } else {
                        $('#deliver_order_modal').replaceWith(data);
                        $('.verify_order').hide();
                        $('#deliver_order_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $('.modal-title').text('发货');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------发货处理------------------------*/
        $(document).on('click', '.submit_deliver_order', function () {
            if ($('[name="shipping_method_id"]').val() == '') {
                DTS.affirm("请选择快递名称");
                return false;
            }
            if ($('[name="waybill_no"]').val() == '') {
                DTS.affirm("请输入快递单号");
                return false;
            }
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                // data: {
                //     'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                //     'action': 'order_invoice',
                //     'method': method,
                //     'pk': pk
                // },
                data: $('#deliver_order_form').serialize(),
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg, data.status == 1);
                        if (data.status == 1) {
                            $('#modal_deliver_order').modal('hide');
                        }
                    } else {
                        $('#modal_deliver_order').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------修改订单模态框------------------------*/

        $('#content').on('click', '.update', function () {
            $('.modal-title').text('修改企业');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        DTS.affirm(data.msg);
                    } else {
                        $('#common_modal').replaceWith(data);
                        $('#common_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        $('#submit_add').hide();
                        $('#submit_update').show();

                        $('#total_price').val($('#order_total_price_yuan').val() * 100);
                        $('#order_total_price_yuan').on('keyup', function () {
                            $('#total_price').val($('#order_total_price_yuan').val() * 100);
                        });
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        $(document).on('click', '#submit_update', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#common_form').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                    if (data.status == 1) {
                        $('#common_modal').modal('hide');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------删除企业------------------------*/
        $('#content').on('click', '.delete', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /************************ 导出Excel**************************/
        $(".order-export-btn").on('click', function () {
            if (!$("#order-export-pane input[type='radio']").is(":checked")) {
                alert("请先选择要导出的商品数据");
                $("#order-export-pane input[type='radio']")[0].focus();
                return;
            }
            var choose = $("#order-export-pane input[type='radio']:checked").val();
            var order_id_list = [];
            if (choose == 'ck') {
                order_id_list = $.map($("#table_order tbody input[type=checkbox]:checked"), function (obj) {
                    return obj.value;
                });
                console.log(order_id_list);
                if (order_id_list.length === 0) {
                    DTS.affirm('必须勾选一行');
                    $("#export_good_modal").modal('hide');
                    return;
                }
            }
            //查询条件
            $("#ex_choose").val(choose);
            $("#ex_order_ids").val(JSON.stringify(order_id_list));
            $("#search_order_form").attr('method', 'post');
            $("#search_order_form").attr('action', $(this).data("api"));
            $("#search_order_form").attr('target', '_blank');
            $("#search_order_form").submit();
            $("#search_order_form").attr('method', 'get');
            $("#search_order_form").attr('action', '');
            $("#search_order_form").removeAttr('target');
            setTimeout(function () {
                $("#export_good_modal").modal('hide');
            }, 1000);
        });

        /*-------------------------批量审核订单------------------------*/

        $('.is_pass').on('click', function () {
            var enter_id_list = $.map($("input[name='chk_list']:checked"), function (obj) {
                return obj.value;
            });

            if (enter_id_list.length === 0) {
                DTS.affirm('必须勾选一行');
                return;
            }
            var is_pass = 0;
            if ($(this).attr('id') == 'verify_pass') {
                is_pass = 1;
            } else {
                is_pass = 0;
            }

            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'id_list': JSON.stringify(enter_id_list),
                    'is_pass': is_pass
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------订单确认收款-------------------------*/
        $(".receipt_order").on("click", function () {
            $('#order_gathering_modal input').val($(this).attr("default_money"));
            $("#confirm_receipt").attr({"data-pk": $(this).data("pk")});
            $('#order_gathering_modal').modal({backdrop: 'static', keyboard: false});
            $('#order_gathering_modal .modal-title').text("确认收款");
            $('#order_gathering_modal .receivable-amount').text($(this).attr("receivable-amount"));
        });

        /*-------------------------提交确认收款-------------------------*/
        $("#confirm_receipt").on("click", function () {
        		var $this=$(this);
        		var num=$('#order_gathering_modal .receivable-amount').text();
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'receipt_order',
                    'real_price': num * 100,
                    'obj_id': $(this).attr("data-pk"),
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data.status == 1) {
                        DTS.affirm(data.msg);
                        var obj=$(".receipt_order[data-pk="+$this.attr("data-pk")+"]").closest("tr");
                        obj.find(".real_money").text(num);
                        obj.find(".trade_state").text('已付款');
                        obj.find(".receipt_order").parent().remove();
                        obj.find(".get_change_price").parent().remove();
                        $('#order_gathering_modal').modal('hide');
                    } else if (data.status == 'err') {// 该订单已经关闭
                        window.location.reload();
                    } else {
                        DTS.affirm(data.msg);
                    }
                },

                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------查看日志-------------------------*/
        $(".ord_log").on('click', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        DTS.affirm(data.msg);
                    } else {
                        $('#common_log_modal').replaceWith(data);
                        $('#common_log_modal').modal({backdrop: 'static', keyboard: false, show: true});
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------查询订单------------------------*/
        var form_val = $('[name="trade_state"]').val() ||
            $('[name="buyer_name"]').val() ||
            $('[name="purchaser_name"]').val() ||
            $('[name="payment_method_type"]').val() ||
            $('[name="ord_time_from"]').val() ||
            $('[name="ord_time_to"]').val() ||
            $('[name="total_price_from"]').val() ||
            $('[name="total_price_to"]').val() ||
            $('[name="order_good_name"]').val() ||
            $('[name="order_invoice_state"]').val() ||
            $('[name="verify_state"]').val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }
    });

    return {
        // 接口定义
        load_order_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#input_enter_name").val($.trim($("#input_enter_name").val()));
            $("#buyer_name").val($.trim($("#buyer_name").val()));
            $("#enter_name").val($.trim($("#enter_name").val()));
            $("#good_name").val($.trim($("#good_name").val()));
            DTS.loading_dialog(true);
            $("#search_order_form").submit();
        },

        update_total_real_price: function () {
            /*-------------------------订单实付总金额------------------------*/
            var total_prices = 0;
            $('.real_price').each(function () {
                var real_price = $(this).text();
                if (real_price) {
                    return total_prices += parseFloat(real_price);
                }
            });
            $(select).text(total_prices);
        }
    };

}($);