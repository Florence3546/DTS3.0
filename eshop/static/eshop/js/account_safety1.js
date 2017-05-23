var DTS = window.DTS || {};
DTS.account_safety = function ($) {
    //登录密码
    $(document).ready(function () {
        //第一步验证手机并发送短信
        $(".account").on("click", "a", function () {
            var phone_yzm = $('.phone_yzm').val();
            if (phone_yzm == undefined || phone_yzm == '') {
                alert("请输入验证码");
                $("#verify-number").focus();
                return;
            }
            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#verify_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=new_password";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
            $(".next").on("click", function () {
                var name = $(this).data("step");
                $(this).closest(".step-box").find(".u1" + name).addClass("active").addClass("first").siblings().removeClass("active");
                $(this).parent().addClass("hide").next().removeClass("hide");
            });

        });


        /*-------------------------倒计时60------------------------*/

        var time = 60;

        function countdown(obj) {
            if (time == 0) {
                $(obj).html('获取验证码');
                $(obj).removeClass('time_60');
                $(obj).addClass('send-code');
                time = 60;
            } else {
                $(obj).html(time + '后重新发送');
                time--;
                setTimeout(function () {
                    countdown(obj);
                }, 1000)
            }
        }

        /*-------------------------验证码手机验证------------------------*/
        $(document).on('click', '.send-code', function () {
            var phone = $(this).parent().siblings().find('[name="phone"]').val();
            if (phone == '') {
                alert('请输入电话号码');
                return false
            }
            var $this = $(this);
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'type': 'message_code',
                    'phone': phone,
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        alert('已发送' + phone);
                        var time_60 = '<a class="time_60">60</a>';
                        $this.replaceWith(time_60);
                        countdown($('.time_60'));
                        $('[name="captcha_0"]').val(data.key);

                    }

                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------验证图形码验证------------------------*/

        $('#id_captcha_1').blur(function () {
            json_data = {
                'response': $('#id_captcha_1').val(),
                'hashkey': $('#id_captcha_0').val()
            };
            $.getJSON('/eshop/ajax_captcha_val', json_data, function (data) {
                if (data['status']) {
                    $('.captcha_text').css('border', '1px solid green');

                } else {
                    $('.captcha_text').css('border', '1px solid red');
                }
            });

        });


        $('.captcha').css({
            'cursor': 'pointer'
        });

        $('.captcha').click(function () {
            console.log('click');
            $.getJSON("/captcha/refresh/",
                function (result) {
                    $('.captcha').attr('src', result['image_url']);
                    $('#id_captcha_0').val(result['key'])
                });
        });

        // 手机验证
        // 第一步提交
        $(".step1").on("click", function () {
            var phone_username = $("#phone_username").val();
            if (phone_username == undefined || phone_username == '') {
                alert("请输入用户名或者手机号");
                $("#phone_username").focus;
                return;
            }
            var captcha_num = $("#captcha-num").val();
            if (captcha_num == undefined || captcha_num == '') {
                alert("请输入验证码");
                $("#captcha_num").focus;
                return;
            }
            $.ajax({
                url: "/eshop/forget_password/",
                type: 'POST',
                data: $("#account_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 2) {
                        alert(data.msg);
                        DTS.forget_password.set_capcha();
                    } else {
                        // 进入下一步
                        // $(".step .second").addClass("active").siblings().removeClass("active");
                        // $(".verify").removeClass("hide").siblings().addClass("hide");
                        window.location.href = "/eshop/forget_password/?step=verify";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // 第三步

        /*-------------------------倒计时60------------------------*/

        var time = 60;

        function countdown(obj) {
            if (time == 0) {
                $(obj).html('获取验证码');
                $(obj).removeClass('time_60');
                $(obj).prop('id', 'send_sms');
                $(obj).addClass('send-code');
                time = 60;
            } else {
                $(obj).html(time + '后重新发送');
                time--;
                setTimeout(function () {
                    countdown(obj);
                }, 1000)
            }
        }

        // 发送短信验证码
        /*-------------------------验证码手机验证------------------------*/
        $(document).on('click', '.send_phone', function () {
            var $this = $(this);
            var phone = $this.data('phone');
            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'step': 'sms_code',
                    'phone': phone
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        alert('已发送' + phone);
                        var time_60 = '<a class="time_60" style="display: inline;">60</a>';
                        $this.replaceWith(time_60);
                        countdown($('.time_60'));
                        $('#id_captcha_0').val(data.key);

                    }


                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });


        $(".step2").on("click", function () {
            var phone_yzm = $('.phone_yzm').val();
            if (phone_yzm == undefined || phone_yzm == '') {
                alert("请输入验证码");
                $("#verify-number").focus();
                return;
            }

            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#verify_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=new_password";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });


            // $(".step .third").addClass("active").siblings().removeClass("active");
            // $(".step .second").addClass("pass");
            // $(".new_password").removeClass("hide").siblings().addClass("hide");
        });

        $(".step3").on("click", function () {
            var passwd = $('[name="passwd"]').val();
            var passwd2 = $('[name="passwd2"]').val();
            if (passwd == '' || passwd2 == '') {
                alert('请输入新密码');
                return false;
            }
            if (passwd != passwd2) {
                alert('密码不一致');
                return false;
            }

            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#new_password_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=complate";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });


        $('.captcha-rsh, .captcha').on('click', function () {
            DTS.forget_password.set_capcha();
        });


        // 邮箱验证
        // 第一步提交
        $(".step1").on("click", function () {
            var phone_username = $("#phone_username").val();
            if (phone_username == undefined || phone_username == '') {
                alert("请输入用户名或者手机号");
                $("#phone_username").focus;
                return;
            }
            var captcha_num = $("#captcha-num").val();
            if (captcha_num == undefined || captcha_num == '') {
                alert("请输入验证码");
                $("#captcha_num").focus;
                return;
            }
            $.ajax({
                url: "/eshop/forget_password/",
                type: 'POST',
                data: $("#account_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 2) {
                        alert(data.msg);
                        DTS.forget_password.set_capcha();
                    } else {
                        // 进入下一步
                        // $(".step .second").addClass("active").siblings().removeClass("active");
                        // $(".verify").removeClass("hide").siblings().addClass("hide");
                        window.location.href = "/eshop/forget_password/?step=verify";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // 第三步

        /*-------------------------倒计时60------------------------*/

        var time = 60;

        function countdown(obj) {
            if (time == 0) {
                $(obj).html('获取验证码');
                $(obj).removeClass('time_60');
                $(obj).prop('id', 'send_sms');
                $(obj).addClass('send-code');
                time = 60;
            } else {
                $(obj).html(time + '后重新发送');
                time--;
                setTimeout(function () {
                    countdown(obj);
                }, 1000)
            }
        }

        // 发送短信验证码
        /*-------------------------验证码手机验证------------------------*/
        $(document).on('click', '.send_phone', function () {
            var $this = $(this);
            var phone = $this.data('phone');
            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'step': 'sms_code',
                    'phone': phone
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        alert('已发送' + phone);
                        var time_60 = '<a class="time_60" style="display: inline;">60</a>';
                        $this.replaceWith(time_60);
                        countdown($('.time_60'));
                        $('#id_captcha_0').val(data.key);

                    }


                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        $(".step2").on("click", function () {
            var phone_yzm = $('.phone_yzm').val();
            if (phone_yzm == undefined || phone_yzm == '') {
                alert("请输入验证码");
                $("#verify-number").focus();
                return;
            }

            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#verify_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=new_password";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });


            // $(".step .third").addClass("active").siblings().removeClass("active");
            // $(".step .second").addClass("pass");
            // $(".new_password").removeClass("hide").siblings().addClass("hide");
        });

        $(".step3").on("click", function () {
            var passwd = $('[name="passwd"]').val();
            var passwd2 = $('[name="passwd2"]').val();
            if (passwd == '' || passwd2 == '') {
                alert('请输入新密码');
                return false;
            }
            if (passwd != passwd2) {
                alert('密码不一致');
                return false;
            }

            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#new_password_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=complate";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });

        });


        $('.captcha-rsh, .captcha').on('click', function () {
            DTS.forget_password.set_capcha();
        });

        // 支付密码
        // 第一步提交
        $(".step1").on("click", function () {
            var phone_username = $("#phone_username").val();
            if (phone_username == undefined || phone_username == '') {
                alert("请输入用户名或者手机号");
                $("#phone_username").focus;
                return;
            }
            var captcha_num = $("#captcha-num").val();
            if (captcha_num == undefined || captcha_num == '') {
                alert("请输入验证码");
                $("#captcha_num").focus;
                return;
            }
            $.ajax({
                url: "/eshop/forget_password/",
                type: 'POST',
                data: $("#account_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 2) {
                        alert(data.msg);
                        DTS.forget_password.set_capcha();
                    } else {
                        // 进入下一步
                        // $(".step .second").addClass("active").siblings().removeClass("active");
                        // $(".verify").removeClass("hide").siblings().addClass("hide");
                        window.location.href = "/eshop/forget_password/?step=verify";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // 第三步

        /*-------------------------倒计时60------------------------*/

        var time = 60;

        function countdown(obj) {
            if (time == 0) {
                $(obj).html('获取验证码');
                $(obj).removeClass('time_60');
                $(obj).prop('id', 'send_sms');
                $(obj).addClass('send-code');
                time = 60;
            } else {
                $(obj).html(time + '后重新发送');
                time--;
                setTimeout(function () {
                    countdown(obj);
                }, 1000)
            }
        }

        // 发送短信验证码
        /*-------------------------验证码手机验证------------------------*/
        $(document).on('click', '.send_phone', function () {
            var $this = $(this);
            var phone = $this.data('phone');
            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'step': 'sms_code',
                    'phone': phone
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        alert('已发送' + phone);
                        var time_60 = '<a class="time_60" style="display: inline;">60</a>';
                        $this.replaceWith(time_60);
                        countdown($('.time_60'));
                        $('#id_captcha_0').val(data.key);

                    }


                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });


        $(".step2").on("click", function () {
            var phone_yzm = $('.phone_yzm').val();
            if (phone_yzm == undefined || phone_yzm == '') {
                alert("请输入验证码");
                $("#verify-number").focus();
                return;
            }

            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#verify_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=new_password";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });


            // $(".step .third").addClass("active").siblings().removeClass("active");
            // $(".step .second").addClass("pass");
            // $(".new_password").removeClass("hide").siblings().addClass("hide");
        });

        $(".step3").on("click", function () {
            var passwd = $('[name="passwd"]').val();
            var passwd2 = $('[name="passwd2"]').val();
            if (passwd == '' || passwd2 == '') {
                alert('请输入新密码');
                return false;
            }
            if (passwd != passwd2) {
                alert('密码不一致');
                return false;
            }

            $.ajax({
                url: $('#url').val(),
                type: 'POST',
                data: $("#new_password_form").serialize(),
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else if (data.status == 1) {
                        window.location.href = "/eshop/forget_password/?step=complate";
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });

        });

        $('.captcha-rsh, .captcha').on('click', function () {
            DTS.forget_password.set_capcha();
        });

    });

    return {
        set_capcha: function () {
            $('.captcha').attr('src', "/common/GenerateCheckCode/?" + Math.random());
        }
    }

}($);