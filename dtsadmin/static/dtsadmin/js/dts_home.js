var DTS = window.DTS || {};
DTS.admin_dtshome = function ($) {
    $(document).ready(function () {
        $(".nav-tabs li").on('click', function () {
            var index = $(this).index();
            $(this).addClass('active').siblings().removeClass('active');
            $(".table tbody").eq(index).removeClass('dn').siblings().addClass('dn');
        })
    })
}($);