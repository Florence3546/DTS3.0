var DTS = window.DTS || {};
DTS.admin_good_category = function ($) {
    $(document).ready(function () {

        $('#table_good_category').on('click', 'a.triangle', function () {
            var tr_obj = $(this).closest('tr');
            var tr_level = Number(tr_obj.attr('level'));
            var next_tr = tr_obj.next();
            var next_level = Number(next_tr.attr('level'));
            if ($(this).hasClass('triangle-bottom')) {
                $(this).removeClass('triangle-bottom');
                while (next_tr.length > 0 && next_level > tr_level) {
                    next_tr.addClass('hide');
                    next_tr = next_tr.next();
                    next_level = Number(next_tr.attr('level'));
                }
            } else {
                $(this).addClass('triangle-bottom');
                while (next_tr.length > 0 && next_level > tr_level) {
                    if (Number(next_tr.attr('level')) === tr_level + 1) {
                        next_tr.removeClass('hide').find('a.triangle').removeClass('triangle-bottom');
                    }
                    next_tr = next_tr.next();
                    next_level = Number(next_tr.attr('level'));
                }
            }
        });

        //搜索商品分类 按钮事件触发
        $("#btn_search").on("click", function () {
            var search_enterprise_name = $.trim($("#search_enterprise_name").val());
            if (search_enterprise_name != undefined && search_enterprise_name != "") {
                $('#table_good_category tbody>tr').addClass('hide');
                $('#table_good_category tbody>tr').each(function () {
                    var td_text = $(this).find('td:eq(0)').text();
                    if (td_text.indexOf(search_enterprise_name) != -1) {
                        $(this).removeClass('hide').find('a.triangle').removeClass('triangle-bottom');
                        var path_list = $(this).attr('obj_path').split('/');
                        $.each(path_list, function (i, obj_id) {
                            if (obj_id) {
                                var temp_tr = $('#table_good_category tbody>tr[obj_id=' + obj_id + ']');
                                temp_tr.removeClass('hide').find('a.triangle').addClass('triangle-bottom');
                            }
                        });
                    }
                })
            } else {
                $('#table_good_category tbody>tr').each(function () {
                    $(this).removeClass('hide').find('a.triangle').addClass('triangle-bottom');
                })
            }
        });

        $.validator.setDefaults({
            submitHandler: function () {
                if ($("#common_form").data("type") == 0) {
                    $.ajax({
                        url: $("#submit_add").attr('api'),
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
                } else {
                    $.ajax({
                        url: $("#submit_update").attr('api'),
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
                }
            }
        });

        // 添加商品分类
        $('#add_root_category').on('click', function () {
            DTS.clear_form('#common_form');
            $('#common_modal').modal({backdrop: 'static', keyboard: false});
            $('.modal-title').text('添加');
            $('#submit_add').show();
            $('#submit_update').hide();
            $('#category_level').html("类目级别：");
            $('#good_category_path').val('/');
            $('#good_category_path_display').text("一级");
            $("#common_form").validate();
        });

        $('#table_good_category .add').on('click', function () {
            DTS.clear_form('#common_form');
            $('#common_modal').modal({backdrop: 'static', keyboard: false});
            $('.modal-title').text('添加子类目');
            $('#submit_add').show();
            $('#submit_update').hide();
            var tr_obj = $(this).closest('tr');
            $('#category_level').html("上级类目：");
            $('#good_category_path').val(tr_obj.attr('obj_full_path'));
            $('#good_category_path_display').text(tr_obj.attr('obj_name'));
            $("#common_form").validate();
        });

        $(document).on('click', '#submit_add', function () {
            $('#common_form').attr({"data-type": 0});
            $('#common_form').submit();
        });

        // 修改商品模态框
        $('#table_good_category').on('click', '.update', function () {
            $('#common_modal').modal({backdrop: 'static', keyboard: false});
            var tr_obj = $(this).closest('tr');
            $('#submit_add').hide();
            $('#submit_update').show();
            if (tr_obj.attr('level') == 0) {
                $('.modal-title').text('修改');
                $('#category_level').html("类目级别：");
                $('#good_category_path_display').text("一级");
            } else {
                $('.modal-title').text('修改子类目');
                $('#category_level').html("上级类目：");
                $('#good_category_path_display').text(tr_obj.attr('obj_path_display'));
            }
            $('#good_category_id').val(tr_obj.attr('obj_id'));
            $('#good_category_name').val(tr_obj.attr('obj_name'));
            $('#good_category_path').val(tr_obj.attr('obj_path'));
            $("#common_form").validate();
        });

        $(document).on('click', '#submit_update', function () {
            $('#common_form').attr({"data-type": 1});
            $('#common_form').submit();
        });


        //删除商品分类
        $('#table_good_category').on('click', '.delete', function () {
            var url = $(this).attr('api');
            DTS.confirm('确定要删除此商品吗?', function () {
                $.ajax({
                    url: url,
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
                        DTS.affirm('发生错误');
                    }
                });

            }, '删除');
        });


    })
}($);