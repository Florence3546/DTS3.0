var DTS = window.DTS || {};
DTS.approval_list = function ($) {
    $(document).ready(function () {
        /*-------------------------日期------------------------*/
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
        /*-------------------------表格多选按钮------------------------*/
        $(".check-all").on('click', function () {
            if (this.checked) {
                $("tbody input").prop("checked", true);
                $("tbody input").closest("tr").addClass("checked");
            } else {
                $("tbody input").prop("checked", false);
                $("tbody input").closest("tr").removeClass("checked");
            }
        });

        $("tbody").on("click", "input", function () {
            if (this.checked) {
                $(this).closest("tr").addClass("checked");
            } else {
                $(this).closest("tr").removeClass("checked");
            }
        });

        // 分页事件绑定
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.approval_list.load_approval_data);
            // DTS.data_table('#table_approval');
        }

        /*-------------------------点击订单编号查看------------------------*/
        $('#content').on('click', '.look_order', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#approve_order_modal').replaceWith(data);
                        $('.verify_order').hide();
                        $('#approve_order_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $("#approve_order_modal .modal-footer").hide();
                        $('.modal-title').text('查看订单');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------点击审核 获取审核改价信息------------------------*/
        $('#content').on('click', '.get_verify_change_price', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'get_approval',
                    'action': 'get_verify_change_price',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#approval_verify_modal').replaceWith(data);
                        $('#approval_verify_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $('.modal-title').text('改价审核');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------审核通过------------------------*/
        $(document).on('click', '.submit_change_price_pass', function () {
            var pk = $(this).data('pk');
            var change_price_list = [];
            var real_total_price = 0;
            $('.discount').each(function () {
                change_price_list.push({
                    "pk": $(this).data('pk'),
                    "change_price": $(this).val()
                });
                real_total_price += $(this).closest("tr").find(".real_price").text() * 100;
            });
            console.log(real_total_price);
            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'get_approval',
                    'action': 'submit_change_price_pass',
                    'pk': pk,
                    'change_price_list': JSON.stringify(change_price_list),
                    'real_total_price': real_total_price,
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg, data.status == 1);
                        $('#approval_verify_modal').modal('hide');
                        window.location.reload();
                    } else {
                        $('#approval_verify_modal').modal({
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

        /*-------------------------审核不通过------------------------*/
        $(document).on('click', '.submit_change_price_nopass', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'get_approval',
                    'action': 'submit_change_price_nopass',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg, data.status == 1);
                        $('#approval_verify_modal').modal('hide');
                    } else {
                        $('#approval_verify_modal').modal({
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

        /*-------------------------点击查看 获取审核模态框------------------------*/
        $('#content').on('click', '.get_look_change_price', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'get_approval',
                    'action': 'get_look_change_price',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#approval_verify_modal').replaceWith(data);
                        $('#approval_verify_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                        });
                        DTS.single_real_price();
                        $('.modal-title').text('查看改价申请');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------slug筛选------------------------*/
        // var href = URI(document.location.href);
        $('.is_my').on('click', function () {
            // href.removeQuery('slug');
            // href.addQuery('slug', $(this).data('value'));
            $("#slug").val($(this).data('value'));
            DTS.approval_list.load_approval_data(1);
            // window.location.href = href.toString();
        });

        /*-------------------------查询订单------------------------*/
        var form_val = $('[name="start_time_from"]').val() ||
            $('[name="finish_time_from"]').val() ||
            $('[name="finish_time_to"]').val() ||
            $('[name="start_time_from"]').val() ||
            $('[name="start_time_to"]').val() ||
            $('[name="ord_time_to"]').val() ||
            $('[name="change_price_state"]').val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }

        /*-----------------------------申请优惠价累加---------------------------*/
        $('.discount_totle_price').each(function () {
            var discount = $(this).data('discount').split(',');
            var totle = 0;
            discount.forEach(function (a) {
                if (parseInt(a)) {
                    totle += parseInt(a);
                }
            });
            totle *= 0.01;
            $(this).text(totle.toFixed(2));
        });

        /*----------------------实际优惠-----------------------------*/
        $('.change_price').each(function () {
            var real_discount = $(this).data('real_discount').split(',');
            var totle = 0;
            real_discount.forEach(function (a) {
                if (parseInt(a)) {
                    totle += parseInt(a);
                }
            });
            totle *= 0.01;
            $(this).text(totle.toFixed(2));
        });
        /*----------------------实付金额-----------------------------*/
        $(".real_total_price").each(function () {
            var obj = $(this).closest('tr');
            var total;
            if (obj.find('.change_price').text() != '0.00') {
                total = obj.find(".order_amount").text() - obj.find('.change_price').text();
                $(this).text(total.toFixed(2));
            } else {
                total = obj.find(".order_amount").text() - obj.find('.discount_totle_price').text();
                $(this).text(total.toFixed(2));
            }
        });
        // 单价折扣处理
        $(document).on('change', 'input.discount', function () {
            var obj = $(this).closest("tr");
            var price = obj.find(".price").text();
            var quantity = obj.find(".quantity").text();
            var total_real_price;
            var discount = $(this).val();
            if (discount > price) {
                alert("单价优惠不得大于单价");
                $(this).val("0.00");
            } else {
                total_real_price = ((price - discount) * quantity).toFixed(2);
                obj.find(".real_price").text(total_real_price);
            }
        });
    });
    return {
        // 接口定义
        load_approval_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#order_code").val($.trim($("#order_code").val()));
            DTS.loading_dialog(true);
            $("#approve_form").submit();
        }
    };

}($);