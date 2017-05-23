var DTS = window.DTS || {};
DTS.account_info = function ($) {
    $(document).ready(function () {
        //
        $(".feedback-nav li").on('click', function () {
            var index = $(this).index();
            $(this).addClass("active");
            $(this).siblings().removeClass("active");
            $(".feedback-content>div").addClass("hide");
            $(".feedback-content>div").eq(index).removeClass("hide");
        });

        //
        $(".feedback-type .message").on('click', function () {
            $(this).addClass("active");
            $(this).siblings().removeClass("active");
            $('#id_feedback_type').val('0');
        });

        //
        $(".feedback-type .suggest").on('click', function () {
            $(this).addClass("active");
            $(this).siblings().removeClass("active");
            $('#id_feedback_type').val('1');
        });

        // 处理全选，复选
        // 全选按钮 click
        $('th .check-all').click(function () {
            if ($(this).is(":checked")) { //全选
                $('table input[type=checkbox]').each(function () {
                    if ($(this).attr("disabled") == undefined) {
                        $(this).prop('checked', true);
                    }
                });
            } else {
                $('table input[type=checkbox]').prop('checked', false);
            }
        });

        // 多选单个选中操作
        $("tbody input[type=checkbox]").on('click', function () {
            var selected_len = $("tbody input[type=checkbox]:checked").length;
            var all_len = $("tbody input[type=checkbox]").length;
            var dis_len = $("tbody input[type=checkbox]:disabled").length;
            if (selected_len == (all_len - dis_len)) {
                $('th .check-all').prop('checked', true);
            } else {
                $('th .check-all').prop('checked', false);
            }
        });

        //  删除咨询反馈（单个删除）
        $('.delete').on('click', function () {
            console.log('afdsa');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.alert(data.msg, function () {
                        window.location.reload();
                    });
                    //window.location.href = '?feedback_type=' + data.feedback_type;
                    // window.location.reload();
                },
                error: function (e) {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // 批量删除
        $("#del_batch").on('click', function () {
            var feed_id_list = $.map($("table input.check-item[type=checkbox]:checked"), function (obj) {
                return obj.value;
            });
            if (feed_id_list.length === 0) {
                alert('必须勾选一行');
                return;
            }
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
                    DTS.alert(data.msg, function () {
                        if (data.status == 1) {
                            $("#s_feedback_type").val('');
                            $("#s_feedback_status").val('');
                            $("#feedback_search_from").submit();
                            //window.location.reload();
                        }
                    });
                }, error: function () {
                    DTS.alert(DTS.tips_error);
                }
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
                alert('必须勾选一行');
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
                    DTS.alert(data.msg, function () {
                        if (data.status == 1) {
                            window.location.reload();
                        }
                    });
                }, error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });


        //
        $('.submit_feedback').on('click', function () {
            console.log('afdsa');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#feedback_form').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.alert(data.msg, function () {
                        window.location.href = '?feedback_type=' + data.feedback_type;
                    });
                },
                error: function (e) {
                    DTS.alert(DTS.tips_error);
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
                        DTS.alert(data.msg);
                    } else {
                        $('#consult_feedback_modal').replaceWith(data);
                        $('#consult_feedback_modal').modal({backdrop: 'static', keyboard: false, show: true});
                    }
                }, error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });
        /* add_info click end */


        // 保存回复咨询反馈
        $(document).on('click', '#modal_feedback_replied_btn', function () {
            $("#info_content").val($.trim($("#info_content").val()));
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#feedback_form').serialize(),
                cache: false,
                success: function (data) {
                    DTS.alert(data.msg, function () {
                        if (data.status == 1) {
                            $('#modal_feedback').modal('hide');
                            window.location.reload()
                        }
                    });
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });
    });

    return {}

}($);
