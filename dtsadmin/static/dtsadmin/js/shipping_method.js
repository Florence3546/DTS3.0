var DTS = window.DTS || {};
DTS.switch = function () {
    $(document).ready(function () {
        $.validator.setDefaults({
            submitHandler: function () {
                if ($("#form_delivery").data("type") == 0) {
                    $.ajax({
                        url: $("#submit_delivery_add").attr("api"),
                        type: 'POST',
                        data: $('#form_delivery').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            DTS.affirm(data.msg, data.status == 1);
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                } else {
                    $.ajax({
                        url: $("#submit_delivery_update").attr('api'),
                        type: 'POST',
                        data: $('#form_delivery').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            DTS.affirm(data.msg, data.status == 1);
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                }
            },
            rules: {
                website: {
                    url: true
                },
                order_no: {
                    required: true,
                    digits: true
                }
            },
            messages: {
                website: {
                    url: "请输入有效网址"
                },
                order_no: {
                    digits: '请输入整数'
                }
            }
        });

        // 添加快递公司
        $('#content').on('click', '.add_delivery', function () {
            DTS.clear_form('#form_delivery');
            $('#modal_delivery').modal({backdrop: 'static', keybord: false, show: true});
            $("#form_delivery").validate();
            $('.modal-title').text('添加快递公司');
            $('#submit_delivery_add').show();
            $('#submit_delivery_update').hide();
            $("#shipping_type").val("");
        });

        $(document).on('click', '#submit_delivery_add', function () {
            $('#form_delivery').attr({"data-type": 0});
            $('#form_delivery').submit();
        });

        // 修改快递模态框弹出
        $('#content').on('click', '.update_delivery', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('#form_delivery [name=csrfmiddlewaretoken]').val()
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        $('#modal_delivery').replaceWith(data);
                        $('#modal_delivery').modal({backdrop: 'static', keyboard: false, show: true});
                        $("#form_delivery").validate();
                        $('.modal-title').text('修改快递');
                        $('#submit_delivery_add').hide();
                        $('#submit_delivery_update').show();
                    }

                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        // 修改模态框提交
        $(document).on('click', '#submit_delivery_update', function () {
            $('#form_delivery').attr({"data-type": 1});
            $('#form_delivery').submit();
        });


        // 删除快递
        $('#content').on('click', '.delete_delivery', function () {
            var url = $(this).attr('api');
            DTS.confirm('确定要删除此商品吗?', function () {
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('#form_delivery [name=csrfmiddlewaretoken]').val()
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1)
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            }, '删除');
        });

        // 修改快递状态
        $('.delivery_is_active').on('click', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('#form_delivery [name=csrfmiddlewaretoken]').val()
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1)
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 启用禁用
        $('.table').on('click', '.switch-default', function () {
            var html;
            var $this = $(this);
            var api = $(this).attr('api');
            var is_active = $(this).attr('is_active');
            if (is_active === '0') {
                html = "禁用后该配送方式不可使用，确定要禁用吗？"
            } else {
                html = "开启后该配送方式可使用！"
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
                        DTS.affirm(data.msg, data.status == 1);
                        DTS.switch($this);
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            });
        });
        var sort_flag = false;
        $("td input").change(function () {
            sort_flag = true;
        });
        //保存排序
        $("#btn_save_sort").on('click', function () {
            var data = [];
            var flag = true;
            $('table input').each(function () {
                var pk = $(this).data('pk');
                var value = $(this).prop('value');
                if (isNaN(value) || value == "") {
                    flag = false;
                }
                data.push({"pk": pk, "value": value});
            });

            if (sort_flag) {
                if (flag) {
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
                            DTS.affirm(data.msg, data.status == 1);
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                } else {
                    DTS.affirm("请输入数字");
                }
            } else {
                DTS.affirm("未进行任何修改");
            }
        });
    })
}($);
