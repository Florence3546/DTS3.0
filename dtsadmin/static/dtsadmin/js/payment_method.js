var DTS = window.DTS || {};
DTS.payment = function ($) {

    $.validator.setDefaults({
        submitHandler: function () {
            if ($("#form_payment").data("type") == 0) {
                $.ajax({
                    url: $("#submit_payment_add").attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'id': $('#id_payment_id').val(),
                        'pay_type': $('#id_pay_type').val(),
                        'logo': $('#id_logo option:selected').attr('logo'),
                        'name_cn': $('#id_name_cn').val(),
                        'order_no': $('#id_order_no').val(),
                        'is_active': $(':radio[name=is_active]:checked').val(),
                        'api_args': JSON.stringify(api_json)
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        // alert(data.msg);
                        // if (data.status == 1) {
                        //     $('#modal_delivery').modal('hide');
                        //     window.location.reload();
                        // }
                        DTS.affirm(data.msg, data.status == 1);
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            } else {
                $.ajax({
                    url: $("#submit_payment_update").attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'id': $('#id_payment_id').val(),
                        'pay_type': $('#id_pay_type').val(),
                        'logo': $('#id_logo option:selected').attr('logo'),
                        'name_cn': $('#id_name_cn').val(),
                        'order_no': $('#id_order_no').val(),
                        'is_active': $(':radio[name=is_active]:checked').val(),
                        'api_args': JSON.stringify(api_json)
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                        // DTS.alert(data.msg, function () {
                        //     window.location.reload();
                        // });
                        // $('#modal_payment').modal('hide');
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            }
        },
        rules: {
            order_no: {
                required: true,
                digits: true
            }
        },
        messages: {
            order_no: {
                digits: '请输入整数',
                min: 1,
                max: 99
            }
        }
    });

    // 添加支付方式
    $('#content').on('click', '.add_payment', function () {
        DTS.clear_form('#form_payment');
        $('#modal_payment').modal({backdrop: 'static', keyboard: false});
        $('.modal-title').text('添加支付方式');
        $('#submit_payment_add').show();
        $('#submit_payment_update').hide();
        $('.pay-method').addClass("hide");
        $(".logo-name").addClass("hide");
        $('.pay-msg').addClass("hide");
        $(".pay-type select").prop("disabled", false);
        $(".pay-method select").prop("disabled", false);
        $("#form_payment").validate();
    });

    // 添加支付方式的模态框选择
    var value;
    $(".pay-type select").off('change');
    $(".pay-type select").on('change', function () {
        value = $(this).val();
        $('.pay-method').removeClass("hide");
        $(".logo-name").addClass("hide");
        $(".pay-msg").addClass("hide");
        $(".pay-method select").val("");
        switch (value) {
            case "0":
                $(".pay-method option").removeClass("hide");
                $("#pay_off").addClass("hide");
                $("#pay_advance").addClass("hide");
                $("#pay_good").addClass("hide");
                break;
            case "1":
                $(".pay-method").addClass("hide");
                $(".offline-msg").removeClass("hide");
                $(".logo-name").removeClass("hide");
                $("#pay_off").attr('selected', "selected");
                $(".logo img").attr('src', $("#pay_off").attr("logo"));
                break;
            case "2":
                $(".pay-method").addClass("hide");
                $(".logo-name").removeClass("hide");
                $("#pay_advance").attr('selected', "selected");
                $(".logo img").attr('src', $("#pay_advance").attr("logo"));
                break;
            case "3":
                $(".pay-method").addClass("hide");
                $(".logo-name").removeClass("hide");
                $("#pay_good").attr('selected', "selected");
                $(".logo img").attr('src', $("#pay_good").attr("logo"));
                break;
        }
    });

    var api_json = {};
    $(".pay-method select").on('change', function () {
        var logo_val = $(this).find("option:selected").attr("logo");
        var val = $(this).val();
        $(".pay-msg").addClass("hide");
        switch (val) {
            case "alipay":
                $("#alipay_msg").removeClass("hide");
                break;
            case "weixin":
                $("#weixin_msg").removeClass("hide");
                break;
            case "wealth":
                $("#wealth_msg").removeClass("hide");
                break;
            case "onlinepay":
                $("#onlinepay_msg").removeClass("hide");
                break;
            case "e-bank":
                $("#e-bank_msg").removeClass("hide");
                break;
        }
        $(".logo-name").removeClass("hide");
        $(".logo img").attr('src', logo_val);
    });

    // 提交添加的支付方式
    $(document).on('click', '#submit_payment_add', function () {
        switch ($('#id_logo').val()) {
            case "alipay":
                api_json = {
                    'taobao_account': $('#id_taobao_account').val(),
                    'cooperate_id': $('#id_cooperate_id').val(),
                    'security_note': $('#id_security_note').val(),
                    'public_key': $('#id_public_key').val(),
                    'private_key': $('#id_private_key').val()
                };
                break;
            case "weixin":
                api_json = {
                    'weixin_no': $('#id_weixin_no').val()
                };
                break;
            case "wealth":
                api_json = {
                    'wealth_no': $('#id_wealth_no').val()
                };
                break;
            case "onlinepay":
                api_json = {
                    'onlinepay_no': $('#id_onlinepay_no').val(),
                };
                break;
            case "e-bank":
                api_json = {
                    'open_ebank': $('#id_open_ebank').val(),
                    'open_eaccount': $('#id_open_eaccount').val(),
                    'open_ename': $('#id_open_ename').val(),
                };
                break;
        }
        switch (value) {
            case "1":
                api_json = {
                    'open_bank': $('#id_open_bank').val(),
                    'open_account': $('#id_open_account').val(),
                    'open_name': $('#id_open_name').val(),
                };
                break;
        }
        $('#form_payment').attr({"data-type": 0});
        $('#form_payment').submit();
    });

    // 修改支付方式
    $('.update_payment').on('click', function () {
        var type = $(this).parent().siblings(".type-td").html();
        var kind_src = $(this).parent().siblings(".kind-td").find("img").attr("src");
        var kind_arr = kind_src.split('.');
        var kind_str = kind_arr[0].split('/')[4];
        $.ajax({
            url: $(this).attr('api'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('#form_payment [name=csrfmiddlewaretoken]').val()
            },
            cache: false,
            success: function (data) {
                if (data.status == 0) {
                    DTS.alert(data.msg);
                } else {
                    $('#modal_payment').replaceWith(data);
                    $('#modal_payment').modal({backdrop: 'static', keyboard: false});
                    $('.modal-title').text('修改支付方式');
                    $('#submit_payment_add').hide();
                    $('#submit_payment_update').show();
                    $(".logo-name").removeClass("hide");
                    $("#form_payment").validate();
                    switch (type) {
                        case "线上支付":
                            $(".pay-method").removeClass("hide");
                            $(".online-msg").removeClass("hide");
                            switch (kind_str) {
                                case "alipay":
                                    $(".online-msg").addClass("hide");
                                    $("#alipay_msg").removeClass("hide");
                                    $("#pay_alipay").attr('selected', "selected");
                                    break;
                                case "weixin":
                                    $(".online-msg").addClass("hide");
                                    $("#weixin_msg").removeClass("hide");
                                    $("#pay_weixin").attr('selected', "selected");
                                    break;
                                case "wealth":
                                    $(".online-msg").addClass("hide");
                                    $("#alipay_msg").removeClass("hide");
                                    $("#pay-wealth").attr('selected', "selected");
                                    break;
                                case "onlinepay":
                                    $(".online-msg").addClass("hide");
                                    $("#onlinepay_msg").removeClass("hide");
                                    $("#pay_onlinepay").attr('selected', "selected");
                                    break;
                                case "e-bank":
                                    $(".online-msg").addClass("hide");
                                    $("#e-bank_msg").removeClass("hide");
                                    $("#pay_ebank").attr('selected', "selected");
                                    break;
                            }
                            break;
                        case "线下支付":
                            $(".offline-msg").removeClass("hide");
                            $("#pay_off").attr('selected', "selected");
                            break;
                        case "预存款支付":
                            $("#pay_advance").attr('selected', "selected");
                            break;
                        case "货到付款":
                            $("#pay_good").attr('selected', "selected");
                            break;
                    }
                }
            },
            error: function () {
                DTS.alert('网络异常，请刷新重试');
            }
        });
    });

    // 取消修改
    $(document).on('click', ".btn-cancel", function () {
        window.location.reload();
    });

    // 修改提交
    $(document).on('click', '#submit_payment_update', function () {
        switch ($('#id_logo').val()) {
            case "alipay":
                api_json = {
                    'taobao_account': $('#id_taobao_account').val(),
                    'cooperate_id': $('#id_cooperate_id').val(),
                    'security_note': $('#id_security_note').val(),
                    'public_key': $('#id_public_key').val(),
                    'private_key': $('#id_private_key').val()
                };
                break;
            case "weixin":
                api_json = {
                    'weixin_no': $('#id_weixin_no').val()
                };
                break;
            case "wealth":
                api_json = {
                    'wealth_no': $('#id_wealth_no').val()
                };
                break;
            case "onlinepay":
                api_json = {
                    'onlinepay_no': $('#id_onlinepay_no').val(),
                };
                break;
            case "e-bank":
                api_json = {
                    'open_ebank': $('#id_open_ebank').val(),
                    'open_eaccount': $('#id_open_eaccount').val(),
                    'open_ename': $('#id_open_ename').val(),
                };
                break;
            case "offlinepay":
                api_json = {
                    'open_bank': $('#id_open_bank').val(),
                    'open_account': $('#id_open_account').val(),
                    'open_name': $('#id_open_name').val(),
                };
                break;
        }
        $('#form_payment').attr({"data-type": 1});
        $('#form_payment').submit();
    });

    // 删除支付方式
    $('#content').on('click', '.delete_payment', function () {
        var api = $(this).attr('api');
        DTS.confirm("删除后无法恢复，您确定要删除吗？", function () {
            $.ajax({
                url: api,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('#form_payment [name=csrfmiddlewaretoken]').val()
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
    });

    // 启用禁用
    $('.table').on('click', '.switch-default', function () {
        var html;
        var $this = $(this);
        var api = $(this).attr('api');
        var is_active = $(this).attr('is_active');
        if (is_active === '0') {
            html = "禁用后该支付方式不可使用，确定要禁用吗？"
        } else {
            html = "开启后该支付方式可使用！"
        }
        DTS.confirm(html, function () {
            $.ajax({
                url: api,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'is_lock': is_active
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    // DTS.alert(data.msg, function () {
                    //     window.location.reload();
                    // });
                    DTS.affirm(data.msg, data.status == 1);
                    DTS.switch($this);
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

    });
    /************************是否修改排序***************************/
    var sort_flag = false;
    $("td input").change(function () {
        sort_flag = true;
    });
    //保存排序
    $("#btn_save_sort").on('click', function () {
        var data = [];
        $('table input').each(function () {
            var pk = $(this).data('pk');
            var value = $(this).prop('value');
            data.push({"pk": pk, "value": value});
        });
        if (sort_flag) {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'data': JSON.stringify(data),
                    'order_name': "order_no"
                },
                cache: false,
                success: function (data) {
                    // DTS.alert(data.msg, function () {
                    //     window.location.reload();
                    // });
                    DTS.affirm(data.msg, data.status == 1);
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        } else {
            DTS.affirm("未进行任何修改");
        }
    });


}($);