$(document).ready(function() {
    $(window).Scrollax();
    //$('#tab-2').hide();
    $('.navbar_toggler ').on('click', function(e) {
        e.preventDefault();
        $('header nav').css({ 'display': 'inline-block', 'color': '#8000000' });
        $('header nav ul li a').css('color', '#31210e');

    });

    console.log("document is ready.....")
    $('.edit-user_profileModal').css('display', 'none');
    $('.edit-user_edu-detModal').css('display', 'none');
    $('.edit-user_empModal').css('display', 'none');
    $('.edit-user_prefModal').css('display', 'none');
    $('.edit-user_file_upModal').css('display', 'none');
    $('#personal-details').on('click', (e) => {
        e.preventDefault();
        //console.log(window.location.href)
        let loc = $(this).attr("href", "{%url 'userinfor' user.id%}");
        console.log("loaction is :" + loc);
        console.log("modal is shown");
        $('.edit-user_profileModal').css('display', 'block');
        //window.location = "{%url 'userinfor' user.id%}";

    });


    $('.close').click(() => {

        $('.edit-user_profileModal').css('display', 'none');
        $('.edit-user_edu-detModal').css('display', 'none');
        $('.edit-user_empModal').css('display', 'none');
        $('.edit-user_prefModal').css('display', 'none');
        $('.edit-user_file_upModal').css('display', 'none');
    });
    window.onclick = function(e) {
        console.log("window clicked ...")
        if (e.target == $('.edit-user_profileModal')) {

            $('.edit-user_profileModal').css('display', 'none');
        }
    };


    $('#countries').animateNumber({

        number: 46,
        color: 'green',
        'font-size': '24px',
        'font-weight': '700',
        numberStep: function(now, tween) {
            var floored_number = Math.floor(now),
                target = $(tween.elem);

            target.text(floored_number);
        }
    }, {
        easing: 'swing',
        duration: 1800
    });
    $('#companies').animateNumber({

        number: 460,
        color: 'green',
        'font-size': '24px',
        'font-weight': '700',
        numberStep: function(now, tween) {
            var floored_number = Math.floor(now),
                target = $(tween.elem);

            target.text(floored_number);
        }
    }, {
        easing: 'swing',
        duration: 1800
    });
    $('#employees').animateNumber({

        number: 120,
        color: 'green',
        'font-size': '24px',
        'font-weight': '700',
        numberStep: function(now, tween) {
            var floored_number = Math.floor(now),
                target = $(tween.elem);

            target.text(floored_number);
        }
    }, {
        easing: 'swing',
        duration: 1800
    });


    $('#md-close1').on('click', function(e) {
        e.preventDefault();
        $('#modal-1').toggleClass("md-show");
    });
    $('#md-close2').on('click', function(e) {
        e.preventDefault();
        $('#modal-2').toggleClass("md-show");
    });
    $('#md-close3').on('click', function(e) {
        e.preventDefault();
        $('#modal-3').toggleClass("md-show");
    });
    $('#md-close4').on('click', function(e) {
        e.preventDefault();
        $('#modal-4').toggleClass("md-show");
    });
    $('#md-close5').on('click', function(e) {
        e.preventDefault();
        $('#modal-5').toggleClass("md-show");
    });

    $('#tab-sec1').click(function(e) {
        e.preventDefault();
        $('#tab-2').show();
        $('#tab-1').hide();
    });
    var tab_no = 0;
    $('.next_tabBtn').on('click', function(e) {
        e.preventDefault();
        $('#tab-' + tab_no).removeClass('active');
        tab_no++;
        $('#tab-' + tab_no).addClass('active');
        if (tab_no == 5) {
            alert("review you details and save it");
            $('#tab-' + 4).removeClass('active');
            tab_no = 0;
            //$('#tab-' + 0).addClass('active');
            $('#profile_summary').css('display', 'block');
            $('#edu-sec').css('display','none')

        }

    });

});