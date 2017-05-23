DTS = window.DTS || {};
// 页面加载事件
DTS.init = function ($) {
    $(document).ready(function () {
        // 回车确定
        $(document).on('keydown', function (e) {
            var target = e.srcElement ? e.srcElement : e.target;
            if (e.keyCode == 13 && target.tagName != 'TEXTAREA') {
                $(target).closest(document).find('.enter_click:visible:eq(0)').click();
            }
        });

        /*-------------------------更多查询条件------------------------*/
        $(".more_query_conditions").on('click', function () {
            if ($(".query_conditions").hasClass("hide")) {
                $(".query_conditions").removeClass("hide");
                $(this).find("i").removeClass("icon-shangxiajiantou-copy").addClass("icon-shangxiajiantou");
            } else {
                $(".query_conditions").addClass("hide");
                $(this).find("i").removeClass("icon-shangxiajiantou").addClass("icon-shangxiajiantou-copy");
            }
        });

        // 日历
        $('.form-control.date').datetimepicker({
            language: 'zh-CN',
            weekStart: 1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 2,
            minView: 2,
            forceParse: 0,
            todayBtn: 1,
            clearBtn: 1
        });
        /*-------------------------下拉菜单自适应------------------------*/
        $("table").on("click", ".dropdown-toggle", function () {
            var h = -$(this).next().height() - 15;
            if (window.innerHeight - $(this).offset().top > 200) {
                $(this).next().css({"top": "100%"});
            } else {
                $(this).next().css({"top": h + "px"});
            }
        });
        
        /*----------------------------后台头部个人资料修改----------------------------*/
        $(document).on('click', '#personage_info', function () {
		        $('#personage_info_modal').modal({backdrop: 'static', keyboard: false});
		    });
		    //-----------------性别-------------------
		    $(".personage_sex").change(function () {
            var gender = $(".personage_sex:checked").val();
            $('#personage_gender').val(gender);
        });
        //------------------个人资料保存-------------------
        $(document).on('click', '#personage_info_save', function () {
		        $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#personage_info_form').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    if (data.status == 1) {
                        $('#personage_info_modal').modal('hide');
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
		    });
		    /***************密码验证6~20字母、数字、下划线****************/
		    function isPasswd(s) { 
						var patrn=/^(\w){6,20}$/; 
						if (!patrn.exec(s)) return false
						return true
				} 
		    //-----------------个人密码修改-------------------
		    $(document).on('click', '#personage_password', function () {
		    		$("#personage_password_form .old_password").val('');
		    		$("#personage_password_form .new_password").val('');
		    		$("#personage_password_form .confirm_password").val('');
		        $('#personage_password_modal').modal({backdrop: 'static', keyboard: false});
		    });
		    //-----------------保存密码修改-------------------
        $(document).on('click', '#personage_password_save', function () {
        		var old_password=$("#personage_password_form .old_password").val();
        		var new_password=$("#personage_password_form .new_password").val();
        		var confirm_password=$("#personage_password_form .confirm_password").val();
        		var flag=isPasswd(new_password)
        		if(!old_password){
        			DTS.affirm("密码不能为空！");
        			return;
        		}
        		if(flag){
        			if(confirm_password===new_password){
        				$.ajax({
		                url: $(this).attr('api'),
		                type: 'POST',
		                data: $('#personage_password_form').serialize(),
		                dataType: 'json',
		                cache: false,
		                success: function (data) {
		                    DTS.affirm(data.msg);
		                    if (data.status == 1) {
		                        $('#personage_password_modal').modal('hide');
		                        window.location.href="/eshop/user_login";
		                    }
		                },
		                error: function () {
		                    DTS.affirm(DTS.tips_error);
		                }
		            });
        			}else{
        				DTS.affirm("两次密码输入不相同，请重新输入！");
        			}
        		}else{
        			DTS.affirm("您输入的密码格式不正确，请重新输入！");
        		}
		    });
        //---------------------退出登录-----------
        $(document).on("click","#log_out",function(){
        	DTS.confirm("确定退出后台系统吗？",function(){
        		window.location.href="/eshop/user_logout";
        	})
        })
        
        /*----------------------------头部我的订单----------------------------*/
        $.ajax({
            url: $('#id_order_count').data('url'),
            type: 'GET',
            cache: false,
            success: function (data) {
                if (data.status == 1) {
                    $('#id_order_count .not_paid').html(data.data.not_paid || '');
                    $('#id_order_count .is_picking').html(data.data.is_picking || '');
                    $('#id_order_count .is_shipping').html(data.data.is_shipping || '');
                } else {
                    console.log('get_order_state fail, 获取订单统计失败');
                }
            }, error: function () {
                console.log('error');
            }
        });
        /*----------------------------头部我的消息----------------------------*/
        $.ajax({
            url: $('#unread_count').data('url'),
            type: 'GET',
            cache: false,
            success: function (data) {
                if (data.status == 1) {
                    $('#unread_count').html(data.unread_num || '');
                } else {
                    console.log('get_order_state fail, 获取我的消息失败');
                }
            }, error: function () {
                console.log('error');
            }
        });
        /*----------------------------头部我的消息----------------------------*/
        $.ajax({
            url: $('.shopping_cart_count').data('url'),
            type: 'GET',
            cache: false,
            success: function (data) {
                if (data.status == 1) {
                    $('.shopping_cart_count').html(data.cart_count || '');
                } else {
                    console.log('get_order_state fail, 获取购物车数量失败');
                }
            }, error: function () {
                console.log('error');
            }
        });
    });
}($);

