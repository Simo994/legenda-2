jQuery(function($) {

    'use strict';

    $('#quote-carousel').carousel({
        pause: true,
        interval: 4000,
    });

    new WOW().init();

    // Обработка только ссылок с якорями на той же странице
    $(function() {
        $('a[href*=#]:not([href=#])').click(function() {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top - 40
                    }, 1000);
                    return false;
                }
            }
        });
    });

    $('#header_wrapper').scrollToFixed();
    $('.res-nav_click').click(function() {
        $('.mainNav').slideToggle();
        return false

    });

    // Простая навигация без onePageNav
    $(document).ready(function() {
        // Обработка активного состояния для ссылок с якорями
        var sections = $('section[id]');
        var navItems = $('#main-nav a[href*="#"]');
        
        $(window).scroll(function() {
            var current = '';
            var scrollTop = $(window).scrollTop();
            
            sections.each(function() {
                var sectionTop = $(this).offset().top - 100;
                if (scrollTop >= sectionTop) {
                    current = $(this).attr('id');
                }
            });
            
            navItems.parent().removeClass('active');
            if (current) {
                $('#main-nav a[href="#' + current + '"]').parent().addClass('active');
            }
            
            // Добавляем/убираем фон для header
            if (scrollTop > 50) {
                $('.header').addClass('addBg');
            } else {
                $('.header').removeClass('addBg');
            }
        });
        
        // Плавная прокрутка для ссылок с якорями только если уже на главной
        navItems.click(function(e) {
            var href = $(this).attr('href');
            var hashIndex = href.indexOf('#');
            if (hashIndex !== -1 && window.location.pathname === "/") {
                e.preventDefault();
                var target = href.substring(hashIndex); // только #aboutUs
                if ($(target).length) {
                    $('html, body').animate({
                        scrollTop: $(target).offset().top - 40
                    }, 950);
                }
            }
        });
    });

});