var DTS = window.DTS || {};
DTS.admin_role = function ($) {
    $(document).ready(function () {
        // 全选所有当前权限的所有子权限
        $(".ch-all").on('click', function () {
            var $this = $(this);
            var perm_id = $this.attr('id');
            if ($this.is(":checked")) { // 选中
                $("input." + "ch-perm-" + perm_id + "[type=checkbox]").prop('checked', true);
                $("input." + "sec-ch-all-" + perm_id + "[type=checkbox]").prop('checked', true);
                DTS.admin_role.set_all_check(true);
            } else {
                $("input." + "ch-perm-" + perm_id + "[type=checkbox]").prop('checked', false);
                $("input." + "sec-ch-all-" + perm_id + "[type=checkbox]").prop('checked', false);
                DTS.admin_role.set_all_check(false);
            }
        });

        // 全选当前二级权限下的所有权限
        $(".sec-ch-all").on('click', function () {
            var $this = $(this);
            var perm_id = $this.attr('id');
            if ($this.is(":checked")) { // 选中
                $("input." + "sec-ch-perm-" + perm_id + "[type=checkbox]").prop('checked', true);
                DTS.admin_role.set_all_check(true);
            } else {
                $("input." + "sec-ch-perm-" + perm_id + "[type=checkbox]").prop('checked', false);
                DTS.admin_role.set_all_check(false);
            }
        });

        // 设置权限选中
        $("table input.perm-item[type=checkbox]").on('click', function () {
            var $this = $(this);
            if ($this.is(":checked")) {
                DTS.admin_role.set_all_check(true);
            } else {
                DTS.admin_role.set_all_check(false);
            }
        });
        // 展开
        $(".basic-set-tr").on('click', function () {
            var $this = $(this).children('.basic-set');
            var perm_id = $this.attr('id');
            if ($this.hasClass('icon-opedown')) {
                $this.removeClass("icon-opedown").addClass("icon-cloright");
                $(".settings-pane-" + perm_id).addClass('hide');
            } else {
                $this.removeClass("icon-cloright").addClass("icon-opedown");
                $(".settings-pane-" + perm_id).removeClass('hide');
            }
        });
        // 设置权限表收缩展开
        $("#hide_show").on('click', function () {
            var txt = $(this).html();
            if (txt == "全部收起") {
                $("#set-permission .iconfont").removeClass("icon-opedown").addClass("icon-cloright");
                $(".settings").addClass("hide");
                $(this).text("全部展开");
            } else {
                $("#set-permission .iconfont").removeClass("icon-cloright").addClass("icon-opedown");
                $(".settings").removeClass("hide");
                $(this).text("全部收起");
            }
        });

        // 设置权限
        $(".set").on('click', function () {
            $("#set-permission").removeClass("hide");
            var role_id = $(this).attr('id');
            $("#role_id").val(role_id);
            $("#set-perm-pane input[type='checkbox']").prop('checked', false);
            // 权限设置面板打开
            $(this).addClass('active');
            $(this).parents("tr").addClass("tr-hover");
            $(this).parents("tr").siblings().removeClass("tr-hover");
            var topH = $(this).offset().top - 375;
            var leftW = $(this).offset().left - 105;
            $('#set-permission').css({"top": topH});
            $('#set-permission').css({"left": leftW});
            // 设置保存权限
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    "role_id": role_id
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data.status == 1) {
                        var perm_list = eval(data.perm_lst);
                        // 循环设置当前角色已有权限
                        $.each(perm_list, function (index, perm) {
                            // document.getElementById(perm.codename).setAttribute("checked",true);
                            var obj = document.getElementById(perm.codename);
                            $(obj).prop("checked", true);
                        });
                        DTS.admin_role.set_all_check(true);
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
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

        // 添加角色
        $('#content').on('click', '.add', function () {
            DTS.clear_form('#common_form');
            $('#common_modal').modal({
                backdrop: 'static',
                keyboard: false,
                show: true
            });
            $('.modal-title').text('添加角色');
            $('#submit_add').show();
            $('#submit_update').hide();
            $('#common_form').validate();
        });
        // 提交添加角色
        $(document).on('click', '#submit_add', function () {
            $('#common_form').attr({"data-type": 0});
            $('#common_form').submit();
        });
        // 修改角色模态框
        $('#content').on('click', '.update', function () {
            $('.modal-title').text('修改角色');
            DTS.loading_dialog(true);
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $(' [name=csrfmiddlewaretoken]').val()
                },
                cache: false,
                success: function (data) {
                    DTS.loading_dialog(false);
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        $('#common_modal').replaceWith(data);
                        $('.modal-title').text('修改角色');
                        $('#common_modal').modal({
                            backdrop: 'static',
                            keyboard: false,
                            show: true
                        });
                        $('#submit_add').hide();
                        $('#submit_update').show();
                        $('#common_form').validate();
                    }
                },
                error: function () {
                    DTS.loading_dialog(false);
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        // 更新角色信息
        $(document).on('click', '#submit_update', function () {
            $('#common_form').attr({"data-type": 1});
            $('#common_form').submit();
        });

        // 删除角色
        $('#content').on('click', '.delete', function () {
            var url = $(this).attr('api');
            DTS.confirm('确定要删除此角色吗?', function () {
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
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
        });

        // 保存角色权限设置
        $("#set-permission #role-save").on('click', function () {
            var perm_code_list = $.map($("table input.perm-item[type=checkbox]:checked"), function (obj) {
                return obj.value;
            });
            // if (perm_code_list.length === 0) {
            //     DTS.affirm('请先选择要授予的权限');
            //     return;
            // }
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'perm_code': JSON.stringify(perm_code_list),
                    'role_id': $('#role_id').val()
                },
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1)
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        // 取消设置
        $("#set-permission #role-cancel").on('click', function () {
            $("#set-permission").addClass("hide");
            $("#table_role tr").removeClass("tr-hover");
            //$("#set-perm-pane input[type='checkbox']").attr('checked',false);
        });
    });

    return {
        // 设置全选按钮是否选中操作
        set_all_check: function (flag) {
            $("input:checkbox[class*=sec-ch-all-]").each(function (index, perm) {
                var $this = $(this);
                // // 当前二级全选下的所有子权限
                var $prev_prem = $this.parent().prev(".basic-td");
                var all_len = $prev_prem.find("input[class*=sec-ch-perm-]").length;
                var sec_len = $prev_prem.find("input[class*=sec-ch-perm-]:checked").length;
                if (flag) {
                    if (sec_len == all_len) {
                        $this.prop("checked", true);
                    }
                } else {
                    if (sec_len < all_len) {
                        $this.prop("checked", false);
                    }
                }
            });
            // 判断当前权限树中，下级权限全选按钮是否选中
            $("input.ch-all[type=checkbox]").each(function (index, perm) {
                var $this = $(this);
                var perm_id = $this.attr("id");
                var all_len = $("input.sec-ch-all-" + perm_id + "[type=checkbox]").length;
                var sec_len = $("input.sec-ch-all-" + perm_id + "[type=checkbox]:checked").length;
                if (flag) {
                    if (sec_len == all_len) {
                        $this.prop("checked", true);
                    }
                } else {
                    if (sec_len < all_len) {
                        $this.prop("checked", false);
                    }
                }
            });
        }
    }

}($);