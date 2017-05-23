/**
 * Created by king5699 on 17/1/10.
 */
var DTS = window.DTS || {};
DTS.home = function ($) {
    $(document).ready(function () {
        $('#btn_submit').on('click', function (e) {
            e.preventDefault();
            var form_data = new FormData($('#test_form')[0]);
            form_data.delete('photo');
            $('#preview img').each(function () {
                form_data.append('photo', $(this).data('file'));
            });
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: form_data,
                dataType: 'json',
                contentType: false,
                processData: false,
                cache: false,
                success: function (data) {
                    alert(data.msg);
                    $('#photo').val(null);
                    $('#preview').empty();
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });

        })
    });

    return {
        // 接口定义
        preview_img: function (files, container_id) {
            if (files.length) {
                for (var i in files) {
                    var file = files[i];
                    var imageType = /^image\//;

                    if (!imageType.test(file.type)) {
                        continue;
                    }

                    var $img = $('<img>');
                    $img.attr('src', window.URL.createObjectURL(file));
                    $img.data('file', file);
                    $img.on('load', function () {
                        window.URL.revokeObjectURL(this.src);
                    });
                    $('#' + container_id).append($img);
                }
            } else {
                $('#' + container_id).empty();
            }
        }
    }
}($);