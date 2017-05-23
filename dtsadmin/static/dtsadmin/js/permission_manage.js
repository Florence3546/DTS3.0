var DTS = window.DTS || {};
DTS.admin_permission = function ($) {
    $(document).ready(function () {
        $('#table_permissions').on('click', 'a.triangle', function () {
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

        $('#table_permissions').on('click', '.active_permission', function () {
            var $this = $(this);
            var tr_obj = $this.closest('tr');
            var is_active = $this.attr('is_active') === 'True' ? 'False' : 'True';
            var api = $(this).attr('api');
            var html;
            if (is_active === "False") {
                html = "禁用后将无权限进行相关的操作，确定是否禁用"
            } else {
                html = "启用后将获得操作相关功能的权限！"
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
                        DTS.switch($this);
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            });

        });
    });

    return {
        // 接口定义
    }
}($);