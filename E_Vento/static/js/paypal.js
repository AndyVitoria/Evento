// Render the PayPal button
paypal.Button.render({
    // Set your environment
    env: 'sandbox', // sandbox | production

    // Specify the style of the button
    style: {
        layout: 'vertical',  // horizontal | vertical
        size: 'medium',    // medium | large | responsive
        shape: 'rect',      // pill | rect
        color: 'gold'       // gold | blue | silver | white | black
    },

    // Specify allowed and disallowed funding sources
    //
    // Options:
    // - paypal.FUNDING.CARD
    // - paypal.FUNDING.CREDIT
    // - paypal.FUNDING.ELV
    funding: {
        allowed: [
            paypal.FUNDING.CARD,
            paypal.FUNDING.CREDIT
        ],
        disallowed: []
    },

    // Enable Pay Now checkout flow (optional)
    commit: true,

    // PayPal Client IDs - replace with your own
    // Create a PayPal app: https://developer.paypal.com/developer/applications/create
    client: {
        sandbox: 'AeQQGdnhXvUWFy1XZM3auBsys7pRYL_2TClcuxb7XI9kc3NwMIn3-cffj8XZQL6AWPkjB1URHnbJwOQz',
        production: 'AfjkH4g8c6WVNt5djvwof7uls1iE0hc1PS6_O9wQBwhokg-A3FLlJymbdROv6z3EXpWqOZD9JagIDvlj'
    },

    payment: function (data, actions) {
        return actions.payment.create({
            payment: {
                transactions: [
                    {
                        amount: {
                            total: total,
                            currency: 'BRL'
                        }
                    }
                ]
            }
        });
    },

    onAuthorize: function (data, actions) {
        return actions.payment.execute()
            .then(function () {
                $.ajax({
                    type: "POST",
                    url: document.URL,
                    data: {
                        'csrfmiddlewaretoken': csrftoken,
                        'type': 'PayPal',
                        'data': data,
                        'carrinhoID': carrinhoID,
                        'total': total
                    }
                }).fail(function () {
                    window.alert('Falha se comunicar com o servidor!');
                }).done(function () {
                    window.alert('Pagamento realizado com sucesso!');
                });
                console.log(data);
            });
    }
}, '#paypal-button-container');

