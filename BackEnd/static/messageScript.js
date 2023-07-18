window.onload=function() {
  const contactsSection = document.getElementById('listForContacts');
  var queryString = window.location.search;
  var urlParams = new URLSearchParams(queryString);
  var userId = urlParams.get('userId');
  console.log(userId);
  const jsonData= {"userId":userId}
  fetch('/getMyFriends', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
      // Handle response data
      console.log(data);
      
      // contactsSection.appendChild(`<ul>`)
      data.forEach(element => {
          const contactDiv = document.createElement('li');
          contactDiv.className = 'listClass';
          contactDiv.innerHTML = `<a onClick=showChatPage(${element.userId},${userId})>
          ${element.firstName}&nbsp;${element.lastName}</a>`
          contactsSection.appendChild(contactDiv);
      });
      // contactsSection.appendChild(`</ul>`)
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
};


function displayContactNames(friendId,callback){
  fetch('/userDetails?userId='+friendId,{
    method: 'GET',
    headers: {
      
    }
  })
  .then(response => response.json())
  .then(data => {
    // Handle response data
    console.log(data);
    const chatHeader = document.getElementById('chatHeaderSection').innerHTML=`<img src={{ url_for('static', filename='pp.jpg') }} alt="Profile Picture"><h2>${data.firstName}&nbsp;${data.lastName}</h2>`;
    // empty(chatHeader);
    callback();
  })
  .catch(error => {
    // Handle any errors
    console.error('Error:', error);
  });
  
}
function showChatPage(friendId,sentBy){
  displayContactNames(friendId,function(){
    console.log('THIS IS EXECUTED');
    showMessages(friendId,sentBy);
  });
  
}
function showMessages(friendId,sentBy){
  console.log('GOING TO MESSAGES'+friendId);
  
  

  // var firstName='First Name';
  const chatSection = document.getElementById('chat');
  
  
  empty(chatSection);
  
  // chatHeader.innerHTML(`<img src="profile-picture.jpg" alt="Profile Picture"><h2>First Name&nbsp;Second Name</h2>`);
  
      const data = {
          "sentBy": sentBy,
          "recipientId":friendId,
          "order":"asc",
          "noOfMessages":100
      };
    
      
      fetch('/getMessages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
        // Handle response data
        console.log(data);
        data.forEach(element => {
          const listElementDiv = document.createElement('li');
          const spanDiv = document.createElement('span');
          spanDiv.className = 'sender';
          spanDiv.innerHTML = `<p>${element.messageContent}</p>`;
          listElementDiv.append(spanDiv);
          const timeSpanDiv = document.createElement('span');
          timeSpanDiv.className = 'time';
          timeSpanDiv.innerHTML = `${element.messageCreationTime}`;
          listElementDiv.append(timeSpanDiv);
          chatSection.appendChild(listElementDiv);
      });
      document.getElementById('message-input').innerHTML=`<input type="text" placeholder="Type your message..." id="message-input-value">
      <button type="submit" onClick=sendMessage(${sentBy},${friendId})>Send</button>`;
      })
      .catch(error => {
        // Handle any errors
        console.error('Error:', error);
      });
    
}
function sendMessage(sentBy,recipientId){
  const data = {
    "sentBy": sentBy,
    "recipientId":recipientId,
    "message":document.getElementById("message-input-value").value
};


fetch('/createMessage', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
  // Handle response data
  console.log(data);
  showMessages(recipientId,sentBy);
})
.catch(error => {
  // Handle any errors
  console.error('Error:', error);
});
}
function empty(element) {
  while(element.firstElementChild) {
     element.firstElementChild.remove();
  }
}