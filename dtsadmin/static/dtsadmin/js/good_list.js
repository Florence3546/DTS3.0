var DTS = window.DTS || {};
DTS.admin_good = function ($) {
    var del_photos = [];
    var del_quas = [];
    $(document).ready(function () {
        $.validator.setDefaults({
            submitHandler: function () {
                var op = $("#op_type").val();
                if (op == 'add') {
                    DTS.disable_btn("#submit_add");
                    DTS.admin_good.submit_add_good();
                } else {
                    DTS.disable_btn("#submit_update");
                    DTS.admin_good.submit_update_good();
                }
            },
            rules: {
                stock_amount: {
                    number: true,
                    max: 2147483647,
                    min: 0
                },
                retail_price: {
                    number: true,
                    min: 0
                },
                member_price: {
                    number: true,
                    min: 0
                }
            },
            messages: {
                stock_amount: {
                    max: "您输入的数值过大"
                }
            },
            errorPlacement: function (error, element) { //指定错误信息位置
                if (element.is(':radio') || element.is(':checkbox')) { //如果是radio或checkbox
                    var name = element.attr('name'); //获取元素的name属性
                    error.appendTo(element.parent().parent().parent()); //将错误信息添加当前元素的父结点后面
                } else {
                    error.appendTo(element.parent());
                }
            }
        });

        // 分页事件绑定
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.admin_good.load_good_data);
            DTS.data_table('#good_tab');
        }
        // 全选按钮 click
        DTS.Check('.check-all', '.check-item');
        // 更多查询条件显示与否控制
        var form_val = $('#search_good_trade_name').val() ||
            $("#search_good_license").val() ||
            $('#search_good_dosage_form').val() ||
            $('#search_good_category').val() ||
            $('#s_is_qua').val() ||
            $("#search_good_is_online").val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }
        // 打开添加商品
        $("#content").on('click', '#add_good', function () {
            DTS.admin_good.clear_form('#common_form');
            $('.modal-title').text('添加商品');
            $("#good_photo").removeClass('hide');
            $("#good_qualification").removeClass('hide');
            $('#submit_add').show();
            $('#submit_update').hide();
            DTS.admin_good.clear_ckeditor();
            DTS.admin_good.init_ckeditor("ck_desc_drug", 1);
            DTS.admin_good.init_ckeditor("ck_desc_good", 1);
            $("#good_photo_main img").remove();
            $("#good_photo_main").html('<span class="photo-main-text">+主图</span>');
            $("#good_photo_pane .pre-img").each(function () {
                $(this).remove();
            });
            $("#good_qua_pane .pre-img").each(function () {
                $(this).remove();
            });
            $('#add_good_modal').modal({
                backdrop: 'static', keyboard: false, show: true
            });
            $('#common_form').validate();
        });
        // 商品主图
        $(document).on('click', '#good_photo_main', function () {
            $("#good_photo_main_file").click();
        });
        // 商品图片
        $(document).on('click', '#good_photo', function () {
            $("#good_photo_file").click();
        });
        // 移除商品图片
        $(document).on('click', '#good_photo_pane .remove-img', function () {
            // 移除图片显示元素
            $(this).parent('.pre-img').remove();
            var exists_len = $("#good_photo").siblings('.pre-img').length;
            if (exists_len != undefined && exists_len < 4) {
                $("#good_photo").removeClass('hide');
            }
            var id = $(this).attr('val');
            if (id != undefined && id != "") {
                del_photos.push(id);
            }
        });
        // 商品资质
        $(document).on('click', '#good_qua', function () {
            $("#good_qua_file").click();
        });
        // 移除资质图片
        $(document).on('click', '#good_qua_pane .remove-img', function () {
            $(this).parent('.pre-img').remove();
            var exists_len = $("#good_qua").siblings('.pre-img').length;
            if (exists_len != undefined && exists_len < 4) {
                $("#good_qua").removeClass('hide');
            }
            var id = $(this).attr('val');
            if (id != undefined && id != "") {
                del_quas.push(id);
            }
        });
        // 提交添加
        $(document).on('click', '#submit_add', function () {
            $("#op_type").val('add');
            $('#common_form').submit();
        });
        // 删除商品
        $('#content').on('click', '.delete', function () {
            var url = $(this).attr('api');
            var page = $("#page").val();
            DTS.confirm('确定要删除此商品吗?', function () {
                // DTS.loading_dialog(true);
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        // DTS.loading_dialog(false);
                        DTS.affirm(data.msg);
                        if (data.status == 1) {
                            var timer = setInterval(function () {
                                clearInterval(timer);
                                DTS.admin_good.load_good_data(page);
                            }, 2000);
                        }
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            }, '删除商品');
        });

        // 打开修改商品窗口
        $(".update_good").on('click', function () {
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
                        $('#add_good_modal').replaceWith(data);
                        $('#add_good_modal').modal({backdrop: 'static', keyboard: false, show: true});
                        $('#add_good_modal .modal-title').text('修改商品');
                        $('#common_form').validate();
                        $('#submit_add').hide();
                        $('#submit_update').show();
                        DTS.admin_good.init_ckeditor("ck_desc_drug", 0);
                        DTS.admin_good.init_ckeditor("ck_desc_good", 0);
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 提交商品更新
        $(document).on('click', '#submit_update', function () {
            $("#op_type").val('upd');
            // DTS.loading_dialog(true);
            $('#common_form').submit();
        });
        // 查看商品 Single 打开弹出框
        $(".look_good").on('click', function () {
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
                        $('#check_good_modal').replaceWith(data);
                        $("#check_good_modal .modal-footer").addClass('hide');
                        $('#check_good_modal .modal-title').text('查看商品');
                        $('#check_good_modal').modal({backdrop: 'static', keyboard: false, show: true});
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 上架下架商品
        $(".switch_online").on('click', function () {
            var method = $(this).attr('method');
            var url = $(this).attr('api');
            var page = $("#page").val();
            var message = "确定要下架该商品吗?";
            var title = "下架商品";
            if (method == 'on') {
                message = "确定要上架该商品吗?";
                title = "上架商品";
            }
            DTS.confirm(message, function () {
                $.ajax({
                    url: url,
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
                                DTS.admin_good.load_good_data(page);
                            }, 2000);
                        }
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            }, title);
        });
        // 审核商品 Single 打开弹出框
        $(".switch_qualified").on('click', function () {
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
                        $('#check_good_modal').replaceWith(data);
                        $('#check_good_modal').modal({backdrop: 'static', keyboard: false, show: true});
                        $('#check_good_modal .modal-title').text('审核商品');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 提交审核【通过商品和不通过商品】
        $(document).on('click', '#check_good_modal .good_check', function () {
            var obj_id = $(this).attr('obj_id');
            var op_type = $(this).attr('op_type');
            var page = $("#page").val();
            $.ajax({
                url: "/dtsadmin/ajax/check_good_status/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'op_type': op_type,
                    'obj_id': obj_id
                },
                cache: false,
                success: function (data) {
                    DTS.alert(data.msg);
                    if (data.status == 1) {
                        var timer = setInterval(function () {
                            clearInterval(timer);
                            DTS.admin_good.load_good_data(page);
                        }, 2000);
                    }
                    $('#check_good_modal').modal('hide');
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 多条件查询
        $("#search_btn").on('click', function () {
            DTS.admin_good.load_good_data(1);
        });
        // 导出Excel
        $("#good-export-btn").on('click', function () {
            if (!$("#good-export-pane input[type='radio']").is(":checked")) {
                DTS.alert("请先选择要导出的商品数据", function () {
                    $("#good-export-pane input[type='radio']")[0].focus();
                });
                return;
            }
            var choose = $("#good-export-pane input[type='radio']:checked").val();
            var good_id_list = [];
            if (choose == 'ck') {
                good_id_list = $.map($("#good_tab input.good-item[type=checkbox]:checked"), function (obj) {
                    return obj.value;
                });
                if (good_id_list.length === 0) {
                    DTS.affirm('必须勾选一行');
                    $("#export_good_modal").modal('hide');
                    return;
                }
            }
            //查询条件
            $("#search_good_external_id").val($.trim($("#search_good_external_id").val()));
            $("#search_good_trade_name").val($.trim($("#search_good_trade_name").val()));
            $("#search_good_license").val($.trim($("#search_good_license").val()));
            $("#ex_choose").val(choose);
            $("#ex_good_ids").val(JSON.stringify(good_id_list));
            $("#search_good_form").attr('action', '/dtsadmin/exportGoodList/');
            $("#search_good_form").attr('target', '_blank');
            $("#search_good_form").submit();
            $("#search_good_form").attr('action', '/dtsadmin/good_list/');
            $("#search_good_form").removeAttr('target');
        });
    });

    return {
        load_good_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#search_good_external_id").val($.trim($("#search_good_external_id").val()));
            $("#search_good_trade_name").val($.trim($("#search_good_trade_name").val()));
            $("#search_good_license").val($.trim($("#search_good_license").val()));
            DTS.loading_dialog(true);
            $("#search_good_form").submit();
        },
        update_ckeditor: function () {
            //更新富文本内容到 Textarea
            if (CKEDITOR.instances != undefined) {
                for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
            }
        },
        clear_ckeditor: function () {
            //清除已经存在的 CKEDITOR
            if (CKEDITOR.instances != undefined) {
                for (name in CKEDITOR.instances) {
                    CKEDITOR.instances[name].destroy();
                }
            }
        },
        init_ckeditor: function (container_id, isEmpty) {
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
                    height: 380,
                    width: 720,
                    filebrowserImageUploadUrl: '/ckeditor/upload/',
                    image_previewText: '',
                }
            );
            if (isEmpty != undefined && isEmpty == 1) {
                editor1.setData('');
            }
            return editor1;
        },
        preview_img: function (files, container_id, len) {
            // 图片预览
            if (files.length) {
                for (var i in files) {
                    var file = files[i];
                    var imageType = /^image\//;
                    // 过滤图片文件
                    if (!imageType.test(file.type)) {
                        continue;
                    }
                    var pre = $('<a class="pre-img"><i class="remove-img">&times;</i></a>')
                    var $img = $('<img>');
                    $img.attr('src', window.URL.createObjectURL(file));
                    $img.data('file', file);
                    $img.on('load', function () {
                        window.URL.revokeObjectURL(this.src);
                    });
                    pre.append($img);
                    var exists_len = $("#" + container_id).siblings('.pre-img').length;
                    if (exists_len != undefined && exists_len < len) {
                        $('#' + container_id).before(pre);
                    }
                    var cur_len = $("#" + container_id).siblings('.pre-img').length;
                    if (cur_len != undefined && cur_len == len) {
                        $('#' + container_id).addClass('hide');
                    }
                }
            } else {
                $('#' + container_id).empty();
            }
        },
        preview_cur_img: function (files, container_id) {
            // 预览图片
            if (files.length) {
                var file = files[0];
                var imgaeType = /^image\//;
                var $img = $('<img class="main-img">');
                $img.attr('src', window.URL.createObjectURL(file));
                $img.data('file', file);
                $img.on('load', function () {
                    window.URL.revokeObjectURL(this.src);
                });
                $('#' + container_id).html($img);
            } else {
                $('#' + container_id).empty();
            }
        },
        clear_search_form: function (form_id) {
            // 清除form表单
            $(form_id).find('input').each(function () {
                switch (this.type) {
                    case 'text':
                        this.value = '';
                        break;
                    case 'password':
                        this.value = '';
                    case 'checkbox':
                    case 'radio':
                        this.checked = false;
                        break;
                }
            });
            $(form_id).find('textarea, select').val('');
        },
        submit_add_good: function () {
            DTS.disable_btn("#submit_add");
            // 提交添加商品
            DTS.admin_good.update_ckeditor();
            var page = $("#page").val();
            var form_data = new FormData($("#common_form")[0]);
            $('#good_photo_pane .pre-img  img').each(function () {
                if ($(this).data('file') != undefined && $(this).data('file') != "") {
                    form_data.append('good_photo', $(this).data('file'));
                }
            });
            $('#good_qua_pane .pre-img img').each(function () {
                if ($(this).data('file') != undefined && $(this).data('file') != "") {
                    form_data.append('good_qua', $(this).data('file'));
                }
            });
            $.ajax({
                url: "/dtsadmin/ajax/add_good/",
                type: 'POST',
                data: form_data,
                dataType: 'json',
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    if (data.status == 1) {
                        $('#add_good_modal').modal('hide');
                        var timer = setInterval(function () {
                            clearInterval(timer);
                            DTS.admin_good.clear_search_form("#search_good_form");
                            DTS.admin_good.load_good_data(1);
                        }, 2000)
                    }
                    DTS.enable_btn("#submit_add");
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                    DTS.enable_btn("#submit_add");
                }
            });
        },
        submit_update_good: function () {
            DTS.disable_btn("#submit_update");
            DTS.admin_good.update_ckeditor();
            var form_data = new FormData($("#common_form")[0]);
            var page = $("#page").val();
            $('#good_photo_pane .pre-img  img').each(function () {
                if ($(this).data('file') != undefined && $(this).data('file') != "") {
                    form_data.append('good_photo', $(this).data('file'));
                }
            });
            $('#good_qua_pane .pre-img img').each(function () {
                if ($(this).data('file') != undefined && $(this).data('file') != "") {
                    form_data.append('good_qua', $(this).data('file'));
                }
            });
            form_data.append('pho_id', JSON.stringify(del_photos));
            form_data.append('qua_id', JSON.stringify(del_quas));
            $.ajax({
                url: "/dtsadmin/ajax/update_good/",
                type: 'POST',
                data: form_data,
                dataType: 'json',
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    if (data.status == 1) {
                        var timer = setInterval(function () {
                            clearInterval(timer);
                            DTS.admin_good.load_good_data(page);
                        }, 2000);
                        $('#add_good_modal').modal('hide');
                    }
                    DTS.enable_btn("#submit_update");
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                    DTS.enable_btn("#submit_update");
                }
            });
        },
        clear_form: function (form_id) {
            $(form_id).find('input').each(function () {
                switch (this.type) {
                    case 'text':
                        this.value = '';
                        break;
                    case 'password':
                        this.value = '';
                    case 'checkbox':
                    case 'radio':
                        this.checked = false;
                        break;
                }
            });
            $(form_id).find("label.error").remove();
            $(form_id).find(".error").removeClass("error");
            $(form_id).find('textarea, select').val('');
        }
    };
}($);