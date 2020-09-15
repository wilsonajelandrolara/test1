



// Create a client instance
  //client = new Paho.MQTT.Client("postman.cloudmqtt.com", 14970);
  var Hini,Hfin,activa;
  client = new Paho.MQTT.Client("maqiatto.com", 8883, "web_" + parseInt(Math.random() * 100, 10));

  // set callback handlers
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;
  var options = {
   useSSL: false,
   userName: "wlara123@outlook.es",
   password: "tomatitos1",
    onSuccess:onConnect,
    onFailure:doFail
  }

  // connect the client
  client.connect(options);
   
  // called when the client connects
  function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("Conectado...");
    client.subscribe("wlara123@outlook.es/test");
  }

  function doFail(e){
    console.log(e);
	
  }

  // called when the client loses its connection
  function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost:"+responseObject.errorMessage);
    }
  }

  // called when a message arrives
  function onMessageArrived(message) {
    console.log("onMessageArrived:"+message.payloadString);
  }
  
  function finalizar(){
    var hora1=document.getElementById("Hfin");
    Hfin=hora1.value;
    console.log(Hfin);
    message = new Paho.MQTT.Message("Hfin;"+Hfin);
    message.destinationName = "wlara123@outlook.es/test1";
    client.send(message);
  }

  function iniciar(){
    var hora2=document.getElementById("Hini");
    Hini=hora2.value;
    console.log(Hini);
    message = new Paho.MQTT.Message("Hini;"+Hini);
    message.destinationName = "wlara123@outlook.es/test1";
    client.send(message);
  }

  function Activate(){
    var ale=document.getElementById("AlertaAlarm")
    activa=1
    message = new Paho.MQTT.Message("activa;"+activa);
    message.destinationName = "wlara123@outlook.es/test1";
    client.send(message);
    ale.innerHTML="Alerma Encendida"
    
  }

  function Disable(){
    var ale=document.getElementById("AlertaAlarm")
    activa=0
    message = new Paho.MQTT.Message("activa;"+activa);
    message.destinationName = "wlara123@outlook.es/test1";
    client.send(message);
    ale.innerHTML="Alerma Desactivada"
  }

  function Open(){
    var ale=document.getElementById("AlertaDoor")
    message = new Paho.MQTT.Message("abrir;1");
    message.destinationName = "wlara123@outlook.es/test1";
    client.send(message);
    ale.innerHTML="Puerta Abierta"
  }

  function Close(){
    var ale=document.getElementById("AlertaDoor")
    message = new Paho.MQTT.Message("abrir;0");
    message.destinationName = "wlara123@outlook.es/test1";
    client.send(message);
    ale.innerHTML="Puerta Cerrada"
  }