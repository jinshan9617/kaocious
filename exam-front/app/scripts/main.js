require.config({
    paths: {
        jquery: '../bower_components/jquery/jquery',
        bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
        cookie: '../bower_components/jquery.cookie/jquery.cookie',
        underscore: '../bower_components/underscore/underscore'
    },
    shim: {
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        },
        cookie: {
            deps: ['jquery']
        },
        underscore:{
            exports:'_'
        }
    }
});

require(['underscore', 'jquery', 'bootstrap', 'cookie'], function (_, $) {
    var currentQuestion;
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
    
    if(!$.cookie('userid') || true){
        $("#loginModal").modal({
            show: true,
            backdrop: 'static'
        });
    }

    document.getElementById("login_btn").onclick = function(e){
        var user_id = document.getElementById('user_id').value;
        document.getElementById("warning").innerHTML = "";
        if(!user_id.replace(" ","")){
            document.getElementById("warning").innerHTML = "user ID can not be empty!";
            return false;
        }
        $.post("/login",
            {"user_id":user_id},
            function(data){
                $("#loginModal").modal("hide");
                renderPaper();
            });
    };
    
    function renderPaper(){
        $.get('/questions',
            function(data){
                var sortData = _.sortBy(data, function(obj){return obj.id;});
                _.each(sortData, function(question, i){
                    question.order = i+1;
                    if(question.type === "select_question"){
                        var questiondiv = document.createElement('div');
                        questiondiv.innerHTML = _.template(document.getElementById("sel_question_template").innerHTML)(question);
                        document.getElementById("questions").appendChild(questiondiv.children[0]);
                        var indexlink = document.createElement("a");
                        indexlink.href = "#";
                        indexlink.innerText = question.order;
                        indexlink.className = "btn btn-default";
                        indexlink.setAttribute("data-qid", question.id);
                        document.getElementById("index").appendChild(indexlink);
                    }
                });
                showQuestion(sortData[0].id);
                $(document.getElementsByClassName("question-area")[0]).show();
                document.getElementById('index').onclick = function(e){
                    var index = e.target || e.srcElement;
                    var qId = index.getAttribute("data-qid");
                    showQuestion(qId);
                };
            });
        $("#paper").show();
    }
    
    function showQuestion(id){
        var questions = document.getElementById("questions").children;
        for(var i=0,l=questions.length; i<l; i++){
            $(questions[i]).hide();
        }
        var current = document.getElementById("question_" + id);
        if(current.nextElementSibling === null){
            document.getElementById("nextquestion").disabled = true;
        }else{
            document.getElementById("nextquestion").removeAttribute("disabled");
        }
        if(current.previousElementSibling === null){
            document.getElementById("prequestion").disabled = true;
        }else{
            document.getElementById("prequestion").removeAttribute("disabled");
        }
        $(current).show();
        currentQuestion = id;
    }

    document.getElementById("nextquestion").onclick = function(e){
        var nextId = document.getElementById("question_"+currentQuestion).nextElementSibling.getAttribute("data-qid");
        showQuestion(nextId);
    };

    document.getElementById("prequestion").onclick = function(e){
        var preId = document.getElementById("question_"+currentQuestion).previousElementSibling.getAttribute("data-qid");
        showQuestion(preId);
    };

    document.getElementById("complete_btn").onclick = function(e){
        var questions = document.getElementById("questions").children;
        var count = 0;
        var len = questions.length;
        function countplus(){
            count++;
            console.log(count);
            return count;
        }
        _.each(questions, function(questionArea, i){
            submitAnswer(questionArea, countplus, len);
        });
    };

    function submitAnswer(questionArea, countplus, len){
        console.log(questionArea);
        var type = questionArea.getAttribute("data-type"),
            id = questionArea.getAttribute("data-qid"),
            postData;
        if(type === "sq"){
            var answerOptions = [];
            var options = questionArea.getElementsByClassName("options");
            for(var i=0,l=options.length; i<l; i++){
                if(options[i].checked === true){
                    answerOptions.push(parseInt(options[i].getAttribute("data-id")));
                }
            }
            postData = {
                type: "select_question",
                options: answerOptions
            };
            $.ajax({
                type: 'POST',
                url: '/answer/' + id,
                data: {"data": JSON.stringify(postData)},
                success: function(res){
                    console.log(res);
                }
            });
            //$.post('/answer/' + id, {"data": JSON.stringify(postData)}).success(function(data){console.log(data)});
        }
    }

    function getReport(){
        alert(1);
    }
/*
    var fileupload = document.getElementById("file");
    fileupload.onchange = function(e){
        var file = e.target.files[0];
        upload(file);
    };
*/    
    function upload(file){
        var reader = new FileReader();
        var xhr = new XMLHttpRequest();
        reader.onloadend = function(e){
        /*
            $.ajax({
                type: "POST",
                url: "/upload",
                enctype: 'multipart/form-data',
                data: {"file": file},
                success: function(data){console.log(data);}
            });
         */
            data = reader.result;
            var formdata = new FormData();
            formdata.append('file', file);
            formdata.append('data', '{"type":"program_question"}');
            xhr.onreadystatechange = function(){
                console.log('a');
            };
            xhr.open('POST','/answer/q0002');
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            xhr.send(formdata);
        };
        reader.readAsDataURL(file);
        
    }


});
