(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();

  }); // end of document ready
})(jQuery); // end of jQuery name space


function topEvents() {
  divTopEvents = $('div#top-eventos');
  for (let i = 0; i < 8; i++){
    newEvent = '<div class="col s12 m3">\n' +
        '                    <div class="card medium">\n' +
        '                        <div class="card-image">\n' +
        '                            <img src="static/images/evento_cards/evento1.png">\n' +
        '                        </div>\n' +
        '                        <h5 class="center black-text">Inauguração da Nova Loja</h5>\n' +
        '                        <div class="card-content">\n' +
        '                            <p>I am a very simple card. I am good at containing small [...] <a href="#">Leia mais</a></p>\n' +
        '                            <br>\n' +
        '                            <p style="font-size: 12px;" class="grey-text"> Vitória/ES</p>\n' +
        '                        </div>\n' +
        '                        <div class="card-action">\n' +
        '                            <a class="light-blue-text" href="#">Gratis</a>\n' +
        '                            <a class="light-blue-text" href="#">Comprar</a>\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>';
    divTopEvents.append(newEvent);

  }

}