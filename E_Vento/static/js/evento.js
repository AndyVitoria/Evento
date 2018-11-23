(function ($) {
    $(function () {
    formatLoteCard();
    loteCardBlank = $('div#lote-card').clone();
    ingressoCardBlank = $('div#ingresso-card').clone();
    setChips();
    $('button#ingresso-card')[0].addEventListener('click', function () {
        addLote(this.id)
    });


    setMoveActionEvento();
    setCEPEvent();
    $('.datepicker').datepicker();
    $('.timepicker').timepicker();
    }); // end of document ready
})(jQuery); // end of jQuery name space


/**
 * Pesquisa de CEP
 *
 * */

function limpa_formulário_cep() {
    //Limpa valores do formulário de cep.
    document.getElementById('id_logradouro').value = ("");
    document.getElementById('id_bairro').value = ("");
    document.getElementById('id_cidade').value = ("");
    document.getElementById('id_estado').value = ("");
}

function meu_callback(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('id_logradouro').value = (conteudo.logradouro);
        document.getElementById('id_bairro').value = (conteudo.bairro);
        document.getElementById('id_cidade').value = (conteudo.localidade);
        document.getElementById('id_estado').value = (conteudo.uf);
    } //end if.
    else {
        //CEP não Encontrado.
        limpa_formulário_cep();
        alert("CEP não encontrado.");
    }
}

function pesquisacep(valor) {

    //Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
    if (cep != "") {

        //Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        //Valida o formato do CEP.
        if (validacep.test(cep)) {

            //Preenche os campos com "..." enquanto consulta webservice.
            document.getElementById('id_logradouro').value = "...";
            document.getElementById('id_bairro').value = "...";
            document.getElementById('id_cidade').value = "...";
            document.getElementById('id_estado').value = "...";

            //Cria um elemento javascript.
            var script = document.createElement('script');

            //Sincroniza com o callback.
            script.src = 'https://viacep.com.br/ws/' + cep + '/json/?callback=meu_callback';

            //Insere script no documento e carrega o conteúdo.
            document.body.appendChild(script);

        } //end if.
        else {
            //cep é inválido.
            limpa_formulário_cep();
            alert("Formato de CEP inválido.");
        }
    } //end if.
    else {
        //cep sem valor, limpa formulário.
        limpa_formulário_cep();
    }
}

function setCEPEvent() {
    $('input#id_cep').each(function (index) {
        this.addEventListener('blur', function (evt) {
                pesquisacep(this.value)
            }
        )

    });
}


/**
 * Chips Categoria
 * */

function setChips() {
    $('.chips-autocomplete').chips({
        placeholder: 'Informe uma Categoria',
        secondaryPlaceholder: '+',
        autocompleteOptions: {
            data: categorias,
            limit: Infinity,
            minLength: 1

        }
    });
}

function formatLoteCard() {
    parent = $('#lote-row');
    parent.children().each(function (index) {
        div = $('<div>');
        if (this.lastChild.name === 'nome')
            div.addClass('col s12');
        else
            div.addClass('col s3');
        div.append(this);
        parent.append(div);
    })
}

/**
 *
 * Ingressos
 */

function buildRemoveBtn(id) {
    let removeBtn = $('<button>'), trashIcon = $('<i>');
    trashIcon.addClass('material-icons');
    trashIcon.text('delete');

    removeBtn.addClass(['btn', 'red', 'white-text']);
    removeBtn.attr('id', id);
    removeBtn.append(trashIcon);
    removeBtn[0].addEventListener('click', function () {
        $('div#' + this.id).remove();
    });
    return removeBtn;
}

ingressoCount = 0;
loteCount = {'ingresso-card': 0};

function addLote(ingressoID) {
    loteCount[ingressoID]++;
    let loteCardClone = loteCardBlank.clone(), lotezone = $('div#' + ingressoID + '-lotezone');

    loteCardClone.attr('id', ingressoID + '-' + loteCardClone.attr('id') + '-' + loteCount[ingressoID]);

    let removeBtn = buildRemoveBtn(loteCardClone.attr('id'));
    removeBtn.addClass('right');
    let divBtn = $('<div>');
    divBtn.addClass('row');
    divBtn.append(removeBtn);
    loteCardClone.children().append(divBtn);

    lotezone.append(loteCardClone);
    loteCardClone.find($('input')).each(
        function (index) {
            this.value = null;
        }
    )
}

function addIngresso() {
    ingressoCount++;
    let cardClone = ingressoCardBlank.clone(), zone = $('div#ingressozone');
    let cardID = cardClone.attr('id') + '-' + ingressoCount;
    cardClone.attr('id', cardID);

    loteCount[cardID] = 0;

    let removeBtn = buildRemoveBtn(cardClone.attr('id'));

    cardClone.find('div#ingresso-row').append(removeBtn);

    zone.append(cardClone);
    let lotezone = cardClone.find('div#ingresso-card-lotezone');
        lotezone.attr('id', cardID  + '-lotezone');

    cardClone.find($('input')).each(
        function (index) {
            this.value = null;
        }
    );

    button = cardClone.children().find('button')[0];
    button.id = cardID;
    button.addEventListener('click', function(){addLote(this.id)});
}
