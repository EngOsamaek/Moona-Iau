jQuery(function ($) {
  'use strict';

  /****======  Sticky Menu ======*******/
  var header = $(".menu-box");
  $(window).on("scroll", function () {
    if ($(this).scrollTop() < 400) {
      header.removeClass("animated fadeInDown fixed");
    } else {
      header.addClass("animated fadeInDown fixed");
    }
  });

  /**********************
   Global Slider
  ***********************/
  $(document).ready(function () {
    var $elementCarousel = $(".globalSlider");
    $elementCarousel.each(function () {
      var appendArrow = $(this).siblings('.slick-arrow-container');
      $(this).slick({
        appendArrows: appendArrow,
        prevArrow: `<span class="slick-btn slick-prev"><i class="flaticon-back"></i></span>`,
        nextArrow: `<span class="slick-btn slick-next"><i class="flaticon-next"></i></span>`
      });
    })
  });

  /****====== Mobile Menu Js ======*******/
  $(".mobile-nav .dropdown-list .mnav-plus-minus").on("click", function () {
    $(this).parent().parent().find(".dropdown").slideToggle();
    $(this).toggleClass("active");
  });

  $(".product-switcher .pswitch-item").on("click", function (e) {
    $(".product-switcher .pswitch-item").removeClass("active");
    $(this).addClass("active");
  });

  $(".productSize .productSizeitem").on("click", function (e) {
    $(".productSize .productSizeitem").removeClass("active");
    $(this).addClass("active");
  });
 
  /**********************
   HomeSlider 2
   ***********************/
  $(".homeSlider2").slick({
    autoplay: false,
    arrows: true,
    prevArrow: "<span class='slick-btn slick-prev'><img src='assets/images/home-2/arrow-left.png'> </span>",
    nextArrow: "<span class='slick-btn slick-next'><img src='assets/images/home-2/arrow-right.png'> </span>",
    dots: false,
    slidesToShow: 1,
    infinite: true,
    dots: true,
    speed: 700,
    autoplaySpeed: 900
  });

  /****======  Increase and decrease number by click  ======*******/
  if ($(".increaseQty").length) {
    var minVal = 1,
      maxVal = 20;
    $(".increaseQty").on("click", function () {
      var $parentElm = $(this).parents(".qtySelector");
      $(this).addClass("clicked");
      setTimeout(function () {
        $(".clicked").removeClass("clicked");
      }, 100);
      var value = $parentElm.find(".qtyValue").val();
      if (value < maxVal) {
        value++;
      }
      $parentElm.find(".qtyValue").val(value);
    });
  };

  if ($(".decreaseQty").length) {
    $(".decreaseQty").on("click", function () {
      var $parentElm = $(this).parents(".qtySelector");
      $(this).addClass("clicked");
      setTimeout(function () {
        $(".clicked").removeClass("clicked");
      }, 100);
      var value = $parentElm.find(".qtyValue").val();
      if (value > 1) {
        value--;
      }
      $parentElm.find(".qtyValue").val(value);
    });
  };

  /* password show hide on form field  */
  if ($(".eye .icon-2").length) {
    $(".eye .icon-2").click(function () {
      var x = document.getElementById("password-field");
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
      $(this).hide();
      $(".eye .icon-1").css("display", "block");
    });
  };

  if ($(".eye .icon-1").length) {
    $(".eye .icon-1").click(function () {
      var x = document.getElementById("password-field");
      if (x.type === "text") {
        x.type = "password";
      } else {
        x.type = "text";
      }
      $(this).hide();
      $(".eye .icon-2").css("display", "block");
    });
  };

  /****======  Jquery tabs  ======*******/
  $(".tabs").tabs({
    neighbors: {
      prev: $("button.prev"),
      next: $("button.next")
    }
  });

  $(".nav-pills .nav-link").on("click", function (e) {
    $(".tab-pane .globalSlider").resize();
    $(".tab-pane .slick-slider").slick("refresh");
  });
 
  /****====== Price Filter ======*******/
  if ($("#price-range").length) {
    $("#price-range").slider({
      range: true,
      min: 0,
      max: 200000,
      values: [0, 200000],
      slide: function (event, ui) {
        $("#priceRange").val("$" + ui.values[0] + " - $" + ui.values[1]);
      }
    });
    $("#priceRange").val("$" + $("#price-range").slider("values", 0) + " - $" + $("#price-range").slider("values", 1));
  };
 
  if ($("#price-range2").length) {
    $("#price-range2").slider({
      range: true,
      min: 0,
      max: 200000,
      values: [0, 200000],
      slide: function (event, ui) {
        $("#priceRange2").val("$" + ui.values[0] + " - $" + ui.values[1]);
      }
    });
    $("#priceRange2").val("$" + $("#price-range2").slider("values", 0) + " - $" + $("#price-range2").slider("values", 1));
  };
  
  /****====== wow js ======*******/
  new WOW().init();

  /****===== MagnificPopup Js ======*******/
  if ($(".popupVideo").length) {
    $('.popupVideo').magnificPopup({
      type: 'iframe'
    });
  };

  /****====== Custom Accordian Js ======*******/
  $(".accordion .accordion-button").on("click", function (e) {
    $(".accordion .globalSlider").resize();
    $(".accordion .slick-slider").slick("refresh");
  });

  /****====== Insta-slider Js ======*******/
  if ($(".insta-slider").length) {
    $(".insta-slider").magnificPopup({
      delegate: 'a',
      type: 'image',
      mainClass: 'mfp-fade',
      removalDelay: 160,
      preloader: false,
      fixedContentPos: false,
      gallery: {
        enabled: true
      },
      zoom: {
        enabled: true,
        duration: 300,
        easing: 'ease-in-out',
        opener: function (openerElement) {
          return openerElement.is('img') ? openerElement : openerElement.find('img');
        }
      }
    });
  };
    
  /****====== Time Countdown Js ======*******/
  if ($(".time-countdown-two").length) {
    $(".time-countdown-two").each(function () {
      var Self = $(this);
      var countDate = Self.data('countdown-time'); // getting date
      Self.countdown(countDate, function (event) {
        $(this).html('<li> <div class="box"> <span class="days">' + event.strftime('%D') + '</span> <span class="timeRef">days</span> </div> </li> <li> <div class="box"> <span class="hours">' + event.strftime('%H') + '</span> <span class="timeRef clr-1">hours</span> </div> </li> <li> <div class="box"> <span class="minutes">' + event.strftime('%M') + '</span> <span class="timeRef clr-2">min</span> </div> </li> <li> <div class="box"> <span class="seconds">' + event.strftime('%S') + '</span> <span class="timeRef clr-3">sec</span> </div> </li>');
      });
    });
  };

  /****====== product single 1  ======*******/
  $(".singleProductOne").slick({
    dots: false,
    infinite: false,
    speed: 300,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    autoplay: false,
    prevArrow: '<button class="arrow-back"><i class="flaticon-back-1"></i> </button>',
    nextArrow: '<button class="arrow-next"><i class="flaticon-next-1"></i></button>',
    autoplaySpeed: 4000,
    asNavFor: '.slider-nav',
    pauseOnHover: false
  });
  $(".singleProductOneNav").slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.slider-for',
    dots: false,
    focusOnSelect: true,
    infinite: false,
    speed: 300,
    arrows: true,  
    autoplay: false,
    autoplaySpeed: 4000,
    prevArrow: '<button class="arrow-back"><i class="flaticon-back-1"></i> </button>',
    nextArrow: '<button class="arrow-next"><i class="flaticon-next-1"></i></button>',
    pauseOnHover: false
  });

  /****====== product single 2  ======*******/ 
  $(".singleProducttwo").slick({
    dots: false,
    infinite: true,  
    speed: 300,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    autoplay: false,
    prevArrow: '<button class="arrow-back"><i class="flaticon-back-1"></i> </button>',
    nextArrow: '<button class="arrow-next"><i class="flaticon-next-1"></i></button>',
    autoplaySpeed: 4000,
    asNavFor: '.slider-nav',
    pauseOnHover: false
  });
  $(".singleProducttwoNav").slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    asNavFor: '.slider-for',
    dots: false,
    focusOnSelect: true,
    infinite: true, 
    vertical: true,
    speed: 300,
    arrows: true,
    autoplay: false,
    autoplaySpeed: 4000,
    prevArrow: '<button class="arrow-back"><i class="flaticon-back-1"></i> </button>',
    nextArrow: '<button class="arrow-next"><i class="flaticon-next-1"></i></button>',
    pauseOnHover: false,
    responsive: [{
        breakpoint: 1399,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 991, 
        settings: { 
          slidesToShow: 4
        }
      },
      {
        breakpoint: 520, 
        settings: {
          slidesToShow: 3
        }
      },

    ]
  });

  /****====== product single 1  ======*******/
  $(".singleProductThree").slick({
    dots: false,
    infinite: false,
    speed: 300,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    autoplay: false,
    prevArrow: '<button class="arrow-back"><i class="flaticon-back-1"></i> </button>',
    nextArrow: '<button class="arrow-next"><i class="flaticon-next-1"></i></button>',
    autoplaySpeed: 4000,
    asNavFor: '.slider-nav',
    pauseOnHover: false
  });
  $(".singleProductThreeNav").slick({ 
    slidesToShow: 5,
    slidesToScroll: 1,
    asNavFor: '.slider-for',
    dots: false,
    focusOnSelect: true,
    infinite: false,
    speed: 300,
    arrows: false,   
    autoplay: false,
    autoplaySpeed: 4000, 
    pauseOnHover: false,
    responsive: [{
      breakpoint: 1399,
      settings: {
        slidesToShow: 4
      }
    },
    {
      breakpoint: 991, 
      settings: { 
        slidesToShow: 5
      }
    },
    {
      breakpoint: 767, 
      settings: {
        slidesToShow: 4
      }
    },

  ]
  });

  /****======  Zoom Product  ======*******/
  if ($(".singleProducttwo .single-item").length) {
    $(".singleProducttwo .single-item").zoom();
  };

  /****======  Bottom to Top Scroll Js  ======*******/
  var ScrollTop = $(".scrollToTop");
  $(window).on("scroll", function () {
    if ($(this).scrollTop() < 500) {
      ScrollTop.removeClass("active");
    } else {
      ScrollTop.addClass("active");
    }
  });

  $(".scrollToTop").on("click", function () {
    $("html, body").animate({
      scrollTop: 0
    }, 250);
    return false;
  });

  $(window).on("load", function () {
    /****======  Newslettser Modal  ======*******/
    $("#newsletter-modal").modal("show");

    /****======  Preloader Js  ======*******/
    function pre_loader() {
      $("#load").fadeOut();
      $('#pre-loader').delay(500).fadeOut(500);
    }
    pre_loader();

  });
}(jQuery));