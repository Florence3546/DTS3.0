var DTS = window.DTS || {};
DTS.admin_area = function ($) {
    $(document).ready(function () {
        // // 行政区展开与收缩
        // $(".triangle").on("click", function () {
        //     if ($(this).closest(".role").children(".role").css("display") == "none") {
        //         $(this).closest(".role").children(".role").css({"display": "block"});
        //         $(this).addClass("triangle-bootom");
        //     } else {
        //         $(this).closest(".role").find(".role").css({"display": "none"});
        //         $(this).closest(".role").find(".triangle").removeClass("triangle-bootom");
        //     }
        // });

        // // 添加行政地区
        // $('#content').on('click', '.add_regional', function () {
        //     DTS.clear_form('#form_regional');
        //     $('#modal_regional').modal({backdrop: 'static', keyboard: false});
        //     $('.modal-title').text('添加行政地区');
        //     $('#submit_regional_add').show();
        //     $('#submit_regional_update').hide();
        //
        //     $('#regional_parent_id').val($(this).attr('data-id'));
        //
        //     // if( $(this).attr('data-id') == '' ){
        //     //   $('#regional_parent_id').val(0);
        //     // }else {
        //     //     $('#regional_parent_id').val($(this).attr('data-id'));
        //     //     $('#regional_parent_id').prop('disabled', true);
        //     // }
        // });
        //
        // $('#submit_regional_add').on('click', function () {
        //     $.ajax({
        //         url: $(this).attr('api'),
        //         type: 'POST',
        //         data: $('#form_regional').serialize(),
        //         dataType: 'json',
        //         cache: false,
        //         success: function (data) {
        //             alert(data.msg);
        //             $('#modal_regional').modal('hide');
        //             window.location.reload();
        //         },
        //         error: function () {
        //             alert('发生错误');
        //         }
        //     });
        // });
        //
        //
        // // 修改行政地区模态框
        // $('#content').on('click', '.update_regional', function () {
        //     $.ajax({
        //         url: $(this).attr('api'),
        //         type: 'POST',
        //         data: {
        //             'csrfmiddlewaretoken': $('#form_regional [name=csrfmiddlewaretoken]').val()
        //         },
        //         cache: false,
        //         success: function (data) {
        //             if (data.status == 0) {
        //                 alert(data.msg);
        //             } else {
        //                 $('#modal_regional').replaceWith(data);
        //                 $('#modal_regional').modal({backdrop: 'static', keyboard: false});
        //                 $('.modal-title').text('修改行政地区');
        //                 $('#submit_regional_add').hide();
        //                 $('#submit_regional_update').show();
        //             }
        //
        //         },
        //         error: function () {
        //             alert('网络异常，请刷新重试');
        //         }
        //     });
        // });
        //
        // // 模态框提交
        // $(document).on('click', '#submit_regional_update', function () {
        //     $.ajax({
        //         url: $(this).attr('api'),
        //         type: 'POST',
        //         data: $('#form_regional').serialize(),
        //         dataType: 'json',
        //         cache: false,
        //         success: function (data) {
        //             alert(data.msg);
        //             $('#modal_regional').modal('hide');
        //             window.location.reload();
        //         },
        //         error: function () {
        //             alert('发生错误');
        //         }
        //     });
        // });

        // // 删除地区
        // $('#content').on('click', '.delete_regional', function () {
        //     $.ajax({
        //         url: $(this).attr('api'),
        //         type: 'POST',
        //         data: {
        //             'csrfmiddlewaretoken': $('#form_regional [name=csrfmiddlewaretoken]').val()
        //         },
        //         dataType: 'json',
        //         cache: false,
        //         success: function (data) {
        //             alert(data.msg);
        //             window.location.reload();
        //         },
        //         error: function () {
        //             alert('网络异常，请刷新重试');
        //         }
        //     });
        // });

        // // 展开下级区域
        // $('#content').on('click', '.stretch', function () {
        //     $.ajax({
        //         url: $(this).attr('api'),
        //         type: 'POST',
        //         data: {
        //             'csrfmiddlewaretoken': $('#form_regional [name=csrfmiddlewaretoken]').val()
        //         },
        //         dataType: 'json',
        //         cache: false,
        //         success: function (data) {
        //             alert(data.msg);
        //             window.location.reload();
        //         },
        //         error: function () {
        //             alert('网络异常，请刷新重试');
        //         }
        //     });
        // });

        /*-------------------------展示------------------------*/

        $('#table_fold').on('click', 'a.triangle', function () {
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

        /*-------------------------启用禁用------------------------*/

        $('#table_fold').on('click', '.active', function () {
            var $this = $(this);
            var tr_obj = $this.closest('tr');
            var is_active = $this.attr('is_active') === 'True' ? 'False' : 'True';
            var api = $(this).attr('api');
            var html;
            if (is_active === 'False') {
                html = "禁用后新增地址无法显示，确定要禁用吗？"
            } else {
                html = "开启后新增地址将会显示！"
            }
            DTS.confirm(html, function () {
                $.ajax({
                    url: api,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'is_active': is_active
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                        $this.attr('is_active', is_active);
                        if (is_active === 'True') {
                            tr_obj.removeClass('disabled');
                        } else {
                            tr_obj.addClass('disabled');
                        }
                        DTS.switch($(this));
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
                window.location.reload();
            });
        });

        /*-------------------------排序------------------------*/

        $(".save_order").on('click', function () {
            var data = [];
            $('.region_order').each(function () {
                if (!$(this).closest('tr').hasClass('hide')) {
                    var pk = $(this).data('pk');
                    var value = $(this).prop('value');
                    data.push({"pk": pk, "value": value});
                }
            });
            console.log(data);

            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'data': JSON.stringify(data),
                    'order_name': "region_order"
                },
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg, data.status == 1);
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

    })
}($);