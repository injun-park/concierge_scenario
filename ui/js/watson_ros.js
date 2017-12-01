

var ros = new ROSLIB.Ros();
var publisher = null;
// If there is an error on the backend, an 'error' emit will be emitted.
ros.on('error', function(error) {
  document.getElementById('connecting').style.display = 'none';
  document.getElementById('connected').style.display = 'none';
  document.getElementById('closed').style.display = 'none';
  document.getElementById('error').style.display = 'inline';
  console.log(error);
});
ros.on('close', function() {
  console.log('Connection closed.');
  document.getElementById('connecting').style.display = 'none';
  document.getElementById('connected').style.display = 'none';
  document.getElementById('closed').style.display = 'inline';
});

// Find out exactly when we made a connection.
ros.on('connection', function() {
  document.getElementById('connecting').style.display = 'none';
  document.getElementById('error').style.display = 'none';
  document.getElementById('closed').style.display = 'none';
  document.getElementById('connected').style.display = 'inline';
  console.log('Connection established!');


  publisher = new ROSLIB.Topic({
    ros : ros,
    name : '/user_input',
    messageType : 'concierge_msgs/ui'
  });

  listener = new ROSLIB.Topic(
    {
      ros : ros,
      name : '/ui_control',
      messageType : 'concierge_msgs/ui_msg'
    }

  );

  listener.subscribe(function(message) {
    //console.log('Received message on ' + listener.name + ': name : ' + message.name +", sentence : " + message.sentence);
    // If desired, we can unsubscribe from the topic as well.
    console.log("message : " + message.toString())
    console.log('Received message on ' + listener.name + ': command : ' + message.command +", sentence : " + message.sentence +", code : " + message.UI_ROBOT_SENTENCE);


    /* command from user : text input */
    // if (command == 4) {
    //   return;
    // }

    command = message.command;
    sentence = message.sentence;

    if (command == 0) {
      return;
    }

    var myDiv = document.getElementById('scrollingChat');
    html = myDiv.innerHTML;

    html = html.replace('<blink>', '');
    html = html.replace('</blink>', '');
    html = html.replace('<marquee>', '');
    html = html.replace('</marquee>', '');
    if(command == 10) { /* display user sentence */
      html += makeUserSentenceHtml(sentence);

    } else if(command == 20) { /* display watson sentence */
      html += makeWatsonSentenceHtml(sentence);
    } else if(command == 30) { /* display MIC */
      html += makeMicListeningHtml();
    }
    myDiv.innerHTML = html
    myDiv.scrollTop = myDiv.scrollHeight;

    //startBlink();

  });

});

//ros.connect('ws://192.168.0.2:9090');
ros.connect('ws://192.168.0.15:9090');

function makeUserSentenceHtml(sentence) {
  html = "\
    <div class = 'segments load'> \
      <div class = 'from-user latest top'> \
        <div class = 'message-inner'  display:table;> \
                  <table border='0'> \
          <tr><td> \
            <img width='50' height='50' src='images/user.jpg'/>\
            <td> <font size='4'>" + sentence + " </font> \
            </td></tr></table> \
        </div> \
      </div> \
    </div> ";

  return html;
}

function makeWatsonSentenceHtml(sentence) {
  html = "\
    <div class = 'segments load'> \
      <div class = 'from-watson latest top'> \
        <div class = 'message-inner' display:table;> \
        <table border='0'> \
          <tr><td> \
            <img width='50' height='50' src='images/watson.jpeg'/>\
            <td> <font size='4'>" + sentence + " </font> \
            </td></tr></table> \
        </div> \
      </div> \
    </div> ";
    //<p> <font size='4' color = 'green' face='verdana'>" + sentence + " </font> \

    return html;
}


function makeMicListeningHtml() {
  html = "\
    <div class = 'segments load'> \
      <div class = 'from-watson latest top'> \
        <div class = 'message-inner' display:table; style='background-color: #ffb3b3'> \
        <table border='0'> \
          <tr><td> \
            <img width='50' height='50' src='images/mic.jpeg'/>\
            <td> <font size='3'> <marquee> say something.....</marquee></font> \
            </td></tr></table> \
        </div> \
      </div> \
    </div> ";
    //<p> <font size='4' color = 'green' face='verdana'>" + sentence + " </font> \
    return html;
}


var speed = 200; //깜빡이는 속도 - 1000은 1초

function doBlink(){
    var blink = document.all.tags("BLINK"); // 문서의 blink 태그 객체를 배열로 받는다.
    for(var i=0; i < blink.length; i++){
        blink[i].style.visibility = blink[i].style.visibility == "" ? "hidden" : "";
    }
}

function startBlink(){
    if(document.all) {
      setInterval("doBlink()", speed);
    }
}
