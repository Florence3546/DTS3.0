var DTS = window.DTS || {};
DTS.admin_feedback = function ($) {
    $(document).ready(function () {

        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.admin_feedback.load_consult_data);
            DTS.data_table('#table_feedback');
        }

        // 处理全选，复选
        DTS.Check(".check-all", ".check-item");

        //  删除咨询反馈（单个删除）
        $('.consult_feedback_delete').on('click', function () {
            var api = $(this).attr('api');
            console.log('afdsa');
            DTS.confirm("删除不可恢复，请确认是否删除?", function () {
                $.ajax({
                    url: api,
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
        });

        // 批量删除
        $("#del_batch").on('click', function () {
            var feed_id_list = $.map($("table input.check-item[type=checkbox]:checked"), function (obj) {
                return obj.value;
            });
            if (feed_id_list.length === 0) {
                DTS.affirm('必须勾选一行');
                return;
            }
            DTS.confirm("删除不可恢复，请确认是否删除?", function () {
                $.ajax({
                    url: '/dtsadmin/consult_feedback/',
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'method': 'del_batch',
                        'cf_ids': JSON.stringify(feed_id_list)
                    },
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                    }, error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            });
        });

        // 设为显示，取消显示（批量处理）
        $("#set_show,#cancel_show").on('click', function () {
            // 获取当前选中所有ID
            var feed_id_list = $.map($("table input.check-item[type=checkbox]:checked"), function (obj) {
                return obj.value;
            });
            // 判断是否选中
            if (feed_id_list.length === 0) {
                DTS.affirm('必须勾选一行');
                return;
            }
            // 获取当前执行操作：显示还是取消显示
            var method = $(this).attr('method');
            $.ajax({
                url: '/dtsadmin/consult_feedback/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': method,
                    'cf_ids': JSON.stringify(feed_id_list)
                },
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        //打开回复咨询反馈模态框
        $(".consult_feedback_replied").on("click", function () {
            $("#consult_feedback_modal .modal-title").html("回复");
            $("#consult_feedback_modal #feedback_type").val("replied");
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
                        $('#consult_feedback_modal').replaceWith(data);
                        $('#consult_feedback_modal').modal({backdrop: 'static', keyboard: false, show: true});
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        // 保存回复咨询反馈
        $(document).on('click', '#modal_feedback_replied_btn', function () {
            $("#info_content").val($.trim($("#info_content").val()));
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#feedback_form').serialize(),
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                    if (data.status == 1) {
                        $('#consult_feedback_modal').modal('hide');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
    });

    return {
        load_consult_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            DTS.loading_dialog(true);
            $("#feedback_search_from").submit();
        }
    }
}($);