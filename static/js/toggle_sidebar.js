$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $(this).find('i').toggleClass('fa fa-angle-double-left').toggleClass('fa fa-angle-double-right');
    $("#wrapper").toggleClass("toggled");
});
