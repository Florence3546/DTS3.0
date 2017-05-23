var DTS = window.DTS || {};
DTS.user_login = function ($) {
    $(document).ready(function () {
        /*-------------------------登录切换------------------------*/

        $(".login-tab a").on("click", function () {
            $(this).addClass("active").siblings().removeClass("active");
            if ($(this).hasClass("login-tab-l")) {
                $(".password").show();
                $(".img-code").show();
                $(".send-code").hide();

                $('#phone_login').hide();
                $('#user_login').show();
            } else {
                $(".password").hide();
                $(".img-code").hide();
                $(".send-code").show();

                $('#user_login').hide();
                $('#phone_login').show();
            }
        });

        /*-------------------------登录------------------------*/

        $(document).on('click', '.login_submit', function () {
            $('.error').css('visibility', 'hidden');
            var data = '';
            // 账户登陆
            if($('.login-tab-l').hasClass('active')){
                data = $('#user_login').serialize();
                if ($('[name="name"]').val() == '') {
                    $('.error').css('visibility', 'visible');
                    $('#err_msg').text('请输入用户名');
                    return false;
                }
                if ($('[name="passwd"]').val() == '') {
                    $('.error').css('visibility', 'visible');
                    $('#err_msg').text('请输入密码');
                    return false;
                }
                if ($('[name="captcha_1"]').val() == '') {
                    $('.error').css('visibility', 'visible');
                    $('#err_msg').text('请输入验证码');
                    return false;
                }


            // 电话登陆
            }else if($('.login-tab-r').hasClass('active')){
                data = $('#phone_login').serialize();
                if($('#phone').val() == ''){
                    $('.error').css('visibility', 'visible');
                    $('#err_msg').text('请填写电话号码');
                    return false;
                }
                if ($('[name="captcha"]').val() == '') {
                    $('.error').css('visibility', 'visible');
                    $('#err_msg').text('请输入验证码');
                    return false;
                }
            }
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: data,
                dataType: 'json',
                cache: false,
                success: function (data, status, xhr) {
                    if (data.status == 0) {
                        $('.error').css('visibility', 'visible');
                        $('#err_msg').text(data.msg);
                    } else {
                        //alert(data.msg);
                        if(data.url){
	                        window.location.href = data.url;
                        }
                    }
                },
                error: function (data, status, error) {
                    if (data.status == '403') {
                        window.location.reload();
                    }
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

        /*-------------------------验证码手机验证------------------------*/
        $(document).on('click', '#send_sms', function () {
            var phone = $('#phone').val();
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
                    'method': 'sms_code',
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
                    alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------短信码验证------------------------*/
        // $('#send_sms').click(function () {
        //     console.log('send_sms');
        //     // TODO by liuhuan 2017-3-24 后期放到captcha-sms库中
        //     num = $('#phone').val();
        //     // num = 18707123609
        //     console.log(num);
        //     $.getJSON("/captcha/sms/" + num,
        //         function (result) {
        //         console.log(result);
        //         alert(num + "发送成功");
        //             $('.captcha').attr('src', result['image_url']);
        //             $('#id_captcha_0').val(result['key'])
        //         });
        //
        // });
    });


}($);





