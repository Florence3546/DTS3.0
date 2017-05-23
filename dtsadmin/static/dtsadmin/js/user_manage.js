var DTS = window.DTS || {};
DTS.admin_user = function ($) {
    $(document).ready(function () {
        // 通用全选功能
        DTS.Check('.check-all', '.check-item');

        // 表头固定
        DTS.data_table('#table_user');

        // 分页事件绑定
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.admin_user.load_user_data);
        }

        /*-------------------------查询------------------------*/
        var form_val = $('#search_usertype').val() ||
            $('#search_full_name').val() ||
            $('#search_enter_name').val() ||
            $('#search_is_active').val() ||
            $('#search_date_joined_from').val() ||
            $('#search_date_joined_to').val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }

        /*-------------------------下拉菜单自适应------------------------*/
        $("table").on("click", ".dropdown-toggle", function () {
            var h = -$(this).next().height() - 15;
            if (window.innerHeight - $(this).offset().top > 200) {
                $(this).next().css({"top": "100%"});
            } else {
                $(this).next().css({"top": h + "px"});
            }
        });

        jQuery.validator.addMethod("isMobile", function (value, element) {
            var mobile = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
            return this.optional(element) || (mobile.test(value));
        }, "请正确填写您的电话号码");
        jQuery.validator.addMethod("isEmail", function (value, element) {
            var email = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/ || /^[a-z\d]+(\.[a-z\d]+)*@([\da-z](-[\da-z])?)+(\.{1,2}[a-z]+)+$/;
            return this.optional(element) || (email.test(value));
        }, "请正确填写您的邮箱");
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
            },
            rules: {
                phone: {
                    isMobile: true
                },
                email: {
                    isEmail: true
                },
                role_list: "required"
            }
        });


        /*-------------------------添加用户------------------------*/
        $('#content').on('click', '.add', function () {
            $(".enterprise_member").addClass("hide");
            $(".system_user").addClass("hide");
            $(".system_enterprise").addClass("hide");
            $(".individual_member").removeClass("hide");
            $(".enterprise_name").removeClass("hide");
            DTS.clear_form('#common_form');
            // 用户类型处理
            $('#user_type').prop('disabled', false);
            // 默认选择性别男 赋值
            $('.radio_checked').prop('checked', true);
            $('#enterprise_gender').val($("[name='sex']:checked").val());
            //重复密码展示
            $('.passwd2').show();
            $('[name="passwd"]').prop('disabled', false);
            $('[name="passwd2"]').prop('disabled', false);
            $('.reset_password').hide();
            // 设置默认密码
            $('#passwd').val('123456');
            $('#passwd2').val('123456');
            $('.default_passwd').show().text('默认密码123456');
            // $('.passwd2').hide();
            // 默认选择不是企业主账户 赋值
            $('.checkbox_NO').prop('checked', true);
            $('#is_main').val($("[name='master']:checked").val());

            $('#common_modal').modal({backdrop: 'static', keyboard: false});
            $('.modal-title').text('添加');
            $('#submit_add').show();
            $('#submit_update').hide();

            //设置表单提交的action
            $('#post_action').val('add_user');

            $("#common_form").validate();

        });

        /*-------------------------添加用户类型切换------------------------*/
        $(document).on('change', '#user_type', function () {
            $(".enterprise_member").addClass("hide");
            $(".system_user").addClass("hide");
            $(".system_enterprise").addClass("hide");
            $(".individual_member").removeClass("hide");
            if ($(this).val() == "Members") { // 个人会员 Members
                $(".individual_member").addClass("hide");
            } else if ($(this).val() == "System") { //系统用户 System
            		$(".system").val($(".system").data('value'));
            		$(".system_enterprise").val($(".system_enterprise").data('value'));
                $(".system_user").removeClass("hide");
                $(".system_enterprise").removeClass("hide");
                $(".enterprise_name").addClass("hide");
            } else if ($(this).val() == "Purchaser"||$(this).val() == "Supplier"||$(this).val() == "Regulator") { //企业用户 Purchaser
                $(".enterprise_member").removeClass("hide");
                $(".enterprise_name").removeClass("hide");
            }
        });


        /*-------------------------性别------------------------*/

        $("[name='sex']").change(function () {
            var gender = $("[name='sex']:checked").val();
            $('#enterprise_gender').val(gender);
        });


        /*-------------------------重置密码------------------------*/
        $(".reset-password").on("click", function () {
            $(this).prev().val("123456");
        });

        $("[name='master']").change(function () {
            var main_master = $("[name='master']:checked").val();
            $('#is_main').val(main_master);
        });
    });

    $(document).on('click', '#submit_add', function () {
    	  console.log($(".system_enterprise").val());
        $('#post_action').val('add_user');
        $('#common_form').attr({"data-type": 0});
        $('#common_form').submit();
    });

    /*-------------------------修改用户模态框------------------------*/
    $('#content').on('click', '.update', function () {
        var pk = $(this).data('pk');
        $.ajax({
            url: $(this).attr('api'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                'action': 'get_user',
                'pk': pk
            },
            cache: false,
            success: function (data) {
                if (data.status == 0) {
                    DTS.affirm(data.msg);
                } else {
                    $('#common_modal').replaceWith(data);
                    $('.modal-title').text('修改用户');
                    $('#common_modal').modal({backdrop: 'static', keyboard: false});
                    $('#submit_add').hide();
                    $('#submit_update').show();
                    // 用户类型处理
                    $('#user_type').prop('disabled', true);
                    var userr_type = $('#user_type').val();
                    $(".enterprise_member").addClass("hide");
                    $(".system_user").addClass("hide");
                    $(".individual_member").removeClass("hide");
                    if (userr_type == "Members") { // 个人会员 Members
                        $(".individual_member").addClass("hide");
                    } else if (userr_type == "System") { //系统用户 System
                        $(".system_user").removeClass("hide");
                        $(".enterprise_name").addClass("hide");
                    } else if (userr_type == "Purchaser"||userr_type == "Supplier"||userr_type == "Regulator") { //企业用户 Purchaser
                        $(".enterprise_member").removeClass("hide");
                        $(".enterprise_name").removeClass("hide");
                        $(".system_enterprise").addClass("hide");
                    }
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

                    //是否是企业主账户赋值
                    $('#is_main').val($("[name='master']:checked").val());
                    $('[name="master"]').on('change', function () {
                        $('#is_main').val($("[name='master']:checked").val());
                    });

                    $('#enterprise_is_master').on('change', function () {
                        $('#enterprise_is_master').val(this.checked ? 'on' : '');
                    });
                    $('#enterprise_is_qualified').on('change', function () {
                        $('#enterprise_is_qualified').val(this.checked ? 'on' : '');
                    });
                    $('#enterprise_is_lock').on('change', function () {
                        $('#enterprise_is_lock').val(this.checked ? 'on' : '');
                    });
                }
            },
            error: function () {
                DTS.affirm(DTS.tips_error);
            }
        });
    });

    // 修改表单提交
    $(document).on('click', '#submit_update', function () {
        $('#post_action').val('update_user');
        $('#common_form').attr({"data-type": 1});
        $('#common_form').submit();
    });


    /*-------------------------查看用户------------------------*/
    $('#content').on('click', '.look_user', function () {
        var pk = $(this).data('pk');
        $.ajax({
            url: $(this).attr('api'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                'action': 'look_user',
                'pk': pk
            },
            cache: false,
            success: function (data, status, xhr) {
                if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                    DTS.affirm(data.msg);
                } else {
                    $('#check_user_modal').replaceWith(data);
                    $('#check_user_modal').modal({backdrop: 'static', keyboard: false});
                    $('.modal-title').text('查看用户');
                }
            },
            error: function () {
                DTS.affirm(DTS.tips_error);
            }
        });
    });


    /*-------------------------删除用户------------------------*/
    $('#content').on('click', '.delete', function () {
        var url = $(this).attr('api');
        DTS.confirm("确认要删除该用户？", function () {
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'update_user',
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

    /*-------------------------锁定 解锁------------------------*/

    $('.is_lock').on('click', function () {
        var id_list = $.map($("input[name='chk_list']:checked"), function (obj) {
            return obj.value;
        });
        console.log($(this).attr('id'));

        if (id_list.length === 0) {
            alert('必须勾选一行');
            return;
        }
        var is_lock = 0;
        if ($(this).attr('id') == 'unlock') {
            is_lock = 1;
        } else {
            is_lock = 0;
        }

        $.ajax({
            url: $(this).attr('api'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                'id_list': JSON.stringify(id_list),
                'is_lock': is_lock
            },
            dataType: 'json',
            cache: false,
            success: function (data) {
                DTS.affirm(data.msg);
                window.location.reload();
            },
            error: function () {
                DTS.affirm(DTS.tips_error);
            }
        });
    });

    return {
        load_user_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#search_username").val($.trim($("#search_username").val()));
            $("#search_full_name").val($.trim($("#search_full_name").val()));
            $("#search_enter_name").val($.trim($("#search_enter_name").val()));
            DTS.loading_dialog(true);
            $("#search_form").submit();
        }
    };

}($);