// 开关
DTS.switch = function (switch_btn) {
    $(document).on('click', '.switch-default', function () {
        var switch_btn = switch_btn.children().eq(0);
        if (switch_btn.hasClass("hide")) {
            switch_btn.removeClass("hide");
            switch_btn.siblings().addClass("hide");
        } else {
            switch_btn.addClass("hide");
            switch_btn.siblings().removeClass("hide");
        }
    });
};

DTS.clear_form = function (form_id) {
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
};

DTS.alert = function (content, fn, title) {
    title = title || '提醒';
    $("#alert_title").html(title);
    $("#alert_content").html(content);
    $('#alert').modal({backdrop: 'static', keyboard: false});
    $("#alert_affirm").on("click", function () {
        $('#alert').modal('hide');
        if (fn != undefined) {
            fn();
        }
    })
};

DTS.confirm = function (content, fn, title) {
    title = title || '提醒';
    $("#confirm_title").html(title);
    $("#confirm_content").html(content);
    $('#confirm').modal({backdrop: 'static', keyboard: false});
    $("#confirm_enter_btn").off('click').on('click', function () {
        $('#confirm').modal('hide');
        if (fn != undefined) {
            fn();
        }
    });
};

// 轻提示框
DTS.affirm = function (content, flag) {
    $("#content_box").html(content);
    var timer, timer_location;
    $("#affirm_box").fadeIn(1000);
    timer = setInterval(function () {
        clearInterval(timer);
        $("#affirm_box").fadeOut(1000);
    }, 2000);
    timer_location = setInterval(function () {
        clearInterval(timer_location);
        if (flag) {
            window.location.reload();
        }
    }, 3000);
    // $("#affirm_box").on('mouseover', function () {
    //     clearInterval(timer);
    // });
    // $("#affirm_box").on('mouseout', function () {
    //     timer = setInterval(function () {
    //         clearInterval(timer);
    //         $("#affirm_box").fadeOut(1000);
    //     }, 1000)
    // });
    // $("#affirm_close").on('click', function () {
    //     clearInterval(timer);
    //     $("#affirm_box").fadeOut(1);
    // });
};

DTS.lack_register = function ($btn) {
    // DTS.lack_register($(".lack_register"));
    $btn.off('click');
    $btn.on('click', function () {
        $("#modal_lack_register").modal({backdrop: 'static', keyboard: false});
        $('#submit_payment_add').attr('good_id', $(this).data('pk'));
    });
    $("#submit_payment_add").off('click');
    $("#submit_payment_add").on('click', function () {
        $.ajax({
            url: $(this).attr('api'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                'good_id': $(this).attr('good_id'),
                'note': $('#lack_note').val()
            },
            dataType: 'json',
            cache: false,
            success: function (data) {
                DTS.affirm(data.msg, data.status == 1);
                $('#modal_lack_register').modal('hide');
            },
            error: function () {
                DTS.affirm(DTS.tips_error);
                // DTS.alert('web端发生错误');
            }
        });
    });
};

//简单全选功能
DTS.Check = function (all, item) {
    // 参数 all 全选框， item 每个独立选项框
    // DTS.Check(".quick-order-tab .check-all", ".quick-order-tab .check-item");
    $(all).on('click', function () {
        if ($(this).is(":checked")) {
            $(item).prop('checked', true);
        } else {
            $(item).prop('checked', false);
        }
    });
    $(item).on('click', function () {
        var $checks = $(item);
        if ($checks.filter(":checked").length == $checks.length) {
            $(all).prop('checked', true);
        } else {
            $(all).prop('checked', false);
        }
    });
};

