var DTS = window.DTS || {};
DTS.admin_enterprise = function ($) {
    $(document).ready(function () {

        // 手机号码或者座机号验证
        jQuery.validator.addMethod("isMobile", function (value, element) {
            var length = value.length;
            var mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0-9]|170)\d{8}$/;
            var phone = /^\d{3}-\d{8}|\d{4}-\d{7}$/;
            return this.optional(element) || (mobile.test(value));
        }, "请正确填写您的电话号码");

        jQuery.validator.addMethod("isEmail", function (value, element) {
            var length = value.length;
            var email = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/ || /^[a-z\d]+(\.[a-z\d]+)*@([\da-z](-[\da-z])?)+(\.{1,2}[a-z]+)+$/;
            return this.optional(element) || (email.test(value));
        }, "请正确填写您的邮箱");

        $.validator.setDefaults({
            submitHandler: function () {
                if ($("#common_form").data("type") == 0) {
                    $.ajax({
                        url: $('.add').attr('api'),
                        type: 'POST',
                        data: $('#common_form').serialize(),
                        dataType: 'json',
                        contentType: false,
                        processData: false,
                        cache: false,
                        success: function (data) {
                            DTS.affirm(data.msg);
                            //返回错误提示
                            if (data.status == 0, data.status == 1) {
                                $('.error').css('visibility', 'visible');
                                $('#err_msg').text(data.msg);
                                $('#submit_add').attr('disabled', false);
                            }
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
                        contentType: false,
                        processData: false,
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
            },
            rules: {
                user_phone: {
                    isMobile: true
                },
                enter_phone: {
                    isMobile: true
                },
                email: {
                    isEmail: true
                }
            },
            message: {}
        });

        /*-------------------------表格多选按钮------------------------*/
        DTS.Check('.check-all', '.check-item');

        // 分页事件绑定
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.admin_enterprise.load_enterprise_data);
            DTS.data_table('#table_enterprises');
        }

        /*-------------------------添加企业------------------------*/
        $('#content').on('click', '.add', function () {
            DTS.clear_form('#common_form');
            // radio 默认选中
            $('.radio_checked').prop('checked', true);
            // 默认选择性别男 赋值
            $('#enterprise_gender').val($("[name='sex']:checked").val());
            //重复密码展示
            $('.passwd2').show();
            $('[name="passwd"]').prop('disabled', false);
            $('[name="passwd2"]').prop('disabled', false);
            $('.reset_password').hide();
            // 删掉图片
            $('.upload_file img').remove();

            $('#common_modal').modal({backdrop: 'static', keyboard: false});
            $('.modal-title').text('添加企业');
            $('#submit_add').show();
            $('#submit_update').hide();

            $("#common_form").validate();
        });

        $(document).on('click', '#submit_add', function () {
            $('#common_form').attr({"data-type": 0});
            $('#common_form').submit();
        });

        /*-------------------------修改企业模态框------------------------*/
        $('#content').on('click', '.update', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'get_enterprise',
                    'pk': pk
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        DTS.affirm(data.msg);
                    } else {
                        $('#common_modal').replaceWith(data);
                        $('.modal-title').text('修改企业');
                        $('#common_modal').modal({backdrop: 'static', keyboard: false});
                        $('#submit_add').hide();
                        $('#submit_update').show();
                        $("#common_form").validate();

                        // 密码处理
                        $('.passwd2').hide();
                        $('[name="passwd"]').prop('disabled', true);
                        $('[name="passwd2"]').prop('disabled', true);
                        $('[name="passwd"]').val('********');
                        $('.reset_password').show();
                        $('.reset_password').on('click', function () {
                            $('[name="passwd"]').prop('disabled', false);
                            $('[name="passwd2"]').prop('disabled', false);
                            $('.passwd2').show();
                            $('[name="passwd"]').val('');
                            $('[name="passwd2"]').val('');
                        });

                        //性别赋值
                        $('#enterprise_gender').val($("[name='sex']:checked").val());
                        $('[name="sex"]').on('change', function () {
                            $('#enterprise_gender').val($("[name='sex']:checked").val());
                        });

                        //地区选择
                        // $('[data-toggle="distpicker"]').distpicker();

                        var region = $('#region').val().split(',');

                        var arg = {};
                        if (region[0]) {
                            arg.province = region[0];
                            $('.province').removeClass('hide');
                        }
                        if (region[1]) {
                            arg.city = region[1];
                            $('.city').removeClass('hide');
                        }
                        if (region[2]) {
                            arg.district = region[2];
                            $('.district ').removeClass('hide');
                        }

                        $('#distpicker').distpicker(arg);
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        $(document).on('click', '#submit_update', function () {
            $('#common_form').attr({"data-type": 1});
            $('#common_form').submit();
        });

        /*-------------------------删除企业------------------------*/
        $('#content').on('click', '.delete', function () {
            var _this = $(this);
            DTS.confirm("你确定要删除吗？", function () {
                $.ajax({
                    url: _this.attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                    }
                });
            })
        });

        /*-------------------------审核企业------------------------*/
        $('#content').on('click', '.check_enter', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'verify_enterprise',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#enterprise_check_modal').replaceWith(data);
                        $('#enterprise_check_modal').modal({backdrop: 'static', keyboard: false});
                        $('.modal-title').text('审核企业');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 审核 通过 不通过
        $(document).on('click', '.verify_enter', function () {
            var pk = $(this).data('pk');
            var method = $(this).data('method');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'verify_enter',
                    'method': method,
                    'pk': pk
                },
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                    if (data.status == 1) {
                        $('#enterprise_check_modal').modal('hide');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------查看企业------------------------*/
        $('#content').on('click', '.look_enter', function () {
            var pk = $(this).data('pk');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'look_enterprise',
                    'pk': pk
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        DTS.affirm(data.msg);
                    } else {
                        $('#enterprise_check_modal').replaceWith(data);
                        $('.verify_enter').hide();
                        $('#enterprise_check_modal').modal({backdrop: 'static', keyboard: false});
                        $('.modal-title').text('查看企业');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------锁定 解锁------------------------*/
        $('.enterprise_is_lock').on('click', function () {
            var enter_id_list = $.map($("input[name='chk_list']:checked"), function (obj) {
                return obj.value;
            });
            if (enter_id_list.length === 0) {
                DTS.affirm('必须勾选一行');
                return;
            }
            var is_lock = 0;
            if ($(this).attr('id') == 'enterprise_lock') {
                is_lock = 1;
            } else {
                is_lock = 0;
            }
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'enter_id_list': JSON.stringify(enter_id_list),
                    'is_lock': is_lock
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
        /*------------------------批量删除------------------------*/

        $('.delete_enterprises').on('click', function () {
            $("#confirm").modal({backdrop: 'static', keyboard: false});
            DTS.confirm('你确定要删除吗？', function () {
                // var enter_id_list = get_enter_id_list();
                var enter_id_list = $.map($("input[name='chk_list']:checked"), function (obj) {
                    return obj.value;
                });
                console.log(enter_id_list);
                $.ajax({
                    url: $('#delete_enterprises').attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'enter_id_list': JSON.stringify(enter_id_list),
                        'action': 'delete_enterprises',
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        if (data.status == 1) {
                            var timer = setInterval(function () {
                                clearInterval(timer);
                                DTS.admin_enterprise.load_enterprise_data(1);
                            }, 2000);
                        }
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            }, '批量删除');
        });

        /*-------------------------查询企业------------------------*/
        var form_val = $('#search_enterprise_legal_repr').val() ||
            $('#search_enterprise_created_from').val() ||
            $('#search_enterprise_created_to').val() ||
            $('#search_enterprise_operate_mode').val() ||
            $('#member_grade').val() ||
            $('#search_enterprise_review_status').val() ||
            $('#search_enterprise_is_lock').val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }

        /*-------------------------性别------------------------*/
        $("[name='sex']").change(function () {
            console.log('member_sex');
            var gender = $("[name='sex']:checked").val();
            $('#enterprise_gender').val(gender);
        });

        /*-------------------------地区设置------------------------*/
        $('[data-toggle="distpicker"]').distpicker();

        var province, City, District;
        $(document).on('change', '.province', function () {
            $(".city").removeClass('hide');
            $(".district").addClass('hide');
            province = $(".province").val();
            $('#region').val(province)
        });

        $(document).on('change', '.city', function () {
            $(".district").removeClass('hide');
            City = $(".city").val();
            $('#region').val(province + ',' + City)
        });

        $(document).on('change', '.district', function () {
            District = $(".district").val();
            $('#region').val(province + ',' + City + ',' + District)
        });

        /*-------------------------经营范围------------------------*/
        function handle_biz_scope() {
            var biz_scope_list = $(".check_box input:checked").map(function () {
                return this.value
            }).get().join(',');
            if (biz_scope_list.length == 0) {
                DTS.affirm('请至少选择经营范围');
                return false;
            } else {
                return biz_scope_list;
            }
        }

        /*-------------------------图片上传------------------------*/
        $(document).on('click', '.upload_file', function () {
            $(this).next("[type='file']").click();
        });
    });

    return {
        load_enterprise_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#search_enterprise_name").val($.trim($("#search_enterprise_name").val()));
            $("#search_enterprise_legal_repr").val($.trim($("#search_enterprise_legal_repr").val()));
            DTS.loading_dialog(true);
            $("#search_enterprise_form").submit();
        },
        // 预览图片
        preview_img: function (files, container_id) {
            if (files.length) {
                var file = files[0];
                var imgaeType = /^image\//;
                var $img = $('<img>');
                $img.attr('src', window.URL.createObjectURL(file));
                $img.data('file', file);
                $img.on('load', function () {
                    window.URL.revokeObjectURL(this.src);
                });
                // $('#' + container_id).append($img);
                $('#' + container_id).html($img);
            } else {
                $('#' + container_id).empty();
            }
        }
    };

}($);
