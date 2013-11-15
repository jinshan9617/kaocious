require.config({
    paths: {
        jquery: '../bower_components/jquery/jquery',
        underscore: '../bower_components/underscore/underscore',
        bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
        cookie: '../bower_components/jquery.cookie/jquery.cookie'
    },
    shim: {
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        },
        cookie: {
            deps: ['jquery']
        },
        underscore: {
            exports: 'underscore'
        }
    }
});

require(['jquery', 'underscore', 'bootstrap', 'cookie'], function ($, _) {
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (true) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var new_q_btn = document.getElementById("new_question");
    new_q_btn.onclick = function(e){
        clearContainer();
        renderNewQuestion();
    };

    function renderNewQuestion(){
       ; 
    }

});
