$(document).ready(function() {
    $('#id_rp_phone').inputmask({"mask": "+7 (999) 999-99-99"});
        function isBlank(str) {
                return (!str || /^\s*$/.test(str));
            }

        function isEmail(email) {
          var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
          return regex.test(email);
        }

        function create_checker(input_selector, error_selector){
            checker = function(){
              var input = $(input_selector),
                value=input.val();
                if (!isBlank(value)){
                     $(error_selector).addClass('hidden');
                    return true;
                } else {
                    $(error_selector).removeClass('hidden');
                    return false;
                }
            };
            return checker
        }

        engine_check = create_checker("input[name='engine']","#rp-engine-error");
        car_check = create_checker("input[name='car']","#rp-car-error");
        parts_check = create_checker("textarea[name='parts']","#rp-parts-error");
        function mail_check(){
            var email_input = $("input[name='mail']"),
                email=email_input.val();
            if (isEmail(email)){
                $("#rp-mail-error").addClass('hidden');
                return true;
            } else {
                $("#rp-mail-error").removeClass('hidden');
                return false;
            }
        }
        phone_check = function(){
            var phone_input = $("#id_rp_phone"),
                phone=phone_input.val(),
                completed = phone_input.inputmask('isComplete');
            if (isBlank(phone) || completed){
                 $("#rp-phone-error").addClass('hidden');
                return true;
            } else {
                $("#rp-phone-error").removeClass('hidden');
                return false;
            }
        };

        $('#parts-request-form').submit(function(event){
            var engine=engine_check(),
                car = car_check(),
                parts = parts_check(),
                mail = mail_check(),
                phone=phone_check();
            event.preventDefault();



            if (engine && car && parts && mail && phone ){
                var data = $(this).serializeArray().reduce(function(obj, item) {
                    obj[item.name] = item.value;
                    return obj;
                }, {});
                data['csrf'] = $("csrfmiddlewaretoken").val();

                console.log(data);
                $.post('/json/parts-request/',data,function(resp){
                    if ('success' in resp){
                        $('#rp-error-send').addClass('hidden');
                        $("#rp-success-send").removeClass('hidden');
                        $('#id-rp-submit-button').attr('disabled', 'disabled');
                    } else if ('errors' in resp) {
                        $('#rp-error-send').removeClass('hidden');
                    }

                });
            } else {
                event.preventDefault();
            }
        });
});