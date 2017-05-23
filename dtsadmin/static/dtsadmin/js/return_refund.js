var DTS = window.DTS || {};
DTS.return_refund = function ($) {
    $(document).ready(function () {
        //分页初始化
        if ($("#total_count").val() > 0) {
            // 表格排序
            DTS.data_table('#table_refund_return');
            // 分页绑定
            DTS.bind_page(DTS.return_refund.load_ret_ref_data);
            // 表格多选
            DTS.Check('.check-all', '.check-item');
        }
        // 更多查询条件显示与否控制
        var form_val = $('#order_no').val() ||
            $("#refund_type").val() ||
            $("#refund_status").val() ||
            $("#end_date").val() ||
            $("#start_date").val();
        if (form_val) {
            $(".query_conditions").removeClass("hide");
        }
        // 点击查询
        $("#ret_ref_search").on('click', function () {
            DTS.return_refund.load_ret_ref_data(1);
        });
        // 订单编号查看模态框
				$('#content').on('click', '.look_order', function() {
					$.ajax({
						url: $(this).attr('api'),
						type: 'POST',
						data: {
							'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
						},
						cache: false,
						success: function(data, status, xhr) {
							if(xhr.getResponseHeader('Content-Type') == 'application/json') {
								DTS.affirm(data.msg);
							} else {
								$('#approve_order_modal').replaceWith(data);
								$('.verify_order').hide();
								$('#approve_order_modal').modal({
									backdrop: 'static',
									keyboard: false
								});
								DTS.single_real_price();
								$("#approve_order_modal .modal-footer").hide();
								$('.modal-title').text('查看订单');
							}
						},
						error: function() {
							DTS.affirm('网络异常，请刷新重试');
						}
					});
				});
        // 打开退款退货审核
        $(".ref-verify").on('click', function () {
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
                        $("#verify-btn").removeClass('hide');
                        $("#finish-btn").addClass('hide');
                        $("#finish-return").addClass('hide');
                        $('#returns_refunds_modal').replaceWith(data);
                        $('#returns_refunds_modal').modal({backdrop: 'static', keyboard: false, show: true});
                        DTS.single_real_price();
                        $("#returns_refunds_modal .modal-title").text('审核');
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 通过审核
        $(document).on('click', '#ret_ref_ok', function () {
            var obj_id = $("#obj_id").val();
            $.ajax({
                url: '/dtsadmin/returns_and_refunds/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'op_type': 'pas',
                    'obj_id': obj_id
                },
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    if (data.status == 1) {
                        $('#returns_refunds_modal').modal('hide');
                        var cur_page = $("#page").val();
                        var timer = setInterval(function () {
                            clearInterval(timer);
                            DTS.return_refund.load_ret_ref_data(cur_page);
                        }, 2000);
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 不通过审核
        $(document).on('click', '#ret_ref_refuse', function () {
            var obj_id = $("#obj_id").val();
            DTS.return_refund.submit_refund('/dtsadmin/returns_and_refunds/', 'ref', obj_id);
        });
        // 查看
        $(".ref-look").on('click', function () {
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
                        $('#returns_refunds_modal').replaceWith(data);
                        $("#returns_refunds_modal .modal-footer").hide();
                        $('#returns_refunds_modal').modal({backdrop: 'static', keyboard: false, show: true});
                        DTS.single_real_price();
                        $("#returns_refunds_modal .modal-title").text('查看');

                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 确认收货弹窗打开
        $(".ref-rec").on('click', function () {
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
                        $('#returns_refunds_modal').replaceWith(data);
                        $("#verify-btn").addClass('hide');
                        $("#finish-btn").removeClass('hide');
                        $("#finish-return").addClass('hide');
                        $('#returns_refunds_modal').modal({backdrop: 'static', keyboard: false, show: true});
                        DTS.single_real_price();
                        $("#returns_refunds_modal .modal-title").text('确认收货');
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 提交确认收货
        $(document).on('click', "#ret_ref_receipt", function () {
            var obj_id = $("#obj_id").val();
            var url = $(this).attr('api');
            DTS.return_refund.submit_refund(url, 'rec', obj_id);
        });
        // 拒绝收货
        $(document).on('click', '#ref_refuse_gd', function () {
            var obj_id = $("#obj_id").val();
            DTS.return_refund.submit_refund('/dtsadmin/returns_and_refunds/', 'ref', obj_id);
        });
        // 确认退款弹窗打开
        $(".ref-fsh").on('click', function () {
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
                        $('#returns_refunds_modal').replaceWith(data);
                        $("#verify-btn").addClass('hide');
                        $("#finish-btn").addClass('hide');
                        $("#finish-return").removeClass('hide');
                        $('#returns_refunds_modal').modal({backdrop: 'static', keyboard: false, show: true});
                        DTS.single_real_price();
                        $("#returns_refunds_modal .modal-title").text('确认退款');
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });
        // 提交确认退款
        $(document).on('click', "#ret_ref_money", function () {
            var obj_id = $("#obj_id").val();
            var url = $(this).attr('api');
            DTS.return_refund.submit_refund(url, 'fsh', obj_id);
        });
        // 拒绝退款
        $(document).on('click', '#ref_ref_money', function () {
            var obj_id = $("#obj_id").val();
            DTS.return_refund.submit_refund('/dtsadmin/returns_and_refunds/', 'ref', obj_id);
        });
    });
    return {
        load_ret_ref_data: function (page) {
            // 查询加载数据
            $("#page").val(page);
            $("#input_ref_id").val($.trim($("#input_ref_id").val()));
            $("#order_id").val($.trim($("#order_id").val()));
            $("#ret_ref_form").submit();
        },
        //初始化模态框
        init_datetime_picker: function () {
            //开始时间
            $("#start_date").datetimepicker({
                format: 'yyyy-mm-dd',
                minView: 2,
                autoclose: true,
                todayBtn: true,
            }).on('changeDate', function () {
                var start_date = $("#start_date").val();
                $("#end_date").datetimepicker('setStartDate', start_date);
                $("#start_date").datetimepicker("hide");
            });
            //结束时间
            $("#end_date").datetimepicker({
                format: "yyyy-mm-dd",
                minView: 2,
                autoclose: true,
                todayBtn: true,
                minuteStep: 1
            }).on('changeDate', function () {
                var start_date = $("#start_date").val();
                var end_date = $("#end_date").val();
                if (start_date != "" && end_date != "") {
                    if (DTS.return_refund.checkEndTime(start_date, end_date)) {
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
            // var cha = (Date.parse(start_date) - Date.parse(end_date)) / 86400000 * 24;
            if (gap > 0) { //开始时间大于结束时间
                return true;
            }
            return false;
        },
        submit_refund: function (url, op_type, obj_id) {
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'op_type': op_type,
                    'obj_id': obj_id
                },
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    if (data.status == 1) {
                        $('#returns_refunds_modal').modal('hide');
                        var timer = setInterval(function () {
                            clearInterval(timer);
                            DTS.return_refund.load_ret_ref_data(1);
                        }, 2000);
                        $('#returns_refunds_modal').modal('hide');
                        DTS.return_refund.load_ret_ref_data(1);
                    }
                }, error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        }
    }
}($);
