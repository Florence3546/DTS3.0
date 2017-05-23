var DTS = window.DTS || {};
DTS.admin_access = function ($) {
    $(document).ready(function () {
        $(".triangle").on("click", function () {
            if ($(this).closest(".role").children(".role").css("display") == "none") {
                $(this).closest(".role").children(".role").css({"display": "block"});
                $(this).addClass("triangle-bootom");
            } else {
                $(this).closest(".role").find(".role").css({"display": "none"});
                $(this).closest(".role").find(".triangle").removeClass("triangle-bootom");
            }
        });
    })
}($);