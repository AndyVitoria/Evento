(function ($) {
    $(function () {

        $('.sidenav').sidenav();
        $('.parallax').parallax();
        $('select').formSelect();

        $('td#evento-ingresso input').each(function (index) {
            this.addEventListener('input', function (evt) {
                if (this.value < 0) {
                    alert("Valor Inválido!");
                    this.value = 0;
                } else {
                    id = this.id;

                    precoId = 'preco-' + id;
                    txId = 'tx-' + id;
                    totId = 'tot-' + id;

                    preco = document.getElementById(precoId);
                    tx = document.getElementById(txId);
                    tot = document.getElementById(totId);

                    preco_val = parseFloat(preco.innerText.split(' ')[1]);
                    tx_val = parseFloat(tx.innerText.split(' ')[1]);

                    tot.innerText = 'R$ ' + ((preco_val + tx_val) * this.value).toFixed(2);
                }
            });
        });

        $('td a').each(function (index) {
            this.addEventListener('click', function (evt) {
                let action = this.id.split(' ');
                $.ajax({
                    type: "GET",
                    url: document.URL,
                    data: {
                        'DELETE': true,
                        'csrfmiddlewaretoken': csrftoken,
                        'id': action[1]
                    }
                }).fail(function () {
                    alert("Falha ao remover evento.")
                }).done(function () {
                    let tr = $('tr#item-' + action[1])[0];
                    tr.parentNode.removeChild(tr)
                });
            });
        });
        var csrftoken = getCookie('csrftoken');
    }); // end of document ready
})(jQuery); // end of jQuery name space


function buildCard(page, nome, img, desc) {
    newEvent = '<div class="col s12 m3">\n' +
        '                    <div class="card medium">\n' +
        '                        <div class="card-image">\n' +
        '                            <img src=' + img + '>\n' +
        '                        </div>\n' +
        '                        <h5 class="center black-text">' + nome + '</h5>\n' +
        '                        <div class="card-content">\n' +
        '                            <p>' + desc + ' [...] <a href="' + page + '">Leia mais</a></p>\n' +
        '                            <br>\n' +
        '                            <p style="font-size: 12px;" class="grey-text"> Vitória/ES</p>\n' +
        '                        </div>\n' +
        '                        <div class="card-action">\n' +
        '                            <a class="light-blue-text" href="#">Gratis</a>\n' +
        '                            <a class="light-blue-text" href="' + page + '">Comprar</a>\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>';
    return newEvent
}

function topEvents(eventData) {
    divTopEvents = $('div#top-eventos');
    for (let i = 0; i < eventData.length; i++) {
        let page = eventData[i]['page'];
        let nome = eventData[i]['evento']['nome'];
        let banner = 'static/images/evento_cards/evento1.png';
        if  (eventData[i]['evento']['banner'] != '')
            banner =  eventData[i]['evento']['banner'];
        let desc = eventData[i]['evento']['descricao'];
        newEvent = buildCard(page, nome, banner, desc);
        divTopEvents.append(newEvent);
    }

}

function getEvents(id) {
    eventList = [];
    $.get('eventos', {id: id}).done(function (data) {
        console.log(data);
        eventData = data['value'];
        topEvents(eventData)
    }, "json");
}

function showEventoCard(id) {
    $('div.novo-evento').each(function () {
        if (this.id === id) {
            $(this).removeClass('hide');
            $(this).addClass('show');
        }
        else {
            $(this).removeClass('show');
            $(this).addClass('hide');
        }
    });
    $('ul#etapas').children().each(function () {
        if (this.id === id) {
            $(this).removeClass('light-blue-text');
            $(this).addClass(['light-blue', 'white-text']);
        } else {
            $(this).removeClass(['light-blue', 'white-text']);
            $(this).addClass('light-blue-text');
        }
    })

}

function setMoveActionEvento() {
    $('div.novo-evento div div button.move').each(function (index) {
        this.addEventListener('click', function (evt) {
            showEventoCard(this.id)
        })
    });
    $('li.novo-evento-etapa').each(function (index) {
        this.addEventListener('click', function (evt) {
            showEventoCard(this.id)
        })
    });

    showEventoCard('info');
}