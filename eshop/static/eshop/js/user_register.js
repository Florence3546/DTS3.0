var DTS = window.DTS || {};
DTS.user_register = function ($) {
    $(document).ready(function () {
        /*-------------------------注册类型切换------------------------*/

        $(".user").on("click", function () {
            $(this).parent().addClass("active").siblings().removeClass("active");
        });
        $(".step1 .next").on("click", function () {
            $(".step1").hide();
            $(".second").addClass("active").siblings().removeClass("active");
            if ($(".step1 .merchant").hasClass("active")) {
                $(".step2 .merchant").show().siblings().hide();
            } else {
                $(".step2 .merchant").hide().siblings().show();
            }
        });

        $(".step2 .back").on("click", function () {
            $(".first").addClass("active").siblings().removeClass("active");
            $(".step2 .merchant").hide().siblings().hide();
            $(".step1").show();
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
                    'phone': phone
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
                    alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------表单验证公用------------------------*/
        function form_verification(form_id) {
            $('.error').text('');
            // 表单前台验证
            // 用户名
            console.log(form_id + ' [name]');
            if ($(form_id + ' [name="username"]').val() == '') {
                $(form_id + ' [name="username"] + .error').text('请输入用户名');
                return false;

            }
            // 姓名
            if ($(form_id + ' [name="first_name"]').val() == '') {
                $(form_id + ' [name="first_name"] + .error').text('请输入用户姓名');
                return false;
            }
            // 手机号码
            var phone = $('[name="phone"]').val();
            if (!phone.match(/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/)) {
                $('[name="phone"] + .error').text('请输入有效的手机号码！');
                return false;
            }
            // 验证码
            if ($('[name="captcha"]').val() == '') {
                $('[name="captcha"]').siblings('.error').text('请填写验证码！');
                return false;
            }
            // 密码
            if ($('[name="passwd"]').val() == '') {
                $('[name="passwd"]+ .error').text('请输入密码！');
                return false;
            }
            if ($('[name="passwd2"]').val() == '') {
                $('[name="passwd2"]+ .error').text('请输入密码！');
                return false;
            }
            if ($('[name="passwd"]').val() != $('[name="passwd2"]').val()) {
                $('[name="passwd2"]+ .error').text('两次密码不一致！');
                return false;
            }
            // 邮箱
            var email = $('[name="email"]').val();
            if (email == '') {
                $('[name="email"] + .error').text('邮箱不能为空！');
                return false;
            }
            if (!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)) {
                $('[name="email"] + .error').text('格式不正确！');
                return false;
            }

        }

        /*-------------------------个人会员注册确认提交------------------------*/

        $(document).on('click', '#member_submit', function () {

            $('.error').text('');
            // 表单前台验证
            // 用户名
            if ($('[name="username"]').val() == '') {
                $('[name="username"] + .error').text('请输入用户名');
                return false;

            }
            // 姓名
            if ($('[name="first_name"]').val() == '') {
                $('[name="first_name"] + .error').text('请输入用户姓名');
                return false;
            }
            // 手机号码
            var phone = $('[name="phone"]').val();
            if (!phone.match(/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/)) {
                $('[name="phone"] + .error').text('请输入有效的手机号码！');
                return false;
            }
            // 验证码
            if ($('[name="captcha"]').val() == '') {
                $('[name="captcha"]').siblings('.error').text('请填写验证码！');
                return false;
            }
            // 密码
            if ($('[name="passwd"]').val() == '') {
                $('[name="passwd"]+ .error').text('请输入密码！');
                return false;
            }
            if ($('[name="passwd2"]').val() == '') {
                $('[name="passwd2"]+ .error').text('请输入密码！');
                return false;
            }
            if ($('[name="passwd"]').val() != $('[name="passwd2"]').val()) {
                $('[name="passwd2"]+ .error').text('两次密码不一致！');
                return false;
            }
            // 邮箱
            var email = $('[name="email"]').val();
            if (email == '') {
                $('[name="email"] + .error').text('邮箱不能为空！');
                return false;
            }
            if (!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)) {
                $('[name="email"] + .error').text('格式不正确！');
                return false;
            }
            // 隐私声明
            if (!$('#member_agreen').is(':checked')) {
                alert('请接受我们的隐私声明');
                return false;
            }

            // 性别
            if (1) {
                $("[name='member_sex']:checked")[0].value
            }

            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#member_form').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        $('#error_modal').modal('show');
                        $('.modal-title').text('提示');
                        $('.error_msg').html(data.msg);
                    }
                    // 个人注册成功
                    if (data.status == 1) {
                        // window.location.href = '/eshop/user_login/'
                        $(".step2").hide();
                        $(".second").addClass("pass");
                        $(".third").addClass("active").siblings().removeClass("active");
                        $(".step3 .merchant").hide().siblings().show();
                    }
                },
                error: function () {
                    alert(DTS.tips_error);
                }
            });

        });

        /*-------------------------企业会员注册确认提交------------------------*/

        $(document).on('click', '#merchant_submit', function (e) {

            // form_verification('#merchant_form');
            // user_verification();
            $('.error').text('');
            // 表单前台验证
            // 用户名
            if ($('#merchant_form [name="username"]').val() == '') {
                $('#merchant_form [name="username"] + .error').text('请输入用户名');
                return false;

            }
            // 姓名
            if ($('#merchant_form [name="first_name"]').val() == '') {
                $('#merchant_form [name="first_name"] + .error').text('请输入用户姓名');
                return false;
            }
            // 手机号码
            var phone = $('#merchant_form [name="phone"]').val();
            if (!phone.match(/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/)) {
                $('#merchant_form [name="phone"] + .error').text('请输入有效的手机号码！');
                return false;
            }
            // 验证码
            if ($('#merchant_form [name="captcha"]').val() == '') {
                $('#merchant_form [name="captcha"]').siblings('.error').text('请填写验证码！');
                return false;
            }
            // 密码
            if ($('#merchant_form [name="passwd"]').val() == '') {
                $('#merchant_form [name="passwd"]+ .error').text('请输入密码！');
                return false;
            }
            if ($('#merchant_form [name="passwd2"]').val() == '') {
                $('#merchant_form [name="passwd2"]+ .error').text('请输入密码！');
                return false;
            }
            if ($('#merchant_form [name="passwd"]').val() != $('#merchant_form [name="passwd2"]').val()) {
                $('#merchant_form [name="passwd2"]+ .error').text('两次密码不一致！');
                return false;
            }
            // 邮箱
            var email = $('#merchant_form [name="email"]').val();
            if (email == '') {
                $('#merchant_form [name="email"] + .error').text('邮箱不能为空！');
                return false;
            }

            if (!$('#merchant_agreen').is(':checked')) {
                alert('请接受我们的隐私声明');
                return false;

            }

            //企业特有属性

            // 企业名称
            if ($('#merchant_form [name="enterprise_name"]').val() == '') {
                $('#merchant_form [name="enterprise_name"]+ .error').text('请输入企业名称！');
                return false;
            }

            if ($('#merchant_form [name="short_name"]').val() == '') {
                $('#merchant_form [name="short_name"]+ .error').text('请输入企业简称！');
                return false;
            }

            if ($('#merchant_form [name="operate_mode"]').val() == '') {
                $('#merchant_form [name="operate_mode"]').siblings('.error').text('请选择经营方式！');
                return false;
            }

            if ($('#merchant_form .region').val() == '') {
                $('#merchant_form .region').siblings('.error').text('请选择所在地区！');
                return false;
            }

            if ($('#merchant_form [name="address"]').val() == '') {
                $('#merchant_form [name="address"]+ .error').text('请输入详细地址！');
                return false;
            }

            if ($('#merchant_form [name="phone"]').val() == '') {
                $('#merchant_form [name="phone"]+ .error').text('请输入企业电话！');
                return false;
            }

            if ($('#merchant_form [name="legal_repr"]').val() == '') {
                $('#merchant_form [name="legal_repr"]+ .error').text('请输入法人代表！');
                return false;
            }

            var biz_scope_list = handle_biz_scope();
            if (!biz_scope_list) {
                return false;
            }
            $('#biz_scope').val(biz_scope_list.join(','));


            e.preventDefault();
            var form_data = new FormData($('#merchant_form')[0]);

            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                // data: $('#merchant_form').serialize(),
                data: form_data,
                dataType: 'json',
                contentType: false,
                processData: false,
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        $('.error').css('visibility', 'visible');
                        var error = JSON.stringify(data.msg);
                        $('#error_modal').modal('show');
                        $('.modal-title').text('提示');
                        $('.error_msg').html(data.msg);
                    }
                    if (data.status == 1) {
                        // window.location.href = '/eshop/user_login/'
                        $(".step2").hide();
                        $(".second").addClass("pass");
                        $(".third").addClass("active").siblings().removeClass("active");
                        $(".step3 .merchant").show().siblings().hide();
                    }
                },
                error: function () {
                    alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------地区设置------------------------*/

        $('#distpicker').distpicker();

        var province, City, District;
        $(document).on('change', '.province', function () {
            $(".city").removeClass('hide');
            $(".district").addClass('hide');
            province = $(".province").val();
            $('#region').val(province)
        });

        $(document).on('change', '.city', function () {
            $(".district").removeClass('hide');
            City = $(".city").val();
            $('#region').val(province + ',' + City)
        });

        $(document).on('change', '.district', function () {
            District = $(".district").val();
            $('#region').val(province + ',' + City + ',' + District)
        });


        /*-------------------------经营范围------------------------*/
        function handle_biz_scope() {
            var biz_scope_list = $.map($(".check_box input:checked"), function (obj) {
                return obj.value;
            });
            if (biz_scope_list.length == 0) {
                alert('请至少选择经营范围');
                return false;
            } else {
                return biz_scope_list;
            }
        }

        /*-------------------------性别------------------------*/
        $('#member_gender').val($("[name='member_sex']:checked")[0].value);
        $('#merchant_gender').val($("[name='merchant_sex']:checked")[0].value);

        $("[name='member_sex']").change(function () {
            console.log('member_sex');
            gender = $("[name='member_sex']:checked")[0].value;
            $('#member_gender').val(gender);
        });

        $("[name='merchant_sex']").change(function () {
            console.log('merchant_sex');
            gender = $("[name='merchant_sex']:checked")[0].value;

            $('#merchant_gender').val(gender);
        });

        /*-------------------------图片上传------------------------*/
        $('.upload_file').on('click', function () {
            $(this).next("[type='file']").click();
            $("[name='member_sex']:checked")[0].value
        });
    });

    return {
        preview_img: function (files, container_id) {
            if (files.length) {
                var file = files[0];
                var imgaeType = /^image\//;
                var $img = $('<img>');
                $img.attr('src', window.URL.createObjectURL(file));
                $img.data('file', file);
                $img.on('load', function () {
                    window.URL.revokeObjectURL(this.src);
                });
                // $('#' + container_id).append($img);
                $('#' + container_id).html($img);

            } else {
                $('#' + container_id).empty();
            }
        }
    }

}($);
