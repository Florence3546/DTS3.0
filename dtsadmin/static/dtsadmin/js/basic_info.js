var DTS = window.DTS || {};
DTS.admin_settings = function ($) {

    //基本信息功能
    $(document).ready(function () {
        /***********前台网站 TAB操作***********/
        // 手机号码或者座机号验证
        jQuery.validator.addMethod("isMobile", function (value, element) {
            var length = value.length;
            var mobile = /^1(3|4|5|7|8)\d{9}$/;
            // var mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0-9]|170)\d{8}$/;
            var phone = /^\d{3}-\d{8}$|\d{4}-\d{7}$/;
            return this.optional(element) || (mobile.test(value)) || (phone.test(value));
        }, "请正确填写您的电话号码");

        $.validator.setDefaults({
            submitHandler: function () {
                DTS.disable_btn("#submit_front_site_add");
                $.ajax({
                    url: '/dtsadmin/basic_info/',
                    type: 'POST',
                    data: $('#form_site_settings').serialize(),
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        DTS.enable_btn("#submit_front_site_add");
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                        DTS.enable_btn("#submit_front_site_add");
                    }
                });
            },
            rules: {
                admin_phone: {
                    isMobile: true
                }
            },
            messages: {}
        });
        $().ready(function () {
            $("#form_site_settings").validate();
            $("#work_date").val($("#select_work_date_start").val())
            $("#work_date_end").val($("#select_work_date_end").val())
        });
        /***********后台LOGO TAB操作***********/
        // 模拟File标签单击事件
        $("#upload_btn").on("click", function () {
            $("#site_logo").trigger("click");
        });
        //File内容change事件
        $("#site_logo").on('change', function () {
            var photoExt = $("#site_logo").val().substr($("#site_logo").val().lastIndexOf(".")).toLowerCase();//获得文件后缀名
            if (/\.(gif|jpg|jpeg|png|GIF|JPG|PNG)$/.test(photoExt)) {
                DTS.admin_settings.preview_img(this.files, 'logo_preview')
            }
        });
        // LOGO图片
        $("#logo_settings_btn").on('click', function () {

            DTS.disable_btn("#logo_settings_btn");
            var fileName = $.trim($("#site_logo").val());
            if (fileName == undefined || fileName == "") {
                DTS.affirm("请先选择要上传的文件");
                DTS.enable_btn("#logo_settings_btn");
                return false;
            }
            var photoExt = $("#site_logo").val().substr($("#site_logo").val().lastIndexOf(".")).toLowerCase();//获得文件后缀名
            if (!/\.(gif|jpg|jpeg|png|GIF|JPG|PNG)$/.test(photoExt)) {
                DTS.affirm("仅支持gif、png、jpg格式的图片文件!");
                DTS.enable_btn("#logo_settings_btn");
                return false;
            }
            var logo_href = $.trim($("#logo_submit").val());
            if (logo_href == "") {
                DTS.affirm('Logo链接地址不能为空!');
                $("#logo_submit").focus();
                DTS.enable_btn("#logo_settings_btn");
                return false;
            }
            var match = /^((ht|f)(tp|tps)?):\/\/([\w\-]+(\.[\w\-]+)*\/)*[\w\-]+(\.[\w\-]+)*\/?(\?([\w\-\.,@?^=%&:\/~\+#]*)+)?/
            if (!match.test(logo_href)) {
                DTS.affirm('Logo链接地址格式输入有误，请核对!');
                $("#logo_submit").select();
                DTS.enable_btn("#logo_settings_btn");
                return false;
            }
            var form_data = new FormData($('#form_logo_settings')[0]);
            $.ajax({
                url: '/dtsadmin/basic_info/',
                type: 'POST',
                data: form_data,
                dataType: 'json',
                contentType: false,
                processData: false,
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    if (data.status == 1) {
                        $("#base_admin_logo").attr('src', data.logo_path);
                        $("#base_admin_href").attr('href', data.logo_href);
                    }
                    DTS.enable_btn("#logo_settings_btn");
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                    DTS.enable_btn("#logo_settings_btn");
                }
            });
        });

        /***********客服设置 TAB操作***********/
        // 按钮操作
        $(document).on('click', '.switch-default', function () {
            var switch_btn = $(this).children().eq(0);
            if (switch_btn.hasClass("hide")) {
                DTS.confirm('修改后将开启该功能，确认是否修改？修改后点击保存生效。', function () {
                    switch_btn.removeClass("hide");
                    switch_btn.siblings().addClass("hide");
                    DTS.affirm("修改成功！");
                });

            } else {
                DTS.confirm('修改后将关闭该功能，确认是否修改？修改后点击保存生效。', function () {
                    switch_btn.addClass("hide");
                    switch_btn.siblings().removeClass("hide");
                    DTS.affirm("修改成功！");
                });
            }
        });

        // 添加客服人员
        $('#add_service').on('click', function () {
            $("#modal_service .modal-title").html("添加客服账号");
            $("#QQ_number").val("");
            $("#nike_name").val("");
            $("#modal_service_sort").val("Y");
            $("#service_account_op").val("add");
            $('#modal_service').modal({backdrop: 'static', keyboard: false, show: true});
        });
        // 编辑客服人员
        $("#edit_service").on("click", function () {
            $("#modal_service .modal-title").html("编辑客服账号")
            var select_op = $('#service_account option:selected');
            if (select_op.length == 0) {
                DTS.affirm("暂无可编辑客服人员！");
                return false;
            }
            //设置弹出框值回显
            $("#QQ_number").val($.trim(select_op.val()));
            $("#nike_name").val($.trim(select_op.text()));
            $("#modal_service_sort").val($.trim(select_op.attr("modal_service_sort")))
            //保存原有值
            $("#old_QQ_number").val($.trim(select_op.val()));
            $("#old_nike_name").val($.trim(select_op.text()));
            $("#old_modal_service_sort").val($.trim(select_op.attr("modal_service_sort")))
            $("#service_account_op").val("up");
            $('#modal_service').modal({backdrop: 'static', keyboard: false, show: true});
        });
        // 删除客服人员
        $("#delete_service").on("click", function () {
            var service_account_list = JSON.parse($("#service_account_list").val());
            var select_op = $('#service_account option:selected');
            if (select_op.length == 0) {
                DTS.affirm("暂无可删除客服人员！");
                return false;
            }
            for (var index = 0; index < service_account_list.length; index++) {
                if (service_account_list[index].QQ_number == select_op.val()) {
                    service_account_list.splice(index, 1);
                }
            }
            DTS.admin_settings.reset_select(service_account_list);
        });
        //客户设置 客户人员添加
        $("#modal_service_account_btn").on("click", function () {
            //当前填入值
            var QQ_number = $.trim($("#QQ_number").val());
            var nike_name = $.trim($("#nike_name").val());
            var modal_service_sort = $.trim($("#modal_service_sort").val());
            var reg = /^[1-9]\d+$/;
            if (QQ_number == undefined || QQ_number == "" || !reg.test(QQ_number)) {
                DTS.affirm("您的QQ号未输入或输入有误，请先核对！");
                $("#QQ_number").select();
                return false;
            }
            if (nike_name == undefined || nike_name == "") {
                DTS.alert("请先输入昵称");
                $("#nike_name").select();
                return false;
            }
            var service_account = {QQ_number: QQ_number, nike_name: nike_name, modal_service_sort: modal_service_sort};
            var service_account_op = $("#service_account_op").val();
            //获取原有JSON串，并转为JSON对象
            var service_account_list = JSON.parse($("#service_account_list").val());
            if (service_account_op == "add") {//添加操作
                service_account_list.push(service_account);
            } else if (service_account_op == "up") {//更新操作
                for (var index = 0; index < service_account_list.length; index++) {
                    //移除原有的,并用新的替代
                    var old_QQ_number = $.trim($("#old_QQ_number").val());
                    if (old_QQ_number == service_account_list[index].QQ_number) {
                        service_account_list.splice(index, 1, service_account);
                    }
                }
            }
            DTS.admin_settings.reset_select(service_account_list, QQ_number);
            $('#modal_service').modal('hide');
        });
        // 提交客服设置
        $("#consult_settings_btn").on("click", function () {
            DTS.disable_btn("#consult_settings_btn");
            DTS.admin_settings.set_isOrNot("consult_setting_pane", "enable_cust_service");
            // 判断工作日
            if ($('#work_date option:selected').attr("val") > $('#work_date_end option:selected').attr("val")) {
                DTS.alert("工作日结束时间应大于工作日开始时间", function () {
                    $("#work_date").focus();
                });
                DTS.enable_btn("#consult_settings_btn");
                return false;
            }
            // 判断在线时间
            if ($('#time_online option:selected').attr("val") > $('#time_online_end option:selected').attr("val")) {
                DTS.alert("在线结束时间应大于在线开始时间", function () {
                    $("#time_online").focus();
                });
                DTS.enable_btn("#consult_settings_btn");
                return false;
            }
            // 判断客服电话
            var phone_ext = $.trim($("#input_service_number").val());
            if (!(/^1(3|4|5|7|8)\d{9}$/.test(phone_ext))) {
                DTS.alert("客服电话输入有误,请核查!", function () {
                    $("#input_service_number").select();
                });
                DTS.enable_btn("#consult_settings_btn");
                return false;
            }
            // 判断客服账号
            var service_account_len = $("#service_account option").length;
            if (service_account_len <= 0) {
                DTS.alert("请至少添加一个客服账号!", function () {
                    $("#service_account").focus();
                });
                DTS.enable_btn("#consult_settings_btn");
                return false;
            }
            $.ajax({
                url: '/dtsadmin/basic_info/',
                type: 'POST',
                data: $('#form_consult_settings').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    DTS.enable_btn("#consult_settings_btn");
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                    DTS.enable_btn("#consult_settings_btn");
                }
            });
        });

        /***********登录验证 TAB操作***********/
        //图片验证
        $(".picture").on('click', function () {
            var switch_btn = $(this).children().eq(0);
            if (switch_btn.hasClass("hide")) {
                $(".picture_verify").removeClass("hide");
            } else {
                $(".picture_verify").addClass("hide");
            }
        });
        //短信验证
        $(".message").on('click', function () {
            var switch_btn = $(this).children().eq(0);
            if (switch_btn.hasClass("hide")) {
                $(".message_verify").removeClass("hide");
            } else {
                $(".message_verify").addClass("hide");
            }
        });
        //提交登录验证
        $("#auth_settings_btn").on("click", function () {
            DTS.disable_btn("#auth_settings_btn");
            DTS.admin_settings.set_isOrNot("picture_limit_pane", "verify_limit_picture");
            DTS.admin_settings.set_isOrNot("message_limit_pane", "message_limit_verify");
            $.ajax({
                url: '/dtsadmin/basic_info/',
                type: 'POST',
                data: $('#form_auth_settings').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    DTS.enable_btn("#auth_settings_btn");
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                    DTS.enable_btn("#auth_settings_btn");
                }
            });
        });

        /******* 信息提醒 TAB操作*******/
        $("#remind_settings_btn").on("click", function () {
            DTS.disable_btn("#remind_settings_btn");
            var remind_arr = [];
            $("#remind_tbody tr").each(function (index) {
                var remind_settings = {};
                var tdArr = $(this).children();
                var reminder_con = tdArr.eq(0).text();
                var reminder_key = tdArr.eq(0).attr('data-key');
                var notify_obj = tdArr.eq(1).text();
                remind_settings['reminder_key'] = reminder_key;
                remind_settings['reminder_con'] = reminder_con;
                remind_settings['notify_obj'] = notify_obj;
                tdArr.eq(2).find(".remind-switch").each(function (index) {
                    var obj = $(this);
                    obj.children().each(function (index) {
                        if (!$(this).hasClass('hide')) {
                            remind_settings[obj.attr('key')] = $(this).attr("val");
                        }
                    });
                });
                tdArr.eq(3).find(".remind-switch").each(function (index) {
                    var obj = $(this);
                    obj.children().each(function (index) {
                        if (!$(this).hasClass('hide')) {
                            remind_settings[obj.attr('key')] = $(this).attr("val");
                        }
                    });
                });
                tdArr.eq(4).find(".remind-switch").each(function (index) {
                    var obj = $(this);
                    obj.children().each(function (index) {
                        if (!$(this).hasClass('hide')) {
                            remind_settings[obj.attr('key')] = $(this).attr("val");
                        }
                    });
                });
                remind_arr.push(remind_settings);
            });
            var form_data = JSON.stringify(remind_arr);
            $("#remind_settings_val").val(form_data);
            $.ajax({
                url: '/dtsadmin/basic_info/',
                type: 'POST',
                data: $("#form_remind_settings").serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    DTS.enable_btn("#remind_settings_btn");
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                    DTS.enable_btn("#remind_settings_btn");
                }
            });
        });
    });

