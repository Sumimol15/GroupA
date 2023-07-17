window.onload=function() {
    const contactsSection = document.getElementById('contacts');
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
            const contactDiv = document.createElement('div');
            contactDiv.className = 'contactsDiv';
            contactDiv.innerHTML = `${element.userName}`
            contactsSection.appendChild(contactDiv);
        });
        // contactsSection.appendChild(`</ul>`)
      })
      .catch(error => {
        // Handle any errors
        console.error('Error:', error);
      });
};