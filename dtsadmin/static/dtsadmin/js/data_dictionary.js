var DTS = window.DTS || {};
DTS.admin_dictionary = function ($) {
    $(document).ready(function () {

        $.validator.setDefaults({
            submitHandler: function () {
                if ($("#form_settings_type").data("type") == 0) {
                    $.ajax({
                        url: $('#submit_settings_type_add').attr('api'),
                        type: 'POST',
                        data: $('#form_settings_type').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {

                            DTS.affirm(data.msg, data.status == 1);
                             if (data.status == 1){
                                $('#modal_settings_type').modal('hide');
                            }
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                } else if ($("#form_settings_type").data("type") == 1) {
                    $.ajax({
                        url: $('#submit_settings_type_update').attr('api'),
                        type: 'POST',
                        data: $('#form_settings_type').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            DTS.affirm(data.msg, data.status == 1);
                             if (data.status == 1){
                                $('#modal_settings_type').modal('hide');
                            }
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                } else if ($("#form_settings_item").data("type") == 0) {
                    $.ajax({
                        url: $('#submit_settings_item_add').attr('api'),
                        type: 'POST',
                        data: $('#form_settings_item').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            DTS.affirm(data.msg, data.status == 1);
                             if (data.status == 1){
                                $('#modal_settings_item').modal('hide');
                            }
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                } else {
                    $.ajax({
                        url: $('#submit_settings_item_update').attr('api'),
                        type: 'POST',
                        data: $('#form_settings_item').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            DTS.affirm(data.msg, data.status == 1);
                            if (data.status == 1){
                                $('#modal_settings_item').modal('hide');
                            }
                        },
                        error: function () {
                            DTS.affirm(DTS.tips_error);
                        }
                    });
                }
            },
            rules: {},
            messages: {}
        });

        // 过滤表格数据
        $('#filter_name').on('change', function () {
            if (this.value) {
                $('#table_settings>tbody>tr').hide();
                var tr_obj = $('#table_settings>tbody>tr[obj_code=' + this.value + ']');
                tr_obj.show();
                $('#table_settings>tbody>tr[obj_s_type_id=' + tr_obj.attr('obj_id') + ']').show();
            } else {
                $('#table_settings>tbody>tr').show();
            }
        });

        // 添加基础设置
        $('#content').on('click', '.add_settings_type', function () {
            form_settings_type.reset();
            $('#modal_settings_type').modal({backdrop: 'static', keyboard: false});
            $('#label_settings_type').text('添加字典项');
            $('#submit_settings_type_add').show();
            $('#submit_settings_type_update').hide();
            $("#form_settings_type").validate();
        });

        $('#submit_settings_type_add').on('click', function () {
            $('#form_settings_type').attr({"data-type": 0});
            $('#form_settings_type').submit();
        });

        // 修改基础设置
        $('#content').on('click', '.update_settings_type', function () {
            // form_settings_type.reset();
            $('#modal_settings_type').modal({backdrop: 'static', keyboard: false});
            $('#label_settings_type').text('修改字典项');
            $('#submit_settings_type_add').hide();
            $('#submit_settings_type_update').show();
            var tr_obj = $(this).closest('tr');
            $('#settings_type_id').val(tr_obj.attr('obj_id'));
            $('#settings_type_name').val(tr_obj.attr('obj_name'));
            $('#settings_type_code').val(tr_obj.attr('obj_code'));
            $('#settings_type_note').val(tr_obj.attr('obj_note'));
            $("#form_settings_type").validate();
        });

        $('#submit_settings_type_update').on('click', function () {
            $('#form_settings_type').attr({"data-type": 1});
            $('#form_settings_type').submit();
        });

        // 删除基础设置
        $('#content').on('click', '.delete_settings_type', function () {
            var _this = $(this);
            DTS.confirm("确认删除？", function () {
                $.ajax({
                    url: _this.attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('#form_settings_type [name=csrfmiddlewaretoken]').val()
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
            })
        });

        // 添加设置子项
        $('#content').on('click', '.add_settings_item', function () {
            form_settings_item.reset();
            $('#modal_settings_item').modal({backdrop: 'static', keyboard: false});
            $('#label_settings_item').text('添加子项');
            $('#submit_settings_item_add').show();
            $('#submit_settings_item_update').hide();
            var tr_obj = $(this).closest('tr');
            $('#settings_item_s_type').val(tr_obj.attr('obj_id'));
            $('#settings_item_s_type_name').text(tr_obj.attr('obj_name'));
            $("#form_settings_item").validate();
        });

        $('#submit_settings_item_add').on('click', function () {
            $('#form_settings_item').attr({"data-type": 0});
            $('#form_settings_item').submit();
        });

        // 修改设置子项
        $('#content').on('click', '.update_settings_item', function () {
            // form_settings_type.reset();
            $('#modal_settings_item').modal({backdrop: 'static', keyboard: false});
            $('#label_settings_item').text('修改子项');
            $('#submit_settings_item_add').hide();
            $('#submit_settings_item_update').show();
            var tr_obj = $(this).closest('tr');
            $('#settings_item_id').val(tr_obj.attr('obj_id'));
            $('#settings_item_s_type').val(tr_obj.attr('obj_s_type_id'));
            $('#settings_item_s_type_name').text(tr_obj.attr('obj_s_type_name'));
            $('#settings_item_name').val(tr_obj.attr('obj_name'));
            $('#settings_item_value').val(tr_obj.attr('obj_value'));
            $('#settings_item_note').val(tr_obj.attr('obj_note'));
            $("#form_settings_item").validate();
        });

        $('#submit_settings_item_update').on('click', function () {
            $('#form_settings_item').attr({"data-type": 1});
            $('#form_settings_item').submit();
        });

        // 删除设置子项
        $('#content').on('click', '.delete_setting_item', function () {
            var tr_obj = $(this).closest('tr');
            var _this = $(this);
            DTS.confirm("确认删除？", function () {
                $.ajax({
                    url: _this.attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('#form_settings_item [name=csrfmiddlewaretoken]').val()
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                        tr_obj.remove();
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            })
        });
    });

    return {
        // 接口定义
    }

}($);
