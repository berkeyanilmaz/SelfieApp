/**
 * Created by berkeyanilmaz on 2017-07-14.
 */

function showSocialMedia() {
    $("#facebook1").css("visibility", "visible");
    $("#instagram1").css("visibility", "visible");
    $("#twitter1").css("visibility", "visible");
}

function showMaximumLogo() {
    $("#maximum").css("visibility", "visible");
}

function hideMaximumLogo() {
    $("#maximum").css("visibility", "hidden");
}

function hideSocialMedia() {
    $("#facebook1").css("visibility", "hidden");
    $("#instagram1").css("visibility", "hidden");
    $("#twitter1").css("visibility", "hidden");
}


session.subscribeToEvent("Selfie/Start", function () {
    hideSocialMedia();
    hideMaximumLogo();
})

session.subscribeToEvent("Selfie/Animation", function () {
    hideSocialMedia();
    showMaximumLogo();
})

session.subscribeToEvent("Selfie/ShowSocial", function () {
    hideMaximumLogo();
    showSocialMedia();
})