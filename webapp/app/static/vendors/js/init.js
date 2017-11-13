(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.dropdown-button').dropdown({
      hover: true,
      belowOrigin: true,
      alignment: 'right',
      inDuration: 300,
      outDuration: 225
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space