// dataTable组件配置
DTS.data_table = function (data) {
    // 调用说明 DTS.data_table('#good_tab', 4, [0, 3, 11]);
    // 参数说明 data 表格名; column 初始化时默认排序的那一列; arr 格式数组，不需要排序的列下标
    $(data).DataTable({
        "bPaginate": false, //翻页功能
        "bLengthChange": false, //改变每页显示数据数量
        "bFilter": false, //过滤功能
        "bSort": false, //排序功能
        "bInfo": false, //页脚信息
        "bAutoWidth": false, //自动宽度
        "bStateSave": false,//数据缓存
        fixedHeader: true, //表头固定
        "oLanguage": {
            "sZeroRecords": "<img src='../../static/dtsadmin/img/no_data.png'>" //表格无数据显示的图片
        }
    });
};

/**
 * @description 分页跳转条件绑定
 * @param callback : 点击页码和上一页，下一页后回调处理
 **/
DTS.bind_page = function (callback) {
    // 绑定分页点击事件
    $(".pagination li a").on('click', function () {
        var num = $(this).attr('page');
        if (num == undefined || num == '') {
            //如果页面获取有问题，就默认加载第一页
            num = 1;
        }
        // 执行回调，进行分页加载
        callback(num);
    });
    // 绑定跳转到第几页事件
    $(".page-No .page_go").on('click', function () {
        // 输入的跳转页
        var num = $(".page_no").val();
        if (num == undefined || num == '') {
            num = 1;//如果页面获取有问题，就默认加载第一页
        }
        // 获取总页数
        var total_page = $(".page_total").text();
        if (total_page != undefined && total_page != '') {
            if (Number(num) > Number(total_page)) {
                //DTS.alert('您输入的页码过大，请输入小于等于'+total_page+'的值','提示');
                // return;
                num = total_page;
            }
        }
        // 执行回调，进行分页加载
        callback(num);
    });
};

/**
 * @description 显示loading窗
 * @param content 提示内容
 * @param showDg bool 显示或者隐藏
 * Use API:
 *      DTS.loading_dialog(true,...); 打开弹窗
 *      DTS.loading_dialog(false); 关闭弹窗
 */
DTS.loading_dialog = function (showDg, content) {
    if (typeof(showDg) != 'boolean') {
        throw new Error("showDg typeError.");
        return;
    }
    if (!showDg) {
        $('#loading').modal('hide');
        return;
    }
    content = content || '数据加载中,请稍后……';
    $("#loading_text").html(content);
    $('#loading').modal({backdrop: 'static', keyboard: false, show: showDg});
};

/**
 * @description 提示信息统计
 */
DTS.tips_error = '网络异常，请稍后刷新重试！';

/**
 * @description 禁用按钮
 * @param obj 按钮ID eg: DTS.disable_btn("#按钮ID");
 */
DTS.disable_btn = function (obj) {
    $(obj).attr('disabled', 'disabled');
    $(obj).addClass('disabled');
};
/**
 * @description 取消禁用按钮
 * @param obj
 */
DTS.enable_btn = function (obj) {
    $(obj).removeAttr('disabled');
    $(obj).removeClass('disabled');
};

/**
 * @description 订单列表、改价审批模态框的单种商品总价
 */
DTS.single_real_price = function () {
    $(".real_price").each(function () {
        obj = $(this).closest('tr');
        discount = obj.find('.discount').text() || obj.find('.discount').val()
        var total = (obj.find(".price").text() - discount) * obj.find('.quantity').text();
        $(this).text(total.toFixed(2));
    });
};

// 阻止冒泡事件
DTS.stop_bubble = function stopBubble(e) {
    //如果提供了事件对象，则这是一个非IE浏览器
    if (e && e.stopPropagation)
    //因此它支持W3C的stopPropagation()方法
        e.stopPropagation();
    else
    //否则，我们需要使用IE的方式来取消事件冒泡
        window.event.cancelBubble = true;
};

//阻止浏览器的默认行为
DTS.prevent_default = function preventDefault(e) {
    //阻止默认浏览器动作(W3C)
    if (e && e.preventDefault)
        e.preventDefault();
    //IE中阻止函数器默认动作的方式
    else
        window.event.returnValue = false;
    return false;
};
