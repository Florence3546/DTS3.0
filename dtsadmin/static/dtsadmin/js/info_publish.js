var DTS = window.DTS || {};
DTS.info_publish = function ($) {
    $(document).ready(function () {
        var editor = {}; //用于获取富文本组件
        $.validator.setDefaults({
            submitHandler: function () {
                DTS.disable_btn("#modal_publish_add_btn");
                //处理CKeditor 提交表单不提交Ckeditor元素
                for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
                if ($("#info_content").val() == "") {
                    DTS.alert("信息内容不能为空");
                    return;
                }
                $.ajax({
                    url: '/dtsadmin/publish_manage/',
                    type: 'POST',
                    data: $("#publish_add_form").serialize(),
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        if (data.status == 1) {
                            $('#modal_information').modal('hide');
                            editor.setData('');
                            DTS.clear_form('#publish_add_form');
                            $("#s_info_type").val('');
                            $("#s_info_status").val('');
                            DTS.info_publish.load_publish_data(1);

                        } else {
                            DTS.enable_btn("#modal_publish_add_btn");
                            return;
                        }
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                        DTS.enable_btn("#modal_publish_add_btn");
                        return;
                    }
                });
            },
            rules: {
                order_no: {
                    required: true,
                    range: [1, 99]
                }
            },
            messages: {
                order_no: {
                    range: '请输入{0}到{1}之间的正整数'
                }
            },
            errorPlacement: function (error, element) { //指定错误信息位置
                if (element.is(':radio') || element.is(':checkbox')) { //如果是radio或checkbox
                    var eid = element.attr('name'); //获取元素的name属性
                    error.appendTo(element.parent()); //将错误信息添加当前元素的父结点后面
                } else {
                    error.insertAfter(element);
                }
            }
        });

        //初始化
        editor = DTS.info_publish.init_ckeditor('info_content');
        //分页初始化
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.info_publish.load_publish_data);
            DTS.data_table("#table-info")
        }
        //查询列表
        $("#info_search_btn").on("click", function () {
            DTS.info_publish.load_publish_data(1);
        });

        // 更多查询条件显示与否控制
        var form_val = $('#s_info_type').val() ||
            $("#s_info_status").val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }
        /*-------------------------表格多选按钮------------------------*/
        DTS.Check('.check-all', '.check-item');

        //打开添加信息模态框
        $("#add_info").on("click", function () {
            $("#modal_information .modal-title").html("添加信息服务");
            $("#modal_information #publish_op_type").val("add");
            DTS.info_publish.init_modal();
            $("#publish_add_form").validate();
            DTS.clear_form('#modal_information');
            editor.setData();
            $('#modal_information').modal({backdrop: 'static', keyboard: false, show: true});
        });

        //保存发布信息
        $(document).on('click', '#modal_publish_add_btn', function () {
            $("#publish_add_form").submit();
        });

        //编辑发布信息
        $(".info_update").on("click", function () {
            $("#modal_information .modal-title").html("编辑信息服务");
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
                        $('#modal_information').replaceWith(data);
                        $("#publish_add_form").validate();
                        $('#modal_information').modal({backdrop: 'static', keyboard: false, show: true});
                        DTS.info_publish.init_modal();
                        $("#modal_information #publish_op_type").val("edit");
                        editor = DTS.info_publish.init_ckeditor('info_content');
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        //删除单个发布信息
        $(".info_delete").on("click", function () {
            var api = $(this).attr('api')
            DTS.confirm("您确定要删除此条资讯公告吗？", function () {
                $.ajax({
                    url: api,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                    },
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        if (data.status == 1) {
                            var timer_reload = setInterval(function () {
                                clearInterval(timer_reload);
                                DTS.info_publish.load_publish_data(1);
                            }, 3000);

                        }
                    }, error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            });
        });
        //批量删除
        $("#delete_batch_btn").on("click", function () {
            DTS.info_publish.info_batch_op('del_batch', "您确定要删除选中的资讯公告吗？");
        });
        // 批量投放信息
        $("#pub_batch_btn").on("click", function () {
            DTS.info_publish.info_batch_op('act_batch', "您确定要投放选中的资讯公告吗？");
        });
        // 批量屏蔽信息
        $("#shield_batch_btn").on("click", function () {
            DTS.info_publish.info_batch_op('shd_batch', "您确定要屏蔽选中的资讯公告吗？");
        });
        // 信息预览
        $(".info_show").on("click", function () {
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
                        $('#modal_info_preview').replaceWith(data);
                        $('#modal_info_preview').modal({backdrop: 'static', keyboard: false, show: true});
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });
    });

    //接口定义
    return {
        //查询加载数据列表
        load_publish_data: function (load_page) {
            $("#page").val(load_page);
            $("#s_info_name").val($.trim($("#s_info_name").val()));
            DTS.loading_dialog(true);
            $("#publish_search_from").submit();
        },
        //初始化模态框
        init_modal: function (obj) {
            //开始时间
            $("#start_date").datetimepicker({
                format: "yyyy-mm-dd",
                minView: 2,
                showMeridian: true,
                autoclose: true,
                pickDate: true,
                pickTime: true,
                todayBtn: true,
                minuteStep: 1
            }).on('changeDate', function (ev) {
                var start_date = $("#start_date").val();
                $("#end_date").datetimepicker('setStartDate', start_date);
                $("#start_date").datetimepicker("hide");
            });
            //结束时间
            $("#end_date").datetimepicker({
                format: "yyyy-mm-dd",
                minView: 2,
                showMeridian: true,
                autoclose: true,
                todayBtn: true,
                minuteStep: 1
            }).on('changeDate', function () {
                var start_date = $("#start_date").val();
                var end_date = $("#end_date").val();
                if (start_date != "" && end_date != "") {
                    if (DTS.info_publish.checkEndTime(start_date, end_date)) {
                        $("#end_date").val('');
                        DTS.affirm("开始时间大于结束时间");
                        return;
                    }
                }
            });
        },
        //判断两个时间
        checkEndTime: function (start_date, end_date) {
            var gap = (Date.parse(start_date) - Date.parse(end_date));
            var cha = (Date.parse(start_date) - Date.parse(end_date)) / 86400000 * 24;
            if (gap > 0) { //开始时间大于结束时间
                return true;
            }
            return false;
        },
        init_ckeditor: function (container_id) {
            //移除高级
            // CKEDITOR.config.removeDialogTabs = 'image:advanced;link:advanced';
            //初始化创建 CKEDITOR
            var editor1 = CKEDITOR.replace(container_id,
                {
                    toolbar: [
                        ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
                        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
                        ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
                        ['Link', 'Unlink', 'Anchor'],
                        ['Image', 'multiimg', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
                        '/',
                        ['Styles', 'Format', 'Font', 'FontSize'],
                        ['TextColor', 'BGColor'],
                        ['Maximize', 'ShowBlocks', '-']
                    ],
                    width: 740,
                    filebrowserImageUploadUrl: '/ckeditor/upload/',
                    image_previewText: '',
                }
            );
            return editor1;
        },
        //批量删除，投放，屏蔽操作
        info_batch_op: function (op_type, msg) {
            var enter_id_list = $.map($("table input.check-item[type=checkbox]:checked"), function (obj) {
                return obj.value;
            });
            if (enter_id_list.length === 0) {
                DTS.affirm('必须勾选一行');
                return;
            }

            console.log(op_type);
            DTS.confirm(msg, function () {
                $.ajax({
                    url: '/dtsadmin/publish_manage/',
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'op_type': op_type,
                        'info_ids': JSON.stringify(enter_id_list)
                    },
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        if (data.status == 1) {
                            var timer_reload = setInterval(function () {
                                clearInterval(timer_reload);
                                DTS.info_publish.load_publish_data(1);
                            }, 3000);

                        }
                    }, error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            });
        }
    }
}($);