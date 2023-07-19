// function displayWelcomeName(friendId,callback){
//   setTimeout(function() {
//   }, 2000);
//   fetch('/userDetails?userId='+friendId,{
//     method: 'GET',
//     headers: {
      
//     }
//   })
//   .then(response => response.json())
//   .then(data => {
//     // Handle response data
//     console.log(data);
   
//     callback();
//   })
//   .catch(error => {
//     // Handle any errors
//     console.error('Error:', error);
   
//     // document.getElementById("welcome").innerHTML=`<p>Welcome USER</p>`;
//   })
// }

window.onload=function() {
  initialLoading();
};

function initialLoading(){
  const contactsSection = document.getElementById('listForContacts');
  
  var queryString = window.location.search;
  var urlParams = new URLSearchParams(queryString);
  var userId = urlParams.get('userId');
  var firstName = urlParams.get('firstName');
  console.log(userId);
  document.getElementById("welcome").innerHTML=`<p>Welcome ${firstName}</p>`;
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
          contactDiv.setAttribute("id","list-id");     
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
}


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
// function showMessages(friendId,sentBy){
//   console.log('GOING TO MESSAGES'+friendId);
  
  

//   // var firstName='First Name';
//   const chatSection = document.getElementById('chat');
  
  
//   empty(chatSection);
  
//   // chatHeader.innerHTML(`<img src="profile-picture.jpg" alt="Profile Picture"><h2>First Name&nbsp;Second Name</h2>`);
  
//       const data = {
//           "sentBy": sentBy,
//           "recipientId":friendId,
//           "order":"asc",
//           "noOfMessages":100
//       };
    
      
//       fetch('/getMessages', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//       })
//       .then(response => response.json())
//       .then(data => {
//         // Handle response data
//         console.log(data);
//         data.forEach(element => {
//           const listElementDiv = document.createElement('li');
//           if(element.sentBy==sentBy){
//             console.log('This message is sending by the logged in user');
//             listElementDiv.className='chat-display-left';
//             const editIcon = document.createElement('span');
//             editIcon.className='edit-icon';
//             editIcon.innerHTML=`<p>edit</p>`;
            
//             editIcon.addEventListener('click', function() {
//               const editedMessage = prompt('Edit the message:', element.messageContent);
//               if (editedMessage !== null && editedMessage !== '') {
//                 // Make a PUT request to the backend API to update the message content
//                 const updatedMessage = { messageId: element.messageId, message: editedMessage };
//                 updateMessage(updatedMessage,friendId,sentBy);
                
//               }});
//             listElementDiv.append(editIcon);
//             //
//             const deleteIcon = document.createElement('span');
//             deleteIcon.className='edit-icon';
//             deleteIcon.innerHTML=`<p>delete</p>`;
            
//             deleteIcon.addEventListener('click', function() {
//               let confirmValue = confirm('(This action cannot be undo) Are you sure to delete?');
//               if (confirmValue) {
//                 // Make a PUT request to the backend API to update the message content
//                 const json = { messageId: element.messageId };
//                 deleteMessage(json,friendId,sentBy);
                
//               }});
//             listElementDiv.append(deleteIcon);
//           }
//           const spanDiv = document.createElement('span');
//           spanDiv.className = 'sender';
//           spanDiv.innerHTML = `<p>${element.messageContent}</p>`;
//           listElementDiv.append(spanDiv);
          
//           const timeSpanDiv = document.createElement('span');
//           timeSpanDiv.className = 'time';
//           timeSpanDiv.innerHTML = `${element.messageCreationTime}`;
          
//           listElementDiv.append(timeSpanDiv);
//           chatSection.appendChild(listElementDiv);
          
//       });
//       document.getElementById('message-input').innerHTML=`<input type="text" placeholder="Type your message..." id="message-input-value">
//       <button type="submit" onClick=sendMessage(${sentBy},${friendId})>Send</button>`;
//       })
//       .catch(error => {
//         // Handle any errors
//         console.error('Error:', error);
//       });
    
// }
function updateMessage(message,friendId,sentBy) {
  // Implement the logic to update the message in the backend using the fetch API
  fetch('/updateMessage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message)
  })
    .then(response => response.json())
    .then(data => {
      console.log('Message updated:', data);
      // Assuming the backend returns the updated message data, you can update the UI accordingly.
      showChatPage(friendId,sentBy);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function deleteMessage(message,friendId,sentBy) {
  // Implement the logic to update the message in the backend using the fetch API
  fetch('/deleteMessage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message)
  })
    .then(response => response.json())
    .then(data => {
      console.log('Message deleted:', data);
      // Assuming the backend returns the updated message data, you can update the UI accordingly.
      showChatPage(friendId,sentBy);
    })
    .catch(error => {
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



document.querySelector('.logout-button').addEventListener('click', function() {
  window.location.href="/";
});


function searchContacts() {
  const searchInput = document.querySelector('#searchInput').value;
  const contactList = document.querySelector('#listForContacts');
  empty(contactList);
  document.getElementById("contact-display-span").innerHTML=``;
  // .innerHTML = '';
  if(searchInput){
    fetch('/getAllUsers') // Replace 'backend-url' with the actual backend API URL
    .then(response => response.json())
    .then(data => {
      const filteredContacts = data.filter(contact => contact.firstName.toLowerCase().includes(searchInput));
      if(filteredContacts.length>0){
        filteredContacts.forEach(contact => {
          const listItem = document.createElement('li');
          listItem.className="listClass";
          const link = document.createElement('a');
          link.href = '#';
          link.textContent = contact.firstName+" "+contact.lastName;
          listItem.appendChild(link);
          contactList.appendChild(listItem);
  
          link.addEventListener('click', function() {
            showChatPage(contact.userId,new URLSearchParams(window.location.search).get('userId'));
             // Replace 'contact.id' with the actual contact ID
          });
        });
      }else{
        console.log(filteredContacts.length);
        document.getElementById("contact-display-span").innerHTML=`<h3>User not found!</h3>`;
      }
      
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }else{
    initialLoading();
  }
  
}


document.querySelector('list-id').addEventListener('click', function(event) {
  const userID = event.target.dataset.userId;
  console.log('USERID----'+userID);
  // setInterval(showMessages(userID,),1000);
});
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
          if(element.sentBy==sentBy){
            console.log('This message is sending by the logged in user');
            listElementDiv.className='chat-display-left';
            const editIcon = document.createElement('span');
            editIcon.className='edit-icon';
            editIcon.innerHTML=`<p>edit</p>`;
            
            editIcon.addEventListener('click', function() {
              const editedMessage = prompt('Edit the message:', element.messageContent);
              if (editedMessage !== null && editedMessage !== '') {
                // Make a PUT request to the backend API to update the message content
                const updatedMessage = { messageId: element.messageId, message: editedMessage };
                updateMessage(updatedMessage,friendId,sentBy);
                
              }});
            listElementDiv.append(editIcon);
            //
            const deleteIcon = document.createElement('span');
            deleteIcon.className='edit-icon';
            deleteIcon.innerHTML=`<p>delete</p>`;
            
            deleteIcon.addEventListener('click', function() {
              let confirmValue = confirm('(This action cannot be undo) Are you sure to delete?');
              if (confirmValue) {
                // Make a PUT request to the backend API to update the message content
                const json = { messageId: element.messageId };
                deleteMessage(json,friendId,sentBy);
                
              }});
            listElementDiv.append(deleteIcon);
          }
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