//接口定义
    return {
        // 图片预览
        preview_img: function (files, container_id) {
            if (files.length) {
                $('#' + container_id).empty();
                var file = files[0];
                var imgaeType = /^image\//;
                var $img = $('<img>');
                $img.attr('src', window.URL.createObjectURL(file));
                $img.attr('class', 'img-responsive');
                $img.data('file', file);
                $img.on('load', function () {
                    window.URL.revokeObjectURL(this.src);
                });
                $('#' + container_id).html($img);
            } else {
                $('#' + container_id).empty();
            }
        },
        //重构select
        reset_select: function (service_account_list, cur_val) {
            $("#service_account").empty();
            for (var index = 0; index < service_account_list.length; index++) {
                var service = service_account_list[index];
                $("#service_account").append("<option value=\"" + service.QQ_number + "\"  modal_service_sort=\"" + service.modal_service_sort + "\">" + service.nike_name + "</option>");
            }
            if (cur_val != undefined && cur_val != "") {
                $("#service_account").val(cur_val);
            }
            $("#service_account_list").val(JSON.stringify(service_account_list));
        },
        // 设置是否
        set_isOrNot: function (doc_id, val_id) {
            $('#' + doc_id).children().each(function (index) {
                if (!$(this).hasClass('hide')) {
                    $("#" + val_id).val($.trim($(this).attr("val")));
                }
            });
        }
    }

}($);