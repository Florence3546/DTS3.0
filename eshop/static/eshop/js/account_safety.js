var DTS = window.DTS || {};
// 发送验证码按钮倒计时
var time = 60;
DTS.account_safety = function ($) {
    //登录密码
    $(document).ready(function () {






        $(".account").on("click", "a", function () {
            var name = "." + $(this).data("name");
            $(name).removeClass("hide").siblings().addClass("hide");
        });
        $(".next").on("click", function () {
            var name = "." + $(this).data("step");
            $(this).closest(".step-box").find(name).addClass("active").addClass("first").siblings().removeClass("active");
            $(this).parent().addClass("hide").next().removeClass("hide");
        });

        $("#set-permission").validate();


        // 获取验证码事件绑定
        $(".gain-code").on('click',function(){
            console.log("发送验证码");
            var $this = $(this);
            var phone = $this.attr("data-phone");
            var url = $('#send_validate_code_url').val();
            console.log(phone);
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'phone': phone,
                },
                cache: false,
                success: function (data) {
                    console.log(data);
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        alert('已发送' + phone);
                        var time_60 = '<a class="time_60">60</a>';
                        $this.replaceWith(time_60);
                        DTS.account_safety.countdown($('.time_60'));
                    }
                },
                error: function () {
                    alert('web端发生错误');
                }
            });
        });

          // 获取新手机号码验证码事件绑定
        $(".phone_code1").on('click',function(){
            console.log("发送验证码");
            var $this = $(this);
            var phone = $('#phone_new').val();
            var url = $('#send_validate_code_new_url').val();
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'phone': phone,
                },
                cache: false,
                success: function (data) {
                    console.log(data);
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        alert('已发送' + phone);
                        var time_60 = '<a class="time_60">60</a>';
                        $this.replaceWith(time_60);
                        DTS.account_safety.countdown($('.time_60'));
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });




        //第一步提交
        $(".step1_submit").on("click", function () {
            var phone_yzm = $('.phone_yzm').val();
            if(phone_yzm == undefined || phone_yzm == ''){
                alert("请输入验证码");
                $("#verify-number").focus();
                return;
            }

            $.ajax({
                url: "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_1',
                    'step': 'verify',
                    'phone': $('#phone').val(),
                    'phone_yzm': phone_yzm
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    }else if(data.status == 1){
                        window.location.href = "/eshop/account_safety/?action=action_1&step=new_password";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        //第二步提交
        $(".step2_submit").on("click", function () {
            var passwd = $('[name="passwd"]').val();
            var passwd2 = $('[name="passwd2"]').val();
            var captcha = $("#captcha").val();
            if (passwd == '' || passwd2 == '') {
                alert('请输入新密码');
                return false;
            }
            if (passwd != passwd2) {
                alert('密码不一致');
                return false;
            }
            if(captcha=='' || captcha==undefined ){
                alert("请输入验证码");
                $("#captcha").focus;
                return;
            }
            $.ajax({
                url: "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_1',
                    'step': 'new_password',
                    'password': $('[name="passwd"]').val(),
                    'password2': $('[name="passwd2"]').val(),
                    'captcha': captcha,
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/account_safety/?action=action_1&step=complete";
                    }
                },
                error: function () {
                    alert('网络异常，请稍后重试!');
                }
            });

        });
        //第三步提交
        $(".step3_submit").on("click", function () {
            var phone_yzm = $('#verify-number2').val();
            console.log(phone_yzm);
            if(phone_yzm == undefined || phone_yzm == ''){
                alert("请输入验证码");
                $("#verify-number2").focus();
                return;
            }

            $.ajax({
                url: "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_2',
                    'step': 'phone',
                    'phone': $('#phone').val(),
                    'phone_yzm': phone_yzm
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    }else if(data.status == 1){
                        window.location.href = "/eshop/account_safety/?action=action_2&step=phone_new";
                    }
                },
                error: function () {
                    alert('网络异常，请稍后重试!');
                }
            });
        });

        //第四步提交
        $(".step4_submit").on("click", function () {
            var phone_new = $('#phone_new').val();
            var phone_code = $('#phone_code').val();
            if ( phone_new == '') {
                alert('请输入新手机号');
                $("#phone_new").focus();
                return;
            }
            if(phone_code==''|| phone_code==undefined ){
                alert("请输入验证码");
                $("#phone_code").focus;
                return;
            }
            $.ajax({
                url:  "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_2',
                    'step': 'phone_new',
                    'phone_new': phone_new,
                    'captcha': phone_code,
                    'phone_code': phone_code,
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/account_safety/?action=action_2&step=complete";
                    }
                },
                error: function () {
                    alert('网络异常，请稍后重试!');
                }
            });

        });

        //第五步提交
        $(".step5_submit").on("click", function () {
            var phone_yzm= $('#phone_yzm').val();
            if (phone_yzm == undefined || phone_yzm == '') {
                alert("请输入验证码");
                $("#phone_yzm").focus();
                return;
            }
            $.ajax({
                url: "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_3',
                    'step': 'verify',
                    'email': $('#email').val(),
                    'captcha': phone_yzm
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    }else if(data.status == 1){
                        window.location.href = "/eshop/account_safety/?action=action_3&step=email";
                    }
                },
                error: function () {
                    alert('网络异常，请稍后重试!');
                }
            });
        });

        //第六步提交
        $(".step6_submit").on("click", function () {
            var email = $('#email').val();
            var email_code = $("#email_code").val();
            if ( email == '') {
                alert('请输入邮箱地址');
                $("#verify-number5").focus();
                return;
            }
            if(email_code=='' ){
                alert("请输入验证码");
                $("#email_code").focus;
                return;
            }
            $.ajax({
                url: "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_3',
                    'step': 'email',
                    'email': email,
                    'captcha': email_code
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/account_safety/?action=action_3&step=complete";
                    }
                },
                error: function () {
                    alert('网络异常，请稍后重试!');
                }
            });

        });

        //第七步保存
        $(".step7_submit").on("click", function () {
            var pay_password = $('#pay_password').val();
            var pay_password2 = $('#pay_password2').val();
            if ( pay_password == '' || pay_password2 == '') {
                alert('请输入支付密码');
                return;
            }
            if (pay_code1 != pay_password2) {
                alert('密码不一致');
                return;
            }
            $.ajax({
                url: "/eshop/account_safety/",
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'action_4',
                    'step': 'pay_password',
                    'pay_password': pay_password2,
                    'pay_password2': pay_password2,
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/account_safety/?action=action_4&step=complete";
                    }
                },
                error: function () {
                    alert('网络异常，请稍后重试!');
                }
            });

        });

        // 刷新验证码
        $('.captcha-rsh, .captcha').on('click', function () {
            DTS.account_safety.set_capcha();
        });
    });

    // 接口定义
    return{
        set_capcha:function(){
            $('.captcha').attr('src', "/common/GenerateCheckCode/?"+Math.random());
        },
       countdown:function(obj) {
			if(time == 0) {
				$(obj).html('获取验证码');
				$(obj).removeClass('time_60');
				$(obj).addClass('send-code');
				time = 60;
			} else {
				$(obj).html(time + '后重新发送');
				time--;
				setTimeout(function() {
					DTS.account_safety.countdown(obj);
				}, 1000)
			}
		}
    }
}($);