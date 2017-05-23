var DTS = window.DTS || {};
DTS.admin_lack = function ($) {
    $(document).ready(function () {

        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.admin_lack.load_lack_data);
            DTS.data_table('#table_order');
        }

        // 更多查询条件显示与否控制
        var form_val = $('#lack_state').val() ||
            $("#register_created_from").val() ||
            $('#register_created_to').val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }

        /*-------------------------表格多选按钮------------------------*/
        DTS.Check('.check-all', '.check-item');

        // 删除
        $('#content').on('click', '.delete', function () {
            var page = $("#page").val();
            DTS.confirm("删除后不可恢复，您确认删除吗？", function () {
                $.ajax({
                    url: $('.delete').attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        if (data.status == 1) {
                            var timer = setInterval(function () {
                                clearInterval(timer);
                                DTS.admin_lack.load_lack_data(page);
                            }, 2000);
                        }
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            }, "删除提醒")
        });

        // 批量删除
        $('#bulk_delete').on('click', function () {
            var id_list = $.map($("input[name='chk_list']:checked"), function (obj) {
                return parseInt(obj.value);
            });
            DTS.confirm("删除后不可恢复，您确认删除吗？", function () {
                $.ajax({
                    url: $('#bulk_delete').attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'id_list': JSON.stringify(id_list)
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
    });

    return {
        // 接口定义
        load_lack_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#good_name").val($.trim($("#good_name").val()));
            DTS.loading_dialog(true);
            $("#search_lack_form").submit();
        }
    }

}($);