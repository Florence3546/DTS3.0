var DTS = window.DTS || {};
DTS.address = function ($) {
    $(document).ready(function () {

        // 收货地址数量
        $("#address_no").text($(".address-box li").length);

        // 手机号码或者座机号验证
        jQuery.validator.addMethod("isMobile", function (value, element) {
            var length = value.length;
            // var mobile = /^1(3|4|5|7|8)\d{9}$/;
            var mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0-9]|170)\d{8}$/;
            // var phone = /^\d{3}-\d{8}|\d{4}-\d{7}$/;
            return this.optional(element) || (mobile.test(value));
        }, "请正确填写您的电话号码");

        //表单验证
        $.validator.setDefaults({
            submitHandler: function () {
                if ($("#form_address").data("type") == 0) {
                    if ($(".address-box li").length == 20) {
                        DTS.affirm("您最多可以添加20个收货地址，您当前的收货地址已经有20个，请删除不常用的地址再添加新地址")
                    } else {
                        $.ajax({
                            url: $('#save_add_address').attr('api'),
                            type: 'POST',
                            data: $('#form_address').serialize(),
                            dataType: 'json',
                            cache: false,
                            success: function (data) {
                                $("#modal_address").modal('hide');
                                DTS.affirm(data.msg, data.status == 1);
                            },
                            error: function () {
                                DTS.alert(DTS.tips_error);
                            }
                        });
                    }

                } else {
                    $.ajax({
                        url: $('#save_update_address').attr('api'),
                        type: 'POST',
                        data: $('#form_address').serialize(),
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            $("#modal_address").modal('hide');
                            DTS.affirm(data.msg, data.status == 1);
                        },
                        error: function () {
                            DTS.alert(DTS.tips_error);
                        }
                    });
                }
            },
            rules: {
                telephone: {
                    isMobile: true
                }
            },
            message: {}
        });

        // 地区控件
        function distpicker() {
            $("#distpicker").distpicker();
            var Province, City, District;
            $(".province").change(function () {
                $(".city").removeClass('hide');
                $(".district").addClass('hide');
                Province = $(".province").val();
                $('#region').val(Province);
            });
            $(".city").change(function () {
                $(".district").removeClass('hide');
                City = $(".city").val();
                $('#region').val(Province + ' ' + City);
            });
            $(".district").change(function () {
                District = $(".district").val();
                $('#region').val(Province + ' ' + City + ' ' + District);
            });
        }

        // 添加收货地址
        $('.add_new').on('click', function () {
            DTS.clear_form('#form_address');
            $(".city").addClass("hide");
            $(".district").addClass("hide");
            $('#modal_address').modal({backdrop: 'static', keyboard: false});
            $('.modal-title').text('添加收货地址');
            $('#save_add_address').show();
            $('#save_update_address').hide();
            distpicker();
            $("#form_address").validate();
        });

        // 提交收货地址模态框
        $(document).on('click', '#save_add_address', function () {
            $('#form_address').attr({"data-type": 0});
            $('#form_address').submit();
        });

        // 修改收货地址模态框
        $('.edit-address').on('click', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('#form_address [name=csrfmiddlewaretoken]').val()
                },
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        alert(data.msg);
                    } else {
                        $('#modal_address').replaceWith(data);
                        $('#modal_address').modal({backdrop: 'static', keyboard: false});
                        $('.modal-title').text('修改收货地址');
                        $('#save_add_address').hide();
                        $('#save_update_address').show();
                        $("#form_address").validate();

                        //地区选择
                        var region = $('#region').val().split(' ');
                        if (region[2]) {
                            $("#distpicker").distpicker({
                                province: region[0],
                                city: region[1],
                                district: region[2]
                            });
                        } else {
                            $(".district").addClass("hide");
                            $("#distpicker").distpicker({
                                province: region[0],
                                city: region[1]
                            });
                        }
                        var Province, City, District;
                        $(".province").change(function () {
                            $(".city").removeClass('hide');
                            $(".district").addClass('hide');
                            Province = $(".province").val();
                            if (Province == undefined) {
                                Province = region[0];
                            }
                            $('#region').val(Province);
                        });
                        $(".city").change(function () {
                            $(".district").removeClass('hide');
                            City = $(".city").val();
                            if (Province == undefined) {
                                Province = region[0];
                            }
                            if (City == undefined) {
                                City = region[1];
                            }
                            $('#region').val(Province + ' ' + City);
                        });
                        $(".district").change(function () {
                            District = $(".district").val();
                            if (Province == undefined) {
                                Province = region[0];
                            }
                            if (City == undefined) {
                                City = region[1];
                            }
                            $('#region').val(Province + ' ' + City + ' ' + District);
                        });
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // 修改地址提交
        $(document).on('click', '#save_update_address', function () {
            $('#form_address').attr({"data-type": 1});
            $('#form_address').submit();
        });

        // 设为默认地址
        $(".set-default").on('click', function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'is_lock': 1
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    $(this).addClass("hide");
                    DTS.affirm(data.msg, data.status == 1);
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            })
        });

        // 删除收货地址
        $('.delete-address').on('click', function () {
            var url = $(this).attr('api');
            var this_id = $(this).data("id");
            DTS.confirm("删除后不可恢复，您确定要删除吗？", function () {
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'id': this_id
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg, data.status == 1);
                    },
                    error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            }, "删除提醒");
        });

    })
}($);

