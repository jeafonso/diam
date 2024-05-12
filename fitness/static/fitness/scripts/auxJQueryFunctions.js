//import flatpickr from 'flatpickr';

// Conteudo do ficheiro antigo de JS
let saveBtn = document.getElementById('saveBtn');
let cancelBtn = document.getElementById('cancelBtn');
let profileInput = document.getElementById("profile_picture");
let imageContainer = document.querySelector('.image-container');
let profileImage = document.getElementById('profile-image');

function editField(fieldName) {
    let fieldInput = document.getElementById(fieldName);

    fieldInput.removeAttribute('readonly');
    saveBtn.style.display = 'inline-block';
    cancelBtn.style.display = 'inline-block';
}

function changePassword() {
    let passwordField = document.getElementById("password");
    passwordField.value = "change";
    let form = document.getElementById("myForm");
    form.submit();
}

function showText() {
    document.querySelector('.overlay-text').style.opacity = '1';
}

function hideText() {
    document.querySelector('.overlay-text').style.opacity = '0';
}

$(document).ready(function() {
    // Carregar páginas com um fade-in
    $("body").fadeIn("fast");
    //$(".reset-opacity").css("opacity" , "1");

    // Função para fazer preview da seleção de uma nova foto de perfil
    $('#profile_picture').on('change', function(event) {
        // Verificar se o ficheiro existe e foi selecionado
        if (this.files && this.files[0]) {
            let imageUrl = URL.createObjectURL(this.files[0]);
            $('#profile-image').attr('src', imageUrl);
        }
    });

    // Remover foto de perfil na navbar
    $(".profile-image").dblclick(function(){
        const image = $(this);
        let repeatCount = 2; // Number of times to repeat inflation and explosion

        function inflateExplode() {
            image.animate({
                width: '70px',
                height: '70px',
                opacity: '0.4'
            }, 500, function() {
                image.animate({
                    width: '50px',
                    height: '50px',
                    opacity: '0.8'
                }, 350, function() {
                    if (repeatCount > 1) {
                        repeatCount--;
                        inflateExplode(); // Repeat the inflation and explosion
                    } else {
                        // After repeating, remove the image
                        image.animate({
                            width: '0px',
                            height: '0px'
                        }, 150);
                    }
                });
            });
        }

        // Start the inflation and explosion animation sequence
        inflateExplode();
    });

    // Voltar a mostrar a foto de perfil (reset das alterações causadas pela animação de cima)
    $(".username").click(function(){
        $(".profile-image").css({
            width: '50px',
            height: '50px',
            top: '0',
            opacity: '1'
        }).hide().fadeIn("slow");
    });

    const insultos = [
        "Abécula", "Abentesma", "Achavascado", "Alimária", "Andrajoso",
        "Barregã", "Biltre", "Cacóstomo", "Cuarra", "Estólido",
        "Estroso", "Estultilóquio", "Nefelibata", "Néscio", "Pechenga",
        "Sevandija", "Somítico", "Tatibitate", "Xexé ou Cheché", "Xexelento"
    ];

    // Validação de comentários
    $('.Validar').click(function(){
        let checkForInsulto = false;
        for (let insulto of insultos){
            if ($('#comentario').val().includes(insulto)){
                $('#comentario').val("");
                checkForInsulto = true;
                break; /* Mini-otimização. Se a lista tivesse milhares de elementos seria
                                                          muito tempo a percorrer tudo. Basta 1 encontrado com sucesso */
            }
        }
        console.log(checkForInsulto);
        if (!checkForInsulto){
            $('#comentario').after("<p style='color: green;'>Comentário aceite, seu Cacóstomo!</p>");
        }
    });


    let saveBtn = $('#saveBtn');
    let cancelBtn = $('#cancelBtn');
    let profileInput = $('#profile_picture');

    $('.image-container').click(function() {
        saveBtn.css("display", 'inline-block');
        cancelBtn.css("display", 'inline-block');
        profileInput.click();
    })

    // Novas coisas para o projeto

    // Mostrar inputs de cliente ou funcionário.
    $('#type-user').change(function() {
        const selectedType = $(this).val();
        if (selectedType == 'cliente') {
            $('#cliente-inputs').show();
            $('#funcionario-inputs').hide();
            $('#cliente-meta').prop('required', true);
            $('#funcionario-cargo').prop('required', false);
        } else if (selectedType == 'funcionario') {
            $('#cliente-inputs').hide();
            $('#funcionario-inputs').show();
            $('#cliente-meta').prop('required', false);
            $('#funcionario-cargo').prop('required', true);
        } else {
            $('#cliente-inputs').hide();
            $('#funcionario-inputs').hide();
        }
    });

    // Ações nos inputs de data do modal para criar Desafios
    const $startDateInput = $('#desafio_data_inicio');
    const $endDateInput = $('#desafio_data_fim');

    $startDateInput.on('input', handleDateChange);
    $endDateInput.on('input', handleDateChange);

    // Event-handler para mudança de valores das datas
    function handleDateChange() {
        const startDateValue = $startDateInput.val();
        const endDateValue = $endDateInput.val();

        // Update do min de data_fim
        if (startDateValue)
            $endDateInput.attr('min', startDateValue);
        else
            $endDateInput.removeAttr('min');    // Remover min quando se faz clear

        // Update do max de data_inicio
        if (endDateValue)
            $startDateInput.attr('max', endDateValue);
        else
            $startDateInput.removeAttr('max');  // Remover max quando se faz clear
    }

    // Meter scroll na lista de desafios quando exceder um certo número
    let desafios = $('.list-group-item');
    let containerDesafios = $('.list-group');
    const nrDesafios = desafios.length; console.log(nrDesafios);

    if (nrDesafios == 3) {
        maxLgHeight = containerDesafios.height();
        localStorage.setItem('maxLgHeight', JSON.stringify(maxLgHeight)); // Guardar no localStorage
    }

    console.log("altura_máxima: " + localStorage.getItem('maxLgHeight'));
    if (nrDesafios > 3 && localStorage.getItem('maxLgHeight')) {
        const maxHeight = JSON.parse(localStorage.getItem('maxLgHeight')); // Buscar max-height do localStorage
        containerDesafios.css({
            'max-height': maxHeight,
            'overflow': 'auto',
            '-webkit-overflow-scrolling': 'touch'
            // Add any other styles you need
        });
    